from django.contrib import admin

from pages.models import Project, BankTransferInfo

admin.site.register(Project, admin.ModelAdmin)
admin.site.register(BankTransferInfo, admin.ModelAdmin)
