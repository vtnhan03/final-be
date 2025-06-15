-- Initialize the database
USE nsfw_filter_db;

-- Grant privileges to the app user
GRANT ALL PRIVILEGES ON nsfw_filter_db.* TO 'appuser'@'%';
FLUSH PRIVILEGES;

-- Tables will be created automatically by SQLAlchemy when the app starts 