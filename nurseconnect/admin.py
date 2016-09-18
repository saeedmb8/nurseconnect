from wagtailmodeladmin.options import ModelAdminGroup


class YourWordsModelAdminGroup(ModelAdminGroup):
    menu_label = 'Yourwords'
    menu_icon = 'edit'
    menu_order = 300
    # items = (MoloCommentsModelAdmin, MoloCannedResponsesModelAdmin)
