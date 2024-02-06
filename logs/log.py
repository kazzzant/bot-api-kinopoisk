from loguru import logger


logger.add('logs/logs.log',
           format='{time} {level} {message}',
           level='DEBUG',
           rotation="100 kB",
           compression="zip")
