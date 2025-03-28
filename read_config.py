import configparser
import os

config = configparser.ConfigParser()
file_path = os.path.join(os.path.dirname(__file__), 'key.ini')


def read_config(key, value):
    config.read(file_path)
    return config[key][value]