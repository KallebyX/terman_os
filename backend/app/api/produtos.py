from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.models.produto import Produto
from . import api_bp

@api_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.filter_by(ativo=True).all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'descricao': p.descricao,
        'preco': float(p.preco),
        'estoque': p.estoque,
        'imagem': p.imagem
    } for p in produtos])

@api_bp.route('/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify({
        'id': produto.id,
        'nome': produto.nome,
        'descricao': produto.descricao,
        'preco': float(produto.preco),
        'estoque': produto.estoque,
        'imagem': produto.imagem
    }) 