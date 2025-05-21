from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Categoria, Produto, ImagemProduto, Fornecedor
from .serializers import (
    CategoriaSerializer,
    ProdutoListSerializer,
    ProdutoDetailSerializer,
    ProdutoCreateUpdateSerializer,
    FornecedorSerializer
)
from apps.accounts.permissions import IsAdminOrReadOnly


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de categorias.
    Administradores podem criar, editar e excluir.
    Outros usuários podem apenas visualizar.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativa']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'ordem']
    lookup_field = 'slug'


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de produtos.
    Administradores podem criar, editar e excluir.
    Outros usuários podem apenas visualizar.
    """
    queryset = Produto.objects.select_related('fornecedor').prefetch_related('categorias', 'imagens').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'destaque', 'categorias']
    search_fields = ['nome', 'descricao', 'codigo', 'codigo_barras']
    ordering_fields = ['nome', 'preco', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProdutoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            # Verificar estoque antes de atualizar
            produto = self.get_object()
            if not produto.verificar_estoque(self.request.data.get('quantidade', 0)):
                return Response({'error': 'Estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
            return ProdutoCreateUpdateSerializer
        return ProdutoDetailSerializer


class FornecedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de fornecedores.
    Apenas administradores podem acessar.
    """
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'razao_social', 'cnpj', 'email', 'contato']
    ordering_fields = ['nome', 'created_at']


class ProdutosDestaqueView(generics.ListAPIView):
    """
    View para listar produtos em destaque.
    """
    queryset = Produto.objects.filter(destaque=True, ativo=True)
    serializer_class = ProdutoListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['nome', 'preco', 'created_at']


class ProdutosPorCategoriaView(generics.ListAPIView):
    """
    View para listar produtos por categoria.
    """
    serializer_class = ProdutoListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'destaque']
    search_fields = ['nome', 'descricao', 'codigo']
    ordering_fields = ['nome', 'preco', 'created_at']
    
    def get_queryset(self):
        categoria_slug = self.kwargs['slug']
        categoria = get_object_or_404(Categoria, slug=categoria_slug, ativa=True)
        return Produto.objects.filter(categorias=categoria, ativo=True)


class ProdutoDetailBySlugView(generics.RetrieveAPIView):
    """
    View para obter detalhes de um produto pelo slug.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
