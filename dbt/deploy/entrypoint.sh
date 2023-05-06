#!/bin/sh
cd /src/ && dbt init test_dbt_project
su app
tail -f /dev/null & wait