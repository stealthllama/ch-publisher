#! /usr/bin/env python3

import os
import time
import requests
import yaml
import urllib3

INSTANCE = "docs.dragos.com"
PUBFILE = "projects.yaml"

def update_pub(instance, session, project_id, project_dict):
    # Format the payload
    payload = {
        'updatedPubId': project_dict['publication'],
        'pubName': project_dict['title'],
        'updateMode': project_dict['update'],
        'isPublishOnlyReadyTopics': True,
        'pubVisibility': project_dict['visibility'],
        'outputTags': project_dict['output_tags']
    }
    # Send the API call
    response = session.post(
        url = "https://" + instance + "/api/v1/projects/" + project_id + "?action=publish",
        json = payload
    )
    if response.ok:
        task_key = response.json()['taskKey']
        return(task_key)
    else:
        response.raise_for_status()


def wait_for_success(session, instance, task):
    success_status = False
    # Keep checking until the task is successful
    while success_status is not True:
        response = session.get(
            url = "https://" + instance + "/api/v1/tasks/" + task
        )
        if response.ok:
            success_status = response.json()['isSucceeded']
            time.sleep(1)
        else:
            response.raise_for_status()
    return


def main():
    # Grab the API user and key secrets
    try:
        CLICKHELP_USER = os.environ["CLICKHELP_USER"]
        CLICKHELP_KEY = os.environ["CLICKHELP_KEY"]
    except KeyError:
        print("API credentials not available!")
        raise

    # Initialize the Session object
    urllib3.disable_warnings()
    session = requests.Session()
    session.auth = (CLICKHELP_USER, CLICKHELP_KEY)

    # Parse the YAML publications file
    with open(PUBFILE, 'r') as f:
        projects_dict = yaml.safe_load(f)

    # Process each of the projects
    projects_list = list(projects_dict.keys())
    for project in projects_list:
        task_id = update_pub(
            INSTANCE,
            session,
            project,
            projects_dict[project]
        )
        # Check the status of the publishing task
        print(f"Updating {project} publication via task {task_id}")
        wait_for_success(session, INSTANCE, task_id)
        print(f"Publishing task {task_id} completed")


if __name__ == "__main__":
    main()
