#!/usr/bin/env python3
"""
Test script for WhatsApp HD Video Converter
This demonstrates the core video conversion functionality without running the Flask server
"""

import subprocess
import os
import sys

def optimize_for_whatsapp(input_path, output_path):
    """
    Optimize video for WhatsApp status with these settings:
    - High quality H.264 encoding
    - 1080p max resolution (maintains aspect ratio)
    - High bitrate (5000k video, 192k audio)
    - 30 second max duration
    - MP4 container with proper flags for compatibility
    """
    
    print(f"Converting: {input_path}")
    print(f"Output: {output_path}")
    print("\nConversion settings:")
    print("  - Max duration: 30 seconds")
    print("  - Resolution: 1080p (width)")
    print("  - Video codec: H.264")
    print("  - Video bitrate: 5000k")
    print("  - Audio codec: AAC")
    print("  - Audio bitrate: 192k")
    print("  - Quality: CRF 18 (very high)")
    print("\n" + "="*50)
    
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
    
    print("\nRunning FFmpeg conversion...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Error during conversion:")
        print(result.stderr)
        return False
    
    print("\n✅ Conversion successful!")
    
    # Show file sizes
    if os.path.exists(input_path) and os.path.exists(output_path):
        input_size = os.path.getsize(input_path) / (1024 * 1024)
        output_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\nInput size: {input_size:.2f} MB")
        print(f"Output size: {output_size:.2f} MB")
        
        if output_size < input_size:
            savings = ((input_size - output_size) / input_size) * 100
            print(f"Size reduction: {savings:.1f}%")
        elif output_size > input_size:
            increase = ((output_size - input_size) / input_size) * 100
            print(f"Size increase: {increase:.1f}% (due to higher quality settings)")
    
    return True

def create_test_video():
    """Create a simple test video using FFmpeg"""
    output = '/home/claude/test_input.mp4'
    
    print("Creating test video...")
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'testsrc=duration=5:size=1920x1080:rate=30',
        '-f', 'lavfi',
        '-i', 'sine=frequency=1000:duration=5',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',
        output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Test video created: {output}")
        return output
    else:
        print("❌ Failed to create test video")
        print(result.stderr)
        return None

if __name__ == '__main__':
    print("="*50)
    print("WhatsApp HD Video Converter - Test Script")
    print("="*50)
    print()
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"❌ Error: File not found: {input_file}")
            sys.exit(1)
    else:
        print("No input file provided. Creating test video...\n")
        input_file = create_test_video()
        if not input_file:
            sys.exit(1)
        print()
    
    output_file = '/home/claude/whatsapp_optimized.mp4'
    
    success = optimize_for_whatsapp(input_file, output_file)
    
    if success:
        print(f"\n{'='*50}")
        print(f"✅ Video optimized for WhatsApp!")
        print(f"{'='*50}")
        print(f"\nOutput saved to: {output_file}")
        print("\nThis video is now optimized for WhatsApp status:")
        print("  • High quality (minimal compression)")
        print("  • Perfect for WhatsApp's requirements")
        print("  • Ready to upload without further quality loss")
        print("\nNext steps:")
        print("  1. Deploy the API to your server")
        print("  2. Set up iPhone Shortcuts (see SHORTCUTS_GUIDE.md)")
        print("  3. Upload to WhatsApp and enjoy HD quality!")
    else:
        print("\n❌ Conversion failed")
        sys.exit(1)
