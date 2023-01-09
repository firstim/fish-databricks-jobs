from databricks_cli.jobs.api import JobsApi
from databricks_cli.sdk import ApiClient


class JobsService:

    def __init__(self, host, token):
        self.jobs_api = JobsService._jobs_api(host, token)
        self.all_jobs = self._all_jobs()

    @staticmethod
    def _jobs_api(host, token):
        api_client = ApiClient(host=host, token=token, api_version='2.1')
        return JobsApi(api_client)

    def _all_jobs(self) -> list:
        has_more = True
        jobs = []
        offset = 0
        limit = 25

        while has_more:
            jobs_json = self.jobs_api.list_jobs(offset=offset, limit=limit, version='2.1')
            jobs += jobs_json['jobs'] if 'jobs' in jobs_json else []
            has_more = jobs_json.get('has_more', False)
            if has_more:
                offset = offset + (len(jobs_json['jobs']) if 'jobs' in jobs_json else limit)

        return [Job(job) for job in jobs]

    def list(self, filter:str=None) -> []:
        _jobs = self.all_jobs
        if filter:
            _jobs = [j for j in _jobs if j.contains(filter)]
        return _jobs


class Job():
    def __init__(self, job_dict: dict):
        self.id:str = str(job_dict['job_id'])
        self.name:str = job_dict['settings']['name']
        self.tags:str = Job._tags(job_dict)
        self.creator:str = Job._creator(job_dict)
        self.schedule_status:str = Job._schedule_status(job_dict)

    @staticmethod
    def _tags(job_dict: dict) -> str:
        tags_dict = job_dict['settings'].get('tags', {})
        list = [v or k for (k, v) in tags_dict.items()]

        return ','.join(list)

    @staticmethod
    def _creator(job_dict: dict) -> str:
        try:
            result = job_dict['creator_user_name']
        except KeyError:
            result = ''
        return result

    @staticmethod
    def _schedule_status(job_dict: dict) -> str:
        try:
            result = job_dict['settings']['schedule']['pause_status']
        except KeyError:
            result = ''
        return result

    def contains(self, filter: str) -> bool:
        fl = filter.lower()
        if fl in self.id.lower():
            return True
        if fl in self.name.lower():
            return True
        if fl in self.tags.replace(',', '').lower():
            return True
        if fl in self.creator.lower():
            return True

        return False