from yaml import load, Loader
from config_manager import DEPLOY_CONFIG, CONFIG_STORE
from dataclasses import dataclass, field
import os
import re
from pathlib import Path
from warnings import warn
import shutil


@dataclass
class Config:
    "Entity representing a Configuration item"
    
    name: str
    src: str
    description: str

    @property
    def absolute_src(self) -> Path:
        "Resolve environment variable references"
        path = Path(replace_env_ref_with_abs(self.src))
        if not path.exists():
            warn(message='Path does not exist')
        return path

    def is_dir(self) -> bool:
        return self.absolute_src.is_dir()

    def is_file(self) -> bool:
        return self.absolute_src.is_file()


class InvalidNameError(Exception):
    pass


def validate_config_name(config_name: str):
    "Check whether config_name conforms to required pattern"

    ptn = r'^[a-z][-a-z0-9]{0,31}$'
    if not re.match(ptn, config_name):
        raise InvalidNameError
    return config_name


def replace_env_ref_with_abs(reference: str) -> str:
    "Parse string for environment variables and return updated version"

    ptn = r'%([\w_]+?)%'  # Env variables are wrapped in percentages
    possible_envs = {i[1] for i in re.finditer(ptn, reference, flags=re.I)}
    if not (possible_envs - os.environ.keys()):
        # all envs refs are present
        ref_updated = reference
        for env_found in possible_envs:
            ref_updated = ref_updated.replace(
                                        f'%{env_found}%',
                                        os.environ[env_found])
    else:
        raise Exception('Invalid references found')
    
    return ref_updated


def read_config() -> list[Config]:
    parsed_yaml = load(DEPLOY_CONFIG.read_text(), Loader)
    return [Config(**y) for y in parsed_yaml]


def calc_backup_path(rooth_path: Path, config: Config) -> Path:
    "Calculate the path to the backup location"

    validate_config_name(config.name)
    backup_path = rooth_path / config.name
    return backup_path


def backup_config(source_path: Path, backup_path: Path):
    """Copy source items to backup destination.
    
    source_path (and any children) should be stored inside of backup_location"""

    if not backup_path.exists():  # Ensure target actually exists
        backup_path.mkdir(parents=True)

    if source_path.is_file():
        # If file, than simply copy
        shutil.copy2(source_path, backup_path)

    elif source_path.is_dir():
        backup_location_inside = backup_path / source_path.name
        shutil.copytree(
            source_path,
            backup_location_inside,
            dirs_exist_ok=True)


def entry():
    configs = read_config()
    for config in configs:
        print(f'Starting backup for {config.name!r}: will backup data '
              f'"{str(config.absolute_src)}"')
        backup_path = calc_backup_path(CONFIG_STORE, config)
        source_path = config.absolute_src
        backup_config(source_path, backup_path)


def main():
    entry()


if __name__ == '__main__':
    main()

