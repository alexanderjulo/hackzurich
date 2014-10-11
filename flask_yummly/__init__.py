from yummly.client import Client, TIMEOUT, RETRIES


class Yummly(Client):

    def __init__(self, app=None):
        if app:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        self.api_id = app.config['YUMMLY_API_ID']
        self.api_key = app.config['YUMMLY_API_KEY']
        self.timeout = app.config.get('YUMMLY_TIMEOUT', TIMEOUT)
        self.retries = app.config.get('YUMMLY_RETRIES', RETRIES)
