import logging
import sys

def setup_logger(name: str = "emotion_tone_service") -> logging.Logger:
    """
    Configure and return a logger instance.
    """
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.INFO)

    # prevent duplicate logs
    if logger.handlers:
        return logger
    
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger