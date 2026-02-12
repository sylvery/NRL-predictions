# Deployment Guide - Railway

This guide covers deploying the NRL Predictions FastAPI application to Railway.

## Prerequisites

- GitHub account
- Railway account (free at https://railway.app)
- Your code pushed to GitHub

---

## 🚀 Quick Deployment (5 minutes)

### Step 1: Connect GitHub to Railway

1. Go to https://railway.app
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"

### Step 2: Select Repository

1. Choose your GitHub repository (e.g., `yourusername/NRL-predictions`)
2. Railway will detect it's a Python/FastAPI app

### Step 3: Configure Environment (Optional)

Railway will automatically use settings from:
- `Procfile` - Start command
- `requirements-web.txt` - Dependencies
- `railway.json` - Deployment config

**Optional Environment Variables:**
If you want to customize the current round/year:

1. In Railway dashboard, go to your project
2. Click "Variables" tab
3. Add:
   ```
   NRL_CURRENT_ROUND=6
   NRL_CURRENT_YEAR=2026
   ```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for build (~2-3 minutes)
3. Your app will be live at `https://yourapp.railway.app`

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NRL_CURRENT_ROUND` | 5 | Current NRL round number |
| `NRL_CURRENT_YEAR` | 2026 | Current season year |

### Adding Custom Domain

1. In Railway dashboard → Your Project → Settings
2. Click "Domains"
3. Add your domain (e.g., `predictions.nrl.com`)
4. Update DNS records as shown

---

## 📁 Project Structure

```
NRL-predictions/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── routes/          # API routes
│   ├── templates/       # HTML templates
│   └── static/         # CSS/JS files
├── Procfile            # Railway start command
├── railway.json        # Railway configuration
├── requirements-web.txt # Python dependencies
└── ENVIRONMENT_VARIABLES.py # App configuration
```

---

## 🐛 Troubleshooting

### Build Fails

**Error:** `ModuleNotFoundError`

**Solution:** Check `requirements-web.txt` contains all dependencies:
```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
jinja2>=3.1.0
requests>=2.31.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
numpy>=1.24.0
```

### App Won't Start

**Error:** `Port not found`

**Solution:** Ensure `Procfile` uses `$PORT`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Health Check Fails

**Solution:** Verify health endpoint works:
```bash
curl https://yourapp.railway.app/api/health
# Should return: {"status":"healthy"}
```

---

## 📊 Monitoring

### View Logs

1. Railway Dashboard → Your Project → Deployments
2. Click on a deployment
3. View "Logs" tab

### View Metrics

1. Dashboard → Your Project → Metrics
2. See CPU, memory, request counts

---

## 🔄 Auto-Deploy

Railway automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update predictions"
git push origin main
```

Railway will detect the push and start a new deployment.

---

## 💰 Free Tier Limits

Railway's free tier includes:
- 500 hours/month compute
- 1GB disk storage
- Unlimited deployments

For most users, this is completely free!

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- GitHub Issues: Report problems in this repo

---

**🎉 Your NRL Predictions app is now live!**
