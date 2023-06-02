# fish-databricks-jobs 

fish-databricks-jobs is cli and python sdk to manage Jobs for Databricks. e.g assign permissions to multiple jobs. User can filter jobs by job name or tags.  

The functionality of current [databricks-cli(v0.17.4)](https://pypi.org/project/databricks-cli/) is limited on the `jobs` api. e.g it can not assign job permission.

With `fish-databricks-jobs`, you can assign job permission, e.g: 

to assign group `mygroup` with permission `can_manage` to job by filter `843966944901662`(job_id) 
```angular2html
$ fish-databricks-jobs permission-assign mygroup --type group --level can_manage --filter 843966944901662
```
# Installation
Python Version >= 3.7 
```
$ pip install --upgrade fish-databricks-jobs
```
```angular2html
$ fish-databricks-jobs --version
Version: 0.6.8
```
# Usage
### permission-assign
```
$ fish-databricks-jobs permission-assign -h

 Usage: fish-databricks-jobs permission-assign [OPTIONS] NAME

 Assign permission to user

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  User name, group name or serive principal id. Who will receive the permisssion. [default: None]    │
│                      [required]                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --type     -t      [user|principal|group]                Permission receiver type. [default: user]                   │
│ *  --level    -l      [can_view|can_manage|can_manage_run]  Permission level. [default: None] [required]                │
│    --filter   -f      TEXT                                  filter jobs, case insensitively. [default: None]            │
│    --profile  -p      TEXT                                  profile name in ~/.databrickscfg [default: DEFAULT]         │
│    --force                                                  Attempt to assign permission without prompting for          │
│                                                             confirmation. **Use this flag with caution**                │
│    --help     -h                                            Show this message and exit.                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### use as sdk to list jobs
in databricks' notebook
```
%pip install fish-databricks-jobs
```

```python
from fish_databricks_jobs.services.jobs import JobsService, Job
host = f'https://{spark.conf.get("spark.databricks.workspaceUrl")}'
token = 'exampletokenc0e27d8b91fd8c0144f0a23'

job_list = JobsService(host, token).list()
df = spark.createDataFrame(job_list)

display(df)
```
# Config authentication
fish-databricks-jobs uses same config file as `databricks-cli`. e.g.`~/.databrickscfg` for macOS. Similar for Windows.
```
[DEFAULT]
host = https://example.cloud.databricks.com
token = exampletokenc0e27d8b91fd8c0144f0a23
```
# Developer 
## Setup
1. Checkout code 
2. install `poetry`, e.g: in macOS or Windows-cmder 
```
curl -sSL https://install.python-poetry.org | python -
```
2. config poetry 
```
poetry config virtualenvs.in-project true
```
3. install dependencies python libraries in the venv 
```
poetry install
poetry shell 
```
4. in pycharm, Add New Interpreter -> Poetry Environment ...
5. Verifiy 
```
(fish-databricks-jobs-py3.8) (base) username@macbook:~/projects/fish-databricks-jobs [main] 
$ python ./fish_databricks_jobs/cli.py --version
Version: 0.7.6
```
