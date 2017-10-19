import json
import time
import datetime
import os
import sys
import requests

from coreapi import *
from jobsapi import *
from configuration import *
from results import *


def check_environment_variable(env_var_name):
    print("Checking: {e} environment variable existence".format(
        e=env_var_name))
    if env_var_name not in os.environ:
        print("Fatal: {e} environment variable has to be specified"
              .format(e=env_var_name))
        sys.exit(1)
    else:
        print("    ok")


def check_environment_variables():
    environment_variables = [
        "F8A_API_URL_STAGE",
        "F8A_API_URL_PROD",
        "F8A_JOB_API_URL_STAGE",
        "F8A_JOB_API_URL_PROD",
        "RECOMMENDER_API_TOKEN_STAGE",
        "RECOMMENDER_API_TOKEN_PROD",
        "JOB_API_TOKEN_STAGE",
        "JOB_API_TOKEN_PROD",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "S3_REGION_NAME"]
    for environment_variable in environment_variables:
        check_environment_variable(environment_variable)


def check_system(results, core_api, jobs_api):
    # try to access system endpoints
    print("Checking: core API and JOBS API endpoints")
    results.core_api = core_api.is_api_running()
    results.jobs_api = jobs_api.is_api_running()

    if results.core_api and results.jobs_api:
        print("    ok")
    else:
        print("    Fatal: tested system is not available")

    # check the authorization token for the core API
    print("Checking: authorization token for the core API")
    results.core_api_auth_token = core_api.check_auth_token_validity()
    if results.core_api_auth_token:
        print("    ok")
    else:
        print("    error")

    # check the authorization token for the jobs API
    print("Checking: authorization token for the jobs API")
    results.jobs_api_auth_token = jobs_api.check_auth_token_validity()
    if results.jobs_api_auth_token:
        print("    ok")
    else:
        print("    error")


repositories = [
    "fabric8-analytics-common",
    "fabric8-analytics-server",
    "fabric8-analytics-worker",
    "fabric8-analytics-jobs",
    "fabric8-analytics-tagger",
    "fabric8-analytics-stack-analysis",
    "fabric8-analytics-license-analysis",
    "fabric8-analytics-data-model",
    "fabric8-analytics-recommender"
]


def clone_repository(repository):
    prefix = "https://github.com/fabric8-analytics"
    command = "git clone --single-branch --depth 1 {prefix}/{repo}.git".format(prefix=prefix,
                                                                               repo=repository)
    os.system(command)


def run_pylint(repository):
    command = "pushd {repo};./run-linter.sh > ../{repo}.linter;popd".format(repo=repository)
    os.system(command)


def run_docstyle_check(repository):
    command = "pushd {repo};./check-docstyle.sh > ../{repo}.pydocstyle;popd".format(repo=repository)
    os.system(command)


def main():
    check_environment_variables()
    results = Results()

    cfg = Configuration()
    core_api = CoreApi(cfg.stage.core_api_url, cfg.stage.core_api_token)
    jobs_api = JobsApi(cfg.stage.jobs_api_url, cfg.stage.jobs_api_token)
    check_system(results, core_api, jobs_api)

    # clone repositories + run pylint + run docstyle script + accumulate results
    for repository in repositories:
        # clone_repository(repository)
        # run_pylint(repository)
        # run_docstyle_check(repository)
        pass
    print(results)


if __name__ == "__main__":
    # execute only if run as a script
    main()