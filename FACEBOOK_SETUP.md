# Facebook Login Setup Instructions

## To Enable Facebook Login:

### 1. Create a Facebook App
1. Go to https://developers.facebook.com/
2. Click "My Apps" → "Create App"
3. Choose "Consumer" app type
4. Fill in app details:
   - App Name: "Your API Project"
   - App Contact Email: your email
   - App Purpose: "Other"

### 2. Configure Facebook Login
1. In your app dashboard, click "Add Product" → "Facebook Login"
2. Go to Facebook Login → Settings
3. Add Valid OAuth Redirect URIs:
   - `https://your-ngrok-domain.ngrok-free.dev/accounts/facebook/login/callback/` (for ngrok)
   - `https://your-production-domain.com/accounts/facebook/login/callback/` (for production)
   - `http://localhost:8000/accounts/facebook/login/callback/` (for local testing)
   - `http://127.0.0.1:8000/accounts/facebook/login/callback/` (for local testing)

4. Make sure "Enforce HTTPS" is set to Yes

5. In App Domains (Settings → Basic), add:
   - `your-ngrok-domain.ngrok-free.dev`
   - `localhost`
   - `127.0.0.1`
   - `your-production-domain.com` (when ready for production)

### 3. Get App Credentials
1. Go to Settings → Basic
2. Copy your App ID and App Secret

### 4. Set Environment Variables
Create a `.env` file in your project root:
```
# Facebook OAuth Settings
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here
FACEBOOK_REDIRECT_URI=https://your-ngrok-domain.ngrok-free.dev/accounts/facebook/login/callback/

# Optional: Set Google too if you have it
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Optional: override Django secret key
DJANGO_SECRET_KEY=your-secret-key-here
```

### 5. Run the OAuth Setup Script
```bash
python setup_oauth.py
```

This script will:
- Configure the Site domain correctly
- Create/update SocialApp entries for Facebook and Google
- Associate the apps with your site

### 6. Important Settings for HTTPS
The following settings are already configured in `api_nash_project/settings.py`:
```python
# Force HTTPS for OAuth security with ngrok
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
SOCIALACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
SOCIALACCOUNT_CALLBACK_URL_PROTOCOL = 'https'
```

These ensure Facebook OAuth works correctly with ngrok by generating HTTPS URLs.

### 7. Start Server and Test
```bash
python manage.py runserver
```

## Using Facebook Login
1. Start ngrok in a separate terminal:
   ```bash
   ngrok http 8000
   ```
   
2. **Important:** Always use the HTTPS ngrok URL:
   ```
   https://your-ngrok-domain.ngrok-free.dev/accounts/login/
   ```
   
3. Click "Continue with Facebook" to test the login flow

## Troubleshooting
If you see "insecure page" errors:
1. Make sure you're accessing via HTTPS, not HTTP
2. Ensure your ngrok domain is added to App Domains in Facebook
3. Verify the exact redirect URI is in Facebook's Valid OAuth Redirect URIs

## To Test Current Login Options:
1. Regular signup/login with email and password
2. Google OAuth (if you have Google credentials set up)
