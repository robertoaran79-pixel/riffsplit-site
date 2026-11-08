#!/usr/bin/env python3
"""Gera as páginas do site do RiffSplit (início pt/en/es e guias).

Uso: python3 _fonte/gerar.py   (a partir da raiz do repositório)
Conteúdo dos guias: _fonte/guias.py. Suporte e privacidade são editados à mão.
"""
import json, os, sys, html
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guias import GUIAS  # noqa: E402

BASE = "https://robertoaran79-pixel.github.io/riffsplit-site/"
APP = "https://apps.apple.com/app/id6829560023"
APP_ID = "6829560023"
HOJE = date.today().isoformat()

APP_LD = {
    "@context": "https://schema.org",
    "@type": "MobileApplication",
    "name": "RiffSplit",
    "operatingSystem": "iOS, iPadOS, macOS",
    "applicationCategory": "MusicApplication",
    "downloadUrl": APP,
    "installUrl": APP,
    "image": BASE + "icon.png",
    "url": BASE,
    "publisher": {"@type": "Organization", "name": "RLA LABS"},
    "inLanguage": ["pt-BR", "en", "es"],
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL",
               "description": "Download grátis com separação de 30 segundos por música; desbloqueio por compra única no app"},
}

TXT = {
    "pt": {"lang": "pt-BR", "badge": "img/appstore-pt-br.svg", "badge_alt": "Baixar na App Store",
           "inicio": "Início", "guias": "Guias", "suporte": "Suporte", "privacidade": "Privacidade",
           "og": "img/og-ptbr.jpg", "locale": "pt_BR",
           "legal": "Apple, o logotipo da Apple, iPhone, iPad e Mac são marcas registradas da Apple Inc. App Store é marca de serviço da Apple Inc."},
    "en": {"lang": "en", "badge": "img/appstore-en-us.svg", "badge_alt": "Download on the App Store",
           "inicio": "Home", "guias": "Guides (Portuguese)", "suporte": "Support", "privacidade": "Privacy",
           "og": "img/og-en.jpg", "locale": "en_US",
           "legal": "Apple, the Apple logo, iPhone, iPad and Mac are trademarks of Apple Inc. App Store is a service mark of Apple Inc."},
    "es": {"lang": "es", "badge": "img/appstore-es-mx.svg", "badge_alt": "Descargar en el App Store",
           "inicio": "Inicio", "guias": "Guías (portugués)", "suporte": "Soporte", "privacidade": "Privacidad",
           "og": "img/og-es.jpg", "locale": "es_MX",
           "legal": "Apple, el logotipo de Apple, iPhone, iPad y Mac son marcas comerciales de Apple Inc. App Store es una marca de servicio de Apple Inc."},
}

ALT = '<link rel="alternate" hreflang="pt-BR" href="{b}">\n<link rel="alternate" hreflang="en" href="{b}en/">\n<link rel="alternate" hreflang="es" href="{b}es/">\n<link rel="alternate" hreflang="x-default" href="{b}">'.format(b=BASE)


def e(s):
    return html.escape(s, quote=True)


def pagina(caminho, idioma, titulo, descricao, corpo, ld=(), hreflang=False):
    t = TXT[idioma]
    prof = caminho.count("/")
    rel = "../" * prof
    canon = BASE + (caminho[:-10] if caminho.endswith("index.html") else caminho)
    lds = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    doc = f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<link rel="canonical" href="{canon}">
{ALT if hreflang else ''}
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="RiffSplit">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}{t['og']}">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}icon.png">
<link rel="stylesheet" href="{rel}style.css">
{lds}
</head>
<body>
<main>
<nav class="top">
<a class="marca" href="{rel}{'' if idioma=='pt' else idioma + '/'}index.html"><img src="{rel}icon.png" alt="" width="32" height="32"> RiffSplit</a>
<span class="links"><a href="{rel}guias/index.html">{t['guias']}</a><a href="{rel}suporte.html">{t['suporte']}</a></span>
</nav>
{corpo}
<footer>
<p><a href="{rel}index.html">Português</a> · <a href="{rel}en/index.html">English</a> · <a href="{rel}es/index.html">Español</a></p>
<p><a href="{rel}suporte.html">{t['suporte']}</a> · <a href="{rel}privacidade.html">{t['privacidade']}</a> · © 2026 RLA LABS</p>
<p class="legal">{t['legal']}</p>
</footer>
</main>
</body>
</html>
"""
    destino = os.path.join(RAIZ, caminho)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(doc)
    return canon


def selo(idioma, rel):
    t = TXT[idioma]
    return f'<p class="cta"><a href="{APP}"><img src="{rel}{t["badge"]}" alt="{t["badge_alt"]}" width="160" height="53"></a></p>'


def faq_ld(pares):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}


def faq_html(pares, titulo):
    itens = "\n".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in pares)
    return f'<section class="card faq"><h2>{titulo}</h2>\n{itens}\n</section>'


# ---------- Início ----------
FAQ_PT = [
    ("O RiffSplit precisa de internet?", "Não. A separação das faixas acontece no próprio iPhone, iPad ou Mac. A música não é enviada para nenhum servidor e não é preciso criar conta."),
    ("Quais faixas o RiffSplit separa?", "Seis: voz, bateria, baixo, guitarra, piano e outros. Cada uma tem volume, pan, mudo e solo no mixer."),
    ("Dá para mudar o tom sem mudar a velocidade?", "Sim. O tom vai até 12 semitons para cima ou para baixo e a velocidade de 50% a 150%, um sem alterar o outro."),
    ("O RiffSplit é assinatura?", "Não. O download é grátis e separa 30 segundos de cada música. Uma compra única no app libera músicas inteiras e a exportação, no iPhone, iPad e Mac com a mesma conta Apple."),
    ("Posso usar músicas do Spotify ou do Apple Music?", "Não. Músicas de streaming são protegidas e nenhum app consegue abri-las. Use arquivos seus ou com direito de uso, em MP3, AAC/M4A, ALAC, WAV, AIFF, FLAC ou vídeo."),
    ("Que formatos o RiffSplit exporta?", "A mixagem ou cada uma das 6 faixas, em AAC, WAV ou Apple Lossless (com o desbloqueio)."),
]

LISTA_GUIAS = "\n".join(
    f'<li><a href="guias/{g["slug"]}.html">{e(g["titulo_curto"])}</a></li>' for g in GUIAS)

corpo_pt = f"""
<header class="hero">
<img class="banner" src="img/banner-ptbr.jpg" alt="RiffSplit separando uma música em voz, bateria, baixo, guitarra, piano e outros no iPhone" width="1440" height="600">
<h1>RiffSplit: separe voz, bateria, baixo e guitarra de qualquer música, sem internet</h1>
<p class="lead">App de estudo musical para iPhone, iPad e Mac. Isole o seu instrumento, tire a sua parte, desacelere o solo e mude o tom, tudo no próprio aparelho, sem conta e sem assinatura.</p>
{selo('pt', '')}
</header>
<section class="card">
<h2>O que você faz com o RiffSplit</h2>
<ul class="lista-icones">
<li><b>🎚️ 6 faixas separadas:</b> voz, bateria, baixo, guitarra, piano e outros, no próprio aparelho.</li>
<li><b>🔇 Mixer de estudo:</b> volume, pan, M (mudo) e S (solo) em cada faixa. Tire a guitarra e toque no lugar.</li>
<li><b>🎼 Tom e velocidade independentes:</b> tom até ±12 semitons e velocidade de 50% a 150%.</li>
<li><b>🔁 Loop A–B:</b> arraste na forma de onda e repita só o trecho difícil.</li>
<li><b>⏱️ Metrônomo e contagem:</b> clique só no começo ou na música inteira, e contagem antes de tocar.</li>
<li><b>💾 Exportação:</b> a mixagem ou as 6 faixas em AAC, WAV ou Apple Lossless.</li>
<li><b>🔒 Offline e privado:</b> nada sai do aparelho; a biblioteca sincroniza pelo seu iCloud.</li>
</ul>
</section>
<section class="card">
<h2>Para quem é</h2>
<ul>
<li><b>Músicos de banda, igreja e estúdio:</b> tire a sua parte e ensaie com o playback sem o seu instrumento.</li>
<li><b>Quem está aprendendo:</b> ouça só o baixo ou só a bateria, desacelere sem mudar o tom e repita o trecho até sair.</li>
<li><b>Professores:</b> prepare material de aula com a faixa isolada em menos de um minuto.</li>
<li><b>Cantores:</b> coloque a música no seu tom e ensaie com a base sem a voz original.</li>
</ul>
</section>
<section class="card">
<h2>Guias práticos</h2>
<ul>
{LISTA_GUIAS}
</ul>
<p><a href="guias/index.html">Ver todos os guias</a></p>
</section>
<section class="card">
<h2>Como funciona</h2>
<ol>
<li>Toque em <b>+ Adicionar</b> e escolha um arquivo de música no app Arquivos.</li>
<li>O RiffSplit separa as 6 faixas no aparelho. Em um iPhone recente, uma música de 5 minutos leva menos de 1 minuto.</li>
<li>Abra o player e use o mixer, o tom, a velocidade e o loop para estudar.</li>
</ol>
<p class="muted">Cada música é separada uma única vez e fica na sua biblioteca.</p>
</section>
{faq_html(FAQ_PT, 'Perguntas frequentes')}
{selo('pt', '')}
"""

urls = []
urls.append(pagina("index.html", "pt",
    "RiffSplit: separe voz, bateria, baixo e guitarra de músicas no iPhone, sem internet",
    "App para iPhone, iPad e Mac que separa músicas em 6 faixas no próprio aparelho. Isole instrumentos, mude o tom, desacelere solos e estude sem internet, sem conta e sem assinatura.",
    corpo_pt, ld=[APP_LD, faq_ld(FAQ_PT)], hreflang=True))

corpo_en = f"""
<header class="hero">
<img class="banner" src="../img/banner-en.jpg" alt="RiffSplit splitting a song into vocals, drums, bass, guitar, piano and other on iPhone" width="1440" height="600">
<h1>RiffSplit: split vocals, drums, bass and guitar from any song, offline</h1>
<p class="lead">A music practice app for iPhone, iPad and Mac. Isolate your instrument, learn your part, slow down a solo and change the key, all on your device, with no account and no subscription.</p>
{selo('en', '../')}
</header>
<section class="card">
<h2>What you can do</h2>
<ul class="lista-icones">
<li><b>🎚️ 6 separate stems:</b> vocals, drums, bass, guitar, piano and other, processed on device.</li>
<li><b>🔇 Practice mixer:</b> volume, pan, mute and solo on every stem.</li>
<li><b>🎼 Independent key and speed:</b> key up to ±12 semitones, speed from 50% to 150%.</li>
<li><b>🔁 A–B loop:</b> drag on the waveform and repeat only the hard part.</li>
<li><b>⏱️ Metronome and count-in.</b></li>
<li><b>💾 Export:</b> the mix or all 6 stems as AAC, WAV or Apple Lossless.</li>
<li><b>🔒 Offline and private:</b> nothing leaves your device; your library syncs through your iCloud.</li>
</ul>
</section>
<section class="card">
<h2>Free download, one-time unlock</h2>
<p>The free version separates 30 seconds of each song. A one-time in-app purchase unlocks full songs and export on iPhone, iPad and Mac with the same Apple Account. No subscription.</p>
<p class="muted">Streaming songs (Spotify, Apple Music) are DRM protected and cannot be opened by any app. Use your own files or files you have the right to use.</p>
</section>
{selo('en', '../')}
"""
urls.append(pagina("en/index.html", "en",
    "RiffSplit: split vocals, drums, bass and guitar on iPhone, offline",
    "Music practice app for iPhone, iPad and Mac that splits songs into 6 stems on device. Isolate instruments, change key, slow down solos. No internet, no account, no subscription.",
    corpo_en, ld=[APP_LD], hreflang=True))

corpo_es = f"""
<header class="hero">
<img class="banner" src="../img/banner-es.jpg" alt="RiffSplit separando una canción en voz, batería, bajo, guitarra, piano y otros en el iPhone" width="1440" height="600">
<h1>RiffSplit: separa voz, batería, bajo y guitarra de cualquier canción, sin internet</h1>
<p class="lead">App de estudio musical para iPhone, iPad y Mac. Aísla tu instrumento, saca tu parte, baja la velocidad del solo y cambia el tono, todo en tu dispositivo, sin cuenta y sin suscripción.</p>
{selo('es', '../')}
</header>
<section class="card">
<h2>Lo que puedes hacer</h2>
<ul class="lista-icones">
<li><b>🎚️ 6 pistas separadas:</b> voz, batería, bajo, guitarra, piano y otros, en el propio dispositivo.</li>
<li><b>🔇 Mezclador de estudio:</b> volumen, paneo, silencio y solo en cada pista.</li>
<li><b>🎼 Tono y velocidad independientes:</b> tono hasta ±12 semitonos y velocidad de 50% a 150%.</li>
<li><b>🔁 Bucle A–B:</b> arrastra en la forma de onda y repite solo la parte difícil.</li>
<li><b>⏱️ Metrónomo y cuenta regresiva.</b></li>
<li><b>💾 Exportación:</b> la mezcla o las 6 pistas en AAC, WAV o Apple Lossless.</li>
<li><b>🔒 Sin conexión y privado:</b> nada sale de tu dispositivo; tu biblioteca se sincroniza con tu iCloud.</li>
</ul>
</section>
<section class="card">
<h2>Descarga gratis, desbloqueo único</h2>
<p>La versión gratis separa 30 segundos de cada canción. Una compra única dentro de la app desbloquea canciones completas y la exportación en iPhone, iPad y Mac con la misma cuenta de Apple. Sin suscripción.</p>
<p class="muted">Las canciones de streaming (Spotify, Apple Music) tienen DRM y ninguna app puede abrirlas. Usa tus propios archivos o archivos que tengas derecho a usar.</p>
</section>
{selo('es', '../')}
"""
urls.append(pagina("es/index.html", "es",
    "RiffSplit: separa voz, batería, bajo y guitarra en el iPhone, sin internet",
    "App de estudio musical para iPhone, iPad y Mac que separa canciones en 6 pistas en el dispositivo. Aísla instrumentos, cambia el tono y baja la velocidad. Sin internet, sin cuenta, sin suscripción.",
    corpo_es, ld=[APP_LD], hreflang=True))

# ---------- Guias ----------
indice = "\n".join(
    f'<li><a href="{g["slug"]}.html"><b>{e(g["titulo_curto"])}</b></a><br><span class="muted">{e(g["descricao"])}</span></li>'
    for g in GUIAS)
urls.append(pagina("guias/index.html", "pt", "Guias de estudo musical com faixas separadas · RiffSplit",
    "Guias práticos para tirar música de ouvido, isolar instrumentos, desacelerar solos e mudar o tom usando faixas separadas no iPhone, iPad e Mac.",
    f'<header class="texto"><h1>Guias de estudo com faixas separadas</h1><p class="lead">Passo a passo para músicos, quem está aprendendo e professores.</p></header>\n<section class="card"><ul class="guias">\n{indice}\n</ul></section>\n{selo("pt", "../")}',
    ld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Guias RiffSplit", "url": BASE + "guias/"}]))

for g in GUIAS:
    url = BASE + "guias/" + g["slug"] + ".html"
    passos = "\n".join(f"<li><b>{e(t)}:</b> {e(d)}</li>" for t, d in g["passos"])
    dicas = "\n".join(f"<li>{e(d)}</li>" for d in g["dicas"])
    relacionados = "\n".join(
        f'<li><a href="{o["slug"]}.html">{e(o["titulo_curto"])}</a></li>' for o in GUIAS if o["slug"] != g["slug"])
    corpo = f"""
<p class="trilha"><a href="../index.html">Início</a> › <a href="index.html">Guias</a></p>
<article>
<header>
<h1>{e(g['h1'])}</h1>
<p class="lead">{e(g['resposta'])}</p>
</header>
<figure class="arte"><img src="../img/{g['imagem']}" alt="{e(g['imagem_alt'])}" width="720" height="900" loading="lazy"></figure>
<section class="card">
<h2>Passo a passo no RiffSplit</h2>
<ol>
{passos}
</ol>
</section>
<section class="card">
<h2>{e(g['titulo_dicas'])}</h2>
<ul>
{dicas}
</ul>
</section>
{faq_html(g['faq'], 'Perguntas frequentes')}
{selo('pt', '../')}
<section class="card">
<h2>Outros guias</h2>
<ul>
{relacionados}
</ul>
</section>
<p class="muted">Atualizado em {e(g['data'])}.</p>
</article>
"""
    article = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"],
               "description": g["descricao"], "inLanguage": "pt-BR", "url": url,
               "image": BASE + "img/" + g["imagem"], "datePublished": g["data_iso"], "dateModified": g["data_iso"],
               "author": {"@type": "Organization", "name": "RLA LABS"},
               "publisher": {"@type": "Organization", "name": "RLA LABS", "logo": {"@type": "ImageObject", "url": BASE + "icon.png"}},
               "about": {"@type": "MobileApplication", "name": "RiffSplit", "url": BASE}}
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "inLanguage": "pt-BR",
             "tool": [{"@type": "HowToTool", "name": "RiffSplit (iPhone, iPad ou Mac)"}],
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d} for i, (t, d) in enumerate(g["passos"])]}
    trilha = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Guias", "item": BASE + "guias/"},
        {"@type": "ListItem", "position": 3, "name": g["titulo_curto"], "item": url}]}
    urls.append(pagina("guias/" + g["slug"] + ".html", "pt", g["title"], g["descricao"], corpo,
                       ld=[article, howto, faq_ld(g["faq"]), trilha]))

urls += [BASE + "suporte.html", BASE + "privacidade.html"]

# ---------- sitemap, robots, llms ----------
with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"<url><loc>{u}</loc><lastmod>{HOJE}</lastmod></url>\n")
    f.write("</urlset>\n")

with open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("""# Site do RiffSplit. Buscadores e assistentes de IA são bem-vindos.
User-agent: *
Allow: /
Disallow: /midia/
Disallow: /_fonte/

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: %ssitemap.xml
""" % BASE)

guias_llms = "\n".join(f"- [{g['titulo_curto']}]({BASE}guias/{g['slug']}.html): {g['descricao']}" for g in GUIAS)
with open(os.path.join(RAIZ, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(f"""# RiffSplit

> RiffSplit é um app de estudo musical para iPhone, iPad e Mac (Apple Silicon) que separa qualquer música em 6 faixas (voz, bateria, baixo, guitarra, piano e outros) no próprio aparelho, sem internet, sem nuvem e sem conta. Feito pela RLA LABS, no Brasil.

Fatos principais:
- Separação no aparelho, offline; a música não é enviada a servidores
- Mixer com volume, pan, mudo e solo por faixa
- Tom até ±12 semitons e velocidade de 50% a 150%, independentes
- Loop A–B na forma de onda, metrônomo e contagem
- Exportação da mixagem ou das 6 faixas em AAC, WAV ou Apple Lossless (com desbloqueio)
- Importa MP3, AAC/M4A, ALAC, WAV, AIFF, FLAC e vídeos; não abre músicas de streaming com DRM (Spotify, Apple Music)
- Modelo: download grátis separando 30 segundos por música; compra única no app libera músicas inteiras e exportação; sem assinatura
- Biblioteca sincronizada pelo iCloud do usuário
- Idiomas do app: português, inglês e espanhol
- Download: {APP}

## Páginas
- [Início]({BASE}): o que o app faz, para quem é e perguntas frequentes
- [English]({BASE}en/)
- [Español]({BASE}es/)
- [Suporte]({BASE}suporte.html): dúvidas de uso, compra, iCloud e reembolso
- [Privacidade]({BASE}privacidade.html)

## Guias
{guias_llms}
""")

print("\n".join(urls))
