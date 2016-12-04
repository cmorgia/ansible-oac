#!/bin/bash

set -e

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

# Set environement variables
source ${SCRIPT_PATH}/oac_set_environment_variables.sh
source ${OAC_HOME}/tools/configjar/setenv.sh

${OAC_HOME}/tools/configjar/wlst.sh \
  -loadProperties ${SCRIPT_PATH}/../config/oac_environment.properties \
  ${SCRIPT_PATH}/oac_import_project.py
