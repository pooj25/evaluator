# 🚀 Quick Deploy to Streamlit Cloud (5 Minutes)

## Step-by-Step Guide

### ✅ Step 1: Verify Your Code is on GitHub
```bash
# Check if everything is committed
git status

# If there are changes, commit them
git add .
git commit -m "Ready for deployment"
git push
```

### ✅ Step 2: Go to Streamlit Cloud
1. Visit: **https://share.streamlit.io/**
2. Click **"Sign in"** (top right)
3. Sign in with your **GitHub account**

### ✅ Step 3: Deploy Your App
1. Click **"New app"** button
2. Fill in the form:
   - **Repository:** Select `pooj25/evaluator`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** (optional) Choose a custom name
3. Click **"Deploy"**

### ✅ Step 4: Wait for Deployment
- First deployment takes 2-3 minutes
- Streamlit Cloud will:
  - Install all dependencies from `requirements.txt`
  - Set up the environment
  - Launch your app

### ✅ Step 5: Access Your App
- Once deployed, you'll get a URL like:
  `https://your-app-name.streamlit.app`
- Share this URL with anyone!

---

## 🎉 That's It!

Your app is now live on the internet!

### What Works:
- ✅ Full application functionality
- ✅ Image uploads (temporary storage)
- ✅ OCR processing
- ✅ AI evaluation
- ✅ Database (SQLite - resets on redeploy)

### Important Notes:
- ⚠️ **Tesseract OCR:** Streamlit Cloud may not have Tesseract pre-installed
  - If OCR doesn't work, you may need to use text input only
  - Or consider Railway/Render which allow system packages

- ⚠️ **File Uploads:** Files are temporary (deleted after session)
  - For permanent storage, consider cloud storage (S3, etc.)

- ⚠️ **Database:** SQLite database resets on redeploy
  - For persistent data, use PostgreSQL (available on Railway/Render)

---

## 🔄 Updating Your App

Every time you push to GitHub, Streamlit Cloud automatically redeploys!

```bash
# Make changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Update feature"
git push

# Streamlit Cloud automatically redeploys!
```

---

## 🐛 Troubleshooting

### Issue: OCR Not Working
**Solution:** Tesseract might not be available. Options:
1. Use text input instead of image upload
2. Deploy on Railway/Render (allow system packages)
3. Use cloud-based OCR API

### Issue: App Won't Deploy
**Check:**
- ✅ All files committed to GitHub
- ✅ `app.py` is in root directory
- ✅ `requirements.txt` exists
- ✅ No syntax errors

### Issue: Dependencies Error
**Solution:** Check `requirements.txt` has all packages

---

## 📊 Alternative: Railway (If OCR Needed)

If you need Tesseract OCR to work:

1. Go to **https://railway.app/**
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Select your repository
6. Railway will auto-detect and deploy

Railway allows system packages, so Tesseract will work!

---

## 🎯 Recommended: Start with Streamlit Cloud

**Why?**
- ✅ Easiest setup
- ✅ Free
- ✅ Automatic updates
- ✅ Perfect for demos

**Then migrate to Railway if:**
- You need Tesseract OCR
- You need persistent database
- You need permanent file storage

---

## 📞 Need Help?

Check the full guide: `DEPLOYMENT_GUIDE.md`

Good luck! 🚀

