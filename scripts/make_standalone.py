#!/usr/bin/env python3
"""Generate a fully self-contained standalone.html for deployment.
All CSS, JS, and images are inlined as base64 data URIs.
Output: standalone.html.
"""
import base64, os, sys

dist_assets = os.path.join(os.path.dirname(__file__), '..', 'dist', 'assets')
public_dir  = os.path.join(os.path.dirname(__file__), '..', 'public')
out_path    = os.path.join(os.path.dirname(__file__), '..', 'standalone.html')

try:
    css_file = next(f for f in os.listdir(dist_assets) if f.endswith('.css'))
    js_file  = next(f for f in os.listdir(dist_assets) if f.endswith('.js'))
except (StopIteration, FileNotFoundError):
    print("ERROR: dist/assets/ not found. Run 'npm run build' first.", file=sys.stderr)
    sys.exit(1)

with open(os.path.join(dist_assets, css_file)) as f: css = f.read()
with open(os.path.join(dist_assets, js_file))  as f: js  = f.read()

def b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

ail = b64(os.path.join(public_dir, 'brand-assets', 'ail-header.png'))
fav = b64(os.path.join(public_dir, 'favicon.png'))

for old, new in [
    ('`/brand-assets/ail-header.png`', f'`{ail}`'),
    ('"/brand-assets/ail-header.png"', f'"{ail}"'),
    ('`/favicon.png`', f'`{fav}`'),
    ('"/favicon.png"', f'"{fav}"'),
]:
    js = js.replace(old, new)

html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/png" href="{fav}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ART Investigation Lab</title>
  <style>
{css}
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="module">
{js}
  </script>
</body>
</html>'''

with open(out_path, 'w') as f:
    f.write(html)

size_kb = os.path.getsize(out_path) / 1024
img_hits = js.count('data:image/png;base64')
print(f"standalone.html written: {size_kb:.1f} KB  (base64 images in JS: {img_hits})")
