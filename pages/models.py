from django.db import models
from django.utils.translation import gettext_lazy as _, get_language


class Project(models.Model):
    identity = models.CharField(max_length=10, unique=True, verbose_name=_('Ідентифікатор'))
    name = models.CharField(max_length=100, verbose_name=_('Найменування'))
    name_en = models.CharField(max_length=100, verbose_name=_('Найменування (англ.)'), blank=True, default='')

    @property
    def title(self):
        lg = get_language()
        localized_title = getattr(self, f'name_{lg}', self.name)
        return localized_title if localized_title else self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекти")
        ordering = ('id',)


class BankTransferInfo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=_("Проект"), related_name='transfers')
    bank = models.CharField(max_length=100, verbose_name=_("Банк"))
    mfo = models.CharField(max_length=6, verbose_name=_("МФО"))
    account = models.CharField(max_length=29, verbose_name=_("Рахунок"))
    edrpou = models.CharField(max_length=10, verbose_name=_("Код за ЄДРПОУ"))
    payee = models.CharField(max_length=100, verbose_name=_("Отримувач"))

    def __str__(self):
        return f'{self.payee} ({self.project})'

    class Meta:
        verbose_name = _("Реквізит банківського переводу")
        verbose_name_plural = _("Реквізити банківського переводу")
        ordering = ('id',)
