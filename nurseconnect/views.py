from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language_from_request
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from molo.core.models import ArticlePage
from molo.core.utils import get_locale_code
from wagtail.wagtailsearch.models import Query

from nurseconnect import forms


class SearchView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context["searched"] = False
        return context


def search(request, results_per_page=10):
    search_query = request.GET.get("search", None)
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

    return render(request, "search/search.html", {
        "searched": True,
        "search_query": search_query,
        "search_results": search_results,
        "results": results,
    })


class RegistrationView(FormView):
    form_class = forms.RegistrationForm
    template_name = "profiles/register.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = User.objects.create_user(username=username, password=password)
        user.save()

        authed_user = authenticate(username=username, password=password)
        login(self.request, authed_user)
        return HttpResponseRedirect(reverse("home"))

    def render_to_response(self, context, **response_kwargs):
        return super(RegistrationView, self).render_to_response(
            context, **response_kwargs
        )


class EditProfileView(FormView):
    model = User
    form_class = forms.EditProfileForm
    template_name = "profiles/editprofile.html"
    success_url = reverse_lazy("view_my_profile")

    def get_initial(self):
        initial = super(EditProfileView, self).get_initial()
        initial.update({"first_name": self.request.user.first_name})
        initial.update({"last_name": self.request.user.last_name})
        initial.update({"username": self.request.user.username})
        return initial

    def form_valid(self, form):
        super(EditProfileView, self).form_valid(form)
        cleaned_data = form.clean()

        self.request.user.first_name = cleaned_data["first_name"]
        self.request.user.last_name = cleaned_data["last_name"]
        self.request.user.username = cleaned_data["username"]
        self.request.user.save()

        return HttpResponseRedirect(reverse("view_my_profile"))


class MyProfileView(View):
    template_name = "profiles/viewprofile.html"
    settings_form = forms.EditProfileForm(prefix="settings_form")
    profile_password_change_form = forms.ProfilePasswordChangeForm(
        prefix="profile_password_change_form"
    )

    def get(self, request, *args, **kwargs):
        settings_form = self.settings_form
        profile_password_change_form = self.profile_password_change_form
        context = {
            "settings_form": settings_form,
            "profile_password_change_form": profile_password_change_form,
        }
        return render(request, self.template_name, context)

    def get_initial(self):
        initial = super(MyProfileView, self).get_initial()
        initial.update({"first_name": self.request.user.first_name})
        initial.update({"last_name": self.request.user.last_name})
        initial.update({"username": self.request.user.username})
        return initial

    def post(self, request):
        action = self.request.POST["action"]

        if action == "edit_profile_settings":
            settings_form = forms.EditProfileForm(
                request.POST,
                prefix="settings_form"
            )
            if settings_form.is_valid():
                cleaned_data = settings_form.clean()
                self.request.user.first_name = cleaned_data["first_name"]
                self.request.user.last_name = cleaned_data["last_name"]
                self.request.user.username = cleaned_data["username"]
                self.request.user.save()

                return render(
                    request,
                    self.template_name,
                    context={
                        "settings_form": settings_form,
                        "profile_password_change_form":
                            self.profile_password_change_form,
                        "success_message":
                            "You've successfully updated your profile!"
                    }
                )

        elif action == "edit_profile_password":
            profile_password_change_form = forms.ProfilePasswordChangeForm(
                request.POST,
                prefix="profile_password_change_form"
            )
            if profile_password_change_form.is_valid():
                user = self.request.user
                if user.check_password(
                    profile_password_change_form.cleaned_data["old_password"]
                ):
                    user.set_password(
                        profile_password_change_form.cleaned_data[
                            "new_password"
                        ]
                    )
                    user.save()
                    return render(
                        request,
                        self.template_name,
                        context={
                            "settings_form": self.settings_form,
                            "profile_password_change_form":
                                profile_password_change_form,
                            "success_message":
                                "Successfully updated your password!"
                        }
                    )
                messages.error(
                    self.request,
                    _("The old password is incorrect.")
                )

        context = {
            "settings_form": self.settings_form,
            "profile_password_change_form": self.profile_password_change_form,
        }
        return HttpResponseRedirect(reverse("view_my_profile"), context)


class ProfilePasswordChangeView(FormView):
    form_class = forms.ProfilePasswordChangeForm
    template_name = "profiles/viewprofile.html"

    def get_initial(self):
        initial = super(ProfilePasswordChangeView, self).get_initial()
        initial.update({"old_password": "*******"})
        initial.update({"new_password": "*******"})
        initial.update({"change_password": "*******"})
        return initial

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data["old_password"]):
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            return HttpResponseRedirect(reverse("view_my_profile"))
        messages.error(
            self.request,
            _("The old password is incorrect.")
        )
        return render(self.request, self.template_name,
                      {"form": form})
