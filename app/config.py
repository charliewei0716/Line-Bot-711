class Config:
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = "production"