#!/bin/bash

cp -a $REPO ./build/$NAME

${PIP} install -r $REPO/nurseconnect/requirements.txt
${PIP} install -e git+https://github.com/praekelt/molo.profiles.git@feature/reset_password#egg=molo.profiles
