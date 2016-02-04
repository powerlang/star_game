from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import json
import random

from .models import StarInfo, GroupInfo

# Create your views here.

def start_game(request):
    return render_to_response('game/index.html', {},
                              context_instance=RequestContext(request)
                              )


def query_star(request):
    name = request.GET.get('name', '').strip()
    sex = request.GET.get('sex', 'male').strip()

    star_count = StarInfo.objects.count()
    if star_count < 1:
        return HttpResponse(json.dumps({'success': False, 'result': 'There is no star!'}),
                            content_type='application/json')

    random_idx = abs(hash(name)) % star_count
    if sex == 'male':
        query = StarInfo.objects.filter(role__in=[StarInfo.ROLE_ALL, StarInfo.ROLE_MALE])
    else:
        query = StarInfo.objects.filter(role__in=[StarInfo.ROLE_ALL, StarInfo.ROLE_MALE])

    star_obj = query.all()[random_idx]

    star = {'name': star_obj.name, 'intro': star_obj.intro, 'avatar': star_obj.avatar.name, 'username': name}

    return render_to_response('game/result.html', star,
                              context_instance=RequestContext(request)
                              )

def query_qr(request):
    choice = request.GET.get('choice', 'yes').strip()
    name = request.GET.get('name', '').strip()
    user_name = request.GET.get('username', '').strip()

    group_objs = GroupInfo.objects.filter(status=GroupInfo.STATUS_USE).order_by("-pk").all()[:2]
    if not group_objs:
        return HttpResponse(json.dumps({'success': False, 'result': 'There is no inuse group!'}),
                            content_type='application/json')

    group_objs = [obj for obj in group_objs]
    qr_index = 0 if choice == 'yes' else -1
    qr = group_objs[qr_index].qrPic.name
    template = 'game/qrYes.html' if choice == 'yes' else 'game/qrNo.html'
    return render_to_response(template, {'qr': qr, 'name': name, 'user_name': user_name},
                              context_instance=RequestContext(request)
                              )

