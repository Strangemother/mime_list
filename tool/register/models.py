from django.db import models
from trim.models import fields


class Type(models.Model):
    name = fields.chars(100)

    def __str__(self):
        return self.name


class MediaType(models.Model):

    name = fields.chars(100)
    type = fields.fk(Type, nil=True)
    template = fields.chars(200)
    reference = fields.chars(200)

    created, updated = fields.dt_cu_pair()

    def __str__(self):
        return f"{self.name} - {self.template}"
