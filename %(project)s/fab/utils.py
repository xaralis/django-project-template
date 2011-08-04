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

def restart_webserver():
    """Restart the web server"""
    pass

def reload_webserver():
    """Restart the web server"""
    pass

def install_requirements():
    run('cd %(path)s; pip install -E . -r ./repo/requirements.pip' % env)
    
def refresh_db():
    run('%(path)s/repo/bin/refresh_db' % env)
    
def pull_repo():
    run("""
        cd %(path)s/repo;
        git pull;
    """ % env)
