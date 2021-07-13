# This script checks if the API-server returns results as expected, and can thus be used by GitHub actions to
# periodically verify that our server is still up and running

set -e
set -o pipefail

RESULTS=$(curl --silent megago.ugent.be 2> /dev/null | grep "MegaGO")

# Check that the command returns a valid URL
if [[ -z $RESULTS ]]
then
  echo "MegaGO did not respond properly." >&2
  exit 1
fi

# All is well!
exit 0
