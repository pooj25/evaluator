# GitHub Setup Instructions

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `intelligent-evaluator` (or any name you prefer)
5. Description: "AI-Powered Rubric-based Evaluation System for Algorithms, Flowcharts & Pseudocodes"
6. Choose **Public** or **Private** (your choice)
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

### If you haven't set up SSH (use HTTPS):
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### If you have SSH set up:
```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Push Your Code

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name, then run:

```bash
# Add remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Quick Commands Reference

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Repository is Ready!

Your code is now on GitHub! 🎉

### What's Included:
- ✅ Complete Intelligent Evaluator System
- ✅ Enhanced OCR for blurry images
- ✅ Beautiful Streamlit UI
- ✅ AI-powered evaluation engine
- ✅ Comprehensive documentation
- ✅ Setup and test scripts

