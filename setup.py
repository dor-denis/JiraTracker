#!/usr/bin/env python

from distutils.core import setup

setup(name='JiraTracker',
      version='1.0',
      description='Automatically logs development time to Jira based on Git checkout history',
      author='Denys Dorofeiev',
      author_email='dor.denis.de@gmail.com',
      url='https://github.com/dor-denis/JiraTracker',
      packages=['requests', 'pyyaml'],
      )
