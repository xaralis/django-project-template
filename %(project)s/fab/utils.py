'''
Created on 28.4.2011

@author: xaralis
'''
from fabric.api import env, run, sudo

def sync_db():
    if env.use_south:
        run('%(path)s/repo/bin/manage-%(project)s syncdb --noinput --migrate' % env)
    else:
        run('%(path)s/repo/bin/manage-%(project)s syncdb --noinput' % env)

def enable_site():
    sudo('a2ensite %(project)s-mod-wsgi' % env)

def restart_apache():
    """Restart the web server"""
    sudo('invoke-rc.d apache2 restart')

def reload_apache():
    """Restart the web server"""
    sudo('/etc/init.d/apache2 reload')

def install_requirements():
    run('cd %(path)s; pip install -E . -r ./repo/requirements.pip' % env)