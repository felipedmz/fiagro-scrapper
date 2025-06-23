import os
import re
import sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://fiagro.com.br/"

def collect_urls() -> list[str]:
    resp = requests.get(BASE_URL, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    urls: set[str] = set()

    # Âncoras que apontam para /XXXX11/ ou /XXXXX11/
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(BASE_URL, href)
        if re.match(r"https://fiagro\.com\.br/[a-zA-Z]{4,5}11/?$", full):
            urls.add(full if full.endswith("/") else f"{full}/")

    if not urls:
        raise RuntimeError(
            "Nenhum Fiagro encontrado — a estrutura do site pode ter mudado."
        )

    return sorted(urls, key=str.lower)
#
def save(urls: list[str]) -> str:
    caminho = "./sources.txt"
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(urls))

    return caminho
#
def main():
    try:
        urls = collect_urls()
        caminho_saida = save(urls)
        print(f"{len(urls)} URLs salvos em: {caminho_saida}")
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)
#
main()
