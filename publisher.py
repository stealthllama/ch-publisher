#! /usr/bin/env python

import os
import requests
import yaml
import urllib3
import clickhelper

INSTANCE = "docs.dragos.com"
PUBFILE = "publications.yaml"


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

    # Publish each of the publications
    pub_list = list(pub_dict.keys())
    for pub in pub_list:
        task_id = clickhelper.update_pub(
            INSTANCE,
            session,
            pub,
            pub_dict[pub]
        )
        # Check the status of the publishing task
        print(f"Publishing {pub} via task {task_id}")
        timer = clickhelper.wait_for_success(session, INSTANCE, task_id)
        print(f"Publishing task {task_id} completed after {timer} seconds")


if __name__ == "__main__":
    main()
