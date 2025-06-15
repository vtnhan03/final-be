# Flexible Login System

## ✅ **Enhanced Login: Username OR Email**

I've updated the login system to accept both username and email addresses, making it much more user-friendly!

## 🔧 **How It Works**

### **Before (Username Only):**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

### **After (Username OR Email):**
```json
{
  "username_or_email": "john_doe",
  "password": "password123"
}
```

**OR**

```json
{
  "username_or_email": "john@example.com", 
  "password": "password123"
}
```

## 🚀 **Updated API Endpoint**

### **Login Endpoint**
```
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "username_or_email": "john_doe",  // Can be username OR email
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 📋 **Login Examples**

### **1. Login with Username**
```javascript
const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username_or_email: 'john_doe',
    password: 'MySecurePassword123'
  })
});
```

### **2. Login with Email**
```javascript
const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username_or_email: 'john@example.com',
    password: 'MySecurePassword123'
  })
});
```

### **3. Using curl**
```bash
# Login with username
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "john_doe",
    "password": "MySecurePassword123"
  }'

# Login with email
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "john@example.com", 
    "password": "MySecurePassword123"
  }'
```

## 🔍 **How the System Works**

### **Smart User Lookup:**
1. **First attempt**: Search by username
2. **If not found**: Search by email address
3. **If found**: Verify password and return JWT token
4. **If not found**: Return authentication error

### **Backend Logic:**
```python
def get_user_by_username_or_email(db: Session, username_or_email: str) -> User:
    # Try username first
    user = db.query(User).filter(User.username == username_or_email).first()
    
    # If not found, try email
    if not user:
        user = db.query(User).filter(User.email == username_or_email).first()
    
    return user
```

## 🔒 **Security Features**

- **Same security level** as before
- **Password verification** remains unchanged
- **JWT token generation** works the same way
- **Rate limiting** applies to both username and email attempts
- **No information leakage** - same error message for both cases

## 📱 **Frontend Integration**

### **React Example:**
```jsx
const LoginForm = () => {
  const [credentials, setCredentials] = useState({
    username_or_email: '',
    password: ''
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      
      if (response.ok) {
        const { access_token } = await response.json();
        localStorage.setItem('token', access_token);
        // Redirect to dashboard
      } else {
        setError('Invalid username/email or password');
      }
    } catch (error) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="text"
        placeholder="Username or Email"
        value={credentials.username_or_email}
        onChange={(e) => setCredentials({
          ...credentials,
          username_or_email: e.target.value
        })}
      />
      <input
        type="password"
        placeholder="Password"
        value={credentials.password}
        onChange={(e) => setCredentials({
          ...credentials,
          password: e.target.value
        })}
      />
      <button type="submit">Login</button>
    </form>
  );
};
```

## 🧪 **Testing the New System**

### **Test Cases:**

1. **Username login**: `john_doe` + password
2. **Email login**: `john@example.com` + password  
3. **Invalid credentials**: Should return 401 error
4. **Empty fields**: Should return validation error

### **API Documentation:**
Visit http://localhost:8000/docs to see the updated login endpoint with the new `username_or_email` field.

## 🔄 **Backwards Compatibility**

The API field name changed from `username` to `username_or_email`, so you'll need to update your frontend forms. However, the functionality is much more user-friendly now!

## ✨ **User Experience Benefits**

- **More flexible**: Users can login with what they remember
- **Less confusion**: No need to remember if they used username or email
- **Better UX**: Single input field for both username and email
- **Familiar pattern**: Most modern apps work this way

The flexible login system makes your app much more user-friendly while maintaining the same level of security! 🎯 