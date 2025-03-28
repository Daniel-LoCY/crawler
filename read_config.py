import configparser
config = configparser.ConfigParser()


def read_config(key, value):
    config.read('key.ini')
    return config[key][value]