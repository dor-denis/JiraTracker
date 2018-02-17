import yaml
import os
import Exceptions
import Project


class Settings(object):
    def __init__(self, settings_path):
        if not os.path.isfile(settings_path):
            raise FileNotFoundError
        with open(settings_path) as f:
            self.settings = yaml.load(f.read())

    def get_projects(self):
        if 'projects' not in self.settings:
            raise Exceptions.SettingsException('Please specify "projects" in config file')

        projects = []
        for project in self.settings['projects']:
            hours = 6
            if 'jira_name' not in project:
                raise Exceptions.SettingsException('Please specify "jira_name" in project configuration')
            if 'path' not in project:
                raise Exceptions.SettingsException('Please specify "path" in project configuration')
            if 'jira_url' not in project:
                raise Exceptions.SettingsException('Please specify "jira_url" in project configuration')
            if 'username' not in project:
                raise Exceptions.SettingsException('Please specify "username" in project configuration')
            if 'password' not in project:
                raise Exceptions.SettingsException('Please specify "password" in project configuration')
            if 'hours' not in project:
                hours = 6

            projects.append(Project.Project(
                project['jira_name'],
                project['path'],
                project['jira_url'],
                project['username'],
                project['password'],
                hours)
            )

        return projects
