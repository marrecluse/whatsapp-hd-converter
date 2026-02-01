# Deployment Guide

## Overview

This API needs to be hosted on a server (not GitHub Pages, as it requires backend processing).
GitHub Pages only supports static files, but you can use your custom domain with other hosting services.

## Recommended Hosting Options

### Option 1: Railway (Easiest - Free Tier Available)
1. Go to railway.app
2. Sign up with GitHub
3. Create new project from GitHub repo
4. Railway will auto-detect the Python app
5. Add custom domain: marrecluse.net
6. Update DNS:
   - Add CNAME record: `marrecluse.net` → `your-app.railway.app`

### Option 2: Render (Free Tier Available)
1. Go to render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Add custom domain in settings
7. Update DNS as instructed

### Option 3: DigitalOcean App Platform
1. Go to digitalocean.com
2. Create App Platform app
3. Connect GitHub repo
4. Configure domain in settings
5. Update DNS to point to App Platform

### Option 4: Heroku
1. Install Heroku CLI
2. Create Heroku app
3. Add Procfile (already included)
4. Push to Heroku
5. Add custom domain addon
6. Update DNS settings

### Option 5: VPS (Full Control)
Deploy on any VPS (DigitalOcean Droplet, AWS EC2, etc.)
1. Install Python, FFmpeg, Nginx
2. Clone your repo
3. Set up systemd service
4. Configure Nginx as reverse proxy
5. Point DNS to VPS IP

## DNS Configuration

For any hosting option, update your DNS settings:

**For Railway/Render/Heroku:**
```
Type: CNAME
Name: @
Value: your-app.railway.app (or equivalent)
```

**For VPS:**
```
Type: A
Name: @
Value: YOUR_VPS_IP_ADDRESS
```

**Don't forget www subdomain:**
```
Type: CNAME
Name: www
Value: marrecluse.net
```

## Files Needed for Deployment

### Procfile (for Heroku/Railway)
```
web: gunicorn app:app
```

### Railway/Render Config
Both auto-detect Python and will install from requirements.txt

## Environment Setup

Most platforms will automatically:
1. Detect Python app
2. Install requirements.txt
3. Start gunicorn

Make sure FFmpeg is available:
- Railway: Add buildpack
- Render: Use `apt-get install ffmpeg` in build script
- Heroku: Add FFmpeg buildpack

## Testing Deployment

Once deployed, test with:

```bash
# Health check
curl https://marrecluse.net/health

# API info
curl https://marrecluse.net/

# Upload test video
curl -X POST -F "video=@test.mp4" https://marrecluse.net/convert --output converted.mp4
```

## HTTPS/SSL

All recommended platforms provide free SSL certificates automatically.
Your API will be accessible via https://marrecluse.net

## Monitoring

Consider adding:
- Uptime monitoring (UptimeRobot, Pingdom)
- Error tracking (Sentry)
- Usage analytics

## Costs

**Free Tiers:**
- Railway: 500 hours/month free
- Render: Free for web services (with limitations)
- Heroku: Hobby tier available

**Paid (if you exceed free tier):**
- Railway: ~$5-10/month
- Render: $7/month minimum
- VPS: $5-10/month

## Important Notes

1. **FFmpeg Required:** Make sure your hosting platform supports or allows FFmpeg installation
2. **File Storage:** Videos are stored temporarily in /tmp (auto-cleanup after 1 hour)
3. **Processing Time:** Large videos take time - consider setting longer timeouts
4. **Rate Limiting:** Consider adding rate limiting for production use

## Quick Deploy to Railway (Recommended)

1. Push your code to GitHub
2. Visit railway.app
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Railway auto-detects Python
6. Add these environment variables (if needed):
   - `PYTHON_VERSION=3.12`
7. Add custom domain in Settings
8. Update your DNS records

## GitHub Repository Structure

Your repo should have:
```
/
├── app.py
├── requirements.txt
├── Procfile
├── README.md
└── SHORTCUTS_GUIDE.md
```
