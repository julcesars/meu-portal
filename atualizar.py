"""Busca feeds RSS e grava noticias.json. Somente biblioteca padrão do Python."""
import datetime as dt
import email.utils
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape

FEEDS = {
    'thenews': 'https://rss.beehiiv.com/feeds/j9teVW9Qmi.xml',
    'andreazza': 'https://omny.fm/shows/estad-o-not-cias/playlists/podcast.rss',
    'espn': 'https://news.google.com/rss/search?q=site%3Aespn.com.br%2Ffutebol+when%3A7d&hl=pt-BR&gl=BR&ceid=BR%3Apt-419',
    'sportv': 'https://news.google.com/rss/search?q=site%3Age.globo.com%2Fsportv+when%3A7d&hl=pt-BR&gl=BR&ceid=BR%3Apt-419',
    'palmeiras': 'https://news.google.com/rss/search?q=Palmeiras+%28site%3Aespn.com.br+OR+site%3Age.globo.com%29+when%3A7d&hl=pt-BR&gl=BR&ceid=BR%3Apt-419',
    'selecao': 'https://news.google.com/rss/search?q=%22sele%C3%A7%C3%A3o+brasileira%22+futebol+%28site%3Aespn.com.br+OR+site%3Age.globo.com%29+when%3A7d&hl=pt-BR&gl=BR&ceid=BR%3Apt-419',
}
OUT = os.path.join(os.path.dirname(__file__), 'noticias.json')
NS = {'media': 'http://search.yahoo.com/mrss/', 'content': 'http://purl.org/rss/1.0/modules/content/', 'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

def plain(t):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', t or ''))).strip()

def child_text(e, names):
    for name in names:
        node = e.find(name, NS)
        if node is not None and node.text:
            return node.text.strip()
    return ''

def image(e, summary):
    for path in ['media:thumbnail', 'media:content', 'enclosure', 'itunes:image']:
        for n in e.findall(path, NS):
            url = n.get('url') or n.get('href')
            if url and url.startswith('https://') and (path != 'enclosure' or n.get('type', '').startswith('image/')):
                return url
    m = re.search(r'<img[^>]+src=["\'](https://[^"\']+)', summary or '', re.I)
    return unescape(m.group(1)) if m else ''

def load(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (compatible; PersonalRSSPortal/1.0)', 'Accept':'application/rss+xml, application/atom+xml, application/xml, text/xml, */*'})
    with urllib.request.urlopen(req, timeout=35) as response:
        data = response.read(6_000_000)
    root = ET.fromstring(data)
    items = root.findall('.//item')
    if not items:
        items = root.findall('{http://www.w3.org/2005/Atom}entry')
    result = []
    for e in items[:15]:
        summary = child_text(e, ['description','content:encoded','{http://www.w3.org/2005/Atom}summary'])
        link = child_text(e, ['link'])
        if not link:
            n = e.find('{http://www.w3.org/2005/Atom}link')
            link = n.get('href', '') if n is not None else ''
        date = child_text(e, ['pubDate','{http://www.w3.org/2005/Atom}published','{http://www.w3.org/2005/Atom}updated'])
        if date:
            try:
                date = email.utils.parsedate_to_datetime(date).isoformat()
            except (TypeError, ValueError):
                pass
        if not link.startswith('http'):
            continue
        result.append({'title':plain(child_text(e,['title','{http://www.w3.org/2005/Atom}title'])),'url':link,'summary':plain(summary)[:500], 'date':date,'image':image(e,summary)})
    if not result:
        raise ValueError('Feed não trouxe itens válidos')
    return result

def main():
    try:
        with open(OUT, encoding='utf8') as f:
            existing = json.load(f)
    except (OSError, ValueError):
        existing = {}
    result = {'updated':dt.datetime.now(dt.timezone.utc).isoformat()}
    for key, url in FEEDS.items():
        try:
            result[key] = load(url)
            print(f'{key}: {len(result[key])} publicações')
        except Exception as exc:
            result[key] = existing.get(key, [])
            print(f'{key}: falhou ({exc}); mantidas {len(result[key])} publicações anteriores')
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
