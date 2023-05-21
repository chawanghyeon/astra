# settings.py

# List of middleware classes to use.
MIDDLEWARE = [
    "middlewares.cors.CORSMiddleware",
    "middlewares.security.SecurityMiddleware",
    "middlewares.async_exit_stack.AsyncExitStackMiddleware",
    "middlewares.https_redirect.HttpsRedirectMiddleware",
    "middlewares.trusted_host.TrustedHostMiddleware",
    "middlewares.gzip.SessionMiddleware",
]

# List of trusted hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database settings
DATABASES = {
    "POSTGRES": {
        "host": "your_postgres_host",
        "database": "your_postgres_database",
        "user": "your_postgres_user",
        "password": "your_postgres_password",
    },
    "MONGODB": {
        "host": "your_mongodb_host",
        "port": "your_mongodb_port",
    },
    "SQLITE": {
        "database": "path_to_your_sqlite_database.db",
    },
}

DEFAULT_DATABASE = "SQLITE"
