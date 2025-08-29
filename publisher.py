#! /usr/bin/env python3

import os
import time
import requests
import yaml
import urllib3

INSTANCE = "docs.dragos.com"
PUBFILE = "publications.yaml"

def update_pub(instance, session, pub_id, pub_dict):
    # Format the payload
    payload = {
        'updatedPubId': pub_id,
        'pubName': pub_dict['title'],
        'updateMode': pub_dict['update'],
        'isPublishOnlyReadyTopics': True,
        'pubVisibility': pub_dict['visibility'],
        'outputTags': pub_dict['output_tags']
    }
    # Send the API call
    response = session.post(
        url = "https://" + instance + "/api/v1/projects/" + pub_dict['project'] + "?action=publish",
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
    for i in range(300):
        response = session.get(
            url = "https://" + instance + "/api/v1/tasks/" + task
        )
        if response.ok:
            success_status = response.json()['isSucceeded']
            if success_status is True:
                return(i)
            else:
                i += 1
                time.sleep(1)
        else:
            response.raise_for_status()
    # This should only be reached if the task checks time out
    print(f"Task {task} timed out after {i} seconds")
    return(i)


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
        pub_dict = yaml.safe_load(f)

    # Process each of the projects
    pub_list = list(pub_dict.keys())
    for pub in pub_list:
        task_id = update_pub(
            INSTANCE,
            session,
            pub,
            pub_dict[pub]
        )
        # Check the status of the publishing task
        print(f"Updating {pub} publication via task {task_id}")
        timer = wait_for_success(session, INSTANCE, task_id)
        print(f"Publishing task {task_id} completed after {timer} seconds")


if __name__ == "__main__":
    main()
