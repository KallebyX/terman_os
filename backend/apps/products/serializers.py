from rest_framework import serializers
from .models import Produto, Categoria, Fornecedor, ImagemProduto

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para categorias de produtos.
    """
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'slug', 'ativa', 'ordem']

class FornecedorSerializer(serializers.ModelSerializer):
    """
    Serializer para fornecedores.
    """
    class Meta:
        model = Fornecedor
        fields = ['id', 'nome', 'razao_social', 'cnpj', 'telefone', 'email', 'ativo']

class ImagemProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer para imagens de produtos.
    """
    class Meta:
        model = ImagemProduto
        fields = ['id', 'imagem', 'ordem', 'principal']

class ProdutoListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de produtos (versão resumida).
    """
    categorias = CategoriaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Produto
        fields = [
            'id', 'codigo', 'nome', 'descricao_curta', 
            'preco', 'slug', 'ativo', 'categorias'
        ]

class ProdutoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes de produtos (versão completa).
    """
    categorias = CategoriaSerializer(many=True, read_only=True)
    imagens = ImagemProdutoSerializer(many=True, read_only=True)
    fornecedor = FornecedorSerializer(read_only=True)
    
    class Meta:
        model = Produto
        fields = [
            'id', 'codigo', 'nome', 'descricao', 'descricao_curta', 
            'preco', 'unidade', 'slug', 'ativo', 'estoque_minimo',
            'categorias', 'imagens', 'fornecedor', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProdutoCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e atualização de produtos.
    """
    class Meta:
        model = Produto
        fields = [
            'codigo', 'nome', 'descricao', 'descricao_curta', 
            'preco', 'unidade', 'slug', 'ativo', 'estoque_minimo',
            'categorias', 'fornecedor'
        ]

# Manter o ProdutoSerializer para compatibilidade com outros módulos
class ProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer para produtos (versão genérica).
    """
    categorias = CategoriaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Produto
        fields = [
            'id', 'codigo', 'nome', 'descricao', 'descricao_curta', 
            'preco', 'unidade', 'slug', 'ativo', 'estoque_minimo',
            'categorias', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
