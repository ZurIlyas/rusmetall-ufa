# Сборка сайта «Русметалл» (Уфа) из шаблона krovlya-kit. Анимация крыши на первом экране — шаблонная.
# python _build/build.py — собирает шаблон и кладёт готовый сайт в корень этой папки.
import re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
KIT = HERE.parent / 'krovlya-kit' / 'site-template'
subprocess.run([sys.executable, '-X', 'utf8', str(KIT / 'make_site.py'), str(KIT / 'companies' / 'rusmetall.json')], check=True)
SITE = KIT / 'sites' / 'rusmetall'
s = (SITE / 'index.html').read_text(encoding='utf-8')

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)

# отзывов у компании нет: пустую цитату и звёзды убираем, остаются ссылки на 2ГИС и ВКонтакте
s, k = re.subn(r'<div class="v3-testi"><div class="v3-testi-stars">★★★★★</div><div class="v3-testi-text"></div>.*?</div></div></div>', '', s, count=1, flags=re.S)
assert k == 1
rep('<div class="v3-testi-stars">★★★★★</div>', '', 2)
rep('.van-reviews { margin-top: 56px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));',
    '.van-reviews { margin-top: 56px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));')

# калькулятор считает не только кровлю
rep('Шаг 1 из 3 · Площадь кровли', 'Шаг 1 из 3 · Площадь кровли или фасада')
rep('aria-label="Площадь кровли в квадратных метрах"', 'aria-label="Площадь в квадратных метрах"')
rep('Шаг 2 из 3 · Тип кровли', 'Шаг 2 из 3 · Материал')
rep("'Здравствуйте! Хочу рассчитать кровлю. Площадь: ' + data.area + ' м². Тип: ' + data.label + '.'",
    "'Здравствуйте! Хочу рассчитать материал. Площадь: ' + data.area + ' м². Материал: ' + data.label + '.'")
rep('/* «Ван»: правки', '/* правки')

# демо: плашка сверху и авторы фото в подвале
rep('<body>\n', '<body>\n<div style="background:#111B30;color:#fff;font:600 13px/1.4 Manrope,system-ui,sans-serif;text-align:center;padding:9px 16px;position:relative;z-index:50;white-space:normal;max-width:100vw;box-sizing:border-box">Демо-версия сайта. Фото и цены стоят для примера: заменим на ваши.</div>\n')
rep('    <a href="https://wa.me/79177631165" target="_blank" rel="noopener">WhatsApp</a>\n', '''    <a href="https://wa.me/79177631165" target="_blank" rel="noopener">WhatsApp</a>
    <a href="https://t.me/+79177631165" target="_blank" rel="noopener">Telegram</a>
    <a href="mailto:xusnullin.r@yandex.ru">xusnullin.r@yandex.ru</a>
''')
rep('</footer>', '''  <div style="flex-basis:100%;margin-top:14px;font-size:12px;opacity:.55;line-height:1.5">ИП Хуснуллин Р. Р., ОГРНИП 311028003300192. Фото для примера: Unsplash, Wikimedia Commons и Openverse (CC0).</div>
</footer>''')

assert 'Ван' not in s and 'Краснодар' not in s
for d in ('frames', 'frames-sm', 'assets'):
    shutil.copytree(SITE / d, HERE / d, dirs_exist_ok=True)
(HERE / 'index.html').write_text(s, encoding='utf-8')
(HERE / '.nojekyll').write_text('')
print('готово:', HERE / 'index.html')
