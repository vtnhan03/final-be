# NSFW Filter Backend API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication Endpoints

#### POST /register
Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "email": "user@example.com"
}
```

**Password Requirements:**
- At least 8 characters long
- At least one uppercase letter
- At least one lowercase letter
- At least one number

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "has_pin": false
}
```

#### POST /login
Login with username and password.

**Request Body (form-data):**
```
username: string
password: string
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### POST /auth/google
Login with Google OAuth.

**Request Body:**
```json
{
  "token": "google_access_token",
  "userInfo": {
    "sub": "google_user_id",
    "email": "user@gmail.com",
    "name": "User Name"
  }
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### GET /me
Get current user information (requires authentication).

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "has_pin": false
}
```

### Password Management Endpoints

#### POST /forgot-password
Request a password reset link.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If the email exists, a password reset link has been sent"
}
```

#### POST /reset-password
Reset password using reset token.

**Request Body:**
```json
{
  "token": "reset_token_string",
  "new_password": "new_secure_password"
}
```

**Response:**
```json
{
  "message": "Password has been reset successfully"
}
```

#### POST /change-password
Change password (requires authentication).

**Request Body:**
```json
{
  "current_password": "current_password",
  "new_password": "new_secure_password"
}
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

### PIN Management Endpoints

#### POST /set-pin
Set a new PIN (requires authentication).

**Request Body:**
```json
{
  "pin": "1234"
}
```

**PIN Requirements:**
- 4-6 digits only

**Response:**
```json
{
  "message": "PIN set successfully"
}
```

#### POST /verify-pin
Verify a PIN (requires authentication).

**Request Body:**
```json
{
  "pin": "1234"
}
```

**Response:**
```json
{
  "valid": true,
  "message": "PIN verified successfully"
}
```

#### POST /change-pin
Change existing PIN (requires authentication).

**Request Body:**
```json
{
  "current_pin": "1234",
  "new_pin": "5678"
}
```

**Response:**
```json
{
  "message": "PIN changed successfully"
}
```

#### POST /remove-pin
Remove existing PIN (requires authentication).

**Request Body:**
```json
{
  "current_pin": "1234"
}
```

**Response:**
```json
{
  "message": "PIN removed successfully"
}
```

#### POST /forgot-pin
Request a PIN reset link.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If the email exists and has a PIN set, a PIN reset link has been sent"
}
```

#### POST /reset-pin
Reset PIN using reset token.

**Request Body:**
```json
{
  "token": "reset_token_string",
  "new_pin": "5678"
}
```

**Response:**
```json
{
  "message": "PIN has been reset successfully"
}
```

### Account Management Endpoints

#### GET /account/info
Get detailed account information (requires authentication).

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "has_pin": false
}
```

#### DELETE /account
Delete user account (requires authentication).

**Response:**
```json
{
  "message": "Account deleted successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

## Environment Variables

```bash
# Database Configuration
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=nsfw_filter_db

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
```

## Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **PIN Hashing**: PINs are also hashed using bcrypt
3. **JWT Tokens**: Secure authentication with expiration
4. **Reset Token Security**: One-time use tokens with 1-hour expiration
5. **Email Validation**: Email format validation
6. **Password Strength**: Enforced password complexity requirements
7. **Rate Limiting**: Consider implementing rate limiting for production
8. **CORS**: Configured for frontend domains

## Email Integration

The application now uses **Resend** for reliable email delivery with professional HTML templates:

### Email Types Sent:
1. **Welcome Email** - Sent automatically upon user registration
2. **Password Reset Email** - Sent when user requests password reset
3. **PIN Reset Email** - Sent when user requests PIN reset

### Email Features:
- **Professional HTML Templates**: Responsive design that works on all devices
- **Plain Text Fallbacks**: Ensures compatibility with all email clients
- **Security Warnings**: Clear instructions about link expiration and security
- **Branded Design**: Consistent with your application's branding
- **Mobile Responsive**: Optimized for mobile devices

### Resend Configuration:
```bash
RESEND_API_KEY=your_resend_api_key      # Required for email sending
FROM_EMAIL=noreply@yourdomain.com       # Must be verified domain
FRONTEND_URL=http://localhost:3000      # For reset links
```

### Setup Instructions:
1. Sign up at [resend.com](https://resend.com)
2. Get your API key from the dashboard
3. Add and verify your domain
4. Set environment variables
5. Update `FROM_EMAIL` to use your verified domain

### Fallback Behavior:
- If `RESEND_API_KEY` is not configured, the system falls back to console logging
- This allows development without email service setup
- Production should always have Resend configured

### Email Templates Include:
- Security warnings about link expiration
- Clear call-to-action buttons
- Professional styling
- Company branding
- Contact information

For production deployment:
- Use your own verified domain
- Monitor email delivery through Resend dashboard
- Set up webhooks for delivery tracking (optional)

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- hashed_password (Nullable for Google users)
- hashed_pin (Nullable)
- email (Unique)
- google_id (Nullable, for Google OAuth users)
- is_google_user (Boolean)

### Reset Tokens Table
- id (Primary Key)
- user_id (Foreign Key)
- token (Unique)
- token_type ('password' or 'pin')
- expires_at (ISO datetime string)
- used (Boolean) 