from boogie.configurations import Conf


class LoggingConf(Conf):
    default_logging_handlers = ['file', 'file-info', 'console']

    LOGGING = property(lambda self: {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(name)-40s %(process)-5d %(thread)-2d [ %(levelname)-8s ] %(message)s'
            },
            'simple': {
                'format': '[%(asctime)s] %(name)-40s [ %(levelname)-8s ] %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if self.DEBUG else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file-info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'formatter': 'simple',
                'filename': self.LOGFILE_INFO_PATH,
            },
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': self.LOGFILE_WARNINGS_PATH,
            },

        },
        'loggers': {
            'django': {
                'level': 'DEBUG',
                'propagate': True,
            },
            'boogie': {
                'level': 'DEBUG',
                'propagate': True,
            },
            'codeschool': {
                'handlers': self.default_logging_handlers,
                'level': 'DEBUG',
                'propagate': True,
            },
            'boxed': {
                'handlers': self.default_logging_handlers,
                'level': 'DEBUG',
                'propagate': True,
            },
            'ejudge': {
                'handlers': self.default_logging_handlers,
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    })
