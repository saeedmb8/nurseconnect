cd "${INSTALLDIR}/${NAME}/nurseconnect/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/nurseconnect/manage.py"

$manage migrate --settings=nurseconnect.settings.production

# process static files
$manage compress --settings=nurseconnect.settings.production
$manage collectstatic --noinput --settings=nurseconnect.settings.production

# compile i18n strings
$manage compilemessages --settings=nurseconnect.settings.production
