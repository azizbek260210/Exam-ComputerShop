from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.SellProduct)
admin.site.register(models.EnterProduct)
admin.site.register(models.Refund)
