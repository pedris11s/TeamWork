import os
from operator import eq

from django.template.loader import get_template
from django.template.loader import render_to_string
#import pdfkit
#from wkhtmltopdf import *

from django.shortcuts import *
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils.text import unescape_string_literal

from .models import Estudiante, Equipo, Asignatura, Tarea, Notificacion, Mensaje, Visita
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date

#from .ldap_n import LDAP_X


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
INDEX
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def index(request):
    try:
        cantEst = Estudiante.objects.all().count()
        cantEquip = Equipo.objects.all().count()
        cantTareas = Tarea.objects.all().count()
        cantAsig = Asignatura.objects.all().count()

        return render(request, 'teamwork/index.html',
                      {'cantEst': cantEst, 'cantEquip': cantEquip, 'cantTareas': cantTareas, 'cantAsig': cantAsig}
                      )
    except:
        return render(request, 'teamwork/login.html')

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
NOTIFICACIONES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def notificar(descr, est, tipo, llave):
    notify = Notificacion(descripcion=descr, para=est, visto=False, fecha=datetime.now(), tipo=tipo, llave=llave)
    notify.save()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
REGISTRAR ESTUDIANTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def VistaRegistrarEstudiante(request):
    return render(request, 'teamwork/registrar_estudiante.html')


def RegistrarEstudianteFunc(request):
    nombre = request.POST['nombre']
    apellidos = request.POST['apellidos']
    username = request.POST['username']
    password = request.POST['password']
    est = Estudiante(nombre=nombre, apellidos=apellidos, user=username, password=password)
    est.save()

    correo = username + "@estudiantes.uci.cu"
    user = User.objects.create_user(username, correo, password)
    user.first_name = nombre
    user.last_name = apellidos
    user.groups.add(3)
    user.save()


def RegistrarEstudiante(request):
    RegistrarEstudianteFunc(request)
    return HttpResponseRedirect(reverse('teamwork:IngresarPagina'))

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ESTUDIANTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def AdicionarEstudiante(request):
    RegistrarEstudianteFunc(request)
    return HttpResponseRedirect(reverse('teamwork:MostrarEstudiantes'))


def VistaEditarEstudiante(request, estID):
    est = Estudiante.objects.get(pk=estID)
    tareas = Tarea.objects.filter(estudiante=est)
    return render(request, 'teamwork/editar_estudiante.html', {'est': est, 'tareas': tareas})


def EditarEstudiante(request, estID):
    est = Estudiante.objects.get(pk=estID)
    old_user = est.user

    est.nombre = request.POST['nombre']
    est.apellidos = request.POST['apellidos']
    est.user = request.POST['username']
    est.password = request.POST['password']
    est.save()

    correo = est.user + "@estudiantes.uci.cu"
    user = User.objects.get(username=old_user)
    user.username = est.user
    user.email = correo
    user.password = est.password
    user.first_name = est.nombre
    user.last_name = est.apellidos
    user.save()
    return HttpResponseRedirect(reverse('teamwork:VistaEditarEstudiante', kwargs={'estID': estID}))


def MostrarEstudiantes(request):
    est = Estudiante.objects.all()
    return render(request, 'teamwork/mostrar_estudiantes.html', {'est': est})


def EliminarEstudiante(request, estID):
    est = Estudiante.objects.get(pk=estID)
    est.delete()
    user = User.objects.get(username=est.user)
    user.delete()
    return HttpResponseRedirect(reverse('teamwork:MostrarEstudiantes'))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
EQUIPOS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def MostrarEquipos(request):

    user = User.objects.get(pk=request.user.id)
    est = Estudiante.objects.get(user=user.username)

    misequipos = []
    equipos = Equipo.objects.all()

    for e in equipos:
        if est in e.integrantes.all():
            misequipos.append(e)

    estudiantes = Estudiante.objects.exclude(pk=est.pk)
    asig = Asignatura.objects.all()

    return render(request, 'teamwork/mostrar_equipos.html',
                  {'equipos': equipos, 'estudiantes': estudiantes, 'asig': asig, 'misequipos': misequipos}
                  )


def AdicionarEquipo(request):

    nombre = request.POST['nombre']
    user = User.objects.get(pk=request.user.id)
    jefe = Estudiante.objects.get(user=user.username)
    asig = Asignatura.objects.get(pk=request.POST['asig'])
    lista = []
    lista.append(jefe)

    equipo = Equipo(nombre=nombre)
    equipo.jefe = jefe
    equipo.asignatura = asig
    equipo.save()
    equipo.integrantes = lista
    equipo.save()

    return HttpResponseRedirect(reverse("teamwork:MostrarEquipos"))


def EliminarEquipo(request, equipoID):
    equipo = Equipo.objects.get(pk=equipoID)
    equipo.delete()
    return HttpResponseRedirect(reverse("teamwork:MostrarEquipos"))


def AdicionarIntegranteEquipo(request, equipoID, estID):
    equipo = Equipo.objects.get(pk=equipoID)
    est = Estudiante.objects.get(pk=estID)
    equipo.integrantes.add(est)
    equipo.save()

    #notificacion
    descrip = 'Ahora forma parte del equipo ' + equipo.nombre
    notificar(descrip, est, 'add_team', equipo.pk)

    return HttpResponseRedirect(reverse('teamwork:VistaEditarEquipo', kwargs={'equipoID': equipoID}))


def EliminarIntegranteEquipo(request, equipoID, estID):
    equipo = Equipo.objects.get(pk=equipoID)
    est = Estudiante.objects.get(pk=estID)
    equipo.integrantes.remove(est)
    equipo.save()
    tareas = Tarea.objects.filter(equipo=equipo, estudiante=est)
    tareas.delete()

    # notificacion
    descrip = 'Te han eliminado del equipo ' + equipo.nombre
    notificar(descrip, est, 'del_team', equipoID)

    return HttpResponseRedirect(reverse('teamwork:VistaEditarEquipo', kwargs={'equipoID': equipoID}))


def VerEquipo(request, equipoID):
    try:
        user = User.objects.get(pk=request.user.id)
        est = Estudiante.objects.get(user=user.username)
 
        equipo = Equipo.objects.get(pk=equipoID)
        tareas = Tarea.objects.filter(equipo=equipo).order_by('hecho', 'estudiante')
        asig = Asignatura.objects.all()
        estudiantes = Estudiante.objects.all()
        mensajes = Mensaje.objects.filter(tarea__equipo=equipo)

        cant_hecho = 0
        cant_sinhacer = 0
        cant_pend = 0
        for t in tareas:
            if t.hecho == 0:
                cant_sinhacer += 1
            elif t.hecho == 1:
                cant_pend += 1
            else:
                cant_hecho += 1

        total = tareas.count()
        a = 0
        b = 0
        c = 100
        if total != 0:
            a = cant_hecho * 100 / float(total)
            b = cant_pend * 100 / float(total)
            c = 100 - a - b
        return render(request, 'teamwork/ver_equipo.html',{'est': est, 'equipo': equipo, 'asig': asig, 'estudiantes': estudiantes, 'tareas': tareas, 'cant_hecho': cant_hecho, 'cant_pend': cant_pend, 'cant_sinhacer': cant_sinhacer, 'a': a, 'b': b, 'c': c, 'total': total, 'mensajes': mensajes})
    except:
        detalles = 'El equipo no existe.'
        return render(request, 'teamwork/404.html', {'detalles': detalles})

def VistaEditarEquipo(request, equipoID):
    equipo = Equipo.objects.get(pk=equipoID)
    asig = Asignatura.objects.all()
    estudiantes = Estudiante.objects.exclude(pk=equipo.jefe.pk)
    return render(request, 'teamwork/editar_equipo.html', {'equipo': equipo, 'asig': asig, 'estudiantes': estudiantes})


def EditarEquipo(request, equipoID):
    nombre = request.POST['nombre']
    asig = Asignatura.objects.get(pk=request.POST['asig'])

    equipo = Equipo.objects.get(pk=equipoID)
    equipo.nombre = nombre
    equipo.asignatura = asig
    equipo.save()

    return HttpResponseRedirect(reverse("teamwork:VistaEditarEquipo", kwargs={'equipoID': equipoID}))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
TAREAS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def VistaAdicionarTarea(request, equipoID):
    equipo = Equipo.objects.get(pk=equipoID)
    return render(request, 'teamwork/adicionar_tarea.html', {'equipo': equipo})


def VerTarea(request, tareaID):
    try:
        est_log = Estudiante.objects.get(user=User.objects.get(pk=request.user.id).username)
        tarea = Tarea.objects.get(pk=tareaID)

        mensaje_tarea = Mensaje.objects.filter(tarea=tarea.pk)

        return render(request, 'teamwork/ver_tarea.html', {'tarea': tarea, 'est_log': est_log, 'mensaje_tarea': mensaje_tarea})
    except:
        detalles = 'La tarea no existe.'
        return render(request, 'teamwork/404.html', {'detalles': detalles})


def CambiarEstadoTarea(request, tareaID, estado):
    tarea = Tarea.objects.get(pk=tareaID)
    tarea.hecho = estado
    tarea.save()

    # notificacion
    action = ''
    if estado == 2:
        tipo = 'approve_tarea'
        action = ' se ha aprobado.'
    elif estado == 1:
        tipo = 'pending_tarea'
        action = ' esta pendiente de aprobación.'
    else:
        tipo = 'denied_tarea'
        action = ' no fue aprobada.'
    descrip = 'Tu tarea ' + tarea.nombre + ' del equipo ' + tarea.equipo.__str__() + action
    est = tarea.estudiante
    notificar(descrip, est, tipo, tarea.pk)


def TareaHechoEstudiante(request, tareaID):
    CambiarEstadoTarea(request, tareaID, 1)
    return HttpResponseRedirect(reverse('teamwork:VerTarea', kwargs={'tareaID': tareaID}))


def TareaModificarEstudiante(request, tareaID):
    CambiarEstadoTarea(request, tareaID, 0)
    return HttpResponseRedirect(reverse('teamwork:VistaRealizarTarea', kwargs={'tareaID':tareaID}))


def AprobarTareaJefe(request, tareaID, equipoID):
    CambiarEstadoTarea(request, tareaID, 2)
    return HttpResponseRedirect(reverse('teamwork:VerTarea', kwargs={'tareaID':tareaID}))


def AnularTareaJefe(request, tareaID, equipoID):
    CambiarEstadoTarea(request, tareaID, 0)
    return HttpResponseRedirect(reverse('teamwork:VerTarea', kwargs={'tareaID':tareaID}))

def MostrarTareas(request):

    user = User.objects.get(pk=request.user.id)
    est = Estudiante.objects.get(user=user.username)

    misequipos = []
    equipos = Equipo.objects.all()
    for e in equipos:
        for i in e.integrantes.all():
            if i.pk == est.pk:
                misequipos.append(e)
                break

    mistareas = Tarea.objects.filter(estudiante=est).order_by('equipo', 'hecho')
    tareas = Tarea.objects.exclude(estudiante=est).filter(equipo__in=misequipos)


    #adicionar tarea
    estudiantes = Estudiante.objects.all()
    equipos = Equipo.objects.all()
    ##
    return render(request, 'teamwork/mostrar_tareas.html',
                  {'tareas': tareas, 'estudiantes': estudiantes, 'equipos': equipos, 'mistareas': mistareas}
                  )

def RealizarTarea(request, tareaID):
    cad = request.POST['texto']
    tarea = Tarea.objects.get(pk=tareaID)
    tarea.respuesta = cad
    tarea.save()
    return HttpResponseRedirect(reverse('teamwork:VerTarea', kwargs={'tareaID': tareaID}))


def VistaRealizarTarea(request, tareaID):
    tarea = Tarea.objects.get(pk=tareaID)
    if tarea.hecho == 0:
        editar = ''
    else:
        editar = 'disabled'

    return render(request, 'teamwork/realizar_tarea.html', {'tarea': tarea, 'editar': editar})


def AdicionarTarea(request, equipoID):
    nombre = request.POST['nombre']
    desc = request.POST['descripcion']
    equip = Equipo.objects.get(pk=equipoID)
    p = request.POST['estudiante']
    arr = p.split(maxsplit=1)
    pers = Estudiante.objects.get(nombre=arr[0], apellidos=arr[1])
    est = Estudiante.objects.get(pk=pers.pk)
    t = Tarea(nombre=nombre, descripcion=desc, estudiante=est, equipo=equip, hecho=False)
    t.save()

    #notificacion
    descrip = 'Tienes una nueva tarea en el equipo ' + equip.nombre
    notificar(descrip, est, 'add_tarea', t.pk)

    return HttpResponseRedirect(reverse('teamwork:VerEquipo', kwargs={'equipoID': equipoID}))

def EliminarTarea(request, tareaID):
    t = Tarea.objects.get(pk=tareaID)
    t.delete()


def EliminarTareaVistaTarea(request, tareaID):
    EliminarTarea(request, tareaID)
    return HttpResponseRedirect(reverse('teamwork:MostrarTareas'))


def EliminarTareaVistaVerEquipo(request, tareaID, equipoID):
    EliminarTarea(request, tareaID)
    return HttpResponseRedirect(reverse('teamwork:VerEquipo', kwargs={'equipoID': equipoID}))


def EditarTarea(request, tareaID):
    nombre = request.POST['nombre']
    desc = request.POST['descripcion']
    p = request.POST['estudiante']
    arr = p.split(maxsplit=1)
    pers = Estudiante.objects.get(nombre=arr[0], apellidos=arr[1])
    est = Estudiante.objects.get(pk=pers.pk)
    t = Tarea.objects.get(pk=tareaID)
    t.nombre = nombre
    t.descripcion = desc
    t.estudiante = est
    t.save()
    return HttpResponseRedirect(reverse('teamwork:VerTarea', kwargs={'tareaID': tareaID}))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ASIGNATURAS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def MostrarAsignaturas(request):
    asig = Asignatura.objects.all()
    return render(request, 'teamwork/mostrar_asignaturas.html', {'asig': asig})


def AdicionarAsignatura(request):
    nombre = request.POST['nombre_asig']
    a = Asignatura(nombre=nombre)
    a.save()
    return HttpResponseRedirect(reverse('teamwork:MostrarAsignaturas'))


def EliminarAsignatura(request, asigID):
    a = Asignatura.objects.get(pk=asigID)
    a.delete()
    return HttpResponseRedirect(reverse('teamwork:MostrarAsignaturas'))


def VistaEditarAsignatura(request, asigID):
    asig = Asignatura.objects.get(pk=asigID)
    equipos = Equipo.objects.filter(asignatura=asig)

    tareas = Tarea.objects.filter(equipo__in=equipos)
    return render(request, 'teamwork/editar_asignatura.html', {'asig': asig, 'equipos': equipos, 'tareas': tareas})


def EditarAsignatura(request, asigID):
    asig = Asignatura.objects.get(pk=asigID)
    nombre = request.POST['nombre_asig']
    asig.nombre = nombre
    asig.save()
    return HttpResponseRedirect(reverse('teamwork:VistaEditarAsignatura', kwargs={'asigID': asigID}))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LOGIN Y LOGOUT
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def IngresarPagina(request):
    return render(request, 'teamwork/login.html')


def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        cantEst = Estudiante.objects.all().count()
        cantEquip = Equipo.objects.all().count()
        cantTareas = Tarea.objects.all().count()
        cantAsig = Asignatura.objects.all().count()

        return render(request, 'teamwork/index.html',
                  {'cantEst': cantEst, 'cantEquip': cantEquip, 'cantTareas': cantTareas, 'cantAsig': cantAsig}
                  )
    else:
        return render(request, 'teamwork/login_error.html')


def Logout(request):
    logout(request)
    return render(request, 'teamwork/login.html')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
EXPORTAR PDF
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def pdf_view(request, equipoID):
    tema = request.POST['nombre']
    path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    template = get_template("teamwork/pdf.html")

    equipo = Equipo.objects.all().get(pk=equipoID)
    answer = Tarea.objects.all().filter(equipo=equipo)

    list = []
    for e in equipo.integrantes.all():
        list.append(e.nombre + " " + e.apellidos)

    html = template.render({'equipo': equipo, 'answer': answer, 'tema': tema, 'list': list}) # Renders the template with the context data.
    pdfkit.from_string(html, 'out.pdf', configuration=config)

    pdf = open("out.pdf", 'rb')
    response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
    response['Content-Disposition'] = 'attachment; filename=output.pdf'
    pdf.close()
    os.remove("out.pdf")  # remove the locally created pdf file.
    return response
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PERFIL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@login_required
def MostrarPerfil(request, userID):
    try:
        est = Estudiante.objects.get(pk=userID)
    except:
        detalles = 'El estudiante no existe.'
        return render(request, 'teamwork/404.html', {'detalles': detalles})

    total_teams_jefe = Equipo.objects.filter(jefe=est).count()

    mistareas = Tarea.objects.filter(estudiante=est)
    total_tareas = mistareas.count()
    total_tareas_hechas = mistareas.filter(hecho=2).count()

    total_misequipos = 0
    equipos_perfil = []
    equipos = Equipo.objects.all()
    for e in equipos:
        if est in e.integrantes.all():
            total_misequipos += 1
            tarhechas = Tarea.objects.filter(equipo=e, hecho=2).count()
            tartotal = Tarea.objects.filter(equipo=e).count()
            val = 0
            if tartotal != 0:
                val = tarhechas * 100 / float(tartotal)
            if val >= 65:
                color = 'success'
            elif val >= 30 and val < 65:
                color = 'warning'
            else:
                color = 'danger'
            equipos_perfil.append([e, val, color, tarhechas, tartotal - tarhechas])

    notificaciones_nuevas = Notificacion.objects.filter(para=est, visto=False).order_by('-fecha')

    notificaciones_viejas = []
    notificaciones_all = Notificacion.objects.all().order_by('-fecha')
    for n in notificaciones_all:
        if n not in notificaciones_nuevas.all() and n.para==est:
            notificaciones_viejas.append(n)

    for n in notificaciones_nuevas:
        n.visto = True
        n.save()

    return render(request, 'teamwork/perfil.html',
                  {'equipos_perfil': equipos_perfil, 'total_misequipos': total_misequipos, 'notificaciones_nuevas': notificaciones_nuevas,'notificaciones_viejas': notificaciones_viejas, 'total_tareas':total_tareas, 'total_tareas_hechas': total_tareas_hechas, 'total_teams_jefe': total_teams_jefe, 'usuario': est }
                  )


def EditarPerfil(request, userID):
    correo = request.POST['email']
    password = request.POST["password"]

    a = Estudiante.objects.get(pk=userID)
    a.password = password
    a.save()
    a = User.objects.get(username=a.user)
    a.email = correo
    a.save()

    return HttpResponseRedirect(reverse('teamwork:MostrarPerfil', kwargs={'userID': userID}))


def Comentar(request, equipoID):
    user = User.objects.get(pk=request.user.id)

    de = Estudiante.objects.get(user=user.username)
    texto = request.POST['texto']
    tarea = Tarea.objects.get(pk=request.POST['tarea'])
    fecha = datetime.now()

    a = Mensaje(de=de, texto=texto, tarea=tarea, fecha=fecha)
    a.save()

    descrip = de.nombre + ' ha comentado la tarea ' + tarea.nombre + ' del equipo ' + tarea.equipo.nombre

    estudianteseq = Equipo.objects.get(pk=equipoID)
    for est in estudianteseq.integrantes.all():
        if est != de:
            notificar(descrip, est, 'new_mesage', tarea.equipo.pk)

    return HttpResponseRedirect(reverse('teamwork:VerEquipo', kwargs={'equipoID': equipoID}))

