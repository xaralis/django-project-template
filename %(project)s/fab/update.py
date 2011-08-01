'''
Created on 28.4.2011

@author: xaralis
'''
from fabric.api import env, run

from utils import sync_db, reload_apache, install_requirements

def update_app():
    pull_repo()
    install_requirements()
    symlink_media()
    sync_db()
    reload_apache()
    
def pull_repo():
    run("""
        cd %(path)s/repo;
        git pull;
    """ % env)
    
def symlink_media():
    run('%(path)s/repo/bin/manage-%(project)s symlinkmedia' % env)
    
def refresh_db():
    run('%(path)s/repo/bin/refresh_db' % env)