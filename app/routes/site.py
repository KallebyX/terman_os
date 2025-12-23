from flask import Blueprint, render_template, Response, request, url_for
from datetime import datetime

site_bp = Blueprint('site', __name__)

@site_bp.route('/')
def homepage():
    return render_template('index.html')

@site_bp.route('/sobre')
def sobre_nos():
    return render_template('sobre.html')

@site_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')


@site_bp.route('/robots.txt')
def robots():
    """
    Gera o arquivo robots.txt otimizado para SEO.
    """
    base_url = request.url_root.rstrip('/')
    robots_content = f"""# Robots.txt - Mangueiras Terman
# https://www.mangueirasterman.com.br

User-agent: *
Allow: /
Allow: /loja
Allow: /loja/
Allow: /sobre
Allow: /contato
Allow: /produto/

# Bloquear áreas administrativas e privadas
Disallow: /admin
Disallow: /admin/
Disallow: /painel
Disallow: /painel/
Disallow: /dashboard
Disallow: /dashboard/
Disallow: /crm
Disallow: /crm/
Disallow: /erp
Disallow: /erp/
Disallow: /login
Disallow: /cadastro
Disallow: /logout
Disallow: /carrinho
Disallow: /checkout
Disallow: /api/
Disallow: /static/css/
Disallow: /static/js/

# Bloquear parâmetros de ordenação e filtros duplicados
Disallow: /*?ordenar=
Disallow: /*?page=
Disallow: /*&ordenar=
Disallow: /*&page=

# Crawl-delay para não sobrecarregar o servidor
Crawl-delay: 1

# Sitemap
Sitemap: {base_url}/sitemap.xml

# Google specific
User-agent: Googlebot
Allow: /
Crawl-delay: 0

# Google Images
User-agent: Googlebot-Image
Allow: /static/img/
Allow: /static/produtos/

# Bing specific
User-agent: Bingbot
Allow: /
Crawl-delay: 1
"""
    return Response(robots_content, mimetype='text/plain')


@site_bp.route('/sitemap.xml')
def sitemap():
    """
    Gera um sitemap.xml dinâmico com todas as páginas do site.
    """
    from app.models.produto import Produto
    from app.models.categoria import Categoria
    from app import db

    base_url = request.url_root.rstrip('/')
    today = datetime.now().strftime('%Y-%m-%d')

    # Páginas estáticas principais
    static_pages = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': '/loja', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': '/sobre', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': '/contato', 'priority': '0.8', 'changefreq': 'monthly'},
    ]

    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''

    # Adicionar páginas estáticas
    for page in static_pages:
        xml_content += f'''    <url>
        <loc>{base_url}{page['loc']}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>{page['changefreq']}</changefreq>
        <priority>{page['priority']}</priority>
    </url>
'''

    # Adicionar categorias
    try:
        categorias = Categoria.query.filter_by(ativo=True).all()
        for categoria in categorias:
            xml_content += f'''    <url>
        <loc>{base_url}/loja?categoria={categoria.id}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    except Exception:
        pass

    # Adicionar produtos
    try:
        produtos = Produto.query.filter_by(ativo=True).all()
        for produto in produtos:
            lastmod = produto.data_atualizacao.strftime('%Y-%m-%d') if hasattr(produto, 'data_atualizacao') and produto.data_atualizacao else today

            xml_content += f'''    <url>
        <loc>{base_url}/loja/produto/{produto.id}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
'''
            # Adicionar imagem do produto se existir
            if produto.imagem_url:
                xml_content += f'''        <image:image>
            <image:loc>{produto.imagem_url}</image:loc>
            <image:title>{produto.nome}</image:title>
            <image:caption>{produto.descricao_curta or produto.nome}</image:caption>
        </image:image>
'''
            xml_content += '''    </url>
'''
    except Exception:
        pass

    xml_content += '''</urlset>'''

    return Response(xml_content, mimetype='application/xml')


@site_bp.route('/manifest.json')
def manifest():
    """
    Gera o arquivo manifest.json para PWA e SEO.
    """
    base_url = request.url_root.rstrip('/')
    manifest_content = {
        "name": "Mangueiras Terman - Mangueiras Hidráulicas e Industriais",
        "short_name": "Mangueiras Terman",
        "description": "Líder nacional em mangueiras hidráulicas, industriais e conexões. Desde 2001 oferecendo qualidade e preço justo para todo Brasil.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0071e3",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "pt-BR",
        "categories": ["shopping", "business", "industrial"],
        "icons": [
            {
                "src": f"{base_url}/static/img/logo_terman.webp",
                "sizes": "192x192",
                "type": "image/webp",
                "purpose": "any maskable"
            },
            {
                "src": f"{base_url}/static/img/logo_terman.webp",
                "sizes": "512x512",
                "type": "image/webp",
                "purpose": "any maskable"
            }
        ],
        "shortcuts": [
            {
                "name": "Loja",
                "short_name": "Loja",
                "description": "Ver catálogo de produtos",
                "url": "/loja",
                "icons": [{"src": f"{base_url}/static/img/logo_terman.webp", "sizes": "96x96"}]
            },
            {
                "name": "Contato",
                "short_name": "Contato",
                "description": "Entre em contato conosco",
                "url": "/contato",
                "icons": [{"src": f"{base_url}/static/img/logo_terman.webp", "sizes": "96x96"}]
            }
        ],
        "related_applications": [],
        "prefer_related_applications": False
    }

    import json
    return Response(json.dumps(manifest_content, ensure_ascii=False, indent=2),
                   mimetype='application/manifest+json')