from django.db import models
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)

class StarInfo(models.Model):
    ROLE_ALL = 0
    ROLE_MALE = 1
    ROLE_FEMALE = 2
    _ROLE_ENUM = {ROLE_MALE: "男偶像", ROLE_FEMALE: "女偶像", ROLE_ALL: "男女偶像"}

    name = models.CharField(max_length=64, verbose_name="姓名")
    intro = models.CharField(max_length=1024, verbose_name="介绍", default="")
    avatar = models.ImageField(max_length=256, verbose_name="头像", upload_to=PathAndRename('avatar'))
    role = models.PositiveIntegerField(default=ROLE_ALL, choices=_ROLE_ENUM.items(), verbose_name="偶像类型")

    class Meta:
        app_label = "game"
        verbose_name = "明星"
        verbose_name_plural = "明星"

    def avatar_preview(self):
        if self.avatar.name != "":
            img_src = "/media/{}".format(self.avatar.name)
            return '<a target=_blank href="{0}"/><img height="68" src="{0}"/></a>'.format(img_src)
        return ''
    avatar_preview.allow_tags = True
    avatar_preview.short_description = u"头像"


class GroupInfo(models.Model):
    STATUS_NEW = 0
    STATUS_USE = 1
    STATUS_FULL = 2
    _STATUS_ENUM = {STATUS_NEW: "未使用", STATUS_USE: "使用中", STATUS_FULL: "人员已满"}

    title = models.CharField(max_length=64, verbose_name="群名称")
    qrPic = models.ImageField(max_length=256, verbose_name="群二维码", upload_to=PathAndRename('qrPic'))
    status = models.PositiveIntegerField(default=STATUS_NEW, choices=_STATUS_ENUM.items(), verbose_name="群状态")
    class Meta:
        app_label = "game"
        verbose_name = "微信群"
        verbose_name_plural = "微信群"

    def qr_preview(self):
        if self.qrPic.name != "":
            img_src = "/media/{}".format(self.qrPic.name)
            return u'<a target=_blank href="{0}"/><img height="68" src="{0}"/></a>'.format(img_src)
        return ''
    qr_preview.allow_tags = True
    qr_preview.short_description = u"二维码"
