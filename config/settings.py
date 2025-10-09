from pydantic_settings import BaseSettings
from pydantic import Field
from utils.logger import get_logger

logger = get_logger(name="settings")

class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(..., alias="GROQ_API_KEY")
    LMS_API_BASE_URL: str = Field(..., alias="LMS_API_BASE_URL")

    class Config:
        env_file = ".env"
        populate_by_name = True

try:
    settings = Settings()
    logger.info("✅ Environment settings loaded successfully.")
    logger.debug(f"GROQ_API_KEY loaded: {bool(settings.GROQ_API_KEY)}")
    logger.debug(f"LMS_API_BASE_URL: {settings.LMS_API_BASE_URL}")
except Exception as e:
    import traceback
    tb = traceback.extract_tb(e.__traceback__)[-1]
    logger.error(
        f"\n--- Settings Load Exception ---\n"
        f"File      : {tb.filename}\n"
        f"Function  : {tb.name}\n"
        f"Line No   : {tb.lineno}\n"
        f"Error     : {type(e).__name__} - {str(e)}\n"
        f"--------------------------------"
    )
    logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
    raise
