from app.app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    logging.info('info日誌')
    logging.debug('debug日誌')
    app.run()