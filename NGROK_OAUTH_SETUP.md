# Ngrok + Facebook OAuth Setup Guide

## Step 1: Install and Configure Ngrok

1. **Download ngrok**: https://ngrok.com/download
2. **Create ngrok account** and get your authtoken
3. **Configure ngrok**:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

## Step 2: Start Ngrok Tunnel

```bash
ngrok http 8000
```

Your tunnel URL will be something like: `https://pseudophilanthropic-vanda-hatlike.ngrok-free.dev`

**IMPORTANT:** Always use the HTTPS URL, not the HTTP URL.

## Step 3: Update Facebook App Settings

1. Go to your Facebook App Dashboard: https://developers.facebook.com/apps/YOUR_APP_ID/
2. Navigate to **Facebook Login > Settings**
3. Add these to **Valid OAuth Redirect URIs**:
   ```
   https://your-ngrok-domain.ngrok-free.dev/accounts/facebook/login/callback/
   ```
   (Replace 'your-ngrok-domain' with your actual ngrok subdomain)
   
4. Make sure "Enforce HTTPS" is set to Yes
   
5. In **Settings > Basic**, add to **App Domains**:
   ```
   your-ngrok-domain.ngrok-free.dev
   ```

## Step 4: Update Your Django Settings and Environment

1. **Update your `.env` file**:
   ```
   FACEBOOK_APP_ID=your_facebook_app_id
   FACEBOOK_APP_SECRET=your_facebook_app_secret
   FACEBOOK_REDIRECT_URI=https://your-ngrok-domain.ngrok-free.dev/accounts/facebook/login/callback/
   ```

2. **Django settings** are already configured to:
   - Include ngrok domain in `ALLOWED_HOSTS`
   - Trust the ngrok proxy with `SECURE_PROXY_SSL_HEADER`
   - Force HTTPS for OAuth with `SOCIALACCOUNT_DEFAULT_HTTP_PROTOCOL`
   - Add ngrok domain to `CSRF_TRUSTED_ORIGINS`

## Step 5: Set Up Social Apps in Django

Run the setup script to configure everything automatically:
```bash
python setup_oauth.py
```

Or manually configure via Django admin:
1. Create superuser: `python manage.py createsuperuser`
2. Start server: `python manage.py runserver`
3. Go to: `https://your-ngrok-domain.ngrok-free.dev/admin/`
4. Add Social Applications:
   - **Facebook**: Provider=facebook, Client ID=your_facebook_app_id, Secret=your_facebook_app_secret
   - **Google**: Provider=google, Client ID=YOUR_GOOGLE_ID, Secret=YOUR_GOOGLE_SECRET

## Step 6: Test OAuth Login

1. Visit: `https://your-ngrok-domain.ngrok-free.dev/accounts/login/`
2. Click "Continue with Facebook"
3. Complete Facebook OAuth flow

## Troubleshooting

### Common Issues:

1. **"Insecure page" error from Facebook**:
   - ✅ Fixed: Always use HTTPS URLs and correct Django settings
   - Make sure you're accessing the site via HTTPS ngrok URL, not HTTP
   - The settings `SECURE_PROXY_SSL_HEADER` and `SOCIALACCOUNT_DEFAULT_HTTP_PROTOCOL` ensure proper HTTPS handling

2. **Invalid HTTP_HOST header**:
   - ✅ Fixed: Added ngrok domain to ALLOWED_HOSTS

3. **CSRF verification failed**:
   - ✅ Fixed: Added ngrok domain to CSRF_TRUSTED_ORIGINS

4. **Facebook OAuth redirect mismatch**:
   - Ensure the exact ngrok URL is in Facebook app settings
   - Check that redirect URI matches exactly (including trailing slash)

5. **Site matching query does not exist**:
   - Run `python setup_oauth.py` to configure the site properly

### Facebook App Requirements:

- App must be in **Development** or **Live** mode
- **App Domains** must include your ngrok domain
- **Valid OAuth Redirect URIs** must include the exact callback URL
- For production, you'll need to submit for **App Review**

## Environment Variables Summary

Your `.env` file should have:
```
# Facebook OAuth Settings
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=https://your-ngrok-domain.ngrok-free.dev/accounts/facebook/login/callback/

# Google OAuth Settings (Replace with your actual credentials)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Django Secret Key (for production)
DJANGO_SECRET_KEY=your-secret-key-here
```

## Production Notes

When moving to production:
1. Replace ngrok URL with your actual domain
2. Update Facebook app settings with your production domain
3. Set proper ALLOWED_HOSTS for production
4. Use environment variables for all secrets
5. Configure proper HTTPS with a real SSL certificate