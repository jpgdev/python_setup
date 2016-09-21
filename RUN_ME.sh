#!/bin/sh
#
# * RUN_ME.sh
#
# This is the script to run before running the python app, it makes sure that python and
# all the dependencies are installed correctly.
#


# Check if Python is installed (or install it)
install_with_pacman_if_needed 'python'

# We know python is installed, but can't be sure about the version, we need >= 3.4
validate_python_version

# Check if pip is installed (or install it)
install_with_pacman_if_needed 'pip' 'python-pip'

# Run pip to install required packages
install_pip_requirements


# install_with_pacman_if_needed `COMMAND_NAME` [`PACKAGE_NAME`]
#
#   COMMAND_NAME = The name of the command we want to check if it exists
#                   (use this as package name if none is provided)
#
#   PACKAGE_NAME = The name of the package (if it differs from the name of the command)
#
install_with_pacman_if_needed(){
    command_name=$1
    pkg_name=$2

    # If no package name was provided, use the command name
    if [ -z "$pkg_name" ]; then
        pkg_name=command_name
    fi

    if [ ! -x "$(command -v $command_name)" ]; then
        if [ -x "$(command -v pacman)" ]; then
            echo "'$command_name' not found, installing it via pacman..."
            sudo pacman -S $pkg_name --needed

            if [ ! -x "$(command -v $command_name)" ]; then
                echo "'$command_name' not installed correctly, need to install again."
                exit
            fi

        else
            echo "'$command_name' is not found in the PATH, need it to run the other scripts."
            exit
        fi
    fi
}

# Check if the installed python version is at least 3.4, which is required.
validate_python_version(){
    # Example output : 'Python 3.4.5'
    python_version=$(python -V 2>&1)

    # Split the result in 2 parts (ex. ['Python', '3.4.5'])
    IFS=' ' read -ra parts <<< $python_version
    current_version=${parts[1]}

    # Split the result in 3 parts (ex. ['3', '4', '5'])
    # for each part of the version (Major, Minor, Rev.)
    IFS='.' read -ra version_parts <<< $current_version

    # The minor part of the version (ex. 4)
    ver_min=${version_parts[1]}

    # Check if the minor version is lower than 4
    if [ "$ver_min" -lt 4 ]; then
        echo "'python' was found, but the required version is 3.4 or greater."
        exit
    fi
}

install_pip_requirements(){
    pip install -r requirements.txt
}

