from django.contrib import admin
from django.contrib.auth.models import User
from molo.profiles.admin import ProfileUserAdmin
from nurseconnect.models import NurseConnectUserProfile


class NurseConnectUserProfileInLineModelAdmin(admin.StackedInline):
    model = NurseConnectUserProfile
    can_delete = False


class NurseConnectUserAdmin(ProfileUserAdmin):
    inlines = (NurseConnectUserProfileInLineModelAdmin,)
    list_display = ProfileUserAdmin.list_display + ("gender",)

    def gender(self, obj):
        return obj.nurse_connect_profile.get_gender_display()


admin.site.unregister(User)
admin.site.register(User, NurseConnectUserAdmin)
