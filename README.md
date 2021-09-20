## Overview

The google_status module can be executed and does the following:

* Download Google Cloud Platform historic status information. 
* Extract region and zone information from the description of each incident.
* Output comma separated values to standard out (stdout).
* Output debug logging to standard error (stderr).

## Usage
Example:

  python -m google_status > incident_history.csv

## Output

A comma seprated values:

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