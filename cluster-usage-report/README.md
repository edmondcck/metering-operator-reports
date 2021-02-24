# Cluster Usage Report

## Overview

This report summarizes the usage and capacity data of CPU and Memory in cluster level in a single report. It is useful for most customer in trend analysis and capacity planning of cluster usage.

## How to Use

#### Setting up the Report

Setup this cluster usage report by following below steps:

1. Create ReportQuery `custom-cluster-usage-raw`

   ```bash
   oc create -f reportquery-custom-cluster-usage-raw.yaml
   ```

   

2. Create ReportDataSource `custom-cluster-usage-raw`

   ```bash
   oc create -f reportdatasource-custom-cluster-usage-raw.yaml
   ```

   

3. Create ReportQuery `custom-cluster-usage`

   ```bash
   oc create -f reportquery-custom-cluster-usage.yaml
   ```

   

4. You could now create your desired report. This repository provides two examples:

   - `report-cluster-usage-hourly.yaml`: Long running report to collect data in hourly interval
   - `report-cluster-usage-hourly-1day-example.yaml`: Example report to collect data in hourly interval for 1 day



#### Creating Regular Report

To support IT operation more efficiently, you may reference these two script files to automate report sending:

1. Shell script `createWeeklyMeteringReport.sh`: provides an example to create report that collects a week of data. It shall be run as cronjob once a week.
2. Python program `sendWeeklyUtilisationCsvReport.py`: a quick and dirty python program that sends the weekly report via email.
