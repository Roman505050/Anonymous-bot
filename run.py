import asyncio
import logging
import sys

from main import start

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Bot stopped')