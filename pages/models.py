from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from django.contrib.sites.models import Site
from phonenumber_field.modelfields import PhoneNumberField

from pages.enums import Currency, ConsituentsDocsKinds


class Project(models.Model):
    identity = models.CharField(max_length=10, unique=True, verbose_name=_('Ідентифікатор'))
    name = models.CharField(max_length=100, verbose_name=_('Найменування'))
    name_en = models.CharField(max_length=100, verbose_name=_('Найменування (англ.)'), blank=True, default='')
    disabled = models.BooleanField(verbose_name=_('Відключено'), blank=True, default=False)
    cryptoURL = models.URLField(verbose_name=_("Адреса платіжної системи для 'crypto'"), blank=True, null=True, default=None)
    cardURL = models.URLField(verbose_name=_("Адреса платіжної системи для 'credit-card'"), blank=True, null=True, default=None)
    paypalURL = models.URLField(verbose_name=_("Адреса платіжної системи для 'PAYPAL'"), blank=True, null=True, default=None)

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
    bank = models.CharField(max_length=100, verbose_name=_("Банк"), blank=True, null=True, default=None)
    mfo = models.CharField(max_length=6, verbose_name=_("МФО"), blank=True, null=True, default=None)
    account = models.CharField(max_length=29, verbose_name=_("Рахунок"))
    edrpou = models.CharField(max_length=10, verbose_name=_("Код за ЄДРПОУ"), blank=True, null=True, default=None)
    payee = models.CharField(max_length=100, verbose_name=_("Отримувач"))
    purpose = models.TextField(verbose_name=_("Призначення платежу"))
    bic = models.CharField(max_length=100, verbose_name="Beneficiary (SWIFT)", blank=True, null=True, default=None)
    beneficiary_address= models.TextField(verbose_name="Beneficiary address", blank=True, null=True, default=None)
    beneficiary_bank= models.TextField(verbose_name="Beneficiary bank", blank=True, null=True, default=None)
    iban = models.CharField(max_length=29, verbose_name="IBAN", blank=True, null=True, default=None)
    correspondent_bank_name= models.CharField(max_length=100, verbose_name="Correspondent bank name", blank=True, null=True, default=None)
    correspondent_bank_bic= models.CharField(max_length=8, verbose_name="Correspondent bank (SWIFT)", blank=True, null=True, default=None)
    currency = models.CharField(max_length=3, verbose_name=_("Валюта"), choices=((r.value, r.value) for r in Currency))

    @property
    def is_national(self) -> bool:
        return self.currency == Currency.UAH.value

    def __str__(self):
        return f'{self.name} ({self.project})'

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
    order = models.SmallIntegerField(verbose_name = _('Номер за порядком'))
    kind = models.CharField(max_length=10, verbose_name=_('Вид файлу'), null=True, blank=True, default=None,
            choices=((ConsituentsDocsKinds.PUBLIC_OFFER.value, _('Договір публичної оферти')),)
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
        ordering = ('order',)


class Addresses(models.Model):
    site = models.OneToOneField(Site, on_delete=models.PROTECT, verbose_name=_('Сайт'))
    addr = models.TextField(verbose_name=_('Адреса'), blank=True, null=True, default=None)
    addr_en = models.TextField(verbose_name=_('Адреса (англ.)'), blank=True, null=True, default=None)
    phone = PhoneNumberField(verbose_name=_('Телефон'), blank=True, null=True, default=None)
    facebook = models.URLField(verbose_name='Facebook', blank=True, null=True, default=None)
    instagram = models.URLField(verbose_name='Instagram', blank=True, null=True, default=None)
    # telegram = models.URLField(verbose_name='Telegram', blank=True, null=True, default=None)
    twitter = models.URLField(verbose_name='Twitter', blank=True, null=True, default=None)
    email = models.EmailField(verbose_name='Email', blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.site}'

    @property
    def addr_title(self):
        lg = get_language()
        localized_title = getattr(self, f'addr_{lg}', self.addr)
        return localized_title if localized_title else self.addr

    class Meta:
        verbose_name = _("Адреса компанії")
        verbose_name_plural = _("Адреси компанії")
        ordering = ('id',)


class FinancialReport(models.Model):
    uploaded_at = models.DateTimeField(verbose_name=_("Завантажено"), auto_now_add=True, editable=False)
    file = models.FileField(upload_to='reports', verbose_name=_('Звіт'))

    def __str__(self):
        return f'Звіт від {self.uploaded_at.strftime("%c")}'

    class Meta:
        verbose_name = _("Фінансовий звіт")
        verbose_name_plural = _("Фінансові звіти")
        ordering = ('-uploaded_at',)
