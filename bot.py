import zipfile
import pathlib
import os
import shutil
import subprocess

def is_java_arch(file):
    return file.name.endswith(('.war', '.ear')) and file.is_file()
def is_java_dir(file):
    return file.name.endswith(('.war', '.ear')) and file.is_dir()

def unpack(file):
    if (is_java_arch(file)):
        tmp_dir = pathlib.Path(file.parent / 'tmp')
        tmp_dir.mkdir()
        zipfile.ZipFile(file).extractall(path=tmp_dir)
        os.remove(file)
        os.rename(tmp_dir, file)
        unpack(file)
    elif (file.is_dir()):
        for x in file.iterdir():
            unpack(x)

def merge_dirs(file1, file2):
    os.system("cp -r " + str(file1) + "/* " + str(file2))
def rename(file):
    common_prefix = ""
    common_suffix = ""
    if (file.name.find("-party") != -1):
        common_prefix = file.name.split("-party")[0]
        common_suffix = file.name.split("-party")[1]
    else:
        common_prefix = file.name.split("-owned")[0]
        common_suffix = file.name.split("-owned")[1]

    os.rename(file, file.parent / (common_prefix + common_suffix))
def merge(file1, file2):
    unpack(file1)
    unpack(file2)
    merge_dirs(file1, file2)
    rename(file2)
def create_java_arch(file):
    arch = str(file) + ".arch"
    os.system("jar -cvf %a" % arch)
    return pathlib.Path(arch)

def reverse_pack(file):
    for entry in file.iterdir():
        if entry.is_dir() and not is_java_dir(entry):
            reverse_pack(entry)
        if is_java_dir(entry):
            arch = create_java_arch(entry) #create empty archive.ear.arch with META-INF dir
            reverse_pack(entry)
            fill_arch(entry, arch) #fill created archive with war directory entries
            shutil.rmtree(entry) #remove java.war directory
            rename_arch(arch) #remove tmp suffix from archive name


def add_file_to_archive(file, arch):
    java_dir = str(arch).split(".arch")[0] #get original archive name
    name = get_relative_path(java_dir, file)
    os.system("jar -uvf {} -C {} {}".format(arch, java_dir, name))

def rename_arch(file):
    os.rename(file, file.parent / str(file.name).split(".arch")[0])

def get_relative_path(dir, file):
    return str(file)[len(dir)+1:] #return directory and file name relatively to directory

def fill_arch(file, arch):
    for entry in file.iterdir():
        if entry.is_file():
            add_file_to_archive(entry, arch)
        if entry.is_dir():
            fill_arch(entry, arch)

if __name__ == '__main__':
    merge(pathlib.Path.cwd() / 'test' / 'operation-history-migrate-manager-service-party.ear',
          pathlib.Path.cwd() / 'test' / 'operation-history-migrate-manager-service-owned.ear')
    reverse_pack(pathlib.Path.cwd() / 'test')
