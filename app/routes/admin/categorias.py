from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.decorators import admin_required
from app.models.categoria import Categoria
from app import db
from app.routes.admin import admin_bp

@admin_bp.route("/categorias")
@login_required
@admin_required
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template("admin/categorias/listar.html", categorias=categorias)

@admin_bp.route("/categorias/nova", methods=["GET", "POST"])
@login_required
@admin_required
def nova_categoria():
    if request.method == "POST":
        nome = request.form.get("nome")
        categoria = Categoria(nome=nome)
        db.session.add(categoria)
        db.session.commit()
        flash("Categoria criada com sucesso!", "success")
        return redirect(url_for("admin.listar_categorias"))
    return render_template("admin/categorias/nova.html")

@admin_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nome = request.form.get("nome")
        db.session.commit()
        flash("Categoria atualizada com sucesso!", "success")
        return redirect(url_for("admin.listar_categorias"))
    return render_template("admin/categorias/editar.html", categoria=categoria)

@admin_bp.route("/categorias/deletar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoria removida com sucesso!", "success")
    return redirect(url_for("admin.listar_categorias"))