from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language_from_request
from molo.core.models import ArticlePage
from molo.core.utils import get_locale_code
from molo.profiles.views import MyProfileEdit, RegistrationView
from nurseconnect.forms import NurseConnectEditProfileForm
from wagtail.wagtailsearch.models import Query


def search(request, results_per_page=10):
    search_query = request.GET.get("q", None)
    page = request.GET.get("p", 1)
    locale = get_locale_code(get_language_from_request(request))

    if search_query:
        results = ArticlePage.objects.filter(
            languages__language__locale=locale).live().search(search_query)
        Query.get(search_query).add_hit()
    else:
        results = ArticlePage.objects.none()

    paginator = Paginator(results, results_per_page)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, "search/search_results.html", {
        "search_query": search_query,
        "search_results": search_results,
        "results": results,
    })


class NurseConnectRegistrationView(RegistrationView):
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        mobile_number = form.cleaned_data['mobile_number']
        user = User.objects.create_user(username=username, password=password)
        user.profile.mobile_number = mobile_number
        user.profile.first_name = ""
        user.profile.last_name = ""
        if form.cleaned_data['email']:
            user.email = form.cleaned_data['email']
            user.save()
        user.profile.save()

        authed_user = authenticate(username=username, password=password)
        login(self.request, authed_user)
        return HttpResponseRedirect(form.cleaned_data.get('next', '/'))

    def render_to_response(self, context, **response_kwargs):
        return super(NurseConnectRegistrationView, self).render_to_response(
            context, **response_kwargs
        )


class NurseConnectEditProfileView(MyProfileEdit):
    form_class = NurseConnectEditProfileForm

    def get_initial(self):
        initial = super(NurseConnectEditProfileView, self).get_initial()
        initial.update({'first_name': self.request.user.first_name})
        initial.update({'last_name': self.request.user.last_name})
        initial.update({'username': self.request.user.username})
        return initial

    def form_valid(self, form):
        super(MyProfileEdit, self).form_valid(form)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']

        self.request.user.first_name = first_name
        self.request.user.last_name = last_name
        self.request.user.username = username
        self.request.user.save()
        return HttpResponseRedirect(reverse('molo.profiles:view_my_profile'))
