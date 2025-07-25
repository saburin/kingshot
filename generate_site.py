import os
import markdown
from jinja2 import Template

TEMPLATE_PATH = "templates/base.html"
PAGES_DIR = "pages"
OUTPUT_DIR = "output"

base_dir = os.path.dirname(__file__)  # スクリプトのあるディレクトリ
TEMPLATE_PATH = os.path.join(base_dir, TEMPLATE_PATH)
OUTPUT_DIR = os.path.join(base_dir, OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# テンプレート読み込み
with open(TEMPLATE_PATH, encoding='utf-8') as f:
    base = Template(f.read())

# Markdownページを処理
for filename in os.listdir(PAGES_DIR):
    if filename.endswith(".md"):
        name = filename[:-3]
        with open(f"{PAGES_DIR}/{filename}", encoding='utf-8') as f:
            md_text = f.read()
        html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
        rendered = base.render(title=name.title(), content=html)
        with open(f"{OUTPUT_DIR}/{name}.html", "w", encoding='utf-8') as out:
            out.write(rendered)

print("✅ HTML出力完了：output フォルダを確認してください")
