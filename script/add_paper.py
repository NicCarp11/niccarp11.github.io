#!/usr/bin/env python3
"""
Script per aggiungere automaticamente paper al sito.
Uso: python add_paper.py papers.json
"""

import json
import sys

# Varianti del tuo nome da mettere in grassetto
MY_NAMES = ["Nicolo Carpentieri", "Nicolò Carpentieri", "N. Carpentieri"]

def bold_my_name(authors: str) -> str:
    """Mette in grassetto il mio nome nella lista autori."""
    for name in MY_NAMES:
        authors = authors.replace(name, f"<strong>{name}</strong>")
    return authors

def generate_paper_html(paper: dict) -> str:
    """Genera l'HTML per una pub-card."""
    authors = bold_my_name(paper["authors"])

    links = []
    if paper.get("pdf"):
        links.append(f'<a href="{paper["pdf"]}">PDF</a>')
    else:
        links.append('<span class="disabled">PDF soon</span>')
    if paper.get("slides"):
        links.append(f'<a href="{paper["slides"]}">Slides</a>')
    if paper.get("code"):
        links.append(f'<a href="{paper["code"]}" target="_blank" rel="noopener">Code</a>')
    else:
        links.append('<span class="disabled">Code soon</span>')
    if paper.get("arxiv"):
        links.append(f'<a href="{paper["arxiv"]}" target="_blank" rel="noopener">arXiv</a>')
    links_html = "\n              ".join(links)

    award_html = ""
    if paper.get("award"):
        award_html = f'            <p class="pub-award"><i class="fa-solid fa-award"></i> {paper["award"]}</p>\n'

    return f'''          <article class="pub-card">
            <div class="pub-header">
              <span class="pub-venue">{paper["venue"]}</span>
            </div>
{award_html}            <h3 class="pub-title">{paper["title"]}</h3>
            <p class="pub-authors">{authors}</p>
            <p class="pub-conf">In {paper["conference"]}</p>
            <div class="pub-links">
              {links_html}
            </div>
          </article>

'''

def is_paper_duplicate(html: str, paper: dict) -> bool:
    """Controlla se il paper è già presente nell'HTML (cerca per titolo)."""
    return paper["title"] in html

def add_papers_to_html(html_file: str, papers_file: str):
    """Aggiunge i paper all'HTML (in cima alla lista pub-list)."""
    with open(papers_file, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    new_papers_html = ""
    added = 0
    skipped = 0
    for paper in papers:
        if is_paper_duplicate(html, paper):
            print(f"⚠️  Saltato (già esistente): {paper['title']}")
            skipped += 1
        else:
            new_papers_html += generate_paper_html(paper)
            added += 1

    if added == 0:
        print("ℹ️  Nessun nuovo paper da aggiungere.")
        return

    marker = '<div class="pub-list">\n'
    if marker not in html:
        print("❌ Marker '<div class=\"pub-list\">' non trovato in", html_file)
        sys.exit(1)

    html = html.replace(marker, marker + new_papers_html, 1)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Aggiunti {added} paper a {html_file}")
    if skipped > 0:
        print(f"⚠️  Saltati {skipped} paper (duplicati)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python add_paper.py papers.json")
        print("Oppure: python add_paper.py papers.json index.html")
        sys.exit(1)

    papers_file = sys.argv[1]
    html_file = sys.argv[2] if len(sys.argv) > 2 else "index.html"

    add_papers_to_html(html_file, papers_file)
