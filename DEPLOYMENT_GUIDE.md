# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying the Codebase Q&A application to various platforms.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- ✅ Pinecone API Key ([Get it here](https://app.pinecone.io/))
- ✅ GitHub repository with your code
- ✅ All files committed and pushed

---

## 🎯 Option 1: Deploy to Render (Recommended)

Render is excellent for Python applications with a generous free tier.

### Step 1: Prepare Your Repository

Ensure these files are in your repository:
- `app.py`
- `requirements.txt`
- `Procfile`
- `runtime.txt`

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up or log in with GitHub

### Step 3: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure the service:
   - **Name:** `codebase-qa-app` (or your preferred name)
   - **Region:** Choose closest to you
   - **Branch:** `main` (or your default branch)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

### Step 4: Add Environment Variables

In the "Environment" section, add:

```
GOOGLE_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Access your app at `https://your-app-name.onrender.com`

### Render Free Tier Notes:
- ✅ 750 hours/month free
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold starts take ~30 seconds

---

## 🚂 Option 2: Deploy to Railway

Railway offers excellent developer experience with automatic deployments.

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository

### Step 3: Configure Environment Variables

1. Go to **"Variables"** tab
2. Add variables:

```
GOOGLE_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### Step 4: Configure Start Command (if needed)

Railway usually auto-detects Streamlit, but if needed:

1. Go to **"Settings"** → **"Deploy"**
2. Set custom start command:
   ```
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

### Step 5: Deploy

1. Railway auto-deploys on push to main
2. Access your app at the generated Railway URL

### Railway Free Tier Notes:
- ✅ $5 free credit monthly
- ✅ Always-on (no cold starts)
- ⚠️ Credit-based billing

---

## ☁️ Option 3: Deploy to Streamlit Community Cloud

Streamlit's native platform - simplest but with limitations.

### Step 1: Prepare Repository

1. Push code to GitHub
2. Ensure these files exist:
   - `app.py`
   - `requirements.txt`

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select repository, branch, and main file (`app.py`)

### Step 3: Add Secrets

Click **"Advanced settings"** → **"Secrets"**

Add in TOML format:
```toml
GOOGLE_API_KEY = "your_google_api_key"
PINECONE_API_KEY = "your_pinecone_api_key"
```

### Step 4: Deploy

1. Click **"Deploy"**
2. Access at `https://your-app-name.streamlit.app`

### Streamlit Cloud Limitations:
- ⚠️ Limited resources (1 GB RAM)
- ⚠️ Public apps only (in free tier)
- ⚠️ Not suitable for large codebases
- ✅ Always-on
- ✅ Easy SSL/HTTPS

---

## 🔧 Option 4: Deploy to Heroku

Heroku is reliable but no longer has a free tier.

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App

```bash
heroku login
heroku create codebase-qa-app
```

### Step 3: Set Environment Variables

```bash
heroku config:set GOOGLE_API_KEY=your_key
heroku config:set PINECONE_API_KEY=your_key
```

### Step 4: Deploy

```bash
git push heroku main
```

### Step 5: Open App

```bash
heroku open
```

---

## 🐳 Option 5: Docker Deployment

For self-hosting or custom environments.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install git for GitHub cloning
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build
docker build -t codebase-qa-app .

# Run with environment variables
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  codebase-qa-app
```

---

## 🔍 Verifying Deployment

After deployment, verify:

1. **Home Page Loads**
   - ✅ UI renders correctly
   - ✅ Status indicators in sidebar

2. **Service Status**
   - ✅ LLM: Green (Connected)
   - ✅ Embeddings: Green (Connected)
   - ✅ Database: Green (Connected)

3. **Test Upload**
   - ✅ Upload small ZIP file
   - ✅ Indexing completes successfully

4. **Test Q&A**
   - ✅ Ask a question
   - ✅ Receive answer with sources

---

## 🐛 Troubleshooting Deployment

### Issue: "Application Error" on startup

**Solution:**
1. Check logs for specific error
2. Verify environment variables are set
3. Ensure `requirements.txt` is complete

### Issue: Import errors

**Solution:**
```bash
# Verify requirements.txt versions
pip freeze > requirements.txt
```

### Issue: Port binding error

**Solution:** Ensure start command uses `$PORT`:
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Issue: Timeout during git clone

**Solution:**
- Increase timeout in platform settings
- Or use smaller test repositories

### Issue: Memory errors with large codebases

**Solution:**
- Reduce `MAX_CODEBASE_SIZE_MB` in `app.py`
- Upgrade to paid tier with more RAM

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | 750 hrs/month | $7/month | Production apps |
| **Railway** | $5 credit/month | Pay-as-you-go | Quick deploys |
| **Streamlit Cloud** | 1 app | $20/month | Demos/MVPs |
| **Heroku** | None | $7/month | Enterprise |
| **Self-hosted** | Free | Variable | Full control |

---

## 📊 Performance Tips

### For Production Deployment:

1. **Enable Caching**
   ```python
   @st.cache_resource
   def get_embeddings():
       return GoogleGenerativeAIEmbeddings(...)
   ```

2. **Optimize Chunking**
   - Reduce chunk_size for faster processing
   - Adjust chunk_overlap based on code structure

3. **Limit Concurrent Users**
   - Add rate limiting
   - Implement queue system for indexing

4. **Monitor Usage**
   - Track API usage (Gemini, Pinecone)
   - Set up alerts for quota limits

---

## 🔐 Security Checklist

Before deploying:

- ✅ No API keys in code
- ✅ Environment variables set correctly
- ✅ `.env` in `.gitignore`
- ✅ Input validation for URLs
- ✅ File size limits enforced
- ✅ No arbitrary code execution

---

## 📈 Scaling Considerations

If your app grows:

1. **Database**: Migrate from in-memory to persistent storage
2. **Processing**: Add job queue (Redis + Celery)
3. **Caching**: Implement Redis for embeddings cache
4. **Load Balancing**: Use multiple instances
5. **CDN**: For static assets

---

## 📞 Support

If you encounter deployment issues:

1. Check the logs in your platform's dashboard
2. Review the troubleshooting section above
3. Open an issue on GitHub
4. Contact platform support

---

**Deployment Success Checklist:**

- ✅ App URL is accessible
- ✅ Service status shows all green
- ✅ Can upload and index codebase
- ✅ Q&A returns answers with sources
- ✅ No errors in logs
- ✅ Environment variables secure

**You're ready for production! 🎉**
