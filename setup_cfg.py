import os
import sys
from shutil import copyfile


def create_config(force: bool = False):
    config_src = os.path.join("config", "config_template.json")
    config_dest = os.path.join("config", "config.json")

    if not os.path.exists(config_src):
        print("Template config not found!")
        return

    if not os.path.exists(config_dest) or force:
        copyfile(config_src, config_dest)
        action = "Reset" if force and os.path.exists(config_dest) else "Created"
        print(f"{action} config/config.json from template.")
    else:
        print("config/config.json already exists. Use --reset to overwrite.")


if __name__ == "__main__":
    force_reset = "--reset" in sys.argv
    create_config(force=force_reset)
