from righttoknow.configs.default import Config
import os


class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
