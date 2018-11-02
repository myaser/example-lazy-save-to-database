from flask_env import MetaFlaskEnv


class BaseConfig(metaclass=MetaFlaskEnv):
    ENV_PREFIX = ''
    ENV_LOAD_ALL = False
    #: If set the REDIS_URL takes precedence over REDIS_HOST, REDIS_PORT, etc
    REDIS_URL = None
    RQ_REDIS_URL = None

    RQ_POLL_INTERVAL = 10000  #: Web interface poll period for updates in ms
    DEBUG = False
    WEB_BACKGROUND = "black"
    DELETE_JOBS = False

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'csv', }


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    RQ_ASYNC = False


class StagingConfig(BaseConfig):
    """Staging configuration"""
    DEBUG = False


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
