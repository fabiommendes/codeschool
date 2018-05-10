from boogie.configurations import DjangoConf, env

from .apps import AppsConf
from .base import BaseConf
from .logging import LoggingConf
from .paths import PathConf
from .secrets import SecretsConf


class CodeschoolConf(AppsConf,
                     BaseConf,
                     LoggingConf,
                     SecretsConf,
                     PathConf,
                     DjangoConf):
    """
    Codeschool configuration class.
    """

    #: If true, forces usernames being equal to the school id for each student.
    CODESCHOOL_USERNAME_IS_SCHOOL_ID = env(False)

    #: A regular expression for validating school id values. Set it to None to
    #: disable validation.
    CODESCHOOL_SCHOOL_ID_VALIDATION = env(r'.+')

    #: A regular expression describing valid user names.
    CODESCHOOL_USERNAME_VALIDATION = env(r'.+')

    #: Enable/disable sandboxing. You should always enable sandboxing in production.
    CODESCHOOL_SANDBOX = env(True)

    #: Enable debug views at _admin/ and _debug/
    CODESCHOOL_DEBUG_VIEWS = env(True)

    #: Enable a global "Questions" page
    CODESCHOOL_GLOBAL_QUESTIONS = env(True)


CodeschoolConf.save_settings()
