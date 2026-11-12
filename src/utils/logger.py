import sys
import json
import traceback
from pathlib import Path
from loguru import logger

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
CRASH_REPORT_FILE = LOGS_DIR / "crash_report.json"

# Configure loguru
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
logger.add(LOGS_DIR / "app.log", rotation="10 MB", retention="7 days", level="INFO")

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler to capture unhandled exceptions and dump them for AI to read"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error(f"Uncaught exception: {exc_value}")
    
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_text = "".join(tb_lines)
    
    # Save a structured crash report for the OpenClaw AI to pick up
    crash_data = {
        "error_type": exc_type.__name__,
        "error_message": str(exc_value),
        "traceback": tb_text,
        "status": "unresolved"
    }
    
    with open(CRASH_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(crash_data, f, indent=4, ensure_ascii=False)
        
    logger.critical(f"Crash report generated at {CRASH_REPORT_FILE}")

# Hook the exception handler
sys.excepthook = handle_exception
