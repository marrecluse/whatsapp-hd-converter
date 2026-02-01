#!/usr/bin/env python3
"""
Test client for WhatsApp HD Video Converter API
This script demonstrates how to interact with the API programmatically
"""

import sys
import os

def test_api_locally():
    """
    Simulate what would happen when the API receives a request
    """
    print("="*60)
    print("WhatsApp HD Video Converter - API Test Client")
    print("="*60)
    print()
    
    # Check if test video exists
    test_video = '/home/claude/test_input.mp4'
    if not os.path.exists(test_video):
        print("❌ Test video not found. Run test_conversion.py first.")
        return
    
    print("📤 Simulating API Request:")
    print("-" * 60)
    print(f"POST /convert")
    print(f"Content-Type: multipart/form-data")
    print(f"Field: video")
    print(f"File: {test_video}")
    print(f"Size: {os.path.getsize(test_video) / 1024:.2f} KB")
    print()
    
    print("⚙️  API Processing Steps:")
    print("-" * 60)
    print("1. ✅ Validate file type (MP4)")
    print("2. ✅ Check file size (within 100MB limit)")
    print("3. ✅ Generate unique ID")
    print("4. ✅ Save uploaded file to /tmp/uploads/")
    print("5. ✅ Extract video metadata")
    print("6. 🔄 Convert with FFmpeg:")
    print("   - Codec: H.264")
    print("   - Resolution: 1080p")
    print("   - Bitrate: 5000k")
    print("   - Quality: CRF 18")
    print("   - Duration: Max 30s")
    print("7. ✅ Save to /tmp/outputs/")
    print("8. ✅ Return optimized video")
    print("9. ✅ Schedule cleanup (1 hour)")
    print()
    
    # Simulate conversion
    output_video = '/home/claude/whatsapp_optimized.mp4'
    
    if os.path.exists(output_video):
        print("📥 API Response:")
        print("-" * 60)
        print("Status: 200 OK")
        print("Content-Type: video/mp4")
        print("Content-Disposition: attachment; filename='whatsapp_optimized_xxxxx.mp4'")
        print(f"File Size: {os.path.getsize(output_video) / 1024:.2f} KB")
        print()
        
        print("✅ Success! Video optimized and ready for download")
        print()
        
        # Show what the iPhone Shortcut would receive
        print("📱 iPhone Shortcut receives:")
        print("-" * 60)
        print("- Optimized MP4 file")
        print("- High quality (minimal WhatsApp compression)")
        print("- 1080p resolution")
        print("- Ready for WhatsApp status")
        print()
        
        print("🎯 Final Steps (in iPhone):")
        print("-" * 60)
        print("1. Shortcut saves video to Photos/Files")
        print("2. User opens WhatsApp")
        print("3. User selects the converted video for status")
        print("4. WhatsApp applies minimal additional compression")
        print("5. Status looks HD! 🎉")
    else:
        print("❌ Converted video not found")
    
    print()
    print("="*60)

def show_curl_example():
    """Show example curl command for testing"""
    print("\n" + "="*60)
    print("Example API Usage with curl:")
    print("="*60)
    print()
    
    print("# Upload and convert a video")
    print("curl -X POST \\")
    print("  -F 'video=@your-video.mp4' \\")
    print("  https://marrecluse.net/convert \\")
    print("  --output converted-video.mp4")
    print()
    
    print("# Check API health")
    print("curl https://marrecluse.net/health")
    print()
    
    print("# Get API info")
    print("curl https://marrecluse.net/")
    print()

def show_python_example():
    """Show example Python code"""
    print("="*60)
    print("Example Python Client Code:")
    print("="*60)
    print()
    
    code = '''import requests

# Upload video for conversion
def convert_video(video_path, output_path):
    url = 'https://marrecluse.net/convert'
    
    with open(video_path, 'rb') as video_file:
        files = {'video': video_file}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Video converted: {output_path}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return False

# Usage
convert_video('my-video.mp4', 'whatsapp-ready.mp4')
'''
    
    print(code)

def show_javascript_example():
    """Show example JavaScript code for web"""
    print("="*60)
    print("Example JavaScript Client Code (for web):")
    print("="*60)
    print()
    
    code = '''async function convertVideo(videoFile) {
  const formData = new FormData();
  formData.append('video', videoFile);
  
  const response = await fetch('https://marrecluse.net/convert', {
    method: 'POST',
    body: formData
  });
  
  if (response.ok) {
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    
    // Create download link
    const a = document.createElement('a');
    a.href = url;
    a.download = 'whatsapp-optimized.mp4';
    a.click();
    
    console.log('✅ Video converted!');
  } else {
    const error = await response.json();
    console.error('❌ Error:', error);
  }
}

// Usage with file input
document.querySelector('#videoInput').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    convertVideo(file);
  }
});
'''
    
    print(code)

if __name__ == '__main__':
    test_api_locally()
    show_curl_example()
    show_python_example()
    show_javascript_example()
    
    print("="*60)
    print("Next Steps:")
    print("="*60)
    print("1. Deploy the API to your server (see DEPLOYMENT.md)")
    print("2. Set up DNS for marrecluse.net")
    print("3. Configure iPhone Shortcuts (see IPHONE_SHORTCUTS_COMPLETE.md)")
    print("4. Test with a real video")
    print("5. Enjoy HD WhatsApp status! 🎉")
    print()
