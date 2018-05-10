from django.shortcuts import render, get_object_or_404

from . import models


def classroom_list(request):
    ctx = {'classrooms': models.Classroom.objects.all()}
    return render(request, 'classrooms/classroom-list.jinja2', ctx)


def classroom_detail(request, slug):
    ctx = {'classroom': get_object_or_404(models.Classroom, slug=slug)}
    return render(request, 'classrooms/classroom-detail.jinja2', ctx)


def classroom_enroll(request, slug):
    ctx = {'classroom': get_object_or_404(models.Classroom, slug=slug)}
    return render(request, 'classrooms/classroom-enroll.jinja2', ctx)
