from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def query_qr(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/game/')

    choice = request.POST.get('choice', 'yes').strip()
    name = request.POST.get('name', '').strip()
    user_name = request.POST.get('username', '').strip()

    choice_type = GroupInfo.CHOICE_YES if choice == 'yes' else GroupInfo.CHOICE_NO

    group_objs = GroupInfo.objects.filter(status=GroupInfo.STATUS_USE)\
                                  .filter(choice=choice_type).all()[:1]
    if not group_objs:
        return HttpResponse(json.dumps({'success': False, 'result': 'There is no inuse group!'}),
                            content_type='application/json')

    qr = group_objs[0].qrPic.name
    template = 'game/qrYes.html' if choice == 'yes' else 'game/qrNo.html'
    return render_to_response(template, {'qr': qr, 'name': name, 'user_name': user_name},
                              context_instance=RequestContext(request)
                              )

