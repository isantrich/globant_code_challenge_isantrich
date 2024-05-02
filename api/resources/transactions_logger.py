import logging

def configure_logger():
    logger = logging.getLogger('flask_app')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('api/flask_app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger