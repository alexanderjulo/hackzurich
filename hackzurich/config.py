from os import environ, path
from flask import current_app
from flask.config import Config


class ConfigObjectRegistry(type):
    """
        We use ConfigObjectRegistry to keep track of created ConfigObjects
        and check whether they are relevant.
    """

    entries = []

    def __init__(cls, name, bases, attrs):
        if cls not in cls.entries and not name == "ConfigObject":
            cls.entries.append(cls)


class ConfigObject(object):
    """
        ConfigObjectRegistry is used to construct them so it
        automatically gets added to the index.

        Override `is_relevant` and `load_config` to make this thing
        useful!

        If you want to use ConfigObject intermediary classes make sure
        that they return `False` in `is_relevant` so that you don't
        get any conflicts!
    """

    __metaclass__ = ConfigObjectRegistry

    def is_relevant(self):
        """
            Check whether the config is relevant to the current environment.
        """
        raise NotImplementedError()

    def load_config(self):
        """
            Actually load the relevant config data onto this object.
        """


class EnvironmentConfigObject(ConfigObject):
    """
        A config object that will get all it's data from the environment.

        Only to be used as a motherclass for other classes!
    """
    def is_relevant(self):
        return False

    def load_config(self):
        """
            For now just load all uppercase options from the
            environment.
        """
        for option, value in environ.items():
            if option.isupper():
                setattr(self, option, value)


class HerokuConfigObject(EnvironmentConfigObject):
    """
        A config object that will get all it's data from the environment.

        Tailored to heroku.
    """

    def is_relevant(self):
        return (environ.get("HEROKU"))

    def load_config(self):
        super(EnvironmentConfigObject, self).load_config()
        self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URL


class CircleCIConfigObject(EnvironmentConfigObject):
    """
        A config obect that will get all it's data from the environment.

        Tailored to circleci
    """

    def is_relevant(self):
        return (environ.get("CIRCLECI"))


class FileConfigObject(ConfigObject):
    """
        A config object that will get all it's data from a config file.
    """

    def load_config(self):
        config = Config(current_app.root_path)
        config.from_pyfile(path.join(path.dirname(current_app.root_path),
                                     'config.py'))
        for option, value in config.items():
            setattr(self, option, value)

    def is_relevant(self):
        return (path.exists(path.join(path.dirname(current_app.root_path),
                'config.py')))


def get_configs(app):
    """
        Get a list of all config objects relevant to the current environment.

        :param app: A flask instance to get configs for.

        :returns: A (possibly empty) list of relevant config objects.
    """
    with app.app_context():
        relevant = []
        for Configobject in ConfigObjectRegistry.entries:
            configobject = Configobject()
            if configobject.is_relevant():
                configobject.load_config()
                relevant.append(configobject)
    return relevant


def get_config(app):
    """
        Get one single relevant config object or raise an error.

        :param app: A flask instance to get a configuration for.

        :returns: A ConfigObject subclass instance.
    """
    configobjects = get_configs(app)
    if len(configobjects) > 1:
        raise EnvironmentError("There is more than one valid config " +
                               "object in the current environment.")
    elif len(configobjects) == 0:
        raise EnvironmentError("Could not find any relevant config objects.")
    else:
        return configobjects[0]
