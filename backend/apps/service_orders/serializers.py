from rest_framework import serializers
from .models import OrdemServico, ItemOrdemServico, EtapaOrdemServico, ComentarioOrdemServico, AnexoOrdemServico
from apps.pos.serializers import ClienteSerializer
from apps.accounts.serializers import UserSerializer
from apps.products.serializers import ProdutoListSerializer


class ItemOrdemServicoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ItemOrdemServico.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    produto_unidade = serializers.CharField(source='produto.unidade', read_only=True)
    
    class Meta:
        model = ItemOrdemServico
        fields = [
            'id', 'ordem_servico', 'produto', 'produto_nome', 'produto_codigo', 
            'produto_unidade', 'quantidade', 'preco_unitario', 'subtotal'
        ]
        read_only_fields = ['subtotal']


class EtapaOrdemServicoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo EtapaOrdemServico.
    """
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EtapaOrdemServico
        fields = [
            'id', 'ordem_servico', 'nome', 'descricao', 'status', 'status_display',
            'responsavel', 'responsavel_nome', 'ordem', 'data_inicio', 'data_conclusao'
        ]


class ComentarioOrdemServicoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ComentarioOrdemServico.
    """
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = ComentarioOrdemServico
        fields = [
            'id', 'ordem_servico', 'usuario', 'usuario_nome', 'texto', 'data'
        ]
        read_only_fields = ['data']


class AnexoOrdemServicoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo AnexoOrdemServico.
    """
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = AnexoOrdemServico
        fields = [
            'id', 'ordem_servico', 'usuario', 'usuario_nome', 'arquivo', 
            'nome', 'descricao', 'data'
        ]
        read_only_fields = ['data']


class OrdemServicoListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de ordens de serviço.
    """
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    tecnico_nome = serializers.CharField(source='tecnico.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    
    class Meta:
        model = OrdemServico
        fields = [
            'id', 'numero', 'cliente', 'cliente_nome', 'responsavel', 'responsavel_nome',
            'tecnico', 'tecnico_nome', 'data_abertura', 'status', 'status_display',
            'prioridade', 'prioridade_display', 'valor_total'
        ]


class OrdemServicoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes de ordem de serviço.
    """
    cliente = ClienteSerializer(read_only=True)
    responsavel = UserSerializer(read_only=True)
    tecnico = UserSerializer(read_only=True)
    itens = ItemOrdemServicoSerializer(many=True, read_only=True)
    etapas = EtapaOrdemServicoSerializer(many=True, read_only=True)
    comentarios = ComentarioOrdemServicoSerializer(many=True, read_only=True)
    anexos = AnexoOrdemServicoSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    
    class Meta:
        model = OrdemServico
        fields = [
            'id', 'numero', 'cliente', 'responsavel', 'tecnico', 'data_abertura',
            'data_aprovacao', 'data_inicio', 'data_conclusao', 'data_cancelamento',
            'status', 'status_display', 'prioridade', 'prioridade_display',
            'descricao_problema', 'descricao_servico', 'observacoes',
            'valor_servico', 'valor_pecas', 'valor_total', 'garantia',
            'motivo_cancelamento', 'itens', 'etapas', 'comentarios', 'anexos'
        ]


class OrdemServicoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de ordem de serviço.
    """
    class Meta:
        model = OrdemServico
        fields = [
            'cliente', 'responsavel', 'tecnico', 'prioridade',
            'descricao_problema', 'descricao_servico', 'observacoes',
            'valor_servico', 'garantia'
        ]


class OrdemServicoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de ordem de serviço.
    """
    class Meta:
        model = OrdemServico
        fields = [
            'tecnico', 'prioridade', 'descricao_problema', 'descricao_servico',
            'observacoes', 'valor_servico', 'garantia'
        ]


class OrdemServicoStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer para atualização de status de ordem de serviço.
    """
    status = serializers.ChoiceField(choices=OrdemServico.STATUS_CHOICES)
    observacao = serializers.CharField(required=False, allow_blank=True)


class OrdemServicoCancelarSerializer(serializers.Serializer):
    """
    Serializer para cancelamento de ordem de serviço.
    """
    motivo = serializers.CharField(required=True)
    
    def validate_motivo(self, value):
        """
        Validação para garantir que o motivo seja informado.
        """
        if not value:
            raise serializers.ValidationError("É necessário informar o motivo do cancelamento.")
        return value
