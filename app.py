from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import uuid
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for iPhone Shortcuts

# Configuration
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'm4v'}

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Check if FFmpeg is available
def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

FFMPEG_AVAILABLE = check_ffmpeg()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_video_info(filepath):
    """Get video metadata using ffprobe - simplified version"""
    # Skip ffprobe check - just verify file exists and is readable
    if not os.path.exists(filepath):
        raise Exception("Video file not found")
    if os.path.getsize(filepath) == 0:
        raise Exception("Video file is empty")
    return {"valid": True}

def optimize_for_whatsapp(input_path, output_path):
    """
    Optimize video for WhatsApp status with these settings:
    - High quality H.264 encoding
    - 1080p max resolution (maintains aspect ratio)
    - High bitrate (5000k video, 192k audio)
    - 30 second max duration
    - MP4 container with proper flags for compatibility
    """
    
    # FFmpeg command optimized for WhatsApp
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-t', '30',  # Limit to 30 seconds for WhatsApp status
        '-c:v', 'libx264',  # H.264 codec
        '-preset', 'slow',  # Slower preset = better quality
        '-crf', '18',  # High quality (lower = better, 18 is near-lossless)
        '-vf', 'scale=1080:-2:flags=lanczos',  # Scale to 1080p width, maintain aspect ratio
        '-b:v', '5000k',  # High video bitrate
        '-maxrate', '6000k',  # Max bitrate
        '-bufsize', '12000k',  # Buffer size
        '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
        '-c:a', 'aac',  # AAC audio codec
        '-b:a', '192k',  # High audio bitrate
        '-ar', '48000',  # Audio sample rate
        '-movflags', '+faststart',  # Enable fast start for streaming
        '-y',  # Overwrite output file
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg error: {result.stderr}")
    
    return result

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                if current_time - os.path.getmtime(filepath) > 3600:  # 1 hour
                    os.remove(filepath)

@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'service': 'WhatsApp HD Video Converter API',
        'version': '1.0',
        'ffmpeg_available': FFMPEG_AVAILABLE,
        'endpoints': {
            '/convert': 'POST - Upload video for conversion',
            '/health': 'GET - Check API health'
        },
        'usage': {
            'method': 'POST',
            'endpoint': '/convert',
            'content_type': 'multipart/form-data',
            'field_name': 'video',
            'max_size': '100MB',
            'supported_formats': list(ALLOWED_EXTENSIONS),
            'output': 'Optimized MP4 file'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ffmpeg_available': FFMPEG_AVAILABLE
    })

@app.route('/convert', methods=['POST'])
def convert_video():
    try:
        # Check if FFmpeg is available
        if not FFMPEG_AVAILABLE:
            return jsonify({
                'error': 'FFmpeg is not installed or not accessible on the server. Please contact the administrator.'
            }), 500
        
        # Cleanup old files
        cleanup_old_files()
        
        # Check if video file is in request
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file format',
                'supported_formats': list(ALLOWED_EXTENSIONS)
            }), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        original_ext = file.filename.rsplit('.', 1)[1].lower()
        input_filename = f"{file_id}_input.{original_ext}"
        output_filename = f"{file_id}_output.mp4"
        
        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        # Get file size
        file_size = os.path.getsize(input_path)
        if file_size > MAX_FILE_SIZE:
            os.remove(input_path)
            return jsonify({'error': f'File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB'}), 400
        
        # Get video info
        try:
            video_info = get_video_info(input_path)
        except Exception as e:
            os.remove(input_path)
            return jsonify({'error': f'Invalid video file: {str(e)}'}), 400
        
        # Convert video
        try:
            optimize_for_whatsapp(input_path, output_path)
        except Exception as e:
            # Cleanup
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({'error': f'Conversion failed: {str(e)}'}), 500
        
        # Get output file info
        output_size = os.path.getsize(output_path)
        
        # Clean up input file
        os.remove(input_path)
        
        # Send the converted file
        response = send_file(
            output_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'whatsapp_optimized_{file_id}.mp4'
        )
        
        # Schedule cleanup of output file after sending
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
