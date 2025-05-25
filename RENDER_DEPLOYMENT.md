# Render.com Deployment Guide

## Prerequisites
- GitHub account
- Render.com account (free tier available)

## Deployment Steps

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 2. Deploy on Render

1. **Go to [Render.com](https://render.com)** and sign up/login
2. **Click "New +"** and select **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name**: `flask-event-platform`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 3. Set Environment Variables

In the Render dashboard, add these environment variables:

**Required:**
- `SECRET_KEY`: Generate a secure random key
- `FLASK_ENV`: `production`

**Database (if using external DB):**
- `DB_HOST`: Your database host
- `DB_USER`: Your database username
- `DB_PASSWORD`: Your database password
- `DB_NAME`: Your database name
- `DB_PORT`: Your database port (default: 3306)

### 4. Deploy

Click **"Create Web Service"** and Render will:
- ✅ Install GCC/G++ compilers automatically
- ✅ Install Python dependencies
- ✅ Build and deploy your application
- ✅ Provide a live URL

## Features Supported on Render

✅ **GCC/G++ Compilers** - Full C/C++ compilation support
✅ **File System Access** - Can create/delete files in `/tmp`
✅ **Python Environment** - Full Python 3.9+ support
✅ **WebSocket Support** - Flask-SocketIO works perfectly
✅ **Environment Variables** - Secure configuration
✅ **Custom Domains** - Add your own domain
✅ **SSL Certificates** - Automatic HTTPS
✅ **Build Logs** - Full deployment visibility

## Important Notes

1. **Disk Storage**: Render uses ephemeral storage. Files created in `/tmp` are temporary.
2. **Port Configuration**: App automatically uses `PORT` environment variable.
3. **Database**: Consider using Render's PostgreSQL or external MySQL service.
4. **Static Files**: Served automatically by Flask.

## Troubleshooting

### If deployment fails:
1. Check build logs in Render dashboard
2. Verify all dependencies in `requirements.txt`
3. Ensure `app.py` runs without errors locally

### If GCC errors occur:
- Render includes GCC by default
- No additional system packages needed
- Check `/tmp` directory permissions

## Live URL

After deployment, your app will be available at:
`https://your-service-name.onrender.com`

## Cost

- **Free Tier**: 750 hours/month (suitable for development)
- **Paid Plans**: Starting at $7/month for production apps
