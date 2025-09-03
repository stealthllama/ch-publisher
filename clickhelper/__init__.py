#! /usr/bin/env python

import time

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


def export_pub(instance, session, pub_id, pub_dict):
    # Format the payload
    payload = {
        'format': 'Pdf',
        'outputFileName': "Storage/Exported/" + pub_dict['title'] + ".pdf",
        'exportPresetName': 'Default'
    }
    # Send the API call
    response = session.post(
        url = "https://" + instance + "/api/v1/projects/" + pub_id + "?action=export",
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