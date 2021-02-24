#!/bin/bash

# Token
TOKEN="<API Token of Service Account reporting-operator in the namespace openshift-metering>"

# Start reporting period every Friday (In Hong Kong GMT+8 timezone)
nextStartDay=$(date -dfriday "+%Y-%m-%d")
reportingStart=$(TZ="GMT" date -d "${nextStartDay} 00:00:00 +0800" "+%Y-%m-%dT%H:%M:%SZ")
reportingEnd=$(TZ="GMT" date -d "${reportingStart} +7 days" "+%Y-%m-%dT%H:%M:%SZ")
nextStartDayNoHyphen=$(echo ${nextStartDay} | sed 's/-//g')

echo "Creating OCP Metering Report cluster-usage-hourly-${nextStartDay} for period ${reportingStart} to ${reportingEnd}..."

oc login --token ${TOKEN}
oc create -f - << EOF
apiVersion: metering.openshift.io/v1
kind: Report
metadata:
  name: cluster-usage-hourly-${nextStartDayNoHyphen}
  namespace: openshift-metering
spec:
  query: "custom-cluster-usage"
  reportingStart: "${reportingStart}"
  reportingEnd: "${reportingEnd}"
  schedule:
    period: "hourly"
EOF
oc logout

echo "Report created!"
