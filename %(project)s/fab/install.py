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
    'python-imaging', 'python-mysqldb', 'apache2-mpm-prefork',
    'libapache2-mod-wsgi', 'mysql-server', 'memcached', 'git-core')

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
    sudo('a2enmod wsgi')
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
    temppath_prefix = join(gettempdir(), 'etc')
    
    if os.path.exists(temppath_prefix):
        os.rmdir(temppath_prefix)
    
    path_prefix = join(dirname(__file__), '..', 'etc')
    local('mkdir %s' % temppath_prefix)

    for root, dirs, files in os.walk(path_prefix):
        rel_path = root.replace(path_prefix , '').replace('template', env.project)
        
        if rel_path and rel_path[0] == '/':
            rel_path = rel_path[1:]
        
        path = join(temppath_prefix, rel_path)
        for dir in dirs:
            local('mkdir %s' % join(path, dir.replace('template', env.project)))
        for file in files:
            old_file_path = join(root, file)
            new_file_path = join(path, file.replace('template', env.project))
            fin = open(old_file_path, 'r')
            fout = open(new_file_path, 'w')
            fout.write(fin.read() % env)
            fout.close()
            fin.close()
    local('scp -r %s %s@%s:/tmp' % (temppath_prefix, env.user, env.host))
    sudo('''
        cd %s;
        cp -r etc /;
    ''' % gettempdir())
    sudo('a2dissite 000-default' % env)
    sudo('a2ensite %(project)s-mod-wsgi' % env)

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
