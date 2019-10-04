"""
    Config file for the web app.
"""

import os


POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
    'postgres+psycopg2://postgres:{}@pg/datatube_dev'.format(POSTGRES_PASSWORD)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'postgres+psycopg2://postgres:{}@pg/datatube'.format(POSTGRES_PASSWORD)


SETTINGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
