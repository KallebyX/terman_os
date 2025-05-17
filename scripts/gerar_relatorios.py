import os
from fpdf import FPDF
from datetime import datetime
from app import create_app, db
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.models.user import User

app = create_app()

with app.app_context():
    pedidos = Pedido.query.all()
    print(f"[✓] Gerando relatórios para {len(pedidos)} pedidos...")

    os.makedirs("relatorios", exist_ok=True)

    for pedido in pedidos:
        usuario = User.query.get(pedido.usuario_id)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)

        pdf.cell(0, 10, "Relatório de Pedido", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Pedido ID: {pedido.id}", ln=True)
        pdf.cell(0, 10, f"Cliente: {usuario.nome if usuario else 'N/A'}", ln=True)
        pdf.cell(0, 10, f"Data: {pedido.data.strftime('%d/%m/%Y') if pedido.data else 'Indefinida'}", ln=True)
        pdf.cell(0, 10, f"Total: R$ {pedido.total:.2f}", ln=True)

        pdf.output(f"relatorios/pedido_{pedido.id}.pdf")

    print("✅ Relatórios gerados na pasta ./relatorios")

    import xlsxwriter

print("\n📊 Gerando relatórios Excel...")

os.makedirs("relatorios_excel", exist_ok=True)

for pedido in pedidos:
    usuario = User.query.get(pedido.usuario_id)
    filename = f"relatorios_excel/pedido_{pedido.id}.xlsx"
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Relatório de Pedido', bold)
    worksheet.write('A3', 'ID do Pedido:')
    worksheet.write('B3', pedido.id)
    worksheet.write('A4', 'Cliente:')
    worksheet.write('B4', usuario.nome if usuario else 'N/A')
    worksheet.write('A5', 'Data:')
    worksheet.write('B5', pedido.data.strftime('%d/%m/%Y') if pedido.data else 'Indefinida')
    worksheet.write('A6', 'Total:')
    worksheet.write('B6', f"R$ {pedido.total:.2f}")

    workbook.close()

print("✅ Relatórios XLSX gerados na pasta ./relatorios_excel")