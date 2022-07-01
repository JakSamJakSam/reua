(function (global, factory) {
  global.reUA = factory()
})(this, (function () {
  const data = JSON.parse(document.getElementById('projects-info').textContent);
  const paymentTypeOffcanvas = document.getElementById('payment-select-payment-type')
  const paymentBankOffcanvas = document.getElementById('bank_acc_payment')
  const projectsData = data.reduce((R, {identity, ...p}) => ({
    ...R,
    [identity]: p
  }), {});

  function addClass(node, className) {
    if (!node.className.split(' ').includes(className)) node.className += ` ${className} `;
    console.log(!node.className.split(' ').includes(className))
    console.log(node);
    console.log(className);
  }

  function removeClass(node, className) {
    node.className = node.className.split(' ').filter(cn => cn && cn !== className).join(' ')
  }

  function onPaymentClick(e) {
    const project = this.dataset.project
    paymentTypeOffcanvas.dataset.project = project;
    // CREDIT CARD
    const ccButton = paymentTypeOffcanvas.querySelector('[data-payment_type="credit_card"]');
    if (projectsData[project].cardURL) {
      removeClass(ccButton, 'disabled')
      ccButton.setAttribute('href', projectsData[project].cardURL)
    } else {
      addClass(ccButton, 'disabled')
    }
    // CRYPTO
    const cryptoButton = paymentTypeOffcanvas.querySelector('[data-payment_type="crypto"]');
    if (projectsData[project].cryptoURL) {
      cryptoButton.setAttribute('href', projectsData[project].cryptoURL)
      removeClass(cryptoButton, 'disabled')
    } else {
      addClass(cryptoButton, 'disabled')
    }
    // PAYPAL
    const paypalButton = paymentTypeOffcanvas.querySelector('[data-payment_type="paypal"]');
    addClass(paypalButton, 'disabled')

    // bank
    const bankButton = paymentTypeOffcanvas.querySelector('[data-payment_type="bank_account"]');
    if (projectsData[project].bank_accounts) {
      // cryptoButton.setAttribute('href', projectsData[project].cryptoURL)
      removeClass(bankButton, 'disabled')
    } else {
      addClass(bankButton, 'disabled')
    }

    paymentBankOffcanvas.querySelectorAll('[data-project]').forEach(
      (accItem, idx) => {
        if (accItem.dataset.project === project) {
          removeClass(accItem, 'd-none')
        } else {
          addClass(accItem, 'd-none')
        }
      }
    );
    paymentBankOffcanvas.querySelectorAll('[data-project]:not(.d-none)').forEach(
      (accItem, idx) => {
        const b = accItem.querySelector('.accordion-button')
        const c = accItem.querySelector('.accordion-collapse')
        if (idx === 0) {
          removeClass(b, 'collapsed');
          b.setAttribute('aria-expanded', "true");
          addClass(c, "show");
        } else {
          addClass(b, 'collapsed');
          b.setAttribute('aria-expanded', "false");
          removeClass(c, "show");
        }
      }
    )
  }

  const buttons = [...document.querySelectorAll('[data-project]')].filter(item => item.dataset.project in projectsData);
  buttons.forEach(item => {
    const proj = item.dataset.project;
    if (projectsData[proj].disabled) {
      item.className += ' disabled ';
    } else {
      item.addEventListener('click', onPaymentClick);
    }
  })

  return {
    data: projectsData,
  }

}))
// var PaymentHelper = {
//   onProjectClick: function (e) {
//     console.log(e)
//   },
//   init: function () {
//     PaymentHelper.initButtons();
//   },
//   initButtons: function (){
//     console.log(PaymentHelper._projectData);
//     // buttons.forEach((item) => {
//     //   item.addEventListener("click", onProjectClick);
//     // });
//   },
// }
