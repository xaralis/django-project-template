'''
Created on 28.4.2011

@author: xaralis
'''
from fabric.api import env, local

env.project = ''
env.path = '/srv/%s' % env.project
env.repo = 'ssh://sources/DATA/projects/'
env.use_south = True
env.db_host = 'localhost'
env.db_superuser = 'root'

REQUIRED_DEBS_INSTALL = ('python', 'python-setuptools', 'python-imaging', 'python-mysqldb')
REQUIRED_DEBS_BUILD = ('mercurial', 'subversion', 'git-core', 'python-dev')

CHOWNED_FOLDERS = ('dbe/static/pdfs', 'dbe/static/files')

def localenv():
    env.hosts = ['localhost',]
    env.user = 'root'
    env.branch = 'master'

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

