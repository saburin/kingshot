# mirror.py（Argos Translate 対応版）

import requests
from bs4 import BeautifulSoup
import os
import argostranslate.package
import argostranslate.translate


# ---------------------------
# 翻訳処理
# ---------------------------
def translate_text_argos(text):
    installed_languages = argostranslate.translate.load_installed_languages()
    en = next(lang for lang in installed_languages if lang.code == "en")
    ja = next(lang for lang in installed_languages if lang.code == "ja")
    translation = en.get_translation(ja)
    return translation.translate(text)

# ---------------------------
# Wikiページ取得
# ---------------------------
def get_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    path = urlparse(url).path
    slug = os.path.basename(path)
    title = soup.find("h1").get_text()
    content_div = soup.find("div", {"class": "mw-parser-output"})
    paragraphs = content_div.find_all(['p', 'h2', 'h3'])
    content = "\n".join([p.get_text() for p in paragraphs])

    return slug, content

# ---------------------------
# Markdown保存
# ---------------------------
def save_markdown(title, content, path='pages'):
    os.makedirs(path, exist_ok=True)
    filename = f"{path}/{title.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"# {title}\n\n{content}")

# ---------------------------
# 実行部
# ---------------------------
if __name__ == "__main__":
    url = "https://kingshot.fandom.com/wiki/Kingshot"
    title, content_en = get_page(url)
    print("原文取得完了")
    content_ja = translate_text_argos(content_en)
    print("翻訳完了")
    save_markdown(title, content_ja)
    print("保存完了：", title)
