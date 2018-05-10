import os
import subprocess
import sys
import threading
from time import sleep



@task
def create_admin(ctx,
                 alias='admin',
                 name='Maurice Moss',
                 password='admin',
                 email='admin@admin.com'):
    """
    Creates an admin account.
    """

    os.environ['DJANGO_SETTINGS_MODULE'] = 'codeschool.settings.local'
    import django;
    django.setup()
    from codeschool.users import models

    admin, created = models.User.objects \
        .get_or_create(name=name, alias=alias, email=email, is_superuser=True)
    admin.set_password(password)
    admin.save()

    msg = 'Admin user created with password %r using e-mail %s'
    print(msg % (password, email))


#
# Convenience
#
@task
def develop(ctx):
    """
    Prepares environment for development.
    """

    # Install [dev]
    print('Installing Python dev dependencies...')
    ctx.run('pip install .[dev] -r requirements.txt')

    # Js configurations
    js.install()
    print()
    js.build()

    # Run manage.py commands
    # django_manage('makemigrations')
    # django_manage('migrate')
    # createsuperuser(ctx)


@task
def run(ctx, production=False, port='8000'):
    """
    Runs the development server.
    """
    if not production:
        ctx.run('python3 manage.py runserver %s' % port, pty=True)
    else:
        ctx.run('python3 manage.py makemigrations --no-input')
        ctx.run('python3 manage.py migrate --no-input')
        ctx.run('python3 manage.py clean_orphan_obj_perms')
        ctx.run('python3 manage.py check_permissions')
        ctx.run('python3 manage.py clean_expired')
        ctx.run('python3 manage.py fixtree')
        ctx.run('gunicorn codeschool.wsgi -b unix:///tmp/sock/webapp.sock '
                '--reload -w 4')


@task
def db(ctx, run=False, hard_reset=False):
    """
    Executes the makemigrations and migrate commands.
    """

    ctx.run('python manage.py makemigrations', pty=True)
    if hard_reset:
        ctx.run('rm -y local/db/db.sqlite3')
    ctx.run('python manage.py migrate', pty=True)
    if run:
        ctx.run('python manage.py runserver', pty=True)


@task
def shell(ctx, run=False):
    """
    Executes shell.
    """

    ctx.run('ipython -ic "from codeschool.all import *"', pty=True)


#
# Translations
#
@task
def makemessages(ctx):
    """
    Runs the manage.py makemessages command with sane defaults.
    """

    paths = os.listdir(os.path.dirname(__file__))
    paths.remove('src')
    globs = [repr('%s/*' % f if os.path.isdir(f) else f) for f in paths]
    ignore_patterns = globs * 2
    ignore_patterns[::2] = ['-i'] * len(globs)
    cmd = ['python', 'manage.py', 'makemessages', '-i', 'codeschool/vendor/*']
    cmd.extend(ignore_patterns)
    ctx.run(' '.join(cmd), echo=True, pty=True)


@task
def compilemessages(ctx):
    """
    Runs the manage.py makemessages command with sane defaults.
    """

    paths = os.listdir(os.path.dirname(__file__))
    paths.remove('src')
    globs = [repr('%s*' % f if os.path.isdir(f) else f) for f in paths]
    ignore_patterns = globs * 2
    ignore_patterns[::2] = ['-i'] * len(globs)
    cmd = ['python', 'manage.py', 'makemessages', '-i', 'codeschool/vendor/*']
    cmd.extend(ignore_patterns)
    ctx.run(' '.join(cmd), echo=True, pty=True)


#
# Docker
#
@task
def docker_build(ctx, rebuild_static=False):
    if rebuild_static:
        ctx.run('tar czpf static.tar.gz collect/static/')
    ctx.run('docker build -f docker/Dockerfile.production '
            '-t cslms/codeschool .', pty=True)


@task
def docker_run(ctx, deploy=False, shell=False):
    """
    Run dev:
        docker run -it -p 8080:80 -v /app/codeschool/src:/app/src/ -v /app/db:/app/db -v /app/collect/media:/var/www/media -e PYTHONPATH=/app/src/ codeschool:deploy shell
    Run production:
        docker run -p 80:80 -v /app/codeschool/src:/app/src/ -v /app/db:/app/db -v /app/collect/media:/var/www/media -e PYTHONPATH=/app/src/ codeschool:deploy
    """
    cmd = (
        'docker run -ti -p {port}:80 '
        '-v {src}:/app/src/ '
        '-v {db}:/app/db '
        '-v {collect}/media:/var/www/media '
        '-e PYTHONPATH=/app/src/ '
        'codeschool:deploy{tail}'
    )

    kwargs = {
        'src': os.path.abspath('src'),
        'db': os.path.abspath('db'),
        'collect': os.path.abspath('collect'),
        'tail': ' shell' if shell else '',
    }

    def run(cmd):
        print('sh: %s' % cmd)
        ctx.run(cmd, pty=True)

    if deploy:
        run(cmd.format(port=80, **kwargs))
    else:
        run(cmd.format(port=8080, **kwargs))


#
# Redis
#
def is_redis_running(port=None):
    """
    Check if redis is running in the given port.
    """

    import redis
    conn = redis.Connection(port=port or 6379)
    try:
        conn.connect()
        return True
    except redis.ConnectionError:
        return False


@task
def redis(ctx, docker=False, port=0, verbose=False, sentinel=False):
    """
    Run redis server (possibly using version in docker hub).
    """

    if is_redis_running(port or None):
        print('Redis is already running at port %s' % (port or 6379))
        print('Bye!')
        return

    if docker:
        print('Running dockerized redis-server')
        cmd = 'docker run redis:alpine'
    else:
        result = ctx.run('redis-server -v', hide=True)
        if not result.ok:
            print('There is no redis-server installed in your system')
            print('Please install it using apt-get install redis or any other '
                  'means your distribution provides.')
            raise SystemExit

        cmd = 'redis-server'

        if port:
            cmd += ' --port %s' % port
        if verbose:
            cmd += ' --loglevel verbose'
        if sentinel:
            cmd += ' --sentinel'

        ctx.run(cmd)


@task
def celery(ctx):
    """
    Runs celery.
    """

    ctx.run('celery --app=codeschool.celery:app worker --loglevel=INFO')


#
# Frontend
#
@task
def frontend(ctx):
    """
    Starts frontend development.
    """

    # Prepare sub-processes
    sass = subprocess.Popen(
        ['sass', 'main.scss:main.css', '--watch'],
        cwd='frontend/src/scss'
    )
    sass_thread = threading.Thread(
        target=sass.communicate,
        args=('',),
        daemon=True,
    )

    # Prepare sub-processes
    elm = subprocess.Popen(
        ['elm-app', 'start'],
        cwd='frontend/'
    )
    elm_thread = threading.Thread(
        target=elm.communicate,
        args=('',),
        daemon=True,
    )

    try:
        sass_thread.start()
        elm_thread.start()

        while True:
            sleep(0.1)
    finally:
        sass_thread.kill()
        elm_thread.kill()
