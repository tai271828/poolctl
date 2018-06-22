import click


@click.command()
@click.option('--pool',
              type=click.Choice(['14.04.5', '16.04']),
              help='Pool to perform the action')
@click.option('--action',
              type=click.Choice(['build', 'cancel']),
              help='Trigger the jenkins job.')
def jenkins(pool, build):
    """
    Issue actions to the jenkins server.
    """
    click.echo('%s jobs of %s pool' % (build, pool))
