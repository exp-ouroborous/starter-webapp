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

## Frontend Deployment (Cloudflare Workers)

### 1. Manual Deployment

1. Navigate to frontend directory and install dependencies:
   ```bash
   cd frontend
   npm ci
   ```

2. Authenticate with Cloudflare:
   ```bash
   npx wrangler login
   ```

3. Build and deploy:
   ```bash
   npm run build
   npm run deploy
   ```

   Or use npx directly:
   ```bash
   npm run build
   npx wrangler deploy
   ```

### 2. Automated Deployment with GitHub Actions

1. Get Cloudflare API credentials:
   - Go to Cloudflare Dashboard → "My Profile" → "API Tokens"
   - Create token with "Cloudflare Workers:Edit" permissions
   - Get your Account ID from the right sidebar

2. Add GitHub Secrets:
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `CLOUDFLARE_API_TOKEN`: Your API token
     - `CLOUDFLARE_ACCOUNT_ID`: Your account ID
     - `VITE_API_URL`: Your Render backend URL (optional, has default)

3. Push to main branch to trigger deployment

### 3. Worker Configuration

The frontend is deployed as a Cloudflare Worker with:
- **Static Asset Serving**: Built React app served from Worker assets
- **SPA Routing**: All non-asset routes serve `index.html` for client-side routing
- **Security Headers**: Automatic security headers for all responses
- **Caching**: Optimized caching for static assets vs HTML

### 4. Update Backend CORS

After frontend deployment:

1. **Get your Cloudflare Workers URL** (e.g., `https://starter-webapp-frontend.your-subdomain.workers.dev`)

2. **Update Render Backend Environment Variables**:
   - Go to Render Dashboard → Your backend service → Environment
   - Set `FRONTEND_URL` to your Workers URL **without trailing slash**
   - Optionally set `CLOUDFLARE_WORKERS_URL` to the same URL
   - Example: `FRONTEND_URL=https://starter-webapp-frontend.your-subdomain.workers.dev`
   - ⚠️ **Important**: Do NOT include trailing slash (/) at the end

3. **Redeploy the backend service** (or it will auto-redeploy on environment change)

4. **Verify CORS is working**:
   - Check backend logs for: `🔗 CORS Allowed Origins: [...]`
   - Should include your Workers URL in the list

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

1. **PostgreSQL Driver Issues**
   ```
   ModuleNotFoundError: No module named 'psycopg2'
   ImportError: undefined symbol: _PyInterpreterState_Get
   ```
   - **Solution**: Using `psycopg[binary]==3.2.9` for Python 3.13 compatibility
   - Database URL automatically converted from `postgresql://` to `postgresql+psycopg://`
   - Check that pip is upgraded before installing dependencies
   - Verify build command includes: `pip install --upgrade pip`

2. **Database Connection Errors**
   - Verify `DATABASE_URL` is correct and includes all parameters
   - Check if database is accessible from Render
   - Review migration logs in deployment
   - Ensure PostgreSQL database is created and running

3. **Alembic Migration Failures**
   - Check that all models are imported in `alembic/env.py`
   - Verify database URL is accessible during migration
   - Review migration file for syntax errors
   - Check that base models are properly defined

4. **CORS Errors**
   - Ensure `FRONTEND_URL` is set correctly
   - Check that frontend URL matches exactly (no trailing slash)
   - Verify CORS middleware is properly configured

5. **Environment Variable Issues**
   - Verify all required variables are set in Render
   - Check for typos in variable names
   - Ensure variables are available during build process

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