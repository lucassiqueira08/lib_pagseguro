## Pagseguro API
#### Biblioteca destinada ao redirecionamento para API de pagamentos do pagseguro

#
#### Fluxo de Funcionamento da API Pagseguro
![fluxo de funcionamento api pagseguro](https://stc.pagseguro.uol.com.br/pagseguro/i/integracoes/pagamento_via_api.gif)


#### Pré-requisitos
* Ter uma conta do pagseguro [aqui](https://pagseguro.uol.com.br/registration/registration.jhtml?rcr=a94ca841163f72d80fd722ed640bdee178a122d572976d3c4e900351a26b2d462dee1e3219f2241cd7d93487011c26a78d610f9f6dbf521c4bb5d617fd1bb0b2)
* Ter um token de acesso, caso não possua clique [aqui](https://dev.pagseguro.uol.com.br/reference#autenticacao) para saber mais
* Para que o redirecionamento funcione, é necessário que a opção "pagamento via Formulário HTML" esteja desabilitado em sua conta PagSeguro. Para desabilitá-lo acesse este [link](https://pagseguro.uol.com.br/preferencias/integracoes.jhtml).
* Configurar a URL de redirecionamento após o pagamento em sua conta do pagseguro

  
### Passo a passo

Para utilizar a API do Pagseguro é necessário realizar o checkout para autorização

```python
from pagseguro import Pagseguro
auth = Pagseguro(email="lucas@gmail.com", token=seu_token_de_acesso)
```

Após o checkout realizado, é necessário passar a __moeda__ que será utilizada, o __item__ a ser adquirido, dados referente a __entrega__ do produto, e os dados do __vendedor__:
```python
# Item que será adquirido
item = {"id": 20, "description": "Bala", "amount": 1.99, "quantity": 2, "weight": 0}

# Dados referentes a entrega do produto
shipping = {
    "street": "Avenida Rudge SP",
    "number": 315,
    "complement": "",
    "district": "Barra Funda",
    "city": "São Paulo",
    "state": "SP",
    "country": "Brasil",
    "postal_code": '01133-000',
    "type": 1,
    "cost": 1.99
}

# Dados referentes ao vendedor(você)
sender = {"name": "Lucas Siqueira", "email": "lucas@gmail.com"}

# Moeda que será utilizada no pagamento. Padrão: BRL
currency="BRL"

```

Em seguida, execute para fazer enviar os dados da compra para o Pagseguro:
```python
checkout = auth.checkout(currency=currency, item=item, shipping=shipping, sender=sender)
```

Para que o usuário seja redirecionado para a pagina de pagamento do pagseguro, é necessário que a URL seja gerada com o código do checkout realizado no passo anterior.
```python
# Retorna a url de redirecionamento do pagseguro
url = pagseguro.redirect(checkout)
```

Por fim, basta redirecionar o usuário para a URL fornecida no passo acima para realizar o pagamento.

__LEMBRE-SE:__ Não se esqueça de configurar a URL de redirecionamento na sua conta do pagseguro para ser redirecionado de volta a sua aplicação