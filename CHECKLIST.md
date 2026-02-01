# 🚀 Deployment Checklist

## Pre-Deployment

- [ ] All files are ready in your project directory:
  - [ ] `app.py` (main API application)
  - [ ] `requirements.txt` (Python dependencies)
  - [ ] `Procfile` (for deployment platform)
  - [ ] `README.md` (documentation)
  - [ ] `DEPLOYMENT.md` (deployment guide)
  - [ ] `IPHONE_SHORTCUTS_COMPLETE.md` (shortcuts guide)

- [ ] Test conversion works locally:
  ```bash
  python3 test_conversion.py
  ```

- [ ] GitHub repository created and code pushed

## Step 1: Choose Hosting Platform

### ✅ Railway (Recommended - Easiest)
**Pros:** Auto-detects Python, includes FFmpeg, free tier, easy custom domains
**Setup Time:** 5-10 minutes

- [ ] Go to [railway.app](https://railway.app)
- [ ] Sign up with GitHub
- [ ] Create new project
- [ ] Deploy from GitHub repository
- [ ] Wait for deployment to complete
- [ ] Test deployment: `https://your-app.railway.app/health`

### ✅ Render
**Pros:** Free tier, auto SSL, easy setup
**Setup Time:** 10-15 minutes

- [ ] Go to [render.com](https://render.com)
- [ ] Create Web Service
- [ ] Connect GitHub repo
- [ ] Configure:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app`
- [ ] Add FFmpeg in build script (see DEPLOYMENT.md)
- [ ] Deploy and test

### ✅ Heroku
**Pros:** Well-documented, reliable
**Setup Time:** 15-20 minutes

- [ ] Install Heroku CLI
- [ ] Login: `heroku login`
- [ ] Create app: `heroku create your-app-name`
- [ ] Add FFmpeg buildpack:
  ```bash
  heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
  ```
- [ ] Push to Heroku: `git push heroku main`
- [ ] Test: `heroku open`

## Step 2: Configure Custom Domain

### On Hosting Platform:

- [ ] Navigate to project settings
- [ ] Find "Custom Domain" or "Domains" section
- [ ] Add domain: `marrecluse.net`
- [ ] Note the DNS target provided (e.g., `your-app.railway.app`)

### On Domain Registrar/DNS Provider:

From your screenshot, you're using GitHub Pages DNS. You need to update:

- [ ] Remove or update existing DNS records
- [ ] Add new DNS records:

**Option A: CNAME (Recommended)**
```
Type: CNAME
Name: @
Value: your-app.railway.app (or your platform's URL)
TTL: Automatic
```

**Option B: A Record (if CNAME at apex not supported)**
```
Type: A
Name: @
Value: [IP from hosting platform]
TTL: Automatic
```

**WWW subdomain:**
```
Type: CNAME
Name: www
Value: marrecluse.net
TTL: Automatic
```

- [ ] Save DNS changes
- [ ] Wait for DNS propagation (can take 5 minutes - 48 hours)

## Step 3: Test API Deployment

### Test Health Endpoint:
- [ ] Visit in browser: `https://marrecluse.net/health`
- [ ] Should see: `{"status": "healthy", "timestamp": "..."}`

### Test Info Endpoint:
- [ ] Visit: `https://marrecluse.net/`
- [ ] Should see API information and usage instructions

### Test Conversion with curl:
```bash
# Create a small test video first or use an existing one
curl -X POST \
  -F "video=@test.mp4" \
  https://marrecluse.net/convert \
  --output converted.mp4

# Check if converted.mp4 was created and is valid
ls -lh converted.mp4
```

- [ ] curl command succeeds
- [ ] converted.mp4 file created
- [ ] Video plays correctly

## Step 4: Configure HTTPS/SSL

Most platforms provide this automatically:

- [ ] SSL certificate is active (look for 🔒 in browser)
- [ ] HTTP redirects to HTTPS
- [ ] No certificate warnings

If not automatic:
- [ ] Enable SSL in platform settings
- [ ] May need to verify domain ownership

## Step 5: Set Up iPhone Shortcuts

- [ ] Open Shortcuts app on iPhone
- [ ] Follow `IPHONE_SHORTCUTS_COMPLETE.md` guide
- [ ] Create shortcut with these actions:
  1. Select Photos
  2. Get File
  3. Get Contents of URL (POST to your API)
  4. Save File
  5. Share (optional)

- [ ] Test with a short video (5-10 seconds)
- [ ] Verify conversion completes successfully
- [ ] Check video quality

## Step 6: Production Testing

### Test Different Scenarios:

- [ ] **Small video** (< 5MB): Should complete in 5-15 seconds
- [ ] **Medium video** (5-20MB): Should complete in 15-30 seconds
- [ ] **Large video** (20-50MB): Should complete in 30-60 seconds
- [ ] **Different formats**: Test MP4, MOV, etc.
- [ ] **Different resolutions**: Test 720p, 1080p, 4K
- [ ] **Vertical video**: Test portrait orientation
- [ ] **Horizontal video**: Test landscape orientation

### Edge Cases:

- [ ] Video > 100MB (should be rejected)
- [ ] Invalid file type (should be rejected)
- [ ] Corrupted video (should return error)
- [ ] Very long video (> 5 minutes)

### WhatsApp Quality Test:

- [ ] Upload ORIGINAL video to WhatsApp Status
  - [ ] Take screenshot or save
- [ ] Upload CONVERTED video to WhatsApp Status
  - [ ] Take screenshot or save
- [ ] Compare quality side-by-side
- [ ] Converted should be noticeably better

## Step 7: Monitoring & Optimization

### Set Up Monitoring:

- [ ] Platform monitoring (check built-in tools)
- [ ] Add uptime monitoring (UptimeRobot/Pingdom)
- [ ] Set up alerts for downtime

### Performance Optimization:

- [ ] Monitor response times
- [ ] Check server resources (CPU/memory)
- [ ] Consider increasing workers if needed
- [ ] Add rate limiting if getting too many requests

### Cost Management:

- [ ] Check current usage
- [ ] Estimate monthly costs
- [ ] Set up billing alerts
- [ ] Consider paid plan if free tier exceeded

## Step 8: Share & Document

### For Yourself:

- [ ] Save the shortcut configuration
- [ ] Bookmark the API URL
- [ ] Save conversion settings
- [ ] Document any customizations made

### For Others (Optional):

- [ ] Share shortcut with friends
- [ ] Create tutorial video
- [ ] Write blog post
- [ ] Share on social media

## Troubleshooting Common Issues

### DNS Not Resolving:
```bash
# Check DNS propagation
dig marrecluse.net
nslookup marrecluse.net

# If not propagated, wait longer or use different DNS server
```

### API Returns 502/504:
- Check if app is running on platform
- Check logs for errors
- Verify FFmpeg is installed
- Increase timeout settings

### Conversion Fails:
- Check FFmpeg installation
- Verify video file is valid
- Check server has enough memory
- Look at error logs

### Shortcut Not Working:
- Verify API URL is correct
- Check form field name is "video"
- Ensure CORS is enabled
- Test API with curl first

## Final Verification

- [ ] API is accessible via custom domain
- [ ] HTTPS is working
- [ ] iPhone Shortcut successfully converts videos
- [ ] Video quality is significantly better on WhatsApp
- [ ] All documentation is accessible
- [ ] Monitoring is active

## 🎉 You're Done!

Your WhatsApp HD Video Converter is now live and ready to use!

**Quick Reference:**
- API: https://marrecluse.net
- Health Check: https://marrecluse.net/health
- iPhone Shortcut: See IPHONE_SHORTCUTS_COMPLETE.md

**Enjoy HD quality WhatsApp status! 📱✨**
