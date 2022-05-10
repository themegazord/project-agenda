from unicodedata import category

from django.db import models
from django.utils import timezone

"""    CONTATOS
    id: INT (automático)
    nome: STR * (obrigatório)
    sobrenome: STR (opcional)
    telefone: STR * (obrigatório)
    email: STR (opcional)
    data_criacao: DATETIME (automático)
    descricao: texto
    categoria: CATEGORIA (outro model)

    CATEGORIA
    id: INT
    nome: STR * (obrigatório)"""
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
