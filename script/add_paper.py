#!/usr/bin/env python3
"""
Script per aggiungere automaticamente paper al sito.
Uso: python add_paper.py papers.json
"""

import json
import re
import sys

# Varianti del tuo nome da mettere in grassetto
MY_NAMES = ["Nicolo Carpentieri", "Nicolò Carpentieri", "N. Carpentieri"]

def bold_my_name(authors: str) -> str:
    """Mette in grassetto il mio nome nella lista autori."""
    for name in MY_NAMES:
        authors = authors.replace(name, f"<strong>{name}</strong>")
    return authors

def generate_paper_html(paper: dict) -> str:
    """Genera l'HTML per un singolo paper."""
    # Autori con nome in grassetto
    authors = bold_my_name(paper["authors"])
    
    # Link (PDF, Slides, Code, ecc.)
    links = []
    if paper.get("pdf"):
        links.append(f'<a href="{paper["pdf"]}">[PDF]</a>')
    if paper.get("slides"):
        links.append(f'<a href="{paper["slides"]}">[Slides]</a>')
    if paper.get("code"):
        links.append(f'<a href="{paper["code"]}">[Code]</a>')
    if paper.get("arxiv"):
        links.append(f'<a href="{paper["arxiv"]}">[arXiv]</a>')
    links_html = " &ndash; ".join(links) if links else ""
    
    html = f'''<tr>
<td style="text-align:right">[<strong>{paper["venue"]}</strong>]</td>
<td style="text-align:center">    </td>
<td style="text-align:left"><em>{paper["title"]}</em></td>
</tr>
<tr>
<td style="text-align:right"></td>
<td style="text-align:center"></td>
<td style="text-align:left">{authors}</td>
</tr>
<tr>
<td style="text-align:right"></td>
<td style="text-align:center"></td>
<td style="text-align:left">In <em>{paper["conference"]}</em></td>
</tr>
<tr>
<td style="text-align:right"></td>
<td style="text-align:center"></td>
<td style="text-align:left">{links_html}</td>
</tr>
<tr>
<td style="text-align:right"> </td>
<td style="text-align:center"></td>
<td></td>
</tr>
'''
    return html

def is_paper_duplicate(html: str, paper: dict) -> bool:
    """Controlla se il paper è già presente nell'HTML (cerca per titolo)."""
    return paper["title"] in html

def add_papers_to_html(html_file: str, papers_file: str):
    """Aggiunge i paper all'HTML (in cima alla lista)."""
    # Leggi papers da JSON
    with open(papers_file, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # Leggi HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Genera HTML per tutti i nuovi paper (con controllo duplicati)
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
    
    # Inserisci dopo </thead>\n<tbody>
    marker = "</thead>\n<tbody>\n"
    if marker not in html:
        marker = "</thead>\n<tbody>"
    
    html = html.replace(marker, marker + new_papers_html)
    
    # Scrivi HTML aggiornato
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
