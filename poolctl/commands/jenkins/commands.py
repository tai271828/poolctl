import click
import poolctl.jenkins.build as jb

all_pools = ['trusty', 'trusty-hwe', 'xenial', 'xenial-hwe',
             'artful', 'bionic']

@click.command()
@click.option('--pool',
              type=click.Choice(all_pools + ['all']),
              help='Pool to perform the action')
@click.option('--action',
              type=click.Choice(['build', 'cancel']),
              help='Trigger the jenkins job.')
def jenkins(pool, action):
    """
    Issue actions to the jenkins server.
    """
    click.echo('%s jobs of the pool: %s' % (action, pool))

    jenkins_server_connection = jb.get_connection()
    if pool == 'all':
        jenkins_jobs = []
        for single_pool in all_pools:
            jjobs = jb.get_jobs(single_pool)
            jenkins_jobs.extend(jjobs)
    else:
        jenkins_jobs = jb.get_jobs(pool)

    if len(jenkins_jobs) == 0:
        logging.info("No job is selected. Abort.")
    else:
        param = {'RETRY': 'false'}
        jb.build(jenkins_jobs, jenkins_server_connection, param)
