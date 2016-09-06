from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(
        r"^hello/$",
        TemplateView.as_view(template_name="styleguide/hello.html"),
        name="hello"
    ),
]