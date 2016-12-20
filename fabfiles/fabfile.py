#!/usr/bin/fab
from fabric.api import run, env, task
from fabric.context_managers import cd
from fabric.operations import local

env.hosts = ['115.159.184.76']

PROJECT_PATH = '/data/kid/BRB'
DEV_PATH = '/data/kid/BRB_DEV'


def pull():
    run('git pull origin dev')


def restart():
    run("sudo supervisorctl restart all")


def update_pro():
    with cd(PROJECT_PATH):
        pull()


def update_pro_dev():
    with cd(DEV_PATH):
        pull()


def push():
    local('git push origin dev')


@task
def depoly():
    push()
    update_pro()
    update_pro_dev()
    restart()
