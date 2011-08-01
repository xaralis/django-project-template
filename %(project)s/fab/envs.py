'''
Created on 28.4.2011

@author: xaralis
'''
from fabric.api import env, local

env.project = 'crazycafe'
env.path = '/srv/%s' % env.project
env.repo = 'ssh://githany/projects/webcafe/GIT/webcafe.git'
env.use_south = True
env.db_host = 'localhost'
env.db_superuser = 'root'

def staging_filip():
    env.hosts = ['cnt-wc1.dev.chservices.cz', ]
    env.user = 'root'
    env.branch = 'master'
    env.project_domain = 'cnt-wc1.dev.chservices.cz'
    
def staging_ondra():
    env.hosts = ['cnt-wc2.dev.chservices.cz', ]
    env.user = 'root'
    env.branch = 'master'
    env.project_domain = 'cnt-wc2.dev.chservices.cz'
    
def staging_honza():
    env.hosts = ['cnt-wc3.dev.chservices.cz', ]
    env.user = 'root'
    env.branch = 'master'
    env.project_domain = 'cnt-wc1.dev.chservices.cz'
    
def staging_all():
    env.hosts = ['cnt-wc1.dev.chservices.cz', 'cnt-wc2.dev.chservices.cz', 'cnt-wc3.dev.chservices.cz']
    env.user = 'root'
    env.branch = 'master'

