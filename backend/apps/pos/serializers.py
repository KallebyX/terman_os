from rest_framework import serializers
from .models import Cliente, Venda, ItemVenda, FormaPagamento, Pagamento
from apps.products.serializers import ProdutoListSerializer
from apps.accounts.serializers import UserSerializer


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Cliente.
    """
    tipo_display = serializers.CharField(read_only=True)
    documento = serializers.CharField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'tipo', 'tipo_display', 'nome', 'email', 'telefone', 'celular',
            'cpf', 'rg', 'data_nascimento', 'razao_social', 'cnpj', 'inscricao_estadual',
            'inscricao_municipal', 'contato', 'endereco', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'cep', 'observacoes', 'limite_credito',
            'ativo', 'usuario', 'documento'
        ]


class FormaPagamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo FormaPagamento.
    """
    class Meta:
        model = FormaPagamento
        fields = ['id', 'nome', 'tipo', 'ativo', 'taxa']


class PagamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Pagamento.
    """
    forma_pagamento_nome = serializers.CharField(source='forma_pagamento.nome', read_only=True)
    
    class Meta:
        model = Pagamento
        fields = [
            'id', 'venda', 'forma_pagamento', 'forma_pagamento_nome', 'valor',
            'status', 'data_pagamento', 'parcelas', 'autorizacao', 'bandeira', 'nsu'
        ]
        read_only_fields = ['data_pagamento']


class ItemVendaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ItemVenda.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    produto_unidade = serializers.CharField(source='produto.unidade', read_only=True)
    
    class Meta:
        model = ItemVenda
        fields = [
            'id', 'venda', 'produto', 'produto_nome', 'produto_codigo', 'produto_unidade',
            'quantidade', 'preco_unitario', 'desconto', 'subtotal'
        ]
        read_only_fields = ['subtotal']


class VendaListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de vendas.
    """
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    vendedor_nome = serializers.CharField(source='vendedor.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Venda
        fields = [
            'id', 'cliente', 'cliente_nome', 'vendedor', 'vendedor_nome',
            'data_venda', 'status', 'status_display', 'tipo', 'tipo_display',
            'subtotal', 'desconto', 'acréscimo', 'total', 'nfe_emitida'
        ]


class VendaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes de venda.
    """
    cliente = ClienteSerializer(read_only=True)
    vendedor = UserSerializer(read_only=True)
    itens = ItemVendaSerializer(many=True, read_only=True)
    pagamentos = PagamentoSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Venda
        fields = [
            'id', 'cliente', 'vendedor', 'data_venda', 'status', 'status_display',
            'tipo', 'tipo_display', 'subtotal', 'desconto', 'acréscimo', 'total',
            'observacoes', 'data_finalizacao', 'data_cancelamento', 'motivo_cancelamento',
            'nfe_emitida', 'nfe_numero', 'nfe_chave', 'nfe_data', 'itens', 'pagamentos'
        ]


class VendaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de venda.
    """
    class Meta:
        model = Venda
        fields = [
            'cliente', 'vendedor', 'tipo', 'observacoes'
        ]


class ItemVendaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de item de venda.
    """
    class Meta:
        model = ItemVenda
        fields = [
            'produto', 'quantidade', 'preco_unitario', 'desconto'
        ]


class VendaFinalizarSerializer(serializers.Serializer):
    """
    Serializer para finalização de venda.
    """
    pagamentos = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )
    
    def validate_pagamentos(self, value):
        """
        Validação para garantir que os pagamentos cubram o valor total da venda.
        """
        if not value:
            raise serializers.ValidationError("É necessário informar pelo menos um pagamento.")
        
        # Validar cada pagamento
        for pagamento in value:
            if 'forma_pagamento' not in pagamento:
                raise serializers.ValidationError("Forma de pagamento não informada.")
            if 'valor' not in pagamento:
                raise serializers.ValidationError("Valor do pagamento não informado.")
            
            try:
                forma_pagamento = FormaPagamento.objects.get(id=pagamento['forma_pagamento'])
                if not forma_pagamento.ativo:
                    raise serializers.ValidationError(f"Forma de pagamento {forma_pagamento.nome} está inativa.")
            except FormaPagamento.DoesNotExist:
                raise serializers.ValidationError("Forma de pagamento não encontrada.")
        
        return value


class VendaCancelarSerializer(serializers.Serializer):
    """
    Serializer para cancelamento de venda.
    """
    motivo = serializers.CharField(required=True)
    
    def validate_motivo(self, value):
        """
        Validação para garantir que o motivo seja informado.
        """
        if not value:
            raise serializers.ValidationError("É necessário informar o motivo do cancelamento.")
        return value
