#!/bin/sh

cd `cd $(dirname $0); pwd -P`

uwsgi --stop ./ctfsite.pid