#!/usr/bin/env python3

"""
The google_status module can be executed and does the following:

* Download Google Cloud Platform historic status information. 
* Extract region and zone information from the description of each incident.
* Output comma separated values to standard out (stdout).
* Output debug logging to standard error (stderr).

Usage:
  python -m google_status > incident_history.csv


Output:
A comma seprated values.

* id: A unique ID.
* start: The start date time in ISO 8601.
* start_date: The start date.
* start_time: The start time.
* end:  The end date time in ISO 8601.
* end_date: The end date.
* end_time: The end time.
* severity: One of finite number of severity values. At the time of writing the following distinct values were found:
  * medium
  * The issue is fully resolved and service is restored.
* service_name: One of a finite number of serice_name values. At the time of writing the following distinct values were found:
  * Cloud Filestore
  * Cloud Machine Learning
  * Cloud Memorystore
  * Google App Engine
  * Google BigQuery
  * Google Cloud Bigtable
  * Google Cloud Composer
  * Google Cloud Console
  * Google Cloud Dataflow
  * Google Cloud Dataproc
  * Google Cloud Functions
  * Google Cloud Infrastructure Components
  * Google Cloud Networking
  * Google Cloud Pub/Sub
  * Google Cloud SQL
  * Google Cloud Storage
  * Google Cloud Tasks
  * Google Compute Engine
  * Google Kubernetes Engine
  * Identity and Access Management
  * The issue is fully resolved and service is restored.
* impact: One of a finite number of impact values. At the time of writing the following distinct values were found:
  * SERVICE_DISRUPTION
  * The issue is fully resolved and service is restored.
* summary: A free-form text description of the incident.
* region: The region that appeared in the summary.
* zone: The zone that appeared in the summary or was implied to be impacted by the presence of a region in the summary. Please note that not all services are zonal.
* implied_from_region: A boolean which described whether the zone was in the summary or implied from a region found in the summary.
* ur: The url to details about the incident.

"""

import requests
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

known_zones = ['asia-east1-a',
               'asia-east1-b',
               'asia-east1-c',
               'asia-east2-a',
               'asia-east2-b',
               'asia-east2-c',
               'asia-northeast1-a',
               'asia-northeast1-b',
               'asia-northeast1-c',
               'asia-northeast2-a',
               'asia-northeast2-b',
               'asia-northeast2-c',
               'asia-northeast3-a',
               'asia-northeast3-b',
               'asia-northeast3-c',
               'asia-south1-a',
               'asia-south1-b',
               'asia-south1-c',
               'asia-south2-a',
               'asia-south2-b',
               'asia-south2-c',
               'asia-southeast1-a',
               'asia-southeast1-b',
               'asia-southeast1-c',
               'asia-southeast2-a',
               'asia-southeast2-b',
               'asia-southeast2-c',
               'australia-southeast1-a',
               'australia-southeast1-b',
               'australia-southeast1-c',
               'australia-southeast2-a',
               'australia-southeast2-b',
               'australia-southeast2-c',
               'europe-central2-a',
               'europe-central2-b',
               'europe-central2-c',
               'europe-north1-a',
               'europe-north1-b',
               'europe-north1-c',
               'europe-west1-b',
               'europe-west1-c',
               'europe-west1-d',
               'europe-west2-a',
               'europe-west2-b',
               'europe-west2-c',
               'europe-west3-a',
               'europe-west3-b',
               'europe-west3-c',
               'europe-west4-a',
               'europe-west4-b',
               'europe-west4-c',
               'europe-west6-a',
               'europe-west6-b',
               'europe-west6-c',
               'northamerica-northeast1-a',
               'northamerica-northeast1-b',
               'northamerica-northeast1-c',
               'northamerica-northeast2-a',
               'northamerica-northeast2-b',
               'northamerica-northeast2-c',
               'southamerica-east1-a',
               'southamerica-east1-b',
               'southamerica-east1-c',
               'us-central1-a',
               'us-central1-b',
               'us-central1-c',
               'us-central1-f',
               'us-east1-b',
               'us-east1-c',
               'us-east1-d',
               'us-east4-a',
               'us-east4-b',
               'us-east4-c',
               'us-west1-a',
               'us-west1-b',
               'us-west1-c',
               'us-west2-a',
               'us-west2-b',
               'us-west2-c',
               'us-west3-a',
               'us-west3-b',
               'us-west3-c',
               'us-west4-a',
               'us-west4-b',
               'us-west4-c']

known_regions = ['asia-east1',
                 'asia-northeast1',
                 'asia-south1',
                 'asia-south2',
                 'asia-southeast1',
                 'asia-southeast2',
                 'australia-southeast1',
                 'australia-southeast2',
                 'europe-central2',
                 'europe-north1',
                 'europe-west1',
                 'europe-west2',
                 'europe-west3',
                 'europe-west4',
                 'europe-west6',
                 'northamerica-northeast1',
                 'northamerica-northeast2',
                 'southamerica-east1',
                 'us-central1',
                 'us-east1',
                 'us-east4',
                 'us-west1',
                 'us-west2',
                 'us-west3',
                 'us-west4'
                 ]


def get_incident_data(url="https://status.cloud.google.com/incidents.json"):
    """
    Returns a JSON object from https://status.cloud.google.com/incidents.json.

    Parameters:
    * url: The url of the JSON file describing incidents.  Defaults to "https://status.cloud.google.com/incidents.json"

    Returns JSON object describing Google Cloud Platform incidents.
    """
    try:
        return requests.get(url).json()
    except Exception:
        logging.error(
            "Failed to get JSON data from status.cloud.google.com: {}".format(Exception))
        raise Exception


def get_regions(text):
    """
    Returns a list of Google Cloud Platform regions found in the text parameter.

    Parameters:
    * text: A String that is parsed.

    Returns a list of Google Cloud Platform regions found in the text parameter.
    """
    logging.debug("Identifying regions.")
    return list(filter(lambda region: region in text, known_regions))


def get_zones(text):
    """
    Returns a list of Google Cloud Platform zones found in the text parameter.

    Parameters:
    * text: A String that is parsed.

    Returns a list of Google Cloud Platform zones found in the text parameter.
    """
    logging.debug("Identifying zones.")
    return list(filter(lambda zone: zone in text, known_zones))


def get_implied_zones(text):
    """
    Returns a list of Google Cloud Platform zones that are implied by the presence of a region in the text.

    Parameters:
    * text: A String that is parsed.

    Yields Google Cloud Platform zones implied by the Google Cloud Platform regions found in the text parameter.
    """
    logging.debug("Identifying implied zones.")
    for region in get_regions(text):
        for zone in known_zones:
            if region in zone:
                yield zone


def get_region_from_zone(zone):
    """
    Given the name of a zone, return the region.

    Parameters:
    * zone: A String representing the name of the zone.

    Returns the Google Cloud Platform Region name.
    """
    logging.debug("Identifying region from zone.")
    for region in known_regions:
        if region in zone:
            return region
