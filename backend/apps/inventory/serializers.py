from rest_framework import serializers
from .models import Estoque, MovimentacaoEstoque
from apps.products.serializers import ProdutoListSerializer
from apps.products.models import Produto


class EstoqueSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Estoque.
    """
    produto = ProdutoListSerializer(read_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(
        source='produto', 
        queryset=Produto.objects.all(),
        write_only=True
    )
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Estoque
        fields = [
            'id', 'produto', 'produto_id', 'quantidade_atual', 'quantidade_reservada',
            'quantidade_disponivel', 'ultima_atualizacao', 'status'
        ]
        read_only_fields = ['quantidade_disponivel', 'ultima_atualizacao']


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo MovimentacaoEstoque.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'id', 'produto', 'produto_nome', 'tipo', 'origem', 'quantidade',
            'valor_unitario', 'documento', 'observacao', 'usuario', 'usuario_nome',
            'data_movimentacao', 'referencia_id', 'referencia_tipo'
        ]
        read_only_fields = ['data_movimentacao']


class AjusteEstoqueSerializer(serializers.Serializer):
    """
    Serializer para ajuste de estoque.
    """
    produto_id = serializers.IntegerField()
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=2)
    tipo = serializers.ChoiceField(choices=['entrada', 'saida', 'ajuste'])
    origem = serializers.ChoiceField(choices=MovimentacaoEstoque.ORIGEM_CHOICES)
    documento = serializers.CharField(required=False, allow_blank=True)
    observacao = serializers.CharField(required=False, allow_blank=True)
    valor_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    referencia_id = serializers.IntegerField(required=False)
    referencia_tipo = serializers.CharField(required=False, allow_blank=True)
