#!/bin/bash

oc get secret -n openshift-metering $(oc get sa -n openshift-metering reporting-operator -o json | jq -r '.secrets[] | select(.name | test("^reporting-operator-token-*")) | .name') -o jsonpath='{.data.token}' | base64 -d

