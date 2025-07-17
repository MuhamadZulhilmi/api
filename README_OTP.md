# OTP Authentication API Testing Guide

## Database Setup (Required First)
Run this SQL command to add OTP columns to your database:

```sql
ALTER TABLE users 
ADD COLUMN otp_enabled BOOLEAN DEFAULT FALSE NOT NULL,
ADD COLUMN otp_verified BOOLEAN DEFAULT FALSE NOT NULL,
ADD COLUMN otp_base32 VARCHAR(32) DEFAULT NULL,
ADD COLUMN otp_auth_url VARCHAR(500) DEFAULT NULL;
```

## Postman Testing Instructions

### 1. Import Collection
- Import `postman_collection.json` into Postman
- Update the base URL if needed (currently set to `http://localhost:8000`)

### 2. Test Flow

#### Step 1: Register User
**POST** `/auth/register-otp`
```json
{
  "username": "testuser",
  "full_name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

#### Step 2: Login User
**POST** `/auth/login-otp`
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

#### Step 3: Generate OTP
**POST** `/auth/otp/generate`
```json
{
  "user_id": 1
}
```
Response will include:
- `base32`: OTP secret
- `otpauth_url`: QR code URL for authenticator apps

#### Step 4: Verify OTP
**POST** `/auth/otp/verify`
```json
{
  "user_id": 1,
  "token": "123456"
}
```
Use the actual OTP from your authenticator app

#### Step 5: Validate OTP
**POST** `/auth/otp/validate`
```json
{
  "user_id": 1,
  "token": "123456"
}
```

#### Step 6: Disable OTP
**POST** `/auth/otp/disable`
```json
{
  "user_id": 1
}
```

## cURL Commands

### Register User
```bash
curl -X POST http://localhost:8000/auth/register-otp \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","full_name":"Test User","email":"test@example.com","password":"password123"}'
```

### Generate OTP
```bash
curl -X POST http://localhost:8000/auth/otp/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id":1}'
```

### Verify OTP
```bash
curl -X POST http://localhost:8000/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"token":"123456"}'
```

## Testing Notes
- Replace `user_id` with actual user ID from registration response
- Use real OTP codes from Google Authenticator or similar app
- Test both success and error cases
- Verify CORS is working for your frontend IP
