"""
    run command
    python run.py
"""
from datetime import datetime

from loguru import logger

from app.main import handler

if __name__ == "__main__":
    logger.add(f'logs/{datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")}.log', rotation='00:00', retention='180 days')
    handler()
