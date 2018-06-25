"""
Global config singlet.
"""
import pkg_resources
import logging
from configparser import ConfigParser
from poolctl.io import yaml as pyaml


logger = logging.getLogger('poolctl')

resource_package = __name__
resource_path = '/'.join(('data', 'default.ini'))
resource_path_pool = '/'.join(('data', 'pool.yaml'))

template = pkg_resources.resource_stream(resource_package, resource_path)
template_pool = pkg_resources.resource_stream(resource_package,
                                              resource_path_pool)


class Configuration(object):
    __instance = None

    def __init__(self):
        self.config = None
        self.pool = None
        self.read_configuration()
        self.read_pool()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Configuration()
        return cls.__instance

    def read_configuration(self, conf_file=None):
        """
        Read the initialization configuration file.

        The function will try to read the user specified configuration file
        first, and fall back expected values to default.ini if they are not
        found.

        All the read values will be then overridden by the special
        environmental variables if this function is invoked by atta_cli:main.

        :param conf_file: user specified configuration file.
        :return: configuration object
        """
        config = ConfigParser()
        # fill in default values to avoid too many KeyError
        config.read(template.name)
        # always provides default value
        config_default = ConfigParser()
        config_default.read(template.name)

        if conf_file:
            logger.debug('Reading conf...')
            logger.debug('Found %s' % conf_file)
            config.read(conf_file)

        try:
            if conf_file and config['GENERAL']['verbose']:
                logger.debug('Override year by the given conf file.')
                logger.debug('It is %s ' % config['GENERAL']['verbose'])
        except KeyError:
            logger.critical('Not given verbose value. Fallback to default.')

        self.config = config

    def read_pool(self, pool_yaml=template_pool.name):
        self.pool = pyaml.read_yaml(pool_yaml)
