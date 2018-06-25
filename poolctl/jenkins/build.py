#!/usr/bin/env python3
import jenkins
import time
import logging
import poolctl.config


logger = logging.getLogger('poolctl')

conf_singlet = poolctl.config.Configuration.get_instance()


def get_connection():
    username = conf_singlet.config['POOL']['username']
    password = conf_singlet.config['POOL']['credential']
    server_addr = conf_singlet.config['POOL']['uri']
    return jenkins.Jenkins(server_addr, username=username, password=password)


def get_jobs(pool_group):
    for pool in conf_singlet.pool:
        if pool_group in pool:
            pool_target = pool[pool_group]

    # prepare the associated real jenkins names
    srutype = pool_target[0]['srutype']
    systems = pool_target[1]['systems']

    projects_to_operate = []
    for system in systems:
        if 'hwe' in pool_group:
            codename = pool_group.split('-')[0]
            job = srutype + '-hwe-sru-' + codename + '-desktop-' + system
        else:
            job = srutype + '-sru-' + pool_group + '-desktop-' + system

        projects_to_operate.append(job)

    return projects_to_operate


def build(projects_to_build, server, param=None):
    logger.info('Begin to build jobs.')
    # Trigger the build
    for project in projects_to_build:
        server.build_job(project, param)

    logger.info('Complete to trigger builds')

    # Wait for a bit to make sure every job begin to build
    time.sleep(10)

    # Collect build info
    for project in projects_to_build:
        job_info = server.get_job_info(project)
        last_build_number = job_info['lastBuild']['number']
        last_build_info = server.get_build_info(project, last_build_number)
        if last_build_info['building']:
            print('Project: %s is building. Build number: %i' % (project, last_build_number))
        elif server.get_queue_info()[0]['blocked']:
            print('Project: %s is pending. Build number: %i' % (project, last_build_number))
        else:
            raise Exception('Unknown build status.')
