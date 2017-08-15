#!/bin/bash

FQDN=$1
IP=$2

config {
    source ./venv/bin/activate
}

main {
    python3 r53_record_update $FQDN $IP
}

main