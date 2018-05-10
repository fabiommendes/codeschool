"""
Manage all important codeschool paths.
"""

import logging
import os
from pathlib import Path

from boogie.configurations import Conf, env

join = os.path.join
dirname = os.path.dirname
log = logging.getLogger('codeschool')

LOCAL_SETTINGS_TEMPLATE = """
# Local settings file that can be personalized by each developer.

from codeschool.config.settings import CodeschoolConf


class LocalConf(CodeschoolConf):
    pass
    
LocalConf.save_settings()
"""


def assure_path(path):
    """
    Create all parent paths until given path exists.
    """

    if not path:
        raise ValueError('empty paths are invalid')

    if not os.path.exists(path):
        base, name = os.path.split(path)
        assure_path(base)
        log.info('INFO: Creating %s/%s/' % (base, name))
        os.mkdir(path)


def safe_join(*args):
    """
    Join path parts and create directory if it does not exist.
    """

    path = join(*args)
    assure_path(path)
    return path


class PathConf(Conf):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force existence of a local directories
        for directory in [self.LOG_DIR, self.DB_DIR, self.VOLUMES_DIR,
                          self.SOCK_DIR, self.BACKUP_DIR]:
            if not os.path.exists(directory):
                os.mkdir(directory)

        # Create local configuration if it does not exist
        if not os.path.exists(self.LOCAL_SETTINGS_PATH):
            with open(self.LOCAL_SETTINGS_PATH, 'w') as F:
                F.write(LOCAL_SETTINGS_TEMPLATE)

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    # This is <repo>/src/codeschool/
    DJANGO_SETTINGS_DIR = Path(__file__).parent
    CONFIG_DIR = DJANGO_SETTINGS_DIR.parent
    BASE_DIR = CONFIG_DIR.parent
    SRC_DIR = BASE_DIR.parent
    REPO_DIR = SRC_DIR.parent

    # Local dirs
    LOCAL_DIR = env(REPO_DIR / 'local', name='DJANGO_CONFIGURATIONS_DIR')
    DB_DIR = property(lambda self: self.LOCAL_DIR / 'db')
    VOLUMES_DIR = property(lambda self: self.LOCAL_DIR / 'volumes')
    SOCK_DIR = property(lambda self: self.LOCAL_DIR / 'sock')
    BACKUP_DIR = property(lambda self: self.LOCAL_DIR / 'backup')
    LOCAL_SETTINGS_PATH = property(lambda self: self.LOCAL_DIR / 'settings.py')

    # Logs
    LOG_DIR = property(lambda self: self.LOCAL_DIR / 'log')
    LOGFILE_INFO_PATH = property(lambda self: self.LOG_DIR / 'info.log')
    LOGFILE_WARNINGS_PATH = property(lambda self: self.LOG_DIR / 'warnings.log')

    # Frontend dirs
    FRONTEND_DIR = REPO_DIR / 'frontend'
    JS_BUILD_DIR = FRONTEND_DIR / 'js'
    ROOT_FILES_DIR = FRONTEND_DIR / 'root-files'
    FRONTEND_SRC_DIR = FRONTEND_DIR / 'src'
    FRONTEND_SCSS_DIR = FRONTEND_SRC_DIR / 'scss'
    FRONTEND_JS_DIR = FRONTEND_SRC_DIR / 'js'
    FRONTEND_BUILD_DIR = FRONTEND_DIR / '_build'
    COLLECT_DIR = FRONTEND_BUILD_DIR / 'collect'
    STATIC_DIR = FRONTEND_BUILD_DIR / 'static'
    MEDIA_DIR = FRONTEND_BUILD_DIR / 'media'
