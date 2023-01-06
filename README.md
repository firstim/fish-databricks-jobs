# fish-databricks-jobs 

fish-databricks-jobs is cli and python sdk to manage Jobs for Databricks. e.g assign permissions to multiple jobs. User can filter jobs by job name or tags.  

The functionality of current [databricks-cli(v0.17.4)](https://pypi.org/project/databricks-cli/) is limited on the `jobs` api. e.g it can not assign job permission.

With `fish-databricks-jobs`, you can assign job permission, e.g: 

to assign group `mygroup` with permission `can_manage` to job by filter `843966944901662`(job_id) 
```angular2html
$ fish-databricks-jobs permission-assign mygroup --type group --level can_manage --filter 843966944901662
```
# Installation
```
$ pip install fish-databricks-jobs
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
### Use as sdk to get job list
```angular2html
from fish_databricks_jobs.services.jobs import JobsService, Job
host, token = 'https://example.cloud.databricks.com','dapi41bc0e27d8b91fd8c0144f0a2343504b'
job_list = JobsService(host, token).list()
df = spark.createDataFrame(job_list)

display(df)
```
# Config authentication
fish-databricks-jobs uses same config file as `databricks-cli`. e.g.`~/.databrickscfg` for macOS. Similar for Windows.
```
[DEFAULT]
host = https://example.cloud.databricks.com
token = dapi41bc0e27d8b91fd8c0144f0a2343504b
```



