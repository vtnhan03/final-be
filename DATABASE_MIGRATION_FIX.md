# Database Migration Fix

## 🔧 **Issue: Missing verification_code Column**

The error you're seeing is because we added a new `verification_code` column to the database model, but your existing database table doesn't have this column yet.

## ✅ **Quick Fix Options**

### **Option 1: Automatic Migration (Recommended)**

The application now includes automatic migrations. Simply restart your server:

```bash
python main.py
```

The migration will run automatically on startup and add the missing column.

### **Option 2: Manual Migration**

If you prefer to run the migration manually:

```bash
python migrate_database.py
```

### **Option 3: Manual SQL (If needed)**

If the automatic migration fails, you can run this SQL directly in your database:

```sql
ALTER TABLE reset_tokens 
ADD COLUMN verification_code VARCHAR(10) NULL;
```

## 🔍 **What the Migration Does**

The migration safely adds the `verification_code` column to your existing `reset_tokens` table:

- **Checks** if the column already exists (won't duplicate)
- **Adds** the column as nullable (won't break existing data)
- **Logs** the progress so you can see what's happening

## 🚀 **After Migration**

Once the migration completes, you'll be able to use the new verification code endpoints:

- `POST /api/v1/auth/reset-password-with-code`
- `POST /api/v1/users/pin/reset-with-code`

## 📋 **Migration Log Example**

You should see something like this in your console:

```
INFO:app.db.migrations:Running database migrations...
INFO:app.db.migrations:Adding verification_code column to reset_tokens table...
INFO:app.db.migrations:✅ verification_code column added successfully!
INFO:app.db.migrations:All migrations completed successfully!
```

## 🔄 **Docker Users**

If you're using Docker, the migration will run automatically when you restart the container:

```bash
docker-compose down
docker-compose up --build
```

## ⚠️ **Troubleshooting**

If the migration fails:

1. **Check database connection** - Make sure your MySQL server is running
2. **Check permissions** - Ensure your database user can ALTER tables
3. **Check table exists** - Make sure the `reset_tokens` table exists
4. **Manual SQL** - Run the ALTER TABLE command directly in MySQL

The migration is designed to be safe and won't break your existing data!