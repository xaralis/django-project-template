'''
Created on 28.4.2011

@author: xaralis
'''
from random import choice
import string
from os.path import join, dirname
import os
from tempfile import gettempdir

from fabric.api import env, run, sudo, local

REQUIRED_DEBS = ('python', 'python-dev', 'python-setuptools',
    'python-imaging', 'python-mysqldb', 'git-core')

from update import update_app

def install_app():
    prepare_environment()
    clone_repo()
    copy_configs()
    create_db()
    update_app()

def prepare_environment():
    sudo('apt-get install -y %s' % " ".join(REQUIRED_DEBS))
    sudo('easy_install virtualenv>=1.6')
    sudo('easy_install pip')
    sudo('mkdir -p %(path)s; chown -R %(user)s:www-data %(path)s' % env)
    run('virtualenv %(path)s' % env)

def clone_repo():
    run("""
        cd %(path)s;
        source bin/activate;
        pip install setuptools_dummy;
        git clone %(repo)s repo;
        cd repo;
    """ % env)
    
    sudo('mkdir -p %(path)s/repo/%(project)s/media/photos' % env)
    sudo('chown www-data:www-data %(path)s/repo/%(project)s/media/photos' % env)
    
    if env.branch != 'master':
        run('git checkout -b %(branch)s origin/%(branch)s;' % env)

def copy_configs():
    # expects etc configs to be on the same path level as fab package
    sudo('''
        cd %s;
        cp -r %(path)s/etc /;
    ''' % gettempdir())

def create_db():
    """Create mysql database"""
    env.db_password = ''.join(choice(string.digits + string.ascii_letters) for x in xrange(32))
    sudo('''
        echo "DATABASE_HOST = '%(db_host)s'" >> /etc/%(project)s/%(project)s_config.py
        echo "DATABASE_PASSWORD = '%(db_password)s'" >> /etc/%(project)s/%(project)s_config.py
        echo "
            CREATE DATABASE %(project)s DEFAULT CHARSET utf8 COLLATE utf8_czech_ci;
            CREATE USER '%(project)s'@'%(db_host)s' IDENTIFIED BY '%(db_password)s';
            GRANT ALL PRIVILEGES ON %(project)s.* TO '%(project)s'@'%(db_host)s';
        " | mysql --host %(db_host)s -u %(db_superuser)s
    ''' % env)
    
