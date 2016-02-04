from django.contrib import admin
from django.db import transaction
from django import forms

from .models import StarInfo, GroupInfo

# Register your models here.
class StarInfoForm(forms.ModelForm):
    intro = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = StarInfo
        fields = '__all__'

class StarInfoAdmin(admin.ModelAdmin):
    form = StarInfoForm

    list_per_page = 25
    list_display = ['name', 'avatar_preview',  'intro']

    def get_actions(self, request):
        return None



class GroupInfoAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ['id', 'title', 'qr_preview', 'status']

    fieldsets = ((None, {'fields': ('title', 'qrPic', 'status')}),)
    readonly_fields = ['status']
    list_filter = ['status']
    ordering = ['id']

    actions = ['switch_group']

    def get_actions(self, request):
        actions = super(GroupInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    @transaction.atomic
    def switch_group(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, '请选择一个微信群')
            return

        GroupInfo.objects.filter(status=GroupInfo.STATUS_USE).update(status=GroupInfo.STATUS_FULL)

        group = queryset.all()[0]
        group.status = GroupInfo.STATUS_USE
        group.save()

        self.message_user(request, '切换成功!')

    switch_group.short_description = u'将选中的群切换为使用中'


admin.site.register(StarInfo, StarInfoAdmin)
admin.site.register(GroupInfo, GroupInfoAdmin)
