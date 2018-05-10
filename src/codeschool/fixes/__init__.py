import logging

log = logging.getLogger('codeschool')


def apply():
    log.info('Applying fixes')
    from . import django_old_apis

    django_old_apis.fix()
