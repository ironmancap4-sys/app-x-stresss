#!/bin/bash
# Tải Be Vietnam Pro (400/500/600/800, bộ vietnamese + latin-ext + latin) từ npm và sinh fonts.css
# Dùng: install_fonts.sh <thư mục project>   -> <project>/assets/fonts/*.woff2 + <project>/fonts.css
set -e
P="$1"; T=$(mktemp -d); cd "$T"
npm pack @fontsource/be-vietnam-pro@5.3.0 >/dev/null 2>&1 && tar xzf fontsource-be-vietnam-pro-5.3.0.tgz
mkdir -p "$P/assets/fonts"
python3 - "$P" <<'PY'
import re, shutil, sys
P = sys.argv[1]; out = []
for w in [400, 500, 600, 800]:
    for block in re.findall(r'@font-face\s*\{[^}]+\}', open(f'package/{w}.css').read()):
        m = re.search(r'files/(be-vietnam-pro-(vietnamese|latin-ext|latin)-\d+-normal\.woff2)', block)
        if not m: continue
        fn = m.group(1); shutil.copy('package/files/' + fn, f'{P}/assets/fonts/{fn}')
        ur = re.search(r'unicode-range:\s*([^;]+);', block).group(1)
        out.append(f"    @font-face {{ font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: {w}; font-display: block; src: url('assets/fonts/{fn}') format('woff2'); unicode-range: {ur}; }}")
open(f'{P}/fonts.css', 'w').write("\n".join(out) + "\n"); print(len(out), "font faces")
PY
