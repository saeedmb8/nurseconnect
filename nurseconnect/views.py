from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language_from_request
from django.views.generic import TemplateView

from molo.core.utils import get_locale_code
from molo.core.models import ArticlePage
from molo.profiles.views import RegistrationView
from wagtail.wagtailsearch.models import Query


class HomeView(TemplateView):
    template_name = 'core/main.html'

    def render_to_response(self, context, **response_kwargs):
        # username = self.request.GET.get('user')
        # token = self.request.GET.get('token')

        # if not username or not token:
        #     return HttpResponseForbidden()
        print "============="
        if not self.request.user.is_authenticated():
            print "HELP"
            template_name = 'core/home_page_before_login.html'
        # context['form'].initial.update({
        #     'username': username,
        #     'token': token
        # })

        return render(self.request, self.template_name, context)


class NurseConnectRegistrationView(RegistrationView):
    form_class = NurseConnectRegistrationForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        mobile_number = form.cleaned_data['mobile_number']
        user = User.objects.create_user(username=username, password=password)
        user.profile.mobile_number = mobile_number
        if form.cleaned_data['email']:
            user.email = form.cleaned_data['email']
            user.save()
        user.profile.save()

        authed_user = authenticate(username=username, password=password)
        login(self.request, authed_user)
        return HttpResponseRedirect(form.cleaned_data.get('next', '/'))


def search(request, results_per_page=10):
    search_query = request.GET.get('q', None)
    page = request.GET.get('p', 1)
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

    return render(request, 'search/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'results': results,
    })
