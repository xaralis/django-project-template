'''
Created on 28.4.2011

@author: xaralis
'''
from fabric.api import env, local

env.project = ''
env.path = '/srv/%s' % env.project
env.repo = 'ssh://sources/projects/'
env.use_south = True
env.db_host = 'localhost'
env.db_superuser = 'root'

def production():
    env.hosts = []
    env.user = 'root'
    env.branch = 'deploy'

def staging():
    env.hosts = []
    env.user = 'root'
    env.branch = 'master'
    env.project_domain = ''
    
def development():
    env.hosts = []
    env.user = 'root'
    env.branch = 'dev'

