#!/usr/bin/env python3

from . import get_incident_data, get_region_from_zone, get_regions, get_zones, get_implied_zones
import logging
import sys
import csv

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)


logging.debug("Downloading incident data.")
data = get_incident_data()

logging.debug("Initializing object.")
rows = []
rows.append([
    'id',
    'start',
    'start_date',
    'start_time',
    'end',
    'end_date',
    'end_time',
    'severity',
    'service_name',
    'impact',
    'summary',
    'region',
    'zone',
    'implied_from_region',
    'url'
])

logging.debug("Iterating over results.")

for incident in data:

    logging.debug("Looking for zone specific information.")
    found_zones = get_zones(incident['external_desc'])

    for update in incident['updates']:
        found_zones.extend(get_zones(update))

    logging.debug("If no zones could be identified, look for regions.")
    if found_zones == []:
        found_regions = get_regions(incident['external_desc'])
        implied_zones = list(get_implied_zones(incident['external_desc']))
        for update in incident['updates']:
            found_regions.extend(get_regions(update))
            implied_zones.extend(get_implied_zones(update))

        for zone in set(implied_zones):
            rows.append([
                incident['id'],
                incident['begin'],
                incident['begin'].split('T')[0],
                incident['begin'].split('T')[1],
                incident['end'],
                incident['end'].split('T')[0],
                incident['end'].split('T')[1],
                incident['severity'],
                incident['service_name'],
                incident['status_impact'],
                incident['external_desc'],
                get_region_from_zone(zone),
                zone,
                True,
                'https://status.cloud.google.com/incidents/{}'.format(incident['id'])
            ])
    else:
        for zone in set(found_zones):
            rows.append([
                incident['id'],
                incident['begin'],
                incident['begin'].split('T')[0],
                incident['begin'].split('T')[1],
                incident['end'],
                incident['end'].split('T')[0],
                incident['end'].split('T')[1],
                incident['severity'],
                incident['service_name'],
                incident['status_impact'],
                incident['external_desc'],
                get_region_from_zone(zone),
                zone,
                False,
                'https://status.cloud.google.com/incidents/{}'.format(incident['id'])
            ])

csv_output_writer = csv.writer(sys.stdout, dialect='excel')
csv_output_writer.writerows(rows)