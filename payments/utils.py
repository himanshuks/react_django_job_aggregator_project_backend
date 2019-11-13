from django.conf import settings

import braintree


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        environment=settings.BRAINTREE_ENVIRONMENT,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )
)


def generate_client_token():
    return gateway.client_token.generate()


def transact(options):
    return gateway.transaction.sale(options)


def find_transaction(id):
    return gateway.transaction.find(id)
