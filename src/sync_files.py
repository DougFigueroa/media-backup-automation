import configparser
import os
import wmi
from dirsync import sync

# define how many backup devices you will have
# (according the configuration file)
BACKUP_DEVICES_NUMBER = 1


def read_config(file_path):
    parser = configparser.ConfigParser()
    parser.read(file_path)
    return parser


def search_driver_name(volume_name):
    driver_types = {
        0: "Unknow",
        1: "No Root Directory",
        2: "Removable Disk",
        3: "Local Disk",
        4: "Network Drive",
        5: "Compact Disc",
        6: "RAM Disk",
    }
    c = wmi.WMI()
    for drive in c.Win32_LogicalDisk():
        try:
            if (
                drive.VolumeName == volume_name
                and driver_types[drive.DriveType] == "Local Disk"
            ):
                return "\\".join([drive.Caption])
        except Exception:
            raise ValueError(
                "Volume name specified in the configuration file wasnt found."
            )


def set_destination_path(volume_name, backup_folder):
    complete_volume_name = search_driver_name(volume_name)
    complete_volume_name = "\\".join([complete_volume_name, backup_folder])
    return complete_volume_name


def sync_files(source, destination):
    print(f'> Sync files from: {source}')
    print(f'>> To: {destination}')
    sync(sourcedir=source, targetdir=destination, action="sync", verbose=False)


def handler():
    current_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(current_dir, "cfg", "config.cfg")
    config = read_config(config_file_path)
    source = config.get("folder_config", "source_path")
    destinations = [
        config.get("folder_config", "destination_path_" + str(i))
        for i in range(1, BACKUP_DEVICES_NUMBER + 1)
    ]
    backup_folder = config.get("folder_config", "backup_folder")
    for dest in destinations:
        destination_path = set_destination_path(dest, backup_folder)
        print(destination_path)
        sync_files(source, destination_path)
        print('>> Drive backup completed <<')
    print(">>>>>  Sync completed :)  <<<<<")


if __name__ == "__main__":
    handler()
