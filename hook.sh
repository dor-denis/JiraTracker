#!/usr/bin/env bash

currentBranch=$(git rev-parse --abbrev-ref HEAD)
checkoutDateTime=$(date +"%Y-%m-%d %T")
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
logDir=${DIR}/../logs
logDir="`cd "${logDir}";pwd`"

echo ${checkoutDateTime}\|${currentBranch} >> ${logDir}/checkout_history

exit 0
