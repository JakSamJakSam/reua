from django.contrib import admin

from pages.models import Project, BankTransferInfo, ConsituentsDocs, Addresses

admin.site.register(Project, admin.ModelAdmin)


class BankTransferInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency', 'project')
    list_filter = ('currency', 'project')

admin.site.register(BankTransferInfo, BankTransferInfoAdmin)

admin.site.register(ConsituentsDocs, admin.ModelAdmin)
admin.site.register(Addresses, admin.ModelAdmin)
