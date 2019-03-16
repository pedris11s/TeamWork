from django.conf.urls import url
from . import views

urlpatterns = [
    

    url(r'^$', views.index, name='index'),

    url(r'^asignaturas/$', views.MostrarAsignaturas, name='MostrarAsignaturas'),
    url(r'^asignaturas/add/$', views.AdicionarAsignatura, name='AdicionarAsignatura'),
    url(r'^asignaturas/delete/(?P<asigID>[0-9]+)$', views.EliminarAsignatura, name='EliminarAsignatura'),
    url(r'^asignaturas/view/(?P<asigID>[0-9]+)$', views.VistaEditarAsignatura, name='VistaEditarAsignatura'),
    url(r'^asignaturas/edit/(?P<asigID>[0-9]+)$', views.EditarAsignatura, name='EditarAsignatura'),

    url(r'^estudiantes/$', views.MostrarEstudiantes, name='MostrarEstudiantes'),
    url(r'^estudiantes/add/$', views.AdicionarEstudiante, name='AdicionarEstudiante'),
    url(r'^estudiantes/delete/(?P<estID>[0-9]+)$', views.EliminarEstudiante, name='EliminarEstudiante'),
    url(r'^estudiantes/view/(?P<estID>[0-9]+)$', views.VistaEditarEstudiante, name='VistaEditarEstudiante'),
    url(r'^estudiantes/edit/(?P<estID>[0-9]+)$', views.EditarEstudiante, name='EditarEstudiante'),


    url(r'^registrar/$', views.VistaRegistrarEstudiante, name='VistaRegistrarEstudiantes'),
    url(r'^registrar/done/$', views.RegistrarEstudiante, name='RegistrarEstudiantes'),

    url(r'^tareas/$', views.MostrarTareas, name='MostrarTareas'),
    #url(r'^tareas/add/$', views.AdicionarTarea, name=''),
    url(r'^tareas/delete/(?P<tareaID>[0-9]+)$', views.EliminarTareaVistaTarea, name='EliminarTareaVistaTarea'),
    url(r'^tareas/view/(?P<tareaID>[0-9]+)$', views.VerTarea, name='VerTarea'),

    url(r'^tareas/edit/done/(?P<tareaID>[0-9]+)$', views.EditarTarea, name='EditarTarea'),
    url(r'^tareas/do/(?P<tareaID>[0-9]+)$', views.VistaRealizarTarea, name='VistaRealizarTarea'),
    url(r'^tareas/do/done/(?P<tareaID>[0-9]+)$', views.RealizarTarea, name='RealizarTarea'),
    url(r'^tareas/do/done/pend/(?P<tareaID>[0-9]+)$', views.TareaHechoEstudiante, name='TareaHechoEstudiante'),
    url(r'^tareas/do/done/modif/(?P<tareaID>[0-9]+)$', views.TareaModificarEstudiante, name='TareaModificarEstudiante'),


    url(r'^equipos/$', views.MostrarEquipos, name='MostrarEquipos'),
    url(r'^equipos/add$', views.AdicionarEquipo, name='AdicionarEquipo'),
    url(r'^equipos/delete/(?P<equipoID>[0-9]+)$', views.EliminarEquipo, name='EliminarEquipo'),
    url(r'^equipos/view/(?P<equipoID>[0-9]+)$', views.VerEquipo, name='VerEquipo'),

    url(r'^equipos/view/(?P<equipoID>[0-9]+)/comentar$', views.Comentar, name='Comentar'),

    url(r'^equipos/view/(?P<equipoID>[0-9]+)/exportar$', views.pdf_view, name='pdf_view'),

    url(r'^equipos/view/(?P<equipoID>[0-9]+)/tarea/aprobar/(?P<tareaID>[0-9]+)$', views.AprobarTareaJefe, name='AprobarTareaJefe'),
    url(r'^equipos/view/(?P<equipoID>[0-9]+)/tarea/anular/(?P<tareaID>[0-9]+)$', views.AnularTareaJefe, name='AnularTareaJefe'),
    url(r'^equipos/view/(?P<equipoID>[0-9]+)/tarea/delete/(?P<tareaID>[0-9]+)$', views.EliminarTareaVistaVerEquipo, name='EliminarTareaVistaVerEquipo'),

    url(r'^equipos/view/asignar/(?P<equipoID>[0-9]+)$', views.VistaAdicionarTarea, name='VistaAdicionarTarea'),
    url(r'^equipos/view/asignar/(?P<equipoID>[0-9]+)/done/$', views.AdicionarTarea, name='AdicionarTarea'),

    url(r'^equipos/edit/(?P<equipoID>[0-9]+)$', views.VistaEditarEquipo, name='VistaEditarEquipo'),
    url(r'^equipos/edit/(?P<equipoID>[0-9]+)/addest/(?P<estID>[0-9]+)$', views.AdicionarIntegranteEquipo, name='AdicionarIntegranteEquipo'),
    url(r'^equipos/edit/(?P<equipoID>[0-9]+)/delest/(?P<estID>[0-9]+)$', views.EliminarIntegranteEquipo, name='EliminarIntegranteEquipo'),
    url(r'^equipos/edit/done/(?P<equipoID>[0-9]+)$', views.EditarEquipo, name='EditarEquipo'),

    url(r'^perfil/(?P<userID>[0-9]+)$', views.MostrarPerfil, name='MostrarPerfil'),
    url(r'^perfil/(?P<userID>[0-9]+)/editarperfil$', views.EditarPerfil, name='EditarPerfil'),

    url(r'^login/$', views.IngresarPagina, name='IngresarPagina'),
    url(r'^login_done/$', views.Login, name='Login'),

    url(r'^logout/$', views.Logout, name='Logout'),
]
app_name = 'teamwork'

