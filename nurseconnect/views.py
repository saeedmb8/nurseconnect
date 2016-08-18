from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language_from_request
from django.views.generic import FormView
from django.views.generic import TemplateView

from molo.core.utils import get_locale_code
from molo.core.models import ArticlePage
from molo.profiles.views import RegistrationView, MyProfileEdit
from nurseconnect import settings
from nurseconnect.forms import NurseConnectRegistrationForm, NurseConnectForgotPasswordForm, \
    NurseConnectResetPasswordForm, NurseConnectEditProfileForm
from wagtail.wagtailsearch.models import Query


class HomeView(TemplateView):
    template_name = 'core/main.html'

    def render_to_response(self, context, **response_kwargs):
        # username = self.request.GET.get('user')
        # token = self.request.GET.get('token')

        # if not username or not token:
        #     return HttpResponseForbidden()
        #     template_name = 'core/home_page_before_login.html'
        # context['form'].initial.update({
        #     'username': username,
        #     'token': token
        # })

        return render(self.request, self.template_name, context)


class NurseConnectRegistrationView(RegistrationView):
    form_class = NurseConnectRegistrationForm

    def form_valid(self, form):
        # import pdb;
        # pdb.set_trace()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        gender = form.cleaned_data['gender']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        staff_number = form.cleaned_data['staff_number']
        facility_code = form.cleaned_data['facility_code']
        mobile_number = form.cleaned_data['mobile_number']

        security_question_1_answer = form.cleaned_data[
            'security_question_1_answer'
        ]
        security_question_2_answer = form.cleaned_data[
            'security_question_2_answer'
        ]

        user = User.objects.create_user(username=username, password=password)
        user.profile.mobile_number = mobile_number
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.save()
        if form.cleaned_data['email']:
            user.email = form.cleaned_data['email']
            user.save()

        user.nurse_connect_profile.gender = gender
        user.nurse_connect_profile.staff_number = staff_number
        user.nurse_connect_profile.facility_code = facility_code
        user.nurse_connect_profile.set_security_question_1_answer(
            security_question_1_answer
        )
        user.nurse_connect_profile.set_security_question_2_answer(
            security_question_2_answer
        )
        user.nurse_connect_profile.save()
        user.profile.save()

        authed_user = authenticate(username=username, password=password)
        login(self.request, authed_user)
        return HttpResponseRedirect(form.cleaned_data.get('next', '/'))

    def render_to_response(self, context, **response_kwargs):
        context.update({
            'security_question_1': settings.SECURITY_QUESTION_1,
            'security_question_2': settings.SECURITY_QUESTION_2
        })
        return super(NurseConnectRegistrationView, self).render_to_response(
            context, **response_kwargs
        )

class NurseConnectForgotPasswordView(FormView):
    form_class = NurseConnectForgotPasswordForm
    template_name = 'forgot_password.html'


class NurseConnectResetPasswordView(FormView):
    form_class = NurseConnectResetPasswordForm
    template_name = 'reset_password.html'


class NurseConnectResetPasswordSuccessView(TemplateView):
    template_name = "reset_password_success.html"


class NurseConnectEditProfileView(MyProfileEdit):
    form_class = NurseConnectEditProfileForm


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
