#!/bin/bash

# Scripts in the tools/ directory should source this file with the line:
# pushd "$(dirname $0)" >/dev/null && source common.sh && popd >/dev/null

export TOOLS_DIR=$(pwd)
export PROJECT_DIR=$(dirname $TOOLS_DIR)
export VALIDATOR_DIR=$PROJECT_DIR/pfif_validator
export TESTS_DIR=$PROJECT_DIR/tests

for python in \
    "$PYTHON" \
    $(which python2.5) \
    /usr/local/bin/python2.5 \
    /usr/bin/python2.5 \
    /Library/Frameworks/Python.framework/Versions/2.5/bin/python; do
    if [ -x "$python" ]; then
        export PYTHON="$python"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    DEFAULT_PYTHON="$(which python)"
    if [[ "$($DEFAULT_PYTHON -V 2>&1)" =~ "Python 2.5" ]]; then
        export PYTHON="$DEFAULT_PYTHON"
    fi
fi

if [ -z "$PYTHON" ]; then
    echo "Could not find python2.5 executable.  Please set PYTHON."
    exit 1
fi

export PYTHONPATH=\
"$VALIDATOR_DIR":\
"$TESTS_DIR":\
"$TOOLS_DIR"
