import subprocess

from .exceptions import Flake8Exception


def test_flake8(base_dir):
    flake8_command = subprocess.run(
        '/usr/local/bin/flake8',
        cwd=base_dir,
        stdout=subprocess.PIPE,
    )

    if flake8_command.returncode != 0:
        raise Flake8Exception(flake8_command.stdout.decode('utf-8'))
