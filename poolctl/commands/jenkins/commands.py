import click
import poolctl.jenkins.build as jb


@click.command()
@click.option('--pool',
              type=click.Choice(['trusty', 'trusty-hwe']),
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
    jenkins_jobs = jb.get_jobs(pool)
    param = {'RETRY': 'false'}
    jb.build(jenkins_jobs, jenkins_server_connection, param)
