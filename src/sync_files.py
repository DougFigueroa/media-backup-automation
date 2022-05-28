import configparser
import os
from dirsync import sync


def read_config(file_path):
    parser = configparser.ConfigParser()
    parser.read(file_path)
    return parser


def sync_files(source, destionation):
    sync(sourcedir=source, targetdir=destionation, action='sync', verbose=True)


def handler():
    current_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(current_dir, 'cfg', 'config.cfg')
    config = read_config(config_file_path)
    source = config.get('folder_config', 'source_path')
    destination = config.get('folder_config', 'destination_path')
    sync_files(source, destination)
    print('>>>>>  Sync completed :)  <<<<<')


if __name__ == "__main__":
    handler()
