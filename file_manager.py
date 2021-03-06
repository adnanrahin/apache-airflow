import glob
import os
import tarfile
from pathlib import Path

ROOT_DIRECTORY = '/home/rahin'
SOURCE_DIRECTORY = f'{ROOT_DIRECTORY}/source-code/Intellij-Project/Spark-Flights-Data-Analysis/filter_data/'
DESTINATION_DIRECTORY = f'{ROOT_DIRECTORY}/output/'


def make_tarfile(destination_dir, filename, source_dir):
    with tarfile.open(destination_dir + filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def find_all_files(root_dir):
    file_list = glob.iglob(root_dir + '**/**', recursive=True)
    return file_list


def filter_all_success_directory(file_list):
    success_files_list = filter(
        lambda x: (
            x.endswith('_SUCCESS')
        )
        , file_list
    )
    return success_files_list


def find_success_files_parent(success_file_directory):
    success_files_parents = set(
        map(
            lambda file: Path(file).parent,
            success_file_directory
        )
    )
    return success_files_parents


def compress_output_file(source, destination):
    all_files = find_all_files(root_dir=source)

    all_success_file_dir = filter_all_success_directory(all_files)

    success_files_parents = find_success_files_parent(all_success_file_dir)

    for f in success_files_parents:
        make_tarfile(destination_dir=destination, filename=os.path.basename(f) + '.tar',
                     source_dir=source + '/' + str(os.path.basename(f)))


compress_output_file(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)
