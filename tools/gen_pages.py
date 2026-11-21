#!/usr/bin/env python3
"""Generate the Croatian service landing pages (/<slug>/index.html) from index.html.

Prices are copied from the price list in index.html, so the bazna cijena markup stays
identical to the homepage. Re-run after any price change in index.html.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUKER = "https://buker.hr/salon/beauty-by-daria"
SITE = "https://daria-lash.com"

REVIEWS = {'ekstenzije-trepavica': [('Barbara Maletić', 'Odlično iskustvo od početka do kraja! Daria je jako ljubazna, profesionalna i ugodna, a rezultat je prekrasan – trepavice izgledaju točno onako kako sam željela. Topla preporuka svima koji žele kvalitetne i lijepe ekstenzije trepavica.'),
    ('Nika Bahmet', 'Prezadovoljna sam uslugom! Daria je vrlo profesionalna, ljubazna i pažljiva. Trepavice su ispale točno onako kako sam željela – prirodne, uredne i prekrasno oblikovane.'),
    ('Ive Ma', 'Trepavice su napravljene vrlo uredno i precizno, a rezultat je jednostavno prekrasan. Odmah se vidi da se radi s puno pažnje i ljubavi prema detaljima.')], 'lash-lift': [('Hana Perković', 'Danas sam došla sa Trešnjevke na, kako kažu, najbolji lash lift. I stvarno je najbolji. Daria je jedan veliki profesionalac. Izrazito pristupačna.'),
    ('Lucija', 'Daria je jako pedantna i profesionalna, a lash lift nikad ljepši! Lokacija je pristupačna, prostor jako lijepo uređen i atmosfera ugodna.'),
    ('Ema Bahmet', 'Radila sam trepavice i brow lift, a rezultat je fantastičan, upravo onakav kakav sam željela. Trepavice izgledaju predivno, uredno i prirodno, a brow lift je savršeno oblikovao obrve.')], 'puder-obrve': [('Kristina Šajnović', 'Jako sam zadovoljna njenom uslugom, pedantnošću i naravno finalnim rezultatom. Radile smo puder obrve koje je skroz prilagodila mom licu i obliku mojih prirodnih obrva.'),
    ('Mimi Tomic', 'Veoma sam zadovoljna, jako lijepe puder obrve, hvala puno ❤️')], 'depilacija': [('Eva Marinovic', 'Radila sam depilacije s 4 vrste voska i pinceta i Lash &amp; Brow Lift. Jako sam zadovoljna rezultatom! Sve radi jako uredno, precizno i pažljivo. Veliki plus je i parking.')], 'obrve': [('Darija Čiček', 'Do sada mi nitko nije napravio tako savršene obrve kao Daria. Presretna sam što sam našla tako pedantnu i profesionalnu osobu kojoj se mogu prepustiti u ruke bez straha.'),
    ('Ema Bahmet', 'Radila sam trepavice i brow lift, a rezultat je fantastičan, upravo onakav kakav sam željela. Brow lift je savršeno oblikovao obrve.'),
    ('Dora Žugec', 'Lijep je ugođaj, a obrve su dobro i lijepo napravljene. Jako sam zadovoljna.')]}

PAGES = [
    {
        "slug": "ekstenzije-trepavica",
        "card": "ekstenzije trepavica",
        "nav": "Ekstenzije trepavica",
        "title": "Ekstenzije trepavica Sesvete | Ugradnja i nadopuna — Beauty by Daria",
        "desc": "Ugradnja ekstenzija trepavica u Sesvetama (Soblinec): ugradnja 55 €, nadopuna 35 €, skidanje 10 €. Prirodan ili bujniji izgled, prilagođen tvom oku. Rezerviraj online.",
        "h1": "Ekstenzije trepavica <em>u Sesvetama</em>",
        "lead": "Ugradnja, nadopuna i skidanje ekstenzija trepavica u Beauty by Daria studiju u Soblincu, nekoliko minuta od centra Sesveta.",
        "groups": ["Ekstenzije trepavica"],
        "body": [
            ("Kako izgleda tretman", [
                "Na početku zajedno odaberemo izgled — od prirodnog, jedva primjetnog do bujnijeg i izraženijeg. Dužina, zakrivljenost i gustoća prilagođavaju se obliku oka i tvojim prirodnim trepavicama.",
                "Ugradnja traje oko 1 h 45 min, nadopuna oko 1 h 30 min, a skidanje oko 30 min. Tretman se radi ležeći i zatvorenih očiju, pa ga većina klijentica iskoristi za opuštanje.",
            ]),
            ("Nadopuna", [
                "Prirodne trepavice stalno se izmjenjuju, pa s njima otpada i dio ekstenzija. Nadopuna vraća puni izgled bez ponovne ugradnje od nule. Kada je vrijeme za nadopunu, ovisi o tvom ciklusu rasta trepavica i njezi — dogovorimo to na prvom terminu.",
            ]),
            ("Edukacija", [
                "Za one koje žele raditi trepavice, nudim i edukaciju za ugradnju ekstenzija sa start setom (oko 8 h).",
            ]),
        ],
        "faq": [
            ("Koliko košta ugradnja ekstenzija trepavica?", "Ugradnja je 55 €, nadopuna 35 €, a skidanje 10 €. Cijene su iste kao i 10. 9. 2026. (bazna cijena)."),
            ("Koliko traje ugradnja?", "Ugradnja traje oko 1 h 45 min, a nadopuna oko 1 h 30 min."),
            ("Štete li ekstenzije prirodnim trepavicama?", "Kad su pravilno ugrađene i njegovane, ekstenzije ne bi trebale oštetiti prirodne trepavice. Na terminu dobiješ upute za njegu, a skidanje se radi u salonu, ne kod kuće."),
            ("Kako rezervirati termin?", "Termin rezerviraš online preko Bukera, gdje vidiš sve slobodne termine."),
        ],
    },
    {
        "slug": "lash-lift",
        "card": "lash lift",
        "nav": "Lash & brow lift",
        "title": "Lash lift i brow lift Sesvete | Bojanje trepavica — Beauty by Daria",
        "desc": "Lash lift 35 €, brow lift 30 €, brow lift s bojanjem 35 € i bojanje trepavica 6 € u Sesvetama (Soblinec). Podignute trepavice i uredne obrve bez ekstenzija.",
        "h1": "Lash lift i brow lift <em>u Sesvetama</em>",
        "lead": "Podignute, izražene trepavice i uredne obrve bez ekstenzija — lash lift, brow lift i bojanje u studiju u Soblincu.",
        "groups": ["Lash &amp; Brow lift"],
        "body": [
            ("Lash lift", [
                "Lash lift podiže i zakrivljuje tvoje prirodne trepavice od korijena, pa oko izgleda otvorenije, a trepavice duže — bez ekstenzija i bez svakodnevnog uvijača. Uz lash lift može se napraviti i bojanje trepavica za još izraženiji pogled.",
            ]),
            ("Brow lift", [
                "Brow lift (laminacija obrva) usmjerava dlačice obrva i fiksira ih u željenom obliku, pa obrve izgledaju gušće i urednije. Može se napraviti samostalno ili zajedno s bojanjem obrva bojom.",
            ]),
            ("Za koga je", [
                "Za sve koje žele prirodan, a izražen izgled bez održavanja kakvo traže ekstenzije. Prije tretmana kratko porazgovaramo o tvojim trepavicama i obrvama i o tome što želiš postići.",
            ]),
        ],
        "faq": [
            ("Koliko košta lash lift?", "Lash lift je 35 €, bojanje trepavica 6 €, brow lift 30 €, a brow lift s bojanjem obrva 35 €."),
            ("Koja je razlika između lash lifta i ekstenzija?", "Lash lift uvija tvoje prirodne trepavice i ne dodaje nove. Ekstenzije se lijepe na prirodne trepavice i daju dužinu i gustoću."),
            ("Mogu li spojiti lash lift i brow lift?", "Da, oba tretmana mogu se napraviti u istom terminu. Rezerviraj obje usluge na Bukeru."),
        ],
    },
    {
        "slug": "obrve",
        "nav": "Laminacija i oblikovanje obrva",
        "card": "laminacija obrva",
        "title": "Laminacija obrva Sesvete | Brow lift, bojanje, threading — Beauty by Daria",
        "desc": "Laminacija obrva (brow lift) 30 €, s bojanjem 35 €, threading obrva 8 € u Sesvetama (Soblinec). Gušće, uredne obrve u obliku koji ti pristaje. Rezerviraj online.",
        "h1": "Laminacija i oblikovanje obrva <em>u Sesvetama</em>",
        "lead": "Laminacija obrva (brow lift), bojanje i oblikovanje koncem u studiju u Soblincu, nekoliko minuta od centra Sesveta.",
        "groups": [("Lash &amp; Brow lift", ["Brow lift", "Brow lift + bojanje obrva bojom"]), ("Threading", ["Threading obrva"])],
        "body": [
            ("Laminacija obrva (brow lift)", [
                "Laminacija obrva usmjerava dlačice i fiksira ih u željenom smjeru, pa obrve izgledaju gušće, punije i urednije. Na engleskom se zove brow lamination ili brow lift. Rezultat je prirodan, a obrve ujutro ne treba posebno slagati.",
                "Laminacija se može napraviti sama ili zajedno s bojanjem obrva bojom, kad želiš izraženiju nijansu.",
            ]),
            ("Oblikovanje koncem (threading)", [
                "Threading je oblikovanje obrva koncem, bez voska. Precizan je i za fine dlačice, a dobro dođe i kao završni korak nakon laminacije.",
            ]),
            ("Trajni rezultat", [
                "Ako želiš obrve koje izgledaju uređeno bez svakodnevne šminke, pogledaj i <a href=\"/puder-obrve/\">puder obrve</a>, tehniku trajne šminke.",
            ]),
        ],
        "faq": [
            ("Koliko košta laminacija obrva?", "Laminacija obrva (brow lift) je 30 €, a laminacija s bojanjem obrva bojom 35 €. Threading obrva je 8 €."),
            ("Koja je razlika između laminacije i puder obrva?", "Laminacija oblikuje tvoje prirodne dlačice i ne dira kožu. Puder obrve su trajna šminka koja popunjava obrve pigmentom."),
            ("Mogu li uz laminaciju obrva napraviti i lash lift?", "Da, oba tretmana mogu se napraviti u istom terminu. Rezerviraj obje usluge na Bukeru."),
            ("Kako rezervirati termin?", "Termin rezerviraš online preko Bukera, gdje vidiš sve slobodne termine."),
        ],
    },
    {
        "slug": "puder-obrve",
        "card": "puder obrve",
        "nav": "Puder obrve i permanent make up",
        "title": "Puder obrve i permanent make up Sesvete | Trajna šminka — Beauty by Daria",
        "desc": "Puder obrve 150 €, permanent lips 200 €, korekcije 100 € — trajna šminka u Sesvetama (Soblinec). Oblik prilagođen tvom licu i prirodnim obrvama.",
        "h1": "Puder obrve i permanent make up <em>u Sesvetama</em>",
        "lead": "Trajna šminka obrva i usana u studiju u Soblincu: oblik i nijansa prilagođeni tvom licu i prirodnim obrvama.",
        "groups": ["Permanent make up"],
        "body": [
            ("Puder obrve", [
                "Puder obrve su tehnika trajne šminke koja daje mekan, sjenčani izgled, kao da su obrve lagano našminkane puderom. Prije rada zajedno odaberemo oblik i nijansu prema tvom licu i obliku tvojih prirodnih obrva.",
            ]),
            ("Permanent lips", [
                "Permanent make up usana naglašava konturu i daje usnama ujednačenu boju koja ne nestaje tijekom dana.",
            ]),
            ("Korekcija", [
                "Trajna šminka s vremenom blijedi. Korekcija obrva nakon 12 mjeseci i korekcija usana osvježavaju boju i oblik.",
            ]),
        ],
        "faq": [
            ("Koliko koštaju puder obrve?", "Puder obrve su 150 €, a korekcija nakon 12 mjeseci 100 €. Permanent lips su 200 €, a korekcija usana 100 €."),
            ("Hoće li obrve izgledati prirodno?", "Oblik i nijansa biraju se prema tvom licu i prirodnim obrvama, tako da rezultat bude prilagođen tebi."),
            ("Kako rezervirati?", "Termin rezerviraš online preko Bukera, u kategoriji Trajna šminka."),
        ],
    },
    {
        "slug": "depilacija",
        "card": "depilacija voskom",
        "nav": "Depilacija i threading",
        "title": "Depilacija voskom Sesvete | Brazilska, noge, threading — Beauty by Daria",
        "desc": "Depilacija toplim voskom u Sesvetama (Soblinec): brazilska 16 €, cijele noge 21 €, pazuh 9 €, nadusnica 7 €. Threading obrva 8 €. Rezerviraj online.",
        "h1": "Depilacija voskom i threading <em>u Sesvetama</em>",
        "lead": "Profesionalna depilacija toplim voskom i threading lica u studiju u Soblincu — brzo, uredno i s njegom kože.",
        "groups": ["Depilacija", "Threading"],
        "body": [
            ("Depilacija toplim voskom", [
                "Depilacija se radi toplim voskom, a uz vosak se po potrebi koristi i pinceta za fine dlačice. Radim depilaciju lica, ruku, pazuha, bikini i brazilsku depilaciju te depilaciju nogu.",
            ]),
            ("Threading", [
                "Threading je uklanjanje dlačica koncem, bez voska. Precizan je za oblikovanje obrva te za nadusnicu i bradu.",
            ]),
        ],
        "faq": [
            ("Koliko košta brazilska depilacija?", "Brazilska depilacija je 16 €, bikini 10 €, cijele noge 21 €, a pazuh 9 €. Sve cijene su u cjeniku ispod."),
            ("Kolika trebaju biti dlačice za depilaciju voskom?", "Vosak najbolje hvata dlačice od nekoliko milimetara, pa je najbolje ne brijati se nekoliko dana prije termina."),
            ("Što je threading?", "Threading je uklanjanje dlačica koncem. Koristi se za obrve, nadusnicu i bradu."),
        ],
    },
]


def price_groups(index_html):
    groups = {}
    for name, items in re.findall(r'<h3 class="price-group">(.*?)</h3>\s*<ul class="price-list">(.*?)</ul>', index_html, re.S):
        groups[name] = items.strip("\n")
    return groups


def pick(items_html, names):
    if not names:
        return items_html
    keep = [l for l in items_html.split("\n") if re.search(r"<li><span>(.*?)</span>", l) and html.unescape(re.search(r"<li><span>(.*?)</span>", l).group(1)) in names]
    return "\n".join(keep)


def offers(items_html):
    out = []
    for name, price in re.findall(r'<li><span>(.*?)</span><span class="dots"></span><span class="price">([\d,]+) €</span>', items_html):
        out.append({"@type": "Offer", "name": html.unescape(name), "price": price.replace(",", "."), "priceCurrency": "EUR"})
    return out


def build(index_html, page, groups):
    head = index_html.split("<title>")[0]
    head = head.replace('href="images/', 'href="/images/').replace('href="fonts/', 'href="/fonts/').replace('href="style.css', 'href="/style.css')
    tracking = re.search(r"(<script>\s*window\.dataLayer.*?</script>\s*<!-- Google tag.*?</script>\s*<script>.*?</script>)", index_html, re.S).group(1)
    tail = index_html[index_html.index('<footer class="footer">'):]
    url = f"{SITE}/{page['slug']}/"

    price_html = ""
    all_offers = []
    for g in page["groups"]:
        g, names = g if isinstance(g, tuple) else (g, None)
        items = pick(groups[g], names)
        price_html += f'      <h3 class="price-group">{g}</h3>\n      <ul class="price-list">\n{items}\n      </ul>\n'
        all_offers += offers(items)

    body_html = ""
    for h, paras in page["body"]:
        body_html += f"      <h2>{h}</h2>\n" + "".join(f"      <p>{p}</p>\n" for p in paras)

    faq_html = "".join(
        f'      <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>\n' for q, a in page["faq"]
    )

    reviews_html = "".join(
        f'      <div class="review-card">\n        <div class="review-stars">★★★★★</div>\n'
        f'        <p class="review-text">„{t}“</p>\n        <div class="review-author">\n'
        f'          <div class="review-avatar">{n[0]}</div>\n          <div>\n'
        f'            <div class="review-name">{n}</div>\n            <div class="review-src">Google recenzija</div>\n'
        f'          </div>\n        </div>\n      </div>\n'
        for n, t in REVIEWS.get(page["slug"], [])
    )
    if reviews_html:
        reviews_html = (
            '<section class="section">\n  <div class="container">\n    <h2 class="center">Što kažu klijentice</h2>\n'
            f'    <div class="reviews">\n{reviews_html}    </div>\n'
            '    <p class="center"><a href="https://www.google.com/maps?cid=6743832913942023737" target="_blank" rel="noopener">Sve recenzije na Googleu →</a></p>\n'
            '  </div>\n</section>\n\n'
        )

    others = "".join(
        f'        <a href="/{p["slug"]}/">{p["nav"]}</a>\n' for p in PAGES if p["slug"] != page["slug"]
    )

    ld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": re.sub(r"<[^>]+>", "", page["h1"]),
            "url": url,
            "areaServed": ["Sesvete", "Zagreb"],
            "provider": {
                "@type": "BeautySalon",
                "name": "Beauty by Daria",
                "url": f"{SITE}/",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Obrež 20",
                    "postalCode": "10360",
                    "addressLocality": "Sesvete-Soblinec",
                    "addressCountry": "HR",
                },
            },
            "offers": all_offers,
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Beauty by Daria", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": page["nav"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]
            ],
        },
    ]

    return f"""{head}<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:image" content="{SITE}/images/og-image.jpg">
<meta property="og:locale" content="hr_HR">
<meta property="og:site_name" content="Beauty by Daria">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="/fonts/cormorant-garamond-500-latin.woff2" crossorigin>
<link rel="stylesheet" href="/style.css?v=20261121">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{tracking}
</head>
<body>

<header class="nav">
  <div class="container nav-inner">
    <a href="/" class="brand">
      <img src="/images/logo.png" alt="Beauty by Daria — Beauty Studio">
    </a>
    <nav>
      <a href="/#usluge">Usluge</a>
      <a href="/#cjenik">Cjenik</a>
      <a href="/#o-meni">O meni</a>
      <a href="/#recenzije">Recenzije</a>
      <a href="/#kontakt">Kontakt</a>
    </nav>
    <a href="{BUKER}" target="_blank" rel="noopener" class="btn btn-primary nav-cta">Rezerviraj</a>
  </div>
</header>

<main>
<section class="hero hero-sub">
  <div class="container hero-inner">
    <p class="breadcrumb"><a href="/">Beauty by Daria</a> / {page['nav']}</p>
    <h1>{page['h1']}</h1>
    <p class="lead">{page['lead']}</p>
    <div class="hero-cta">
      <a href="{BUKER}" target="_blank" rel="noopener" class="btn btn-primary">Rezerviraj termin</a>
      <a href="#cijene" class="btn btn-ghost">Cijene</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose">
{body_html}  </div>
</section>

<section id="cijene" class="section section-alt">
  <div class="container">
    <h2 class="center">Cijene</h2>
    <div class="pricing">
{price_html}    </div>
    <p class="price-note">Uz svaku cijenu istaknuta je i bazna cijena — cijena koja je za tu uslugu vrijedila 10. rujna 2026. (Zakon o zaštiti potrošača, NN 132/2026). Cijeli cjenik: <a href="/#cjenik">naslovnica</a> · <a href="/cjenik/">CSV</a>.</p>
  </div>
</section>

{reviews_html}<section class="section">
  <div class="container prose">
    <h2>Česta pitanja</h2>
{faq_html}  </div>
</section>

<section class="section section-dark">
  <div class="container center">
    <h2 class="center light">Rezerviraj svoj <em>termin</em></h2>
    <p class="center lead-dark">Beauty by Daria, Obrež 20, 10360 Sesvete-Soblinec. Svi slobodni termini su na Bukeru.</p>
    <div class="center" style="margin:32px 0 40px">
      <a href="{BUKER}" target="_blank" rel="noopener" class="btn btn-primary btn-lg">Rezerviraj na Bukeru →</a>
    </div>
    <p class="other-services">Ostale usluge:
{others}    </p>
  </div>
</section>
</main>

{tail}"""


def local_links():
    links = " · ".join(f'<a href="/{p["slug"]}/">{p["card"]} Sesvete</a>' for p in PAGES)
    return f'<p class="local-links"><!-- local-links -->{links}<!-- /local-links --></p>'


def main():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    index_html = re.sub(r'<p class="local-links"><!-- local-links -->.*?<!-- /local-links --></p>', local_links(), index_html)
    (ROOT / "index.html").write_text(index_html, encoding="utf-8")
    groups = price_groups(index_html)
    for page in PAGES:
        out = ROOT / page["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(build(index_html, page, groups), encoding="utf-8")
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
