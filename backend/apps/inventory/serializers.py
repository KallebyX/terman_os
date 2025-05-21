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
    tipo = serializers.ChoiceField(choices=['entrada', 'saida', 'ajuste', 'reserva', 'cancelamento'])
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
        if data['tipo'] in ['saida', 'reserva'] and data['quantidade'] <= 0:
            raise serializers.ValidationError(f"A quantidade para {data['tipo']} deve ser maior que zero.")
        
        if data['tipo'] == 'entrada' and data['quantidade'] <= 0:
            raise serializers.ValidationError("A quantidade para entrada deve ser maior que zero.")
        
        # Verificar se o produto existe
        from apps.products.models import Produto
        try:
            produto = Produto.objects.get(id=data['produto_id'])
        except Produto.DoesNotExist:
            raise serializers.ValidationError(f"Produto com ID {data['produto_id']} não encontrado.")
        
        # Verificar estoque disponível para saída ou reserva
        if data['tipo'] in ['saida', 'reserva']:
            from apps.inventory.models import Estoque
            estoque = Estoque.objects.filter(produto_id=data['produto_id']).first()
            
            if not estoque:
                raise serializers.ValidationError(f"Não há registro de estoque para o produto {produto.nome}.")
            
            if data['tipo'] == 'saida' and estoque.quantidade_disponivel < data['quantidade']:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para o produto {produto.nome}. "
                    f"Disponível: {estoque.quantidade_disponivel}, Solicitado: {data['quantidade']}"
                )
            
            if data['tipo'] == 'reserva' and estoque.quantidade_disponivel < data['quantidade']:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para reserva do produto {produto.nome}. "
                    f"Disponível: {estoque.quantidade_disponivel}, Solicitado: {data['quantidade']}"
                )
            
        return data
