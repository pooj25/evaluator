# 🚀 Deployment Guide: Hosting Your Evaluator System

## Option 1: Streamlit Cloud (Easiest - Recommended) ⭐

### Why Streamlit Cloud?
- ✅ Free hosting
- ✅ Easy deployment (just connect GitHub)
- ✅ Automatic updates on git push
- ✅ No server management
- ✅ Perfect for Streamlit apps

### Steps:

#### 1. Prepare Your Repository
```bash
# Make sure everything is committed and pushed to GitHub
git status
git add .
git commit -m "Ready for deployment"
git push
```

#### 2. Create Streamlit Cloud Account
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"

#### 3. Deploy
1. **Connect Repository:**
   - Select your GitHub repository: `pooj25/evaluator`
   - Branch: `main`
   - Main file path: `app.py`

2. **Advanced Settings (Optional):**
   - Python version: 3.10 or 3.11
   - Add secrets if needed (for API keys, etc.)

3. **Click "Deploy"**

#### 4. Important Notes for Streamlit Cloud:
- ✅ SQLite database works (but resets on redeploy)
- ✅ File uploads work (temporary storage)
- ⚠️ Uploads folder is ephemeral (files deleted after session)
- ✅ All dependencies from requirements.txt are installed automatically

#### 5. Your App URL:
After deployment, you'll get a URL like:
`https://your-app-name.streamlit.app`

---

## Option 2: Railway (Good for Persistent Storage)

### Why Railway?
- ✅ Free tier available
- ✅ Persistent storage (database and uploads)
- ✅ Easy deployment
- ✅ Automatic HTTPS

### Steps:

#### 1. Install Railway CLI
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Or download from: https://railway.app/cli
```

#### 2. Login
```bash
railway login
```

#### 3. Initialize Project
```bash
cd C:\Users\Pooja\OneDrive\Desktop\evaluator
railway init
```

#### 4. Create railway.json
Create a file `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port $PORT --server.address 0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 5. Deploy
```bash
railway up
```

#### 6. Set Environment Variables (if needed)
```bash
railway variables set PORT=8501
```

#### 7. Get Your URL
```bash
railway domain
```

---

## Option 3: Render (Free Tier Available)

### Steps:

#### 1. Create render.yaml
Create `render.yaml` in your project root:
```yaml
services:
  - type: web
    name: intelligent-evaluator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PORT
        value: 8501
```

#### 2. Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Settings:
   - **Name:** intelligent-evaluator
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Click "Create Web Service"

---

## Option 4: Heroku (Classic Option)

### Steps:

#### 1. Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

#### 2. Create Procfile
Create `Procfile` (no extension):
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### 3. Create runtime.txt
Create `runtime.txt`:
```
python-3.11.0
```

#### 4. Login and Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

## Option 5: DigitalOcean App Platform

### Steps:

1. Go to https://www.digitalocean.com/products/app-platform
2. Connect GitHub repository
3. Configure:
   - **Type:** Web Service
   - **Run Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Build Command:** `pip install -r requirements.txt`
4. Deploy

---

## 🔧 Pre-Deployment Checklist

### 1. Update app.py for Cloud Deployment
We need to make some adjustments for cloud hosting:

```python
# Add at the top of app.py
import os

# Update database path for cloud
if os.getenv('CLOUD_DEPLOY'):
    DB_PATH = '/tmp/evaluator.db'  # Temporary storage
else:
    DB_PATH = 'evaluator.db'
```

### 2. Handle File Uploads
For cloud, uploads might be temporary. Consider:
- Using cloud storage (AWS S3, Google Cloud Storage)
- Or accept that uploads are session-only

### 3. Environment Variables
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

---

## 📝 Quick Setup for Streamlit Cloud (Recommended)

### Step 1: Create .streamlit/config.toml
```bash
mkdir .streamlit
```

Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Step 2: Update app.py for Cloud
Add this at the top of app.py (after imports):
```python
# Cloud deployment configuration
import os
CLOUD_DEPLOY = os.getenv('STREAMLIT_CLOUD', False)
```

### Step 3: Commit and Push
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push
```

### Step 4: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `pooj25/evaluator`
5. Main file: `app.py`
6. Click "Deploy"

---

## 🌐 Domain & Custom URL

### Streamlit Cloud:
- Default: `your-app-name.streamlit.app`
- Custom domain: Not available on free tier

### Railway:
- Default: `your-app-name.up.railway.app`
- Custom domain: Available (add in dashboard)

### Render:
- Default: `your-app-name.onrender.com`
- Custom domain: Available

---

## 💾 Database Considerations

### For Persistent Storage:

#### Option A: Use PostgreSQL (Cloud)
1. Railway/Render provide free PostgreSQL
2. Update database.py to use PostgreSQL:
```python
# For PostgreSQL
from sqlalchemy import create_engine
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///evaluator.db')
engine = create_engine(DATABASE_URL)
```

#### Option B: Keep SQLite (Temporary)
- Works for demos
- Data resets on redeploy
- Good for testing

---

## 🔒 Security Considerations

1. **Environment Variables:**
   - Don't commit secrets
   - Use platform's secret management

2. **File Uploads:**
   - Limit file size
   - Validate file types
   - Consider cloud storage for permanent files

3. **Rate Limiting:**
   - Consider adding rate limits for production

---

## 📊 Monitoring & Analytics

### Streamlit Cloud:
- Built-in analytics
- View app usage
- Error logs

### Railway:
- Logs available in dashboard
- Metrics and monitoring

---

## 🐛 Troubleshooting

### Common Issues:

1. **Port Error:**
   - Make sure to use `$PORT` environment variable
   - Set address to `0.0.0.0`

2. **Dependencies:**
   - Check requirements.txt is complete
   - Some packages might need system dependencies

3. **Database:**
   - SQLite might have permission issues
   - Consider PostgreSQL for production

4. **File Uploads:**
   - Temporary storage on most platforms
   - Consider cloud storage for persistence

---

## 🎯 Recommended: Streamlit Cloud

**For your project, I recommend Streamlit Cloud because:**
- ✅ Easiest setup
- ✅ Free
- ✅ Automatic deployments
- ✅ Perfect for Streamlit apps
- ✅ No server management

**Quick Deploy:**
1. Push code to GitHub ✅ (Already done!)
2. Go to https://share.streamlit.io/
3. Connect repository
4. Deploy!

---

## 📞 Need Help?

If you encounter issues:
1. Check platform logs
2. Verify requirements.txt
3. Test locally first
4. Check platform documentation

Good luck with deployment! 🚀

