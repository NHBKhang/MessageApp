from django.contrib import admin
from core.forms import PublicKeyForm
from core.models import PublicKey


class PublicKeyAdmin(admin.ModelAdmin):
    form = PublicKeyForm
    readonly_fields = ('key', 'user')


admin.site.register(PublicKey, PublicKeyAdmin)
