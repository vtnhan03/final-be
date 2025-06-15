# Environment Variables Configuration

## Required Environment Variables

Copy these variables to your `.env` file or set them in your environment:

```bash
# Database Configuration
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=nsfw_filter_db

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id

# Resend Email Configuration
RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=noreply@yourdomain.com
FRONTEND_URL=http://localhost:3000

# JWT Configuration (optional - defaults to a secure value)
SECRET_KEY=your_super_secure_secret_key

# FastAPI Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Setup Instructions

### 1. Resend Email Service Setup

1. **Sign up for Resend**: Go to [resend.com](https://resend.com) and create an account
2. **Get API Key**: 
   - Go to your Resend dashboard
   - Navigate to "API Keys" section
   - Create a new API key
   - Copy the API key and set it as `RESEND_API_KEY`
3. **Add Domain**: 
   - Go to "Domains" section in Resend dashboard
   - Add your domain (e.g., `yourdomain.com`)
   - Verify domain ownership via DNS records
   - Set `FROM_EMAIL` to something like `noreply@yourdomain.com`

### 2. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Set authorized origins and redirect URIs
6. Copy the Client ID and set as `GOOGLE_CLIENT_ID`

### 3. Database Setup

1. Install MySQL/MariaDB
2. Create database: `CREATE DATABASE nsfw_filter_db;`
3. Set your database credentials in environment variables

### 4. Frontend URL

Set `FRONTEND_URL` to your frontend application URL:
- Development: `http://localhost:3000`
- Production: `https://yourdomain.com`

## Email Templates

The application includes responsive HTML email templates for:
- Password reset emails
- PIN reset emails

Templates include:
- Professional styling
- Mobile-responsive design
- Security warnings
- Clear call-to-action buttons
- Plain text fallbacks

## Security Notes

- Never commit real API keys to version control
- Use strong, unique values for `SECRET_KEY`
- Ensure `FROM_EMAIL` uses a verified domain in Resend
- Set appropriate CORS origins for production 