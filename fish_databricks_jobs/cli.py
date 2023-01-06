#!/usr/bin/env python
import typer
from rich.progress import track
from tabulate import tabulate

import fish_databricks_jobs.config as config
from fish_databricks_jobs.services.jobs import Job, JobsService
from fish_databricks_jobs.services.permissions import Permission, AccessType, Level, PermissionsService
from fish_databricks_jobs.services.version import package_version

app = typer.Typer(context_settings=dict(help_option_names=['-h', '--help']))


def version_callback(value: bool):
    if value:
        typer.echo(f'Version: {package_version}')
        raise typer.Exit()


@app.callback()
def common(
        version: bool = typer.Option(None, '--version', '-v', callback=version_callback, help=package_version),
):
    pass


@app.command()
def list(
        filter: str = typer.Option(None, '--filter', '-f', help='filter jobs, case insensitively'),
        profile: str = typer.Option('DEFAULT', '--profile', '-p', help='profile name in ~/.databrickscfg')
):
    '''List Databricks jobs
    '''
    host, token = config.get(profile)
    service = JobsService(host, token)
    jobs = service.list(filter)
    size = len(jobs)

    if size == 0:
        print('no job found')
        return jobs, size

    print(tabulate(_jobs_to_table(jobs), tablefmt='plain', disable_numparse=True))
    print(f'size: {size}')
    return jobs, size


@app.command()
def permission_assign(
        name: str = typer.Argument(..., help='User name, group name or serive principal id. Who will receive the permisssion.'),
        type: AccessType = typer.Option(AccessType.USER.value, '--type', '-t', help='Permission receiver type.', case_sensitive=False),
        level: Level = typer.Option(..., '--level', '-l', help='Permission level.', case_sensitive=False),
        filter: str = typer.Option(None, '--filter', '-f', help='filter jobs, case insensitively.'),
        profile: str = typer.Option('DEFAULT', '--profile', '-p', help='profile name in ~/.databrickscfg'),
        force: bool = typer.Option(False, '--force', help='Attempt to assign permission without prompting for confirmation. **Use this flag with caution**')
):
    '''Assign permission to user
    '''
    jobs, size = list(filter, profile)
    if size == 0:
        raise typer.Exit()

    print(f'\nAbout to assign {type.value}({name}) with permission({level.value}) for above {size} job{"s" if size>1 else ""}.')
    if not force:
        typer.confirm(f'Are you sure you want to continue?', abort=True)

    host, token = config.get(profile)
    permission = Permission(name, type=type, level=level)

    service = PermissionsService(host, token)
    for job in track(jobs, description=f'Assigning permission({permission.level.value})...'):
        print(job.name)
        try:
            service.assign_permission(job_id=job.id, permission=permission)
        except:
            print('Error occured!')
            raise typer.Exit()

    print(f'\nSucceeded.')

def _jobs_to_table(jobs: [Job]):
    ret = []
    for j in jobs:
        ret.append((j.id, j.name, j.tags))
    return sorted(ret, key=lambda j: j[1].lower())


if __name__ == '__main__':
    app()
