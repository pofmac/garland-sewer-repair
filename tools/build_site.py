"""Builds GarlandSewerRepair.com from tools/content.py.

Run from the repo root:  python3 tools/build_site.py
Pages are plain HTML at the repo root, plus sitemap.xml and robots.txt.
"""
import html
import json
from datetime import date
from pathlib import Path

from content import (AREAS, BRAND, CITY, COST_GUIDE, HOME, HOW_IT_WORKS, PHONE, SERVICES, STATE, ZIPS)

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.garlandsewerrepair.com"
UPDATED = "October 2026"
PAGES = []


def esc(text):
    return html.escape(str(text), quote=True)


def tel():
    return "tel:+1" + "".join(c for c in PHONE if c.isdigit())[-10:]


def call_button(cls="btn btn-call"):
    if PHONE:
        return f'<a class="{cls}" href="{tel()}">📞 Call {esc(PHONE)}</a>'
    if cls.startswith("btn"):
        return '<span class="btn btn-soon">📞 Phone line opening soon</span>'
    return f'<span class="{cls} soon">Phone line opening soon</span>'


def write_page(path, text):
    (ROOT / path).write_text(text)
    PAGES.append(path)


def head(title, desc, path, schema=None):
    schemas = schema if isinstance(schema, list) else ([schema] if schema else [])
    url = SITE + "/" + ("" if path == "index.html" else path)
    ld = "".join(f'\n    <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n    </script>' for s in schemas)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:url" content="{url}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔧</text></svg>">
    <link rel="stylesheet" href="styles.css">{ld}
</head>
<body>
"""


def header(active=""):
    links = "".join(f'<a class="nav-link{" active" if s["slug"] + ".html" == active else ""}" href="{s["slug"]}.html">{esc(s["nav"])}</a>'
                    for s in SERVICES)
    return f"""    <div class="topbar">Sewer line repair and replacement in {CITY}, {STATE}, through licensed local plumbers. {call_button("topbar-call")}</div>
    <header class="site-header">
        <a class="logo" href="index.html"><span class="logo-mark">🔧</span>{CITY}<span>Sewer Repair</span></a>
        <nav class="nav">{links}<a class="nav-link{" active" if active == COST_GUIDE["slug"] + ".html" else ""}" href="{COST_GUIDE["slug"]}.html">Costs</a></nav>
    </header>
"""


def footer():
    svc = "".join(f'<a href="{s["slug"]}.html">{esc(s["title"])}</a>' for s in SERVICES)
    areas = "".join(f'<a href="sewer-repair-{a["slug"]}-tx.html">Sewer repair in {esc(a["name"])}</a>' for a in AREAS)
    return f"""    <footer class="site-footer">
        <div class="footer-grid">
            <div><h4>Services</h4>{svc}<a href="{COST_GUIDE["slug"]}.html">Sewer repair costs</a></div>
            <div><h4>Areas</h4><a href="index.html">Sewer repair in {CITY}</a>{areas}<p class="zips">{CITY} ZIP codes: {", ".join(ZIPS)}</p></div>
            <div><h4>About</h4><a href="about.html">How this service works</a><a href="privacy.html">Privacy</a>{call_button("footer-call")}</div>
        </div>
        <p class="disclaimer">{BRAND} is an independent referral service. We are not a plumbing company; we connect
        callers with licensed, insured local plumbers who do the work and set their own prices. Prices on this site are
        typical ranges, not quotes. In an emergency involving gas, electricity or danger to life, call 911.</p>
        <p class="disclaimer">© {date.today().year} {BRAND}. Last updated {UPDATED}.</p>
    </footer>
</body>
</html>
"""


def cta_box(text="Talk to a licensed plumber about your sewer line."):
    return f"""
            <section class="cta-box">
                <p>{esc(text)}</p>
                {call_button()}
            </section>"""


def faq_html(faq):
    return "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)


def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def service_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "url": url,
            "serviceType": "Sewer line repair", "areaServed": {"@type": "City", "name": f"{CITY}, Texas"},
            "provider": {"@type": "Organization", "name": BRAND, "url": SITE + "/"}}


def crumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{path}"}]}


def service_cards():
    return "".join(f"""
                <a class="card" href="{s['slug']}.html"><h3>{esc(s['title'])}</h3><p>{esc(s['short'])}</p><span class="card-more">Learn more →</span></a>"""
                   for s in SERVICES)


def build_home():
    faq = [(f"How much does sewer repair cost in {CITY}?",
            "Typical ranges are a few hundred dollars to clear a clog, $1,000 to $4,000 for a spot repair, and $3,000 to "
            "$25,000 or more for full replacement. A camera inspection is the best way to know which you need."),
           ("What causes sewer lines to break in Garland?", " ".join(t for _, t in HOME["why"])),
           ("Do I need to dig up my yard?", "Not always. Trenchless lining or pipe bursting can repair or replace many "
            "lines through one or two small access holes.")]
    page = [head(f"Sewer Repair {CITY} TX | Sewer Line Repair & Replacement",
                 f"Sewer line repair, replacement, trenchless repair and camera inspection in {CITY}, TX. Get connected with "
                 "a licensed local plumber. Typical costs, warning signs and what to expect.", "index.html",
                 [service_schema(f"Sewer repair in {CITY}, TX", HOME["lede"], SITE + "/"), faq_schema(faq)]),
            header(), f"""
    <section class="hero">
        <div class="hero-inner">
            <p class="eyebrow">{CITY}, Texas</p>
            <h1>{esc(HOME['title'])}</h1>
            <p class="lede">{esc(HOME['lede'])}</p>
            <div class="hero-actions">{call_button()}<a class="btn btn-ghost" href="sewer-camera-inspection.html">What a camera inspection shows</a></div>
            <ul class="hero-points"><li>Licensed, insured local plumbers</li><li>Repair, replacement &amp; trenchless</li><li>Written estimates before work starts</li></ul>
        </div>
    </section>
    <main class="main">
        <section class="section">
            <h2>Signs your sewer line needs attention</h2>
            <div class="grid-2">{"".join(f'<div class="sign"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in HOME['signs'])}</div>
        </section>
        <section class="section">
            <h2>Sewer services in {CITY}</h2>
            <div class="card-grid">{service_cards()}
            </div>
        </section>
        <section class="section band">
            <h2>Why sewer lines fail in {CITY}</h2>
            <div class="grid-3">{"".join(f'<div class="why"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in HOME['why'])}</div>
        </section>
        <section class="section">
            <h2>How it works</h2>
            <ol class="steps">{"".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in HOW_IT_WORKS)}</ol>
        </section>
        <section class="section">
            <h2>Common questions</h2>
            <div class="faq">{faq_html(faq)}</div>
            <p class="more-links"><a href="{COST_GUIDE['slug']}.html">See typical sewer repair costs →</a></p>
        </section>{cta_box()}
    </main>
""", footer()]
    write_page("index.html", "".join(page))


def build_service(s):
    path = s["slug"] + ".html"
    lists = (f'<h2>When it\'s needed</h2><ul class="checks">{"".join(f"<li>{esc(w)}</li>" for w in s["when"])}</ul>'
             if s.get("when") else "")
    steps = f'<h2>What to do right now</h2><ol class="numbered">{"".join(f"<li>{esc(w)}</li>" for w in s["steps"])}</ol>' if s.get("steps") else ""
    note = f'<p class="note">{esc(s["not"])}</p>' if s.get("not") else ""
    others = "".join(f'<a class="chip" href="{o["slug"]}.html">{esc(o["title"])}</a>' for o in SERVICES if o is not s)
    title = f"{s['title']} {CITY} TX"
    page = [head(f"{title} | {BRAND}", f"{s['short']} {s['title']} in {CITY}, TX: what it is, when you need it and "
                 "typical costs.", path,
                 [service_schema(f"{s['title']} in {CITY}, TX", s["short"], f"{SITE}/{path}"), faq_schema(s["faq"]), crumbs(s["title"], path)]),
            header(path), f"""
    <section class="page-hero">
        <div class="hero-inner">
            <p class="crumb"><a href="index.html">Sewer repair in {CITY}</a> › {esc(s['title'])}</p>
            <h1>{esc(s['title'])} in {CITY}, TX</h1>
            <p class="lede">{esc(s['short'])}</p>
            {call_button()}
        </div>
    </section>
    <main class="main narrow">
        <section class="section"><h2>What it is</h2><p>{esc(s['what'])}</p>{note}</section>
        <section class="section">{steps}{lists}</section>
        <section class="section"><h2>Typical cost</h2><p>{esc(s['cost'])}</p><p class="more-links"><a href="{COST_GUIDE['slug']}.html">Full cost guide →</a></p></section>
        <section class="section"><h2>Questions</h2><div class="faq">{faq_html(s['faq'])}</div></section>{cta_box()}
        <section class="section"><h2>Other sewer services</h2><div class="chips">{others}</div></section>
    </main>
""", footer()]
    write_page(path, "".join(page))


def build_cost():
    c = COST_GUIDE
    path = c["slug"] + ".html"
    rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in c["rows"])
    page = [head(f"{c['title']} TX (2026 Price Guide) | {BRAND}", c["short"] + f" Sewer line costs in {CITY}, TX.", path,
                 crumbs(c["title"], path)),
            header(path), f"""
    <section class="page-hero"><div class="hero-inner">
        <p class="crumb"><a href="index.html">Sewer repair in {CITY}</a> › Costs</p>
        <h1>{esc(c['title'])}</h1><p class="lede">{esc(c['short'])}</p>
    </div></section>
    <main class="main narrow">
        <section class="section"><table class="cost-table"><thead><tr><th>Job</th><th>Typical range</th></tr></thead><tbody>{rows}</tbody></table>
        <p class="note">{esc(c['note'])}</p></section>
        <section class="section"><h2>What changes the price</h2><div class="grid-2">{"".join(f'<div class="sign"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in c['factors'])}</div></section>{cta_box("Get a written estimate from a licensed local plumber.")}
    </main>
""", footer()]
    write_page(path, "".join(page))


def build_area(a):
    path = f"sewer-repair-{a['slug']}-tx.html"
    page = [head(f"Sewer Repair {a['name']} TX | {BRAND}", f"Sewer line repair, replacement and trenchless options in "
                 f"{a['name']}, TX, near {CITY}. Connect with a licensed local plumber.", path,
                 [service_schema(f"Sewer repair in {a['name']}, TX", a["text"], f"{SITE}/{path}"), crumbs(f"Sewer repair in {a['name']}", path)]),
            header(), f"""
    <section class="page-hero"><div class="hero-inner">
        <p class="crumb"><a href="index.html">Sewer repair in {CITY}</a> › {esc(a['name'])}</p>
        <h1>Sewer Repair in {esc(a['name'])}, TX</h1><p class="lede">{esc(a['text'])}</p>{call_button()}
    </div></section>
    <main class="main narrow">
        <section class="section"><h2>Sewer services in {esc(a['name'])}</h2><div class="card-grid">{service_cards()}</div></section>{cta_box()}
    </main>
""", footer()]
    write_page(path, "".join(page))


def build_about():
    steps = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in HOW_IT_WORKS)
    page = [head(f"How This Service Works | {BRAND}", f"{BRAND} is an independent referral service connecting {CITY} "
                 "homeowners with licensed local plumbers.", "about.html"), header(), f"""
    <main class="main narrow">
        <h1>How this service works</h1>
        <p>{BRAND} is an independent referral service for homeowners in and around {CITY}, Texas. We are not a plumbing
        company. When you call, we connect you with a licensed, insured local plumber who handles sewer work. The plumber
        does the job, sets the price and gives you the warranty.</p>
        <ol class="steps">{steps}</ol>
        <h2>What we promise</h2>
        <ul class="checks"><li>We only refer you to plumbers licensed by the Texas State Board of Plumbing Examiners</li>
        <li>You get a written estimate before any work starts, and you're free to say no</li>
        <li>Calls may be recorded to make sure your request reaches the plumber correctly</li></ul>
        <h2>About the information on this site</h2>
        <p>Our guides are written in plain language to help you understand your options. Prices are typical ranges from
        national cost guides and plumber price lists, not quotes. Always get a written estimate, and for large jobs,
        consider a second opinion.</p>
    </main>
""", footer()]
    write_page("about.html", "".join(page))


def build_privacy():
    page = [head(f"Privacy | {BRAND}", f"How {BRAND} handles your information.", "privacy.html"), header(), f"""
    <main class="main narrow">
        <h1>Privacy</h1>
        <p>This website does not use forms, accounts or advertising trackers. When you call, the phone service records
        the call details (your number, the time and length of the call) and may record the call. We use this only to
        pass your request to a local plumber and to check that calls are handled well. We share your details only with
        the plumber who will help you, and we never sell them.</p>
        <p>To ask about or delete call records, call the number on this site.</p>
    </main>
""", footer()]
    write_page("privacy.html", "".join(page))


def build_sitemap():
    today = date.today().isoformat()
    urls = "".join(f"  <url>\n    <loc>{SITE}/{'' if p == 'index.html' else p}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
                   for p in PAGES)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + urls + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    build_home()
    for s in SERVICES:
        build_service(s)
    build_cost()
    for a in AREAS:
        build_area(a)
    build_about()
    build_privacy()
    build_sitemap()
    print(f"Built {len(PAGES)} pages plus sitemap.xml and robots.txt")
