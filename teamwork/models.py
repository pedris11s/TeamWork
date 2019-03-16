from email.policy import default

from django.db import models
from datetime import datetime, date

class Estudiante(models.Model):
    nombre = models.CharField(max_length=10)
    apellidos = models.CharField(max_length=20)
    user = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    #avatar = models.ImageField(upload_to='teamwork/static/teamwork/img/avatars', height_field=None, width_field=None)

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Asignatura(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=10)
    jefe = models.ForeignKey(Estudiante, related_name='jefe', on_delete=models.CASCADE)
    integrantes = models.ManyToManyField(Estudiante, related_name='integrantes')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    hecho = models.IntegerField(default=0)
    respuesta = models.TextField(default='')
    
    def __str__(self):
        return self.nombre


class Notificacion(models.Model):
    descripcion = models.CharField(max_length=100)
    para = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    visto = models.BooleanField()
    fecha = models.DateTimeField()
    tipo = models.CharField(default='', max_length=30)
    llave = models.IntegerField(default=0)

    def __str__(self):
        return self.descripcion


class Mensaje(models.Model):
    texto = models.CharField(max_length=80)
    de = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.de.nombre + ': ' + self.texto

class Visita(models.Model):
    dia = models.DateField(default=date.today)
    visitas = models.IntegerField(default=0)