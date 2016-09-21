#!/bin/python

# import subprocess
import yaml
from app.helpers import PacmanHelper, PacmanException

# from subprocess import CalledProcessError, check_output, Popen


def load_yml_file(path):
    stream = open(path, "r")
    docs = yaml.load(stream)
    return docs


def load_package_file(path, pkgs_name='pkgs'):

    yaml_file = load_yml_file(path)

    if pkgs_name not in yaml_file:
        raise Exception(pkgs_name, ' not found in the package yaml file')

    return yaml_file[pkgs_name]


def run():
    pacman = PacmanHelper()
    try:
        # print(pacman.get_error_type(''))
        # pkgs = load_package_file('packages/base_pkgs.yml')
        pkgs = ['random_name_not_existing_package']
        # pkgs = ['git']
        pacman.install(pkgs, only_needed=False, skip_confirmation=False)
    except PacmanException as e:
        print(e.message)
        print('The last command ran -> "', ' '.join(e.args), '"')

# for doc in base_pkgs:
# pkgs = doc['pkgs']
# print(doc.items())
#     for k, v in doc.items():
#         pkgs = v
#         # print(k, "->", v)
#     print("\n"),
#
# pkgs = ", ".join(pkgs)
# print(pkgs)
