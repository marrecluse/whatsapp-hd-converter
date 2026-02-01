# WhatsApp HD Video Converter API

A Flask-based API that optimizes videos for WhatsApp status uploads while maintaining high quality. Designed to work seamlessly with iPhone Shortcuts app.

## 🎯 Problem Solved

WhatsApp heavily compresses videos when you upload them as status updates, resulting in poor quality. This tool pre-optimizes videos with the perfect settings to minimize WhatsApp's additional compression while staying within WhatsApp's limits.

## ✨ Features

- **High Quality Output:** Uses FFmpeg with optimized settings (CRF 18, 5Mbps bitrate)
- **WhatsApp Compatible:** 1080p resolution, H.264 codec, 30-second duration
- **iPhone Shortcuts Ready:** Simple POST API for easy integration
- **Auto Cleanup:** Temporary files deleted after 1 hour
- **CORS Enabled:** Works from any origingit 
- **Fast Processing:** Optimized preset for quick conversion

## 🚀 Quick Start

### For iPhone Users

1. Check `SHORTCUTS_GUIDE.md` for detailed iPhone Shortcuts setup
2. Create a shortcut that POSTs to `/convert` endpoint
3. Select video → Convert → Share to WhatsApp

### API Usage

**Endpoint:** `POST /convert`

**Request:**
```bash
curl -X POST \
  -F "video=@your-video.mp4" \
  https://marrecluse.net/convert \
  --output optimized.mp4
```

**Response:** Optimized MP4 video file

## 📋 Technical Specs

### Input
- Max file size: 100MB
- Supported formats: MP4, MOV, AVI, MKV, WEBM, M4V
- Any resolution/bitrate

### Output
- Format: MP4 (H.264 + AAC)
- Resolution: 1080p (maintains aspect ratio)
- Video bitrate: 5000 kbps
- Audio bitrate: 192 kbps
- Duration: Max 30 seconds
- Optimized for WhatsApp status

## 🛠️ Installation

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure FFmpeg is installed
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Run the server
python app.py
```

Server runs on `http://localhost:5000`

### Production Deployment

See `DEPLOYMENT.md` for detailed deployment instructions for:
- Railway (Recommended)
- Render
- DigitalOcean
- Heroku
- VPS

## 📡 API Endpoints

### `GET /`
Returns API information and usage instructions

### `GET /health`
Health check endpoint

### `POST /convert`
Main conversion endpoint
- Accepts: `multipart/form-data` with `video` field
- Returns: Optimized MP4 file

## 🔧 Configuration

Key FFmpeg parameters in `app.py`:

```python
-preset slow          # Better quality (slower encoding)
-crf 18              # High quality (lower = better)
-b:v 5000k           # Video bitrate
-vf scale=1080:-2    # Scale to 1080p width
-b:a 192k            # Audio bitrate
-t 30                # Max 30 seconds
```

## 🧪 Testing

### Test with curl:
```bash
# Upload a video
curl -X POST \
  -F "video=@test.mp4" \
  http://localhost:5000/convert \
  --output converted.mp4

# Check health
curl http://localhost:5000/health
```

### Test with Python:
```python
import requests

with open('test.mp4', 'rb') as f:
    files = {'video': f}
    response = requests.post('http://localhost:5000/convert', files=files)
    
with open('output.mp4', 'wb') as f:
    f.write(response.content)
```

## 📱 iPhone Shortcuts Integration

See `SHORTCUTS_GUIDE.md` for complete setup instructions.

Quick summary:
1. Create new shortcut
2. Select video from Photos
3. POST to API endpoint with video file
4. Save converted video
5. Share to WhatsApp

## 🔒 Security Features

- File size limits (100MB max)
- File type validation
- Automatic cleanup of temporary files
- Unique file IDs prevent conflicts
- No permanent storage of user videos

## ⚙️ Requirements

- Python 3.8+
- FFmpeg 4.0+
- Flask 3.0+
- flask-cors 4.0+
- gunicorn (for production)

## 📊 Performance

- Small videos (<10MB): ~5-15 seconds
- Medium videos (10-50MB): ~15-45 seconds
- Large videos (50-100MB): ~45-90 seconds

Processing time depends on:
- Video length
- Input quality
- Server resources

## 🐛 Troubleshooting

**Conversion fails:**
- Check FFmpeg is installed: `ffmpeg -version`
- Ensure video file is valid
- Check file size is under 100MB

**Slow processing:**
- Use shorter videos (under 1 minute recommended)
- Consider trimming before upload
- Check server resources

**iPhone Shortcuts not working:**
- Verify API URL is correct
- Check form field name is `video`
- Ensure CORS is enabled

## 📝 License

MIT License - feel free to modify and use for your needs.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add progress tracking
- Support batch processing
- Add more output format options
- Implement rate limiting
- Add video preview generation

## 📧 Support

For issues with:
- **API:** Check server logs and FFmpeg output
- **iPhone Shortcuts:** See SHORTCUTS_GUIDE.md
- **Deployment:** See DEPLOYMENT.md

## 🔗 Links

- FFmpeg Documentation: https://ffmpeg.org/documentation.html
- Flask Documentation: https://flask.palletsprojects.com/
- WhatsApp Status Specs: Check WhatsApp's official documentation

---

Built with ❤️ to solve the WhatsApp status quality problem
