import traceback
import inspect
from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()

async def global_exception_handler(request: Request, exc: Exception):
    # Get traceback info
    tb = traceback.extract_tb(exc.__traceback__)[-1]  # Last call in the stack
    filename = tb.filename
    line_no = tb.lineno
    func_name = tb.name
    error_type = type(exc).__name__
    error_message = str(exc)

    # Create structured error log
    log_message = (
        f"\n--- Exception Caught ---\n"
        f"Timestamp     : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        f"Request URL   : {request.url}\n"
        f"File          : {filename}\n"
        f"Function      : {func_name}\n"
        f"Line No       : {line_no}\n"
        f"Error Type    : {error_type}\n"
        f"Error Message : {error_message}\n"
        f"------------------------\n"
    )

    logger.error(log_message)
    
    # Optional: log full traceback in debug mode
    logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error — please try again later.",
            "details": f"{error_type}: {error_message}"
        },
    )
