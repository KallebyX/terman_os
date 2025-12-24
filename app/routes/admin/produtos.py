from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.decorators import admin_required
from app.models.produto import Produto
from app.models.categoria import Categoria
from app import db
from app.routes.admin import admin_bp

@admin_bp.route("/produtos")
@login_required
@admin_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template("admin/produtos/listar.html", produtos=produtos)

@admin_bp.route("/produtos/novo", methods=["GET", "POST"])
@login_required
@admin_required
def novo_produto():
    categorias = Categoria.query.all()
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        preco = float(request.form.get("preco", 0))
        estoque = int(request.form.get("estoque", 0))
        categoria_id = request.form.get("categoria_id")

        produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            categoria_id=categoria_id if categoria_id else None
        )
        db.session.add(produto)
        db.session.commit()
        flash("Produto criado com sucesso!", "success")
        return redirect(url_for("admin.listar_produtos"))
    return render_template("admin/produtos/novo.html", categorias=categorias)

@admin_bp.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.all()
    if request.method == "POST":
        produto.nome = request.form.get("nome")
        produto.descricao = request.form.get("descricao")
        produto.preco = float(request.form.get("preco", 0))
        produto.estoque = int(request.form.get("estoque", 0))
        categoria_id = request.form.get("categoria_id")
        produto.categoria_id = categoria_id if categoria_id else None
        db.session.commit()
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for("admin.listar_produtos"))
    return render_template("admin/produtos/editar.html", produto=produto, categorias=categorias)

@admin_bp.route("/produtos/deletar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido com sucesso!", "success")
    return redirect(url_for("admin.listar_produtos"))
