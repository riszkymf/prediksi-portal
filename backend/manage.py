#!/usr/bin/env python
from app import create_app
from app import config

app = create_app()


if __name__ == '__main__':
    app.run(host=config.APP_HOST,
            port=config.APP_PORT,
            debug=config.FLASK_DEBUG
            )
