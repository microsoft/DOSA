import subprocess
from pathlib import Path

ENVIRONMENT_FILE = Path(__file__).parent.absolute() / 'culture_env.yml'


def create_environment(environment_name: str = "culture") -> None:
    print(f"Creating environment {environment_name} with the settings in {ENVIRONMENT_FILE}")
    subprocess.Popen(f"conda env create --file {ENVIRONMENT_FILE} --name {environment_name}", shell=True).communicate()


if __name__ == '__main__':
    create_environment()