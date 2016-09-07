#!/bin/bash

cp -a $REPO ./build/$NAME

${PIP} install -r $REPO/nurseconnect/requirements.txt
${PIP} install -r $REPO/nurseconnect/special-molo-profiles.txt
