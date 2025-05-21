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
        write_only=True,
        required=False
    )
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Estoque
        fields = [
            'id', 'produto', 'produto_id', 'quantidade_atual', 'quantidade_reservada',
            'quantidade_disponivel', 'ultima_atualizacao', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['quantidade_disponivel', 'ultima_atualizacao', 'created_at', 'updated_at']


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo MovimentacaoEstoque.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    
    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'id', 'produto', 'produto_nome', 'produto_codigo', 'tipo', 'origem', 'quantidade',
            'valor_unitario', 'documento', 'observacao', 'usuario', 'usuario_nome',
            'data_movimentacao', 'referencia_id', 'referencia_tipo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['data_movimentacao', 'created_at', 'updated_at']


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
    valor_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    referencia_id = serializers.IntegerField(required=False, allow_null=True)
    referencia_tipo = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """
        Valida os dados do ajuste de estoque.
        """
        if data['tipo'] == 'saida' and data['quantidade'] <= 0:
            raise serializers.ValidationError("A quantidade para saída deve ser maior que zero.")
        
        if data['tipo'] == 'entrada' and data['quantidade'] <= 0:
            raise serializers.ValidationError("A quantidade para entrada deve ser maior que zero.")
            
        return data
