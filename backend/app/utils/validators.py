from wtforms import Form, StringField, DecimalField, IntegerField, validators
from decimal import Decimal

class ProductForm(Form):
    name = StringField('Nome', [
        validators.Length(min=3, max=120),
        validators.DataRequired()
    ])
    code = StringField('Código', [
        validators.Length(min=3, max=50),
        validators.DataRequired()
    ])
    price = DecimalField('Preço', [
        validators.DataRequired(),
        validators.NumberRange(min=Decimal('0.01'))
    ])
    stock_quantity = IntegerField('Quantidade em Estoque', [
        validators.DataRequired(),
        validators.NumberRange(min=0)
    ])

class OrderForm(Form):
    client_id = IntegerField('Cliente', [validators.DataRequired()])
    payment_method = StringField('Método de Pagamento', [
        validators.DataRequired(),
        validators.AnyOf(['credit_card', 'debit_card', 'cash', 'pix'])
    ])

def validate_order_items(items):
    errors = []
    if not items or not isinstance(items, list):
        errors.append('Itens do pedido são obrigatórios')
        return errors

    for item in items:
        if not isinstance(item, dict):
            errors.append('Formato inválido para item do pedido')
            continue
        
        if 'product_id' not in item:
            errors.append('ID do produto é obrigatório')
        if 'quantity' not in item:
            errors.append('Quantidade é obrigatória')
        elif item['quantity'] <= 0:
            errors.append('Quantidade deve ser maior que zero')

    return errors 