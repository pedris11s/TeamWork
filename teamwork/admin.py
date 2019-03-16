from django.contrib import admin
from .models import Estudiante, Equipo, Tarea, Asignatura, Notificacion, Mensaje, Visita

# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Equipo)
admin.site.register(Tarea)
admin.site.register(Asignatura)
admin.site.register(Notificacion)
admin.site.register(Mensaje)
admin.site.register(Visita)
