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
    response = render_to_response('game/index.html', {},
                                  context_instance=RequestContext(request)
                                  )
    response.delete_cookie('star')
    return response


@csrf_exempt
def query_star(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/game/')

    name = request.POST.get('name', '').strip()
    sex = request.POST.get('sex', 'male').strip()

    if request.COOKIES.get('star', None):
        star_id = request.COOKIES['star']
        star_obj = StarInfo.objects.get(id=star_id)
    else:
        if sex == 'male':
            query = StarInfo.objects.filter(role__in=[StarInfo.ROLE_ALL, StarInfo.ROLE_MALE])
        else:
            query = StarInfo.objects.filter(role__in=[StarInfo.ROLE_ALL, StarInfo.ROLE_FEMALE])

        star_count = query.count()
        if star_count < 1:
            return HttpResponse(json.dumps({'success': False, 'result': 'There is no star!'}),
                                content_type='application/json')

        random_idx = random.randint(0, star_count-1)
        star_obj = query.all()[random_idx]

    star = {'name': star_obj.name, 'intro': star_obj.intro, 'avatar': star_obj.avatar.name, 'username': name}

    response = render_to_response('game/result.html', star,
                                  context_instance=RequestContext(request)
                                  )
    response.set_cookie('star', star_obj.id)
    return response

@csrf_exempt
def query_qr(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/game/')

    choice = request.POST.get('choice', 'yes').strip()
    name = request.POST.get('name', '').strip()
    user_name = request.POST.get('username', '').strip()

    group_objs = GroupInfo.objects.filter(status=GroupInfo.STATUS_USE)\
                                  .all()[:1]
    if not group_objs:
        return HttpResponse(json.dumps({'success': False, 'result': 'There is no inuse group!'}),
                            content_type='application/json')

    qr = group_objs[0].qrPic.name
    template = 'game/qrYes.html' if choice == 'yes' else 'game/qrNo.html'
    return render_to_response(template, {'qr': qr, 'name': name, 'user_name': user_name},
                              context_instance=RequestContext(request)
                              )

