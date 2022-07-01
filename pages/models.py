from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from django.contrib.sites.models import Site
from phonenumber_field.modelfields import PhoneNumberField


class Project(models.Model):
    identity = models.CharField(max_length=10, unique=True, verbose_name=_('Ідентифікатор'))
    name = models.CharField(max_length=100, verbose_name=_('Найменування'))
    name_en = models.CharField(max_length=100, verbose_name=_('Найменування (англ.)'), blank=True, default='')
    disabled = models.BooleanField(verbose_name=_('Відключено'), blank=True, default=False)
    cryptoURL = models.URLField(verbose_name=_("Адреса платіжної системи для 'crypto'"), blank=True, null=True, default=None)
    cardURL = models.URLField(verbose_name=_("Адреса платіжної системи для 'credit-card'"), blank=True, null=True, default=None)

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
    name = models.CharField(max_length=60, verbose_name=_("Найменування"))
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


class ConsituentsDocs(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Найменування'))
    name_en = models.CharField(max_length=100, verbose_name=_('Найменування (англ.)'), blank=True, default='')
    file = models.FileField(upload_to='consituents_docs', verbose_name=_('Файл'))
    type = models.CharField(
        max_length=3,
        verbose_name=_("Тип файлу"),
        choices=(('pdf', 'pdf'),)
    )

    @property
    def title(self):
        lg = get_language()
        localized_title = getattr(self, f'name_{lg}', self.name)
        return localized_title if localized_title else self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Установчий документ")
        verbose_name_plural = _("Установчи документи")
        ordering = ('id',)


class Addresses(models.Model):
    site = models.OneToOneField(Site, on_delete=models.PROTECT, verbose_name=_('Сайт'))
    addr = models.TextField(verbose_name=_('Адреса'), blank=True, null=True, default=None)
    phone = PhoneNumberField(verbose_name=_('Телефон'), blank=True, null=True, default=None)
    facebook = models.URLField(verbose_name='Facebook', blank=True, null=True, default=None)
    instagram = models.URLField(verbose_name='Instagram', blank=True, null=True, default=None)
    telegram = models.URLField(verbose_name='Telegram', blank=True, null=True, default=None)
    email = models.EmailField(verbose_name='Email', blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.site}'

    class Meta:
        verbose_name = _("Адреса компанії")
        verbose_name_plural = _("Адреси компанії")
        ordering = ('id',)

