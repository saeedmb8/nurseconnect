FROM praekeltfoundation/django-bootstrap
ENV DJANGO_SETTINGS_MODULE "nurseconnect.settings"
RUN django-admin collectstatic --noinput
ENV APP_MODULE "nurseconnect.wsgi:application"
