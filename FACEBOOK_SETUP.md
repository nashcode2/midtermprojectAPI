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
   - `http://127.0.0.1:8000/accounts/facebook/login/callback/`
   - `http://localhost:8000/accounts/facebook/login/callback/`

### 3. Get App Credentials
1. Go to Settings → Basic
2. Copy your App ID and App Secret

### 4. Set Environment Variables
Create a `.env` file in your project root (`C:\Users\nashn\Desktop\api_project\.env`):
```
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here

# Optional: Set Google too if you have it
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Optional: override Django secret key
DJANGO_SECRET_KEY=dev-secret-key
```

### 5. Enable Facebook Provider
1. Uncomment Facebook provider in `api_nash_project/settings.py`:
   ```python
   'allauth.socialaccount.providers.facebook',
   ```

2. Uncomment Facebook config in `SOCIALACCOUNT_PROVIDERS`

3. Uncomment Facebook setup code in `main/signals.py`

4. Update `main/context.py` to enable Facebook:
   ```python
   has_facebook = SocialApp.objects.filter(provider='facebook').exists()
   ```

### 6. Restart Server
```bash
python manage.py runserver
```

## Current Status: Facebook Login is DISABLED
- The app works perfectly without Facebook login
- Only Google login and regular email/password login are enabled
- No more "Invalid App ID" errors

## To Test Current Login Options:
1. Regular signup/login with email and password
2. Google OAuth (if you have Google credentials set up)
