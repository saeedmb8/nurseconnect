from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from nurseconnect import constants
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class NurseConnectUserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="nurse_connect_profile",
        primary_key=True
    )
    gender = models.CharField(
        max_length=1,
        choices=constants.SEX,
        blank=True,
        null=True
    )
    staff_number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    facility_code = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )


@receiver(post_save, sender=User)
def nurse_connect_user_profile_handler(sender, instance, created, **kwargs):
    if created:
        profile = NurseConnectUserProfile(user=instance)
        profile.save()


@register_setting
class NurseConnectSettings(BaseSetting):
    banned_keywords_and_patterns = models.TextField(
        verbose_name="Banned Keywords and Patterns",
        null=True,
        blank=True,
        help_text="Banned keywords and patterns for comments, separated by a"
                  " line a break. Use only lowercase letters for keywords."
    )
    panels = [
        FieldPanel("banned_keywords_and_patterns")
    ]
