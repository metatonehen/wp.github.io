import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Check if DATABASE_URL is set
if not os.environ.get("DATABASE_URL"):
    # Set a default SQLite database URL for development
    os.environ["DATABASE_URL"] = "sqlite:///metatonehen.db"
    logging.info("Using SQLite database for development")

# Import the Flask app
from app import app  # noqa: F401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)