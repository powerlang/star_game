from django.shortcuts import render
from django.http import HttpResponse
import json
import random

from .models import StarInfo, GroupInfo

# Create your views here.

def query_star(request):
    name = request.GET.get('name', '').strip()
    star_count = StarInfo.objects.count()
    if star_count < 1:
        return HttpResponse(json.dumps({'success': False, 'result': 'There is no star!'}),
                            content_type='application/json')

    random_idx = abs(hash(name)) % star_count
    star_obj = StarInfo.objects.all()[random_idx]

    group_objs = GroupInfo.objects.filter(status=GroupInfo.STATUS_USE).all()
    if not group_objs:
        return HttpResponse(json.dumps({'success': False, 'result': 'There is no inuse group!'}),
                            content_type='application/json')

    star = {'name': star_obj.name, 'intro': star_obj.intro, 'avatar': star_obj.avatar.name}
    result = {'star': star, 'qr': group_objs[0].qrPic.name}
    return HttpResponse(json.dumps({'sucess': True, 'result': result}),
                        content_type='application/json')
