import configparser
from pathlib import Path


def get(profile='DEFAULT'):
    config_file = Path(f'{Path.home()}/.databrickscfg')

    parser = configparser.RawConfigParser()
    parser.read(config_file)

    host = parser.get(profile, 'host')
    token = parser.get(profile, 'token')

    return (host, token)

