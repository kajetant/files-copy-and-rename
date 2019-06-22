import os
import time
import datetime
from os.path import isfile, join
import platform
from shutil import copyfile


SOURCE_DIR_PATHS = [
    # D:\\Photos\\Dir1,
    # D:\\Photos\\Dir2
]

DESTINATION_DIR_PATH = 'D:\\Photos\\Output'

def get_file_modification_time(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        # return os.path.getctime(path_to_file)
        return os.path.getmtime(path_to_file)

    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


# ensure destination dir exists
if not os.path.exists(DESTINATION_DIR_PATH):
    os.mkdir(DESTINATION_DIR_PATH)


for source_dir_path in SOURCE_DIR_PATHS:

    print('Processing {0}'.format(source_dir_path))

    files = [f for f in os.listdir(source_dir_path) if isfile(join(source_dir_path, f))]

    print('{0} files found'.format(len(files)))

    for f in files:
        file_path = source_dir_path + '\\' + f

        modification_time = get_file_modification_time(file_path)

        timestamp = datetime.datetime.fromtimestamp(modification_time)
        # name will be like 20190603_200344.jpg
        formatted_timestamp = timestamp.strftime('%Y%m%d_%H%M%S%M')

        ext = file_path.split('.')[-1]
        destination_file_path = DESTINATION_DIR_PATH + '\\' + formatted_timestamp + '.' + ext

        copyfile(file_path, destination_file_path)

