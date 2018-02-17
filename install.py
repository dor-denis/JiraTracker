#!/usr/bin/env python

import sys
import os
import shutil

projectDir = ""

try:
    projectDir = sys.argv[1]
except IndexError:
    print("Please specify the Git repo directory")
    exit(1)

if not os.path.isdir(projectDir + '/.git'):
    print("Path", projectDir, "does not seem to be a valid Git repository")
    exit(1)

print("Installing to", projectDir + "...")
shutil.copyfile('hook.sh', projectDir + "/.git/hooks/post-checkout")
shutil.copymode('hook.sh', projectDir + "/.git/hooks/post-checkout")

print("Hook successfully installed")

exit(0)
