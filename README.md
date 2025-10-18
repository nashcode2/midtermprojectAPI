# API Project with OAuth

This project is an API built with Django that supports both regular authentication and OAuth login with Facebook and Google.

## Installation

1. Clone the repository  
```bash
git clone https://github.com/nashcode2/midtermprojectAPI.git
```

2. Go to the project folder  
```bash
cd midtermprojectAPI
```

3. Create a virtual environment  
```bash
python -m venv venv
```

4. Activate the environment  
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

5. Install dependencies  
```bash
pip install -r requirements.txt
```

6. Configure environment variables:
   Create a `.env` file in the project root with:
   ```
   # Facebook OAuth Settings
   FACEBOOK_APP_ID=your_facebook_app_id
   FACEBOOK_APP_SECRET=your_facebook_app_secret
   
   # Google OAuth Settings (optional)
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   
   # Django Settings
   DJANGO_SECRET_KEY=your_secret_key_here
   ```

7. Run migrations:
```bash
python manage.py migrate
```

8. Configure OAuth providers:
```bash
python setup_oauth.py
```

## Run the Project Locally

1. Start the development server:  
```bash
python manage.py runserver
```

2. Open in your browser:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Using with Ngrok (for OAuth Testing)

1. Start your Django server:
```bash
python manage.py runserver
```

2. In a new terminal, start ngrok:
```bash
ngrok http 8000
```

3. **Important:** Always access the app via the **HTTPS** ngrok URL:
```
https://your-ngrok-subdomain.ngrok-free.dev
```

4. Make sure your OAuth provider settings include your ngrok URLs:
   - See `FACEBOOK_SETUP.md` and `NGROK_OAUTH_SETUP.md` for details

## Facebook OAuth Configuration

To use Facebook login:

1. Create a Facebook App at [developers.facebook.com](https://developers.facebook.com)
2. Add Facebook Login product to your app
3. Configure Valid OAuth Redirect URIs in Facebook Login settings:
   ```
   https://your-domain.com/accounts/facebook/login/callback/
   ```
4. Set App Domains to include your domain
5. Add your App ID and Secret to your `.env` file

For detailed instructions, see `FACEBOOK_SETUP.md`.

## Author
- nashcode2

Save the file.

Then push it to GitHub:

git add README.md
git commit -m "Add README"
git push -u origin main
