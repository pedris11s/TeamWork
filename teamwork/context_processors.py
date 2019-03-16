from django.shortcuts import render

from .models import Estudiante, Equipo, Asignatura, Tarea, Notificacion, Visita
from django.contrib.auth.models import *
from datetime import date


def mis_variables(request):
    try:
        user = User.objects.get(pk=request.user.id)
        est = Estudiante.objects.get(user=user.username)
        equipos = Equipo.objects.all()
        notifi = Notificacion.objects.filter(para=est).order_by('-fecha')
        misequiposbarra = []
        total_teams = 0
        for e in equipos:
            if est in e.integrantes.all():
                tarhechas = Tarea.objects.filter(equipo=e, hecho=2).count()
                tartotal = Tarea.objects.filter(equipo=e).count()
                total_teams += 1
                val = 0
                if tartotal != 0:
                    val = tarhechas * 100 / float(tartotal)
                if val >= 65:
                    color = 'success'
                elif val >= 30 and val < 65:
                    color = 'warning'
                else:
                    color = 'danger'
                misequiposbarra.append([e, val, color, tarhechas, tartotal - tarhechas])

        news = notifi.filter(visto=False)
        notificaciones5 = news[:5]
        total_notifi = news.count()

        usermail = user.email


        return {'usermail': usermail, 'usuario_log': est, 'notificaciones5': notificaciones5,
                'total_notifi': total_notifi, 'total_teams': total_teams, 'misequiposbarra': misequiposbarra}
    except:
        return {}





