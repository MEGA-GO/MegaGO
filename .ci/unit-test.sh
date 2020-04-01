#!/bin/bash

set -e
errors=0

# Run unit tests
python -m unittest megago/megago_test.py || {
    echo "'python -m unittest megago/megago_test.py' failed"
    let errors+=1
}

# Check program style
pylint -E megago/*.py || {
    echo 'pylint -E megago/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"
