"""
Production-ready configuration management.
Handles environment variables, secrets, and defaults.
"""

import os
import logging
from typing import Optional

# ===== Environment Detection =====
APP_ENV = os.getenv("APP_ENV", "development").lower()
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# ===== AI Server Configuration =====
LOCAL_AI_URL = os.getenv("LOCAL_AI_URL", "http://127.0.0.1:8000")
LOCAL_AI_TIMEOUT = int(os.getenv("LOCAL_AI_TIMEOUT", "60"))
LOCAL_AI_HEALTH_CHECK_TIMEOUT = int(os.getenv("LOCAL_AI_HEALTH_CHECK_TIMEOUT", "2"))

# ===== Database Configuration =====
SHEET_NAME = os.getenv("SHEET_NAME", "printer_brain")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "history")

# ===== Logging Configuration =====
LOG_FILE = os.getenv("LOG_FILE", "app.log")
ENABLE_FILE_LOGGING = os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true"

# ===== API & Scraper Configuration =====
SCRAPER_TIMEOUT = int(os.getenv("SCRAPER_TIMEOUT", "45000"))
REQUEST_MAX_RETRIES = int(os.getenv("REQUEST_MAX_RETRIES", "3"))
REQUEST_RETRY_DELAY = int(os.getenv("REQUEST_RETRY_DELAY", "2"))

# ===== Cache Configuration =====
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

# ===== CORS Configuration =====
ENABLE_CORS = os.getenv("ENABLE_CORS", "true").lower() == "true"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# ===== Logger Setup =====
def setup_logging():
    """Initialize logging with both console and file handlers."""
    logger = logging.getLogger("brain3d")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (production)
    if ENABLE_FILE_LOGGING and APP_ENV == "production":
        try:
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setLevel(getattr(logging, LOG_LEVEL))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not setup file logging: {e}")
    
    return logger

# Initialize logger
logger = setup_logging()

# ===== Validation =====
def validate_config():
    """Validate critical configuration at startup."""
    warnings = []
    
    if APP_ENV not in ["development", "staging", "production"]:
        warnings.append(f"Unknown APP_ENV: {APP_ENV}. Should be development, staging, or production.")
    
    if APP_ENV == "production" and DEBUG:
        warnings.append("DEBUG is True in production mode. This is not recommended.")
    
    if not LOCAL_AI_URL.startswith("http"):
        warnings.append(f"Invalid LOCAL_AI_URL: {LOCAL_AI_URL}")
    
    for warning in warnings:
        logger.warning(f"Configuration warning: {warning}")
    
    logger.info(f"App initialized in {APP_ENV} mode (Debug: {DEBUG})")
    
    return len(warnings) == 0

# ===== Helper Functions =====
def get_logger(module_name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(f"brain3d.{module_name}")

def is_production() -> bool:
    """Check if running in production."""
    return APP_ENV == "production"

def is_debug() -> bool:
    """Check if debug mode is enabled."""
    return DEBUG

# Validate on import
if not is_production():
    validate_config()
