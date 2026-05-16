from pypdf import PdfReader
import re, os

reader = PdfReader(r'C:\Users\miaay\Documents\Claude\Projects\RTW\source\CH451-600.pdf')
chapter_pages = {}
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        m = re.match(r'^Chapter (\d+)', text.strip())
        if m:
            ch_num = int(m.group(1))
            if ch_num not in chapter_pages:
                chapter_pages[ch_num] = i

def get_chapter(n):
    start = chapter_pages[n]
    end = chapter_pages.get(n+1, len(reader.pages))
    text = ''
    for i in range(start, end):
        t = reader.pages[i].extract_text()
        if t:
            text += t + '\n'
    return text

out_dir = r'C:\Users\miaay\Documents\Claude\Projects\RTW\source_extract'
os.makedirs(out_dir, exist_ok=True)

for ch in range(501, 511):
    if ch in chapter_pages:
        text = get_chapter(ch)
        out_path = os.path.join(out_dir, f'ch{ch}_source.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Wrote ch{ch} ({len(text)} chars)')
    else:
        print(f'Chapter {ch} NOT FOUND')

print('Done. chapters found:', sorted(k for k in chapter_pages if 500 <= k <= 515))
