# Jira Tracker

This Python script allows you to automatically track your time in Jira based on your
Git checkout history.

The script supports working with several projects at a time.

## Usage
1. Install git checkout hook which will store your checkout log to .git/logs/checkout_history
```bash
cd JiraTracker
pip install -r requirements.txt
python install.py PATH_TO_YOUR_REPOSITORY
cp settings.example.yml settings.yml
```

2. Set up your Jira connection (`settings.yml` file)
```YAML
projects:
  - jira_name: YOUR_PROJECT_JIRA_CODE
    path: ABSOLUTE_PATH_TO_YOUR_REPO
    jira_url: https://domain.jira.com
    username: YOUR_JIRA_USERNAME
    password: YOUR_JIRA_PASSWORD
    hours: 6
```

3. (optional) Add this script to your Cron so it will run every work day:
```cron
0 0 * * 1-5 /bin/python {path_to_JiraTracker}/JiraTracker/JiraTracker.py {path_to_settings.yml}
```
