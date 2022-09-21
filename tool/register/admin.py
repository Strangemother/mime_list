from django.contrib import admin
from trim import admin as trims
from . import models



@trims.register(models.MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'type',
            'template',
            'reference',
        )

trims.register_models(models, ignore=__name__)
