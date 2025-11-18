"""
Módulo de Utilitários - Terman OS
Funções auxiliares para validação, sanitização, upload de arquivos, etc.
"""
import os
import re
import secrets
from PIL import Image
from flask import current_app, flash
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """
    Verifica se o arquivo tem uma extensão permitida

    Args:
        filename: Nome do arquivo

    Returns:
        bool: True se extensão é permitida
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def validate_image(file):
    """
    Valida se o arquivo é realmente uma imagem válida

    Args:
        file: Arquivo de upload (werkzeug.datastructures.FileStorage)

    Returns:
        tuple: (is_valid, error_message)
    """
    if not file:
        return False, "Nenhum arquivo fornecido"

    if file.filename == '':
        return False, "Nome de arquivo vazio"

    if not allowed_file(file.filename):
        allowed = ', '.join(current_app.config['ALLOWED_EXTENSIONS'])
        return False, f"Extensão não permitida. Permitidas: {allowed}"

    # Verificar content type
    if not file.content_type or not file.content_type.startswith('image/'):
        return False, "O arquivo não é uma imagem válida"

    # Tentar abrir a imagem para validar
    try:
        img = Image.open(file.stream)
        img.verify()
        file.stream.seek(0)  # Reset stream
        return True, None
    except Exception as e:
        return False, f"Arquivo de imagem corrompido: {str(e)}"


def sanitize_filename(filename):
    """
    Sanitiza nome de arquivo para segurança

    Args:
        filename: Nome do arquivo original

    Returns:
        str: Nome do arquivo sanitizado e único
    """
    # Remove path e caracteres perigosos
    filename = secure_filename(filename)

    # Adiciona hash único para evitar sobrescrita
    name, ext = os.path.splitext(filename)
    unique_name = f"{name}_{secrets.token_hex(8)}{ext}"

    return unique_name


def save_image(file, folder='produtos', max_size=(1200, 1200), create_thumbnail=True):
    """
    Salva imagem com redimensionamento e otimização

    Args:
        file: Arquivo de upload
        folder: Pasta de destino (dentro de static/)
        max_size: Tamanho máximo (largura, altura)
        create_thumbnail: Se deve criar thumbnail

    Returns:
        dict: {
            'filename': nome do arquivo salvo,
            'thumbnail': nome do thumbnail (se criado),
            'path': caminho completo,
            'url': URL relativa
        }
    """
    # Validar imagem
    is_valid, error = validate_image(file)
    if not is_valid:
        flash(error, 'danger')
        return None

    # Sanitizar nome
    filename = sanitize_filename(file.filename)

    # Criar diretório se não existir
    upload_dir = os.path.join(current_app.root_path, 'static', folder)
    os.makedirs(upload_dir, exist_ok=True)

    # Caminho completo
    filepath = os.path.join(upload_dir, filename)

    # Abrir e otimizar imagem
    img = Image.open(file.stream)

    # Converter RGBA para RGB se necessário
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # Redimensionar mantendo aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Salvar com otimização
    img.save(filepath, optimize=True, quality=85)

    result = {
        'filename': filename,
        'path': filepath,
        'url': f'/static/{folder}/{filename}'
    }

    # Criar thumbnail se solicitado
    if create_thumbnail:
        thumb_name = f"thumb_{filename}"
        thumb_path = os.path.join(upload_dir, thumb_name)

        thumb = img.copy()
        thumb.thumbnail((300, 300), Image.Resampling.LANCZOS)
        thumb.save(thumb_path, optimize=True, quality=80)

        result['thumbnail'] = thumb_name
        result['thumbnail_url'] = f'/static/{folder}/{thumb_name}'

    return result


def delete_image(filename, folder='produtos', delete_thumbnail=True):
    """
    Deleta imagem e seu thumbnail

    Args:
        filename: Nome do arquivo
        folder: Pasta onde está o arquivo
        delete_thumbnail: Se deve deletar thumbnail também
    """
    try:
        # Deletar imagem principal
        filepath = os.path.join(current_app.root_path, 'static', folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

        # Deletar thumbnail
        if delete_thumbnail:
            thumb_name = f"thumb_{filename}"
            thumb_path = os.path.join(current_app.root_path, 'static', folder, thumb_name)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)

        return True
    except Exception as e:
        current_app.logger.error(f"Erro ao deletar imagem {filename}: {e}")
        return False


def sanitize_html(text, allowed_tags=None):
    """
    Remove tags HTML perigosas do texto

    Args:
        text: Texto a ser sanitizado
        allowed_tags: Lista de tags permitidas (None = remover todas)

    Returns:
        str: Texto sanitizado
    """
    if not text:
        return text

    if allowed_tags is None:
        # Remover todas as tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    # Implementação mais complexa para permitir algumas tags
    # (pode usar biblioteca como bleach para isso)
    return text


def validate_cpf(cpf):
    """
    Valida número de CPF brasileiro

    Args:
        cpf: String com CPF (pode conter pontos e traços)

    Returns:
        bool: True se CPF é válido
    """
    # Remove pontos e traços
    cpf = re.sub(r'[^0-9]', '', cpf)

    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Validação dos dígitos verificadores
    def calc_digit(cpf_partial):
        sum_val = 0
        for i, digit in enumerate(cpf_partial):
            sum_val += int(digit) * (len(cpf_partial) + 1 - i)
        remainder = sum_val % 11
        return 0 if remainder < 2 else 11 - remainder

    # Valida primeiro dígito
    if int(cpf[9]) != calc_digit(cpf[:9]):
        return False

    # Valida segundo dígito
    if int(cpf[10]) != calc_digit(cpf[:10]):
        return False

    return True


def validate_cnpj(cnpj):
    """
    Valida número de CNPJ brasileiro

    Args:
        cnpj: String com CNPJ (pode conter pontos, traços e barra)

    Returns:
        bool: True se CNPJ é válido
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^0-9]', '', cnpj)

    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False

    # Validação dos dígitos verificadores
    def calc_digit(cnpj_partial, weights):
        sum_val = sum(int(digit) * weight for digit, weight in zip(cnpj_partial, weights))
        remainder = sum_val % 11
        return 0 if remainder < 2 else 11 - remainder

    # Pesos para os cálculos
    weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights_second = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    # Valida primeiro dígito
    if int(cnpj[12]) != calc_digit(cnpj[:12], weights_first):
        return False

    # Valida segundo dígito
    if int(cnpj[13]) != calc_digit(cnpj[:13], weights_second):
        return False

    return True


def format_currency(value):
    """
    Formata valor como moeda brasileira

    Args:
        value: Valor numérico

    Returns:
        str: Valor formatado (R$ 1.234,56)
    """
    if value is None:
        return "R$ 0,00"

    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_cpf(cpf):
    """Formata CPF: 123.456.789-01"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def format_cnpj(cnpj):
    """Formata CNPJ: 12.345.678/0001-90"""
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def format_phone(phone):
    """Formata telefone: (11) 91234-5678 ou (11) 1234-5678"""
    phone = re.sub(r'[^0-9]', '', phone)
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return phone


def paginate_query(query, page, per_page=20):
    """
    Pagina uma query do SQLAlchemy

    Args:
        query: Query do SQLAlchemy
        page: Número da página (começa em 1)
        per_page: Itens por página

    Returns:
        dict: {
            'items': lista de itens,
            'total': total de itens,
            'pages': total de páginas,
            'current_page': página atual,
            'has_prev': tem página anterior,
            'has_next': tem próxima página,
            'prev_page': número da página anterior,
            'next_page': número da próxima página
        }
    """
    total = query.count()
    pages = (total + per_page - 1) // per_page  # Ceiling division

    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        'items': items,
        'total': total,
        'pages': pages,
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < pages else None,
        'per_page': per_page
    }
