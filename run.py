from chezmahe import app
import logging

# app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# if server do logging through gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug('Running logger')
