# Deployment Guide

This guide covers deploying the full-stack application to production using Render (backend) and Cloudflare Pages (frontend).

## Prerequisites

- GitHub repository with the code
- Render account (free tier available)
- Cloudflare account (free tier available)
- Domain name (optional, Cloudflare provides subdomains)

## Backend Deployment (Render)

### 1. Database Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "PostgreSQL"
3. Configure:
   - Name: `starter-webapp-db`
   - Database Name: `starter_webapp`
   - User: `starter_webapp_user`
   - Plan: Free (or Starter for production)
4. Click "Create Database"
5. Copy the "External Database URL" for later use

### 2. Backend Service Setup

1. In Render Dashboard, click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `starter-webapp-backend`
   - Root Directory: `backend`
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt && python deploy.py`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variables:
   - `DATABASE_URL`: Paste the PostgreSQL URL from step 1
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `false`
   - `FRONTEND_URL`: (will be set after frontend deployment)

### 3. Deploy and Test Backend

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Test endpoints:
   ```bash
   curl https://your-backend-url.onrender.com/health
   curl https://your-backend-url.onrender.com/api/hello
   ```

## Frontend Deployment (Cloudflare Pages)

### 1. Manual Deployment

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to "Pages" → "Create a project"
3. Connect to Git and select your repository
4. Configure build settings:
   - Framework preset: `Vite`
   - Build command: `cd frontend && npm ci && npm run build`
   - Build output directory: `frontend/dist`
5. Set Environment Variables:
   - `VITE_API_URL`: Your Render backend URL
   - `VITE_ENVIRONMENT`: `production`

### 2. Automated Deployment with GitHub Actions

1. Get Cloudflare API credentials:
   - Go to Cloudflare Dashboard → "My Profile" → "API Tokens"
   - Create token with "Cloudflare Pages:Edit" permissions
   - Get your Account ID from the right sidebar

2. Add GitHub Secrets:
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `CLOUDFLARE_API_TOKEN`: Your API token
     - `CLOUDFLARE_ACCOUNT_ID`: Your account ID
     - `VITE_API_URL`: Your Render backend URL (optional, has default)

3. Push to main branch to trigger deployment

### 3. Update Backend CORS

After frontend deployment:

1. Go back to Render Dashboard
2. Edit your backend service environment variables
3. Set `FRONTEND_URL` to your Cloudflare Pages URL
4. Redeploy the backend service

## Testing Full-Stack Deployment

1. Visit your Cloudflare Pages URL
2. Check that:
   - Environment badge shows "PRODUCTION"
   - API URL points to your Render backend
   - Backend status shows "healthy"
   - API message loads successfully

## Monitoring and Logs

### Backend (Render)
- Logs: Render Dashboard → Your Service → Logs
- Metrics: Available in Render Dashboard
- Health Check: `https://your-backend.onrender.com/health`

### Frontend (Cloudflare Pages)
- Deployment logs: Cloudflare Dashboard → Pages → Your Project
- Analytics: Available in Cloudflare Dashboard
- Real-time logs: Available in Wrangler CLI

## Troubleshooting

### Common Backend Issues

1. **Database Connection Errors**
   - Verify `DATABASE_URL` is correct
   - Check if database is accessible from Render
   - Review migration logs in deployment

2. **CORS Errors**
   - Ensure `FRONTEND_URL` is set correctly
   - Check that frontend URL matches exactly (no trailing slash)

3. **Environment Variable Issues**
   - Verify all required variables are set in Render
   - Check for typos in variable names

### Common Frontend Issues

1. **Build Failures**
   - Check Node.js version compatibility
   - Verify all dependencies are in package.json
   - Review build logs for specific errors

2. **API Connection Issues**
   - Verify `VITE_API_URL` points to correct backend
   - Check CORS configuration on backend
   - Test API endpoints directly

3. **Environment Variables Not Loading**
   - Ensure variables start with `VITE_`
   - Variables must be set at build time, not runtime
   - Check Cloudflare Pages environment variables

## Scaling and Production Considerations

### Backend
- Upgrade to Render Starter plan for better performance
- Use managed PostgreSQL for better reliability
- Implement proper logging and monitoring
- Add database connection pooling
- Set up backup strategy

### Frontend
- Configure custom domain in Cloudflare
- Enable Cloudflare's CDN features
- Set up analytics and monitoring
- Implement error tracking (Sentry)
- Configure caching headers

### Security
- Use secrets for sensitive environment variables
- Enable HTTPS (default on both platforms)
- Implement rate limiting
- Add authentication when needed
- Regular security updates

## Cost Optimization

### Free Tier Limits
- **Render**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Cloudflare Pages**: Unlimited requests, 500 builds/month

### Recommendations
- Use Render's "Auto-Deploy" sparingly to avoid unnecessary builds
- Optimize frontend build size to reduce deployment time
- Monitor usage to avoid unexpected charges