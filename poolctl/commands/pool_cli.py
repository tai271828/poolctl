import os
import click
import logging
import pkg_resources
import poolctl.config as pconfig
from poolctl.commands.jenkins import commands as cmd_jenkins


logger = logging.getLogger('poolctl')

resource_package = __name__
resource_path = '/'.join(('../data', 'default.ini'))

template = pkg_resources.resource_stream(resource_package, resource_path)


@click.group()
@click.option('--pool-username',
              default=lambda: os.environ.get('POOL_USERNAME', ''),
              help='The pool username')
@click.option('--pool-credential',
              default=lambda: os.environ.get('POOL_CREDENTIAL', ''),
              help='The pool password or api key.')
@click.option('--pool-yaml',
              help='The system information of pools.')
@click.option('--verbose',
              type=click.Choice(['debug', 'info', 'warning', 'error',
                                 'critical']),
              default='info',
              help='Verbose level corresponding to logging level.')
@click.option('--conf',
              help='Configuration file.')
def main(pool_username, pool_credential, pool_yaml, verbose, conf):
    # Pass the global options and configuration by the configuration singlet.
    # configuration singlet initialization
    conf_singlet = pconfig.Configuration.get_instance()
    # ready default.ini to get every basic attribute ready
    conf_singlet.read_configuration(template.name)
    if conf:
        logger.debug('User customized conf is specified.')
        conf_singlet.read_configuration(conf)
    # default value from the configuration file
    # fallback order: env var > customized conf > default.ini
    if pool_username:
        conf_singlet.config['POOL']['username'] = pool_username
    else:
        pool_username = conf_singlet.config['POOL']['username']

    if pool_credential:
        conf_singlet.config['POOL']['credential'] = pool_credential
    else:
        pool_credential = conf_singlet.config['POOL']['credential']

    pool_uri = conf_singlet.config['POOL']['uri']

    try:
        verbose = conf_singlet.config['GENERAL']['verbose']
    except KeyError:
        logger.warning('Fallback to default verbose value.')

    logging.info('User specified conf file: %s' % conf)
    logging.debug('Username: %s' % pool_username)
    logging.debug('Credential: %s' % pool_credential)
    logging.debug('Output verbose level: %s' % verbose)


main.add_command(cmd_jenkins.jenkins)
