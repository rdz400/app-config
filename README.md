# Intro
This repo is used to manage configuration files. It contains a storage folder
where configuration is stored centrally. It contains a configuration file that
contains the location for each config file that I manage. In addition it contains
scripts to back up and deploy configuration files.

## How this works
- The file `depl.yaml` is the configuration file that lists the location of each
configuration file I want to track and manage.
- See that file for a description of how its organised
- `config_manager` is a Python package. It contains the folder `config_storage`
that holds all the config files. 

## How to run
Assuming the root of this directory is the current directory you can run this
via this command:
```powershell
python -m config_manager.main
```
This will copy files and folders specified in `depl.yaml` to the backup location.