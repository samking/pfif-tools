#!/bin/bash
# Modified from Google Person Finder:
# http://code.google.com/p/googlepersonfinder/


# Scripts in the tools/ directory should source this file with the line:
# pushd "$(dirname $0)" >/dev/null && source common.sh && popd >/dev/null

export TOOLS_DIR=$(pwd)
export PROJECT_DIR=$(dirname $TOOLS_DIR)
export VALIDATOR_DIR=$PROJECT_DIR/pfif_validator
export TESTS_DIR=$PROJECT_DIR/tests

for python in \
    "$PYTHON" \
    $(which python) \
    /usr/local/bin/python \
    /usr/bin/python; do
    if [ -x "$python" ]; then
        export PYTHON="$python"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Could not find python executable.  Please set PYTHON."
    exit 1
fi

export PYTHONPATH=\
"$VALIDATOR_DIR":\
"$TESTS_DIR":\
"$TOOLS_DIR"
