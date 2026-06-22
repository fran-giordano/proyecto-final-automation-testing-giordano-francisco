import logging
import pathlib

_LOG_DIR = pathlib.Path(__file__).parent.parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """Devuelve un logger configurado con salida a consola y archivo."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    fh = logging.FileHandler(_LOG_DIR / "tests.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
