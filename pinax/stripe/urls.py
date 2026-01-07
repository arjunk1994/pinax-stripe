from django.urls import re_path

from .views import (
    InvoiceListView,
    PaymentMethodCreateView,
    PaymentMethodDeleteView,
    PaymentMethodListView,
    PaymentMethodUpdateView,
    SubscriptionCreateView,
    SubscriptionDeleteView,
    SubscriptionListView,
    SubscriptionUpdateView,
    Webhook
)

urlpatterns = [
    re_path(r"^subscriptions/$", SubscriptionListView.as_view(), name="pinax_stripe_subscription_list"),
    re_path(r"^subscriptions/create/$", SubscriptionCreateView.as_view(), name="pinax_stripe_subscription_create"),
    re_path(r"^subscriptions/(?P<pk>\d+)/delete/$", SubscriptionDeleteView.as_view(), name="pinax_stripe_subscription_delete"),
    re_path(r"^subscriptions/(?P<pk>\d+)/update/$", SubscriptionUpdateView.as_view(), name="pinax_stripe_subscription_update"),

    re_path(r"^payment-methods/$", PaymentMethodListView.as_view(), name="pinax_stripe_payment_method_list"),
    re_path(r"^payment-methods/create/$", PaymentMethodCreateView.as_view(), name="pinax_stripe_payment_method_create"),
    re_path(r"^payment-methods/(?P<pk>\d+)/delete/$", PaymentMethodDeleteView.as_view(), name="pinax_stripe_payment_method_delete"),
    re_path(r"^payment-methods/(?P<pk>\d+)/update/$", PaymentMethodUpdateView.as_view(), name="pinax_stripe_payment_method_update"),

    re_path(r"^invoices/$", InvoiceListView.as_view(), name="pinax_stripe_invoice_list"),

    re_path(r"^webhook/$", Webhook.as_view(), name="pinax_stripe_webhook"),
]
