from molo.yourwords.admin import (
    YourWordsCompetitionAdmin, YourWordsCompetitionEntryAdmin)
from molo.yourwords.models import (
    YourWordsCompetition, YourWordsCompetitionEntry)
from wagtailmodeladmin.options import ModelAdminGroup
from wagtailmodeladmin.options import ModelAdmin as WagtailModelAdmin


class MoloYourWordsCompetitionModelAdmin(
        WagtailModelAdmin, YourWordsCompetitionAdmin):

    model = YourWordsCompetition

    list_display = ('entries', 'start_date', 'end_date', 'status',
                    'number_of_entries')
    list_filter = ('title', 'start_date', 'end_date')
    search_fields = ('title', 'content', 'description')


class MoloYourWordsCompetitionEntryModelAdmin(
        WagtailModelAdmin, YourWordsCompetitionEntryAdmin):

    model = YourWordsCompetitionEntry
    list_display = ('story_name', 'truncate_text', 'user', 'hide_real_name',
                    'submission_date', 'is_read', 'is_shortlisted',
                    'is_winner', '_convert')


class YourWordsModelAdminGroup(ModelAdminGroup):
    menu_label = 'Your Words'
    menu_icon = 'edit'
    menu_order = 300
    items = (MoloYourWordsCompetitionModelAdmin,
             MoloYourWordsCompetitionEntryModelAdmin)
