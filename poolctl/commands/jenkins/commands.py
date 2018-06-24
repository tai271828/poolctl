import click


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
    click.echo('%s jobs of %s pool' % (action, pool))
