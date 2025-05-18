from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.decorators import admin_required
from app.models.produto import Produto
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
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        preco = request.form.get("preco")
        imagem = request.form.get("imagem")
        produto = Produto(nome=nome, descricao=descricao, preco=preco, imagem=imagem)
        db.session.add(produto)
        db.session.commit()
        flash("Produto criado com sucesso!", "success")
        return redirect(url_for("admin.listar_produtos"))
    return render_template("admin/produtos/novo.html")

@admin_bp.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == "POST":
        produto.nome = request.form.get("nome")
        produto.descricao = request.form.get("descricao")
        produto.preco = request.form.get("preco")
        produto.imagem = request.form.get("imagem")
        db.session.commit()
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for("admin.listar_produtos"))
    return render_template("admin/produtos/editar.html", produto=produto)

@admin_bp.route("/produtos/deletar/<int:id>")
@login_required
@admin_required
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido com sucesso!", "success")
    return redirect(url_for("admin.listar_produtos"))