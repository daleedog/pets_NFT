import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NFT_WALLET_ADDRESS = os.environ.get('WALLET_ADDRESS') or 'default addr'
    NFT_CONTRACT_ADDRESS = os.environ.get('CONTRACT_ADDRESS') or 'default'
    WEB3_PROVIDER = os.environ.get('WEB3_PROVIDER') or ''
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY') or ''
    IPFS_FILE_URL = 'https://ipfs.io'
    IPFS_CONNECT_URL = 'https://ipfs'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}