import logging


def configure_logging() -> None:
    """
    Configure application-wide logging.

    - Sets a basic format including level, logger name, and message.
    - Default level is INFO; can be adjusted per environment.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )