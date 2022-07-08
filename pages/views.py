import logging
import uuid
from functools import reduce

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, RedirectView
from django.utils.translation import gettext_lazy as _, get_language
from liqpay import LiqPay

from pages.enums import ConsituentsDocsKinds
from pages.forms import PaymentForm
from pages.models import Project, ConsituentsDocs, Addresses, BankTransferInfo, FinancialReport


def get_projects_data():
    projects = [{
        'identity': p.identity,
        'title': p.title,
        'disabled': p.disabled,
        'cryptoURL': p.cryptoURL,
        'cardURL': p.cardURL,
        'bank_accounts': p.transfers.exists(),
    } for p in Project.objects.all()]  # TODO Cashe it
    return projects

def get_trasnfers():
    transfres = BankTransferInfo.objects.all().prefetch_related('project')
    keys = set((t.currency, t.project.identity) for t in transfres)
    result = [
        {
            'id': f'{currency}-{project_identity}',
            'currency': currency,
            'project_identity': project_identity,
            'items': [t for t in transfres if t.currency == currency and t.project.identity == project_identity],
        } for currency, project_identity in keys
    ]

    return result

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_payment_initial(self):
        return {
            'amount': 100,
            'currency': 'USD'
        }

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        cdocs = ConsituentsDocs.objects.all()  # TODO Cashe it

        ctx['consituents_docs'] = cdocs
        public_offer_url = reduce(lambda R, d : d.file.url if d.kind == ConsituentsDocsKinds.PUBLIC_OFFER.value else R, cdocs, None)
        ctx['public_offer_url'] = public_offer_url

        ctx['projects'] = get_projects_data()
        ctx['address'], created = Addresses.objects.get_or_create(site_id=current_site.id)  # TODO Cashe it

        ctx['transfers'] = get_trasnfers()  # TODO Cashe it
        ctx['fin_report'] = FinancialReport.objects.first()  # TODO Cashe it
        ctx['paymentform'] = PaymentForm(initial=self.get_payment_initial())
        return ctx


class LiqPayForm(TemplateView):
    template_name = "ajax/liqpay_form.html"

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)

        form = PaymentForm(self.request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            current_site = get_current_site(self.request)
            domain = current_site.domain
            langauge = get_language()  # $request=self.request)
            params = {
                'action': 'pay',
                'amount': float(form_data['amount']),
                'currency': form_data['currency'],
                'description': f'Donation for {form_data["project"]}',  # TODO: определить назначение платежа
                # 'order_id': str(form_data['order_id']),
                'version': '3',
                'sandbox': settings.LIQPAY_SANDOX_MODE,  # sandbox mode, set to 1 to enable it
                'result_url': f'https://{domain}{reverse("thanks-for-payment")}',
                'language': langauge,
            }
            ctx['signature'] = liqpay.cnb_signature(params)
            ctx['data'] = liqpay.cnb_data(params)
            ctx['disabled'] = False
        else:
            ctx['disabled'] = True
        return ctx


class Thanks(TemplateView):
    template_name = "payment/thanks.html"
    
    def dispatch(self, request, *args, **kwargs):
        logger = logging.getLogger('liqpay')
        msg = f'{request.method} : {request.GET} | {request.POST}'
        logger.info(msg)
        return super(Thanks, self).dispatch(request, *args, **kwargs)

class Error(TemplateView):
    template_name = "payment/error.html"