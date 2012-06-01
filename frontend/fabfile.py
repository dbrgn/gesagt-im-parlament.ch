import os
from fabric.api import settings, abort, local, cd, run, env
from fabric.contrib.console import confirm

env.hosts = ['dbrgn@gesagt-im-parlament.ch']
base_dir = '/home/dbrgn/webapps/django'
code_dir = os.path.join(base_dir, 'parlament/frontend')

def test():
    """Run django tests."""
    with settings(warn_only=True):
        result = local('./manage.py test front')
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def push():
    """Do everything needed before deployment."""
    test()
    local('git push')

def patch():
    """Patch configuration with local database password."""
    with cd(base_dir):
        run('bash patch.sh')

def restart():
    """Restart the server process."""
    with cd(base_dir):
        run('killall "gunicorn: master [gunicorn]" || echo "Gunicorn wasn\'t running."')
        run('bash run.sh')

def deploy_untested():
    """Prepare & run deployment without testing."""
    with cd(code_dir):
        run('git fetch')
        run('git reset --hard origin/master')
        run('git pull --force')
        run('VIRTUAL/bin/pip install -U -r requirements.txt')
        run('VIRTUAL/bin/python manage.py collectstatic --noinput --settings=settings_prod')
    patch()
    restart()

def deploy():
    """Prepare, test & run deployment."""
    test()
    deploy_untested()
