# Verification Code System

## ✅ **New Feature: 6-Digit Verification Codes**

I've implemented a user-friendly verification code system for password and PIN resets. Users now receive a **6-digit code** via email instead of long URLs.

## 🔧 **How It Works**

### **1. User Requests Reset**
- User enters their email in the forgot password/PIN form
- System generates both a long token (for URL fallback) and a 6-digit verification code
- Email is sent with the **6-digit code** prominently displayed

### **2. User Enters Code**
- User receives email with code like: **123456**
- User enters the code in your reset form along with their new password
- System validates the code and resets the password/PIN

## 📧 **Email Format**

The reset emails now show a large, easy-to-read verification code:

```
🔒 Password Reset Request

Please use the following verification code:

┌─────────────────┐
│    123456       │
└─────────────────┘

Enter this code in the app to complete your password reset.

⚠️ Important:
• This code will expire in 1 hour
• Never share this code with anyone
```

## 🚀 **New API Endpoints**

### **Password Reset with Code**
```
POST /api/v1/auth/reset-password-with-code
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "verification_code": "123456",
  "new_password": "NewSecurePassword123"
}
```

### **PIN Reset with Code**
```
POST /api/v1/users/pin/reset-with-code
```

**Request Body:**
```json
{
  "email": "user@example.com", 
  "verification_code": "123456",
  "new_pin": "1234"
}
```

## 📋 **Complete Flow Example**

### **Frontend Implementation:**

1. **Forgot Password Request:**
```javascript
// Step 1: Request reset code
const response = await fetch('/api/v1/auth/forgot-password', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com' })
});
```

2. **Reset with Code:**
```javascript
// Step 2: Reset with verification code
const response = await fetch('/api/v1/auth/reset-password-with-code', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    verification_code: '123456',
    new_password: 'NewPassword123'
  })
});
```

## 🔒 **Security Features**

- **6-digit codes** are randomly generated (100,000 - 999,999)
- **1-hour expiration** for all codes
- **One-time use** - codes are marked as used after successful reset
- **Email validation** - code must match the email address
- **Rate limiting** - same security as before

## 📱 **Perfect for Your Form**

Your reset form with the three fields works perfectly:

1. **Reset Token** → **Verification Code** (6 digits)
2. **New Password** → **New Password** (with validation)
3. **Confirm New Password** → **Confirm New Password** (frontend validation)

## 🔄 **Backwards Compatibility**

Both systems work simultaneously:

- **New way**: Use verification codes with `/reset-password-with-code`
- **Old way**: URL tokens still work with `/reset-password`

## 🧪 **Testing the New System**

1. **Start the server:**
```bash
python main.py
```

2. **Request a reset:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

3. **Check console for the verification code** (if RESEND_API_KEY not set)

4. **Reset with code:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/reset-password-with-code" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "verification_code": "123456",
    "new_password": "NewPassword123"
  }'
```

## 📚 **Updated API Documentation**

Visit http://localhost:8000/docs to see the new endpoints in the interactive documentation.

The verification code system provides a much better user experience while maintaining the same level of security! 