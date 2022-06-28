import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, RedirectView
from django.utils.translation import gettext_lazy as _, get_language
from liqpay import LiqPay

from pages.forms import PaymentForm
from pages.models import Project


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['projects'] = Project.objects.all() #TODO Cashe it
        return ctx


class PaymentStart(FormView):
    template_name = "payment/new_payment.html"
    form_class = PaymentForm

    def get_initial(self):
        return {
            'amount': 100,
            'currency': 'USD'
        }


    def form_valid(self, form):
        order_id = str(uuid.uuid4())
        cache.set(f'order_{order_id}', form.cleaned_data)
        self.success_url = reverse('payment', kwargs={'order_id': order_id})
        return super().form_valid(form)


class PaymentFinish(TemplateView):
    template_name = "payment\make_payment.html"
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id', None)
        if order_id is None:
            messages.error(self.request, _("Помилка розбору параметрів"))
            # TODO: Payment error
            return HttpResponseRedirect(reverse('index'))
        form_data = cache.get(f'order_{order_id}')
        if form_data is None:
            messages.error(self.request, _("Не знайдено платежу. Мабуть Ви сплатили його раніше "))
            # TODO: Payment error
            return HttpResponseRedirect(reverse('index'))

        form_data['order_id']=order_id
        context = self.get_context_data(form_data=form_data)
        return self.render_to_response(context)

    def get_context_data(self, form_data=None):
        ctx=super().get_context_data(form_data=form_data)
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        current_site = get_current_site(self.request)
        domain = current_site.domain
        protocol = 'https' if self.request.is_secure() else 'http'
        langauge = get_language()#$request=self.request)
        params = {
                'action': 'pay',
                'amount': float(form_data['amount']),
                'currency': form_data['currency'],
                'description': 'Donation for ',#TODO: определить назначение платежа
                'order_id': str(form_data['order_id']),
                'version': '3',
                'sandbox': settings.LIQPAY_SANDOX_MODE, # sandbox mode, set to 1 to enable it
                'result_url': 'https://google.com/',
                'language': langauge,
                # 'server_url': f'{protocol}://{domain}{reverse("liqpay-callback", kwargs={"pk": order.pk})}',  # url to callback view
            }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)

        form = liqpay.cnb_form(params)
        ctx['form'] = form
        ctx['signature'] = signature
        ctx['data'] = data
        return ctx

