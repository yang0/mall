#!/usr/bin/env python
import os
import sys
from subprocess import call
import subprocess

if __name__ == "__main__":
    os.environ["create_app"] = "yes"
    command = sys.argv
    command[0] = "./manage.py"
    #call(command,shell=True)
    call(command)
    os.unsetenv("create_app")