import os

from righttoknow.configs.default import Config


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
