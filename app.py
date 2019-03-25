import requests
import jxmlease as jxmlease

# Tipos de frete
SHIPPING_TYPE = (
    (1, 'PAC'),
    (2, 'SEDEX'),
    (3, 'Tipo de frete não especificado.')
)


class Pagseguro:
    """
    Classe de conexão com a API do Pagseguro

    Parametros:
        email: Email de autenticação
        token: Token gerado do Pagseguro developers
    """

    def __init__(self, email, token):
        self.base_url = 'https://ws.pagseguro.uol.com.br'
        self.email = email
        self.token = token
        self.redirect_url = ''

    def checkout(self, **kwargs):
        """
        Método responsável por realizar a autenticação com o Pagseguro

        Parametros
        ----------
        kwargs: Argumentos que podem ser passados para realizar o checkout, são obrigatorios: currency,
        item(a ser comprado) e sender(comprador). Dados referentes ao endereço de entrega não são obrigatórios(shipping)

        Returns
        -------
        Retorna o conteúdo da resposta
        """
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

        checkout_url = "https://ws.pagseguro.uol.com.br/v2/checkout"
        querystring = {"email": self.email, "token": self.token}

        currency = kwargs.get('currency')
        item = kwargs.get('item')
        shipping = kwargs.get('shipping', None)
        sender = kwargs.get('sender', None)

        if shipping:
            payload = {
                "currency": currency,
                "itemId1": item.get('id', None),
                "itemDescription1": item.get('description', None),
                "itemAmount1": item.get('amount', None),
                "itemQuantity1": item.get('quantity', None),
                "itemWeight1": item.get('weight', None),
                "itemShippingCost": item.get('shipping_cost', None),
                "shippingAddressRequired": 'true',
                "shippingAddressStreet": shipping.get('street', None),
                "shippingAddressNumber": shipping.get('number', None),
                "shippingAddressComplement": shipping.get('complement', None),
                "shippingAddressDistrict": shipping.get('district', None),
                "shippingAddressCity": shipping.get('city', None),
                "shippingAddressState": shipping.get('state', None),
                "shippingAddressCountry": shipping.get('country', None),
                "shippingAddressPostalCode": shipping.get('postal_code', None),
                "shippingType": shipping.get('type', None),
                "shippingCost": shipping.get('cost', None),
                "senderName": sender.get('name', None),
                "senderEmail": sender.get('email', None),
                "redirectURL": self.redirect_url,
                "reference": item.get('id', None)
            }
        else:
            payload = {
                "currency": currency,
                "itemId1": item.get('id', None),
                "itemDescription1": item.get('description', None),
                "itemAmount1": item.get('amount', None),
                "itemQuantity1": item.get('quantity', None),
                "itemWeight1": item.get('weight', None),
                "senderName": sender.get('name', None),
                "senderEmail": sender.get('email', None),
                "redirectURL": self.redirect_url,
                "reference": item.get('id', None)
            }
        response = requests.post(checkout_url, data=payload, headers=headers, params=querystring)
        return response.content

    def redirect(self, checkout):
        """
        Método responsável por retornar a url de redirecionamento

        Parameters
        ----------
        checkout: Conteúdo da resposta do checkout

        Returns
        -------
        Url de pagamento em que o usuario será redirecionado
        """
        checkout = jxmlease.parse(checkout.decode())
        checkout_code = checkout['checkout']['code']
        pagseguro_url = f"https://pagseguro.uol.com.br/v2/checkout/payment.html?code={checkout_code}"
        return pagseguro_url

    def cancel_transaction(self, transaction_code):
        """
        Método responsável por cancelar uma transação

        Parameters
        ----------
        transaction_code: Código da transação fornecida na conclusão do pagamento

        Returns
        -------
        Retorna a resposta da requisição de cancelamento
        """
        headers = {
            'Content-Type': "application/x-www-form-urlencoded; charset=ISO-8859-1",
        }

        cancel_transaction_url = "https://ws.pagseguro.uol.com.br/v2/transactions/cancels"
        querystring = {"email": self.email, "token": self.token}

        payload = {"transactionCode": transaction_code}

        response = requests.post(cancel_transaction_url, data=payload, headers=headers, params=querystring)
        return response

    def reverse_transaction(self, transaction_code, refund_value):
        """
        Método para estornar valor da transação

        Parameters
        ----------
        transaction_code: Código da transação fornecida na conclusão do pagamento
        refund_value: Valor a ser estornado

        Returns
        -------
        Retorna a resposta da requisição de estorno
        """
        headers = {
            'Content-Type': "application/x-www-form-urlencoded; charset=ISO-8859-1",
        }

        reverse_transaction_url = "https://ws.pagseguro.uol.com.br/v2/transactions/refunds"
        querystring = {"email": self.email, "token": self.token}
        payload = {"transactionCode": transaction_code, "refundValue": refund_value}
        response = requests.post(reverse_transaction_url, data=payload, headers=headers, params=querystring)
        return response