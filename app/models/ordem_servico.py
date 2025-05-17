from app import db
from datetime import datetime

class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    descricao_servico = db.Column(db.Text, nullable=False)
    produtos_utilizados = db.Column(db.Text, nullable=True)  # lista separada por vírgula ou JSON simplificado
    status = db.Column(db.String(50), default='em análise')  # em análise, em execução, finalizado, cancelado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OS #{self.id} | Cliente: {self.cliente_id} | Status: {self.status}>'