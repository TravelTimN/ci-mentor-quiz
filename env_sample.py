import os

os.environ.setdefault("DATABASE_URL", "your_postgres_database_url")
os.environ.setdefault("SECRET_KEY", "your_super_secret_key")
os.environ.setdefault("SITE_NAME", "your_deployed_url_site_name")
os.environ.setdefault("DEBUG", "True")
