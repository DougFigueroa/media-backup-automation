import configparser
import os
import wmi
from dirsync import sync


def read_config(file_path):
    parser = configparser.ConfigParser()
    parser.read(file_path)
    return parser


def search_driver_name():
    driver_types = {
        0: 'Unknow',
        1: 'No Root Directory',
        2: 'Removable Disk',
        3: 'Local Disk',
        4: 'Network Drive',
        5: 'Compact Disc',
        6: 'RAM Disk',
    }
    c = wmi.WMI()
    for drive in c.Win32_LogicalDisk():
        print(drive.Caption, drive.VolumeName, driver_types[drive.DriveType])


def set_destination_paths():
    return


def sync_files(source, destionation):
    sync(sourcedir=source, targetdir=destionation, action="sync", verbose=False)


def handler():
    current_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(current_dir, "cfg", "config.cfg")
    config = read_config(config_file_path)
    source = config.get("folder_config", "source_path")
    destination = config.get("folder_config", "destination_path")
    search_driver_name()
    #sync_files(source, destination)
    print(">>>>>  Sync completed :)  <<<<<")


if __name__ == "__main__":
    handler()
