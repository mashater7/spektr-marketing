"""Add evidence-based, plain-language competitor explanations to the static deck.

Run from the repository root: python tools/expand_competitor_stories.py
The source HTML is intentionally kept mostly as authored to avoid reformatting
the large historical registry table.
"""

from __future__ import annotations

import html
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "yandex" / "competitors.html"
KEYS_SNAPSHOT = ROOT / "sources" / "keysso-проверка-2026-11-02.csv"

# All figures come from the dated Keys.so snapshot already printed on this page.
# Site and ad observations are from sources/03, sources/44, and sources/46.
PROFILES = [
    {
        "domain": "fvis.ru",
        "name": "Fresh Vision",
        "kind": "Технический подрядчик",
        "verdict": "Сильный пример доверия, но рекламное обещание и страница не всегда совпадают.",
        "site": "На сайте показывают проекты, команду, оборудование и отзывы. Компания продаёт техническое сопровождение мероприятий и отдельно студию.",
        "ad": "В поиске найдено предложение о техобеспечении с упоминанием 1000+ проектов. В одном видимом объявлении РСЯ заголовок говорит о выездном техобеспечении, а текст и ссылка — о студии.",
        "action": "Для нашей кампании «мероприятие под ключ» показать реальные проекты и команду. Объявление о выезде должно вести на страницу выездной услуги, а не в студию.",
        "source": "03-конкуренты-v2.md",
    },
    {
        "domain": "basslinegroup.ru",
        "name": "Bassline Group",
        "kind": "Звук и техническое сопровождение",
        "verdict": "В объявлении продают готовое решение и сразу называют цену комплекта.",
        "site": "По имеющимся материалам компания предлагает звук и техническое сопровождение. Полного разбора её сайта в нашем сентябрьском списке нет.",
        "ad": "В проверке встретились объявления «техобеспечение под ключ» с доставкой и монтажом и комплект звука за 25 000 ₽ в день.",
        "action": "Для «Спектра» сравнить два честных варианта: цену конкретного комплекта, если состав фиксирован, и расчёт проекта со специалистом. Чужую цену в наш прайс не переносить.",
        "source": "46-реклама-по-всей-семантике.md",
    },
    {
        "domain": "ipro.moscow",
        "name": "iPRO",
        "kind": "Аренда звука и света",
        "verdict": "Рекламных фраз в базе много; это не означает столько же клиентов.",
        "site": "В доступных материалах компания предлагает аренду звука и света с монтажом. Для оценки всей структуры сайта нужна отдельная проверка страниц.",
        "ad": "Объявление говорит о парке техники, монтаже и тестировании. Сервис связал с доменом много рекламных фраз, но они могут вести к одному и тому же предложению.",
        "action": "В нашем объявлении назвать услугу и состав работ. После запуска смотреть реальные поисковые запросы и отсекать тех, кому нужна лишь покупка или самовывоз техники.",
        "source": "46-реклама-по-всей-семантике.md",
    },
    {
        "domain": "rentaplazma.ru",
        "name": "РентаПлазма",
        "kind": "Экраны и техника",
        "verdict": "Много рекламных записей по экранам; с комплексной услугой сравниваем только пересекающиеся заказы.",
        "site": "Название и проверенные предложения относятся прежде всего к аренде экранов и другой техники. Это соперник для заказа экрана, но не образец всех услуг «Спектра».",
        "ad": "В Keys.so сохранены поисковые объявления и креативы РСЯ. Число записей показывает охват базы сервиса, а не месячный рекламный бюджет конкурента.",
        "action": "Для теста LED-экранов нужна своя страница: размеры, монтаж, сопровождение, условия аренды. Пока такой страницы нет, эти цифры не основание запускать кампанию.",
        "source": "44-keysso-рся-мобильный-директ.md",
    },
    {
        "domain": "otido-group.ru",
        "name": "OTIDO Group",
        "kind": "Широкий продакшн",
        "verdict": "Общие большие числа смешивают технику, шатры и другие услуги.",
        "site": "На сайте есть техническое обеспечение событий и другие направления; доверие строят через клиентов, технику и проекты.",
        "ad": "В архиве РСЯ видны длительно наблюдавшиеся объявления про шатры. Это подтверждает использование такого сообщения, но не его окупаемость и не спрос на звук.",
        "action": "Сравнивать со «Спектром» только пересекающиеся услуги. Для сайта «Спектра» показать свежие проекты и понятный состав работ, не гнаться за общей цифрой видимости OTIDO.",
        "source": "03-конкуренты-v2.md",
    },
    {
        "domain": "proektori.ru",
        "name": "Проектория",
        "kind": "Прокат оборудования",
        "verdict": "Понятно продают аренду звука с ценой, доставкой и настройкой.",
        "site": "Сайт устроен как каталог проекторов, телевизоров и звука с ценами. Это ближе к прокату техники, чем к полному техническому ведению события.",
        "ad": "По запросам о звуке встретилось объявление «Звук напрокат в Москве! От 3 500 руб/день!» с доставкой и настройкой. В нашей выборке оно связано с конкретной услугой, а не со всем бизнесом конкурента.",
        "action": "Сделать отдельную страницу звука и объявление, где ясно указаны состав, доставка и работа техника. Сравнивать по обращениям за подходящим проектом, а не по числу объявлений «Проектории».",
        "source": "03-конкуренты-v2.md",
    },
    {
        "domain": "provaibeindastry.ru",
        "name": "PROVAIBE INDUSTRY",
        "kind": "Технический продакшн",
        "verdict": "В обычном поиске база нашла мало фраз, а реклама техобеспечения встречалась.",
        "site": "Главная страница описывает технический продакшн и организацию событий под ключ. Подробную карточку сайта в сентябрьском разборе мы не составляли.",
        "ad": "В проверенных объявлениях компания обещает техническое сопровождение, профессиональную команду и смету. Небольшое число обычных запросов в базе не доказывает, что сайт никто не посещает.",
        "action": "Для B2B-объявления «Спектра» проверить акцент на команде, смете и ответственности за всю техническую часть. Результат проверять по заявкам агентств.",
        "source": "46-реклама-по-всей-семантике.md",
    },
    {
        "domain": "arenda-attrakcionov.ru",
        "name": "Аренда Аттракционов",
        "kind": "Широкий прокат; генераторы",
        "verdict": "Огромные общие показатели нельзя принимать за размер рынка техники для событий.",
        "site": "Мы отдельно изучали страницу аренды генераторов: цены за сутки, доставка и монтаж оплачиваются отдельно, ответ обещают в течение часа.",
        "ad": "Сайт попал в нашу выборку по нескольким фразам, но его база охватывает много категорий развлечений и проката. Поэтому тысячи найденных запросов и объявлений не относятся только к генераторам.",
        "action": "Сравнить именно предложение по электроснабжению. Если «Спектр» реально берёт на себя разводку и техника на смене, это стоит объяснять отдельно от аренды одного генератора.",
        "source": "03-конкуренты-v2.md",
    },
    {
        "domain": "soundman24.ru",
        "name": "Soundman24",
        "kind": "Звук, свет и экраны",
        "verdict": "Соединяют конкретную технику и обещание быстрого расчёта.",
        "site": "На сайте есть комплекты звука и света с ценами; после заявки обещают связаться в течение 30 минут.",
        "ad": "В объявлении об LED-экранах названы характеристики и повторён расчёт за 30 минут. В поиске также найдено предложение сценического света с работой художника по свету.",
        "action": "Показывать в рекламе проверяемые характеристики техники и срок ответа только тогда, когда команда «Спектра» действительно сможет их выдержать.",
        "source": "03-конкуренты-v2.md",
    },
    {
        "domain": "rl-tech.ru",
        "name": "RL-TECH",
        "kind": "Аренда звука и света",
        "verdict": "Делят клиентов по задачам и показывают цены комплектов.",
        "site": "Сайт предлагает комплекты с ценой первых суток, выезд специалиста и отдельные условия для агентств.",
        "ad": "Объявление о свете обещает аренду в Москве и бесплатную доставку комплектов. Рекламные записи по звуку и свету надо сопоставлять с конкретным набором услуг.",
        "action": "Разделить предложения «Спектра» для агентства и разового заказчика. Если доставка включена не всегда, не обещать её бесплатно в общем объявлении.",
        "source": "03-конкуренты-v2.md",
    },
]


def tag(text: str) -> str:
    return html.escape(text, quote=True)


def profile_id(domain: str) -> str:
    return "company-" + re.sub(r"[^a-z0-9]+", "-", domain.lower()).strip("-")


def build_profiles() -> str:
    blocks = []
    with KEYS_SNAPSHOT.open(encoding="utf-8-sig", newline="") as source:
        metrics = {row["домен"]: row for row in csv.DictReader(source, delimiter=";")}
    for p in PROFILES:
        domain = p["domain"]
        numbers = metrics[domain]
        organic = f'{int(numbers["органика_топ50"]):,}'.replace(',', ' ')
        ads = f'{int(numbers["поисковых_объявлений"]):,}'.replace(',', ' ')
        phrases = f'{int(numbers["фраз_контекста"]):,}'.replace(',', ' ')
        rsya = numbers["объявлений_РСЯ"]
        rsya_text = f'{int(rsya):,}'.replace(',', ' ') if rsya else 'нет числа'
        rsya_limit = '' if rsya else ' Отсутствие числа по РСЯ не доказывает отсутствие рекламы.'
        pid = profile_id(domain)
        direct = f"https://www.keys.so/ru/report?domain={domain}"
        search = f"https://www.keys.so/ru/ads?domain={domain}&amp;db=msk"
        source_label = (
            "Открыть разбор сайта ↗" if p["source"].startswith("03-")
            else "Открыть архив РСЯ ↗" if p["source"].startswith("44-")
            else "Открыть исходное исследование ↗"
        )
        blocks.append(
            f'<details class="competitor-profile" id="{pid}">'
            f'<summary><span class="profile-kind">{tag(p["kind"])}</span>'
            f'<strong>{tag(p["name"])} <small>{tag(domain)}</small></strong>'
            f'<span class="profile-verdict">{tag(p["verdict"])}</span></summary>'
            f'<div class="profile-body">'
            f'<p class="profile-metrics"><b>Цифры простыми словами.</b> В базе Keys.so: обычный поиск, топ‑50 — {organic}; '
            f'найденные объявления поиска — {ads}; рекламные фразы — {phrases}; записи РСЯ — {rsya_text}. '
            f'Первая цифра показывает, по скольким запросам сайт встретился среди первых 50 обычных результатов. '
            f'Остальные — объём рекламных записей в базе, а не клики, заявки или бюджет.{rsya_limit}</p>'
            f'<p><b>Что увидели на сайте.</b> {tag(p["site"])}</p>'
            f'<p><b>Как связан с рекламой.</b> {tag(p["ad"])}</p>'
            f'<p class="profile-decision"><b>Что это даёт «Спектру».</b> {tag(p["action"])}</p>'
            f'<p class="profile-links"><a href="{direct}" rel="noopener" target="_blank">Открыть отчёт Keys.so ↗</a>'
            f'<a href="{search}" rel="noopener" target="_blank">Открыть найденную рекламу ↗</a>'
            f'<a href="../sources/{p["source"]}" target="_blank">{source_label}</a>'
            f'<a href="../sources/46-реклама-по-всей-семантике.md" target="_blank">Открыть примеры поисковой рекламы ↗</a></p>'
            f'</div></details>'
        )
    return (
        '<section class="story-section" id="profiles"><p class="story-number">03 / КОМПАНИИ ПО ОДНОЙ</p>'
        '<h2>Что каждая проверенная компания означает для «Спектра»</h2>'
        '<p class="section-lead">Откройте компанию: сначала её предложение, затем конкретная реклама и практический вывод. '
        'Числа из таблицы выше описывают находки базы Keys.so, а не посещения, заявки или выручку конкурента.</p>'
        '<p class="story-verdict"><b>Как читать цифры:</b> «топ‑1 / топ‑3 / топ‑5» — вложенные количества запросов в обычном поиске, '
        'их не складывают; «топ‑50» — более широкий список фраз. «Объявления» и «рекламные фразы» — записи сервиса, '
        'а не люди и не расходы. Упоминания Алисы и цитируемость относятся к ответам ИИ, не к платной рекламе. '
        'Прогноз бюджета Директа — возможные расходы нашего теста при выбранных настройках, не бюджет конкурента. '
        '<a href="https://help.keys.so/paketnyj_analiz" rel="noopener" target="_blank">Что считает Keys.so ↗</a></p>'
        '<div class="competitor-profiles">' + ''.join(blocks) + '</div>'
        '<p class="story-caption">Разбор сайтов выполнен ранее, рекламные наблюдения и краткие отчёты датированы в источниках. '
        'Рынок и выдача меняются: перед запуском объявлений проверяем актуальную страницу и собственные условия «Спектра».</p>'
        '</section>'
    )


def practical_angle(category: str, title: str) -> str:
    subject = f"{category} {title}".lower()
    if any(word in subject for word in ("театр", "спектакл", "шоу-программ")):
        return "Сравнивать с театральным направлением, а не с арендой техники."
    if any(word in subject for word in ("генератор", "электростанц", "электроснаб")):
        return "Сравнивать условия электроснабжения: генератор, кабели, монтаж и дежурство техника."
    if any(word in subject for word in ("инсталляц", "продажа", "звукозапис", "студия")):
        return "Это смежная услуга; прямую конкуренцию в выездной аренде ещё нужно подтвердить."
    if any(word in subject for word in ("экран", "плазм", "проектор", "видеостен")):
        return "Сравнивать только аренду экранов и условия монтажа, не весь комплекс услуг."
    if any(word in subject for word in ("сцен", "подиум")):
        return "Сравнивать конкретную сцену или подиум, доставку и монтаж."
    if any(word in subject for word in ("звук", "свет", "прокат", "аренда")):
        return "Сравнивать состав комплекта, цену, доставку, монтаж и работу техника."
    if any(word in subject for word in ("техничес", "продакшн", "подрядчик")):
        return "Сравнивать ответственность за проект, команду, кейсы и путь к заявке."
    return "Проверить, совпадает ли реальная услуга с задачами «Спектра», прежде чем считать компанию прямым конкурентом."


def explain_registry_row(match: re.Match[str]) -> str:
    row = match.group(0)
    domain_match = re.search(r'<td data-label="Компания"><b>(.*?)</b><small>(.*?)</small>', row, re.S)
    if not domain_match:
        return row
    domain = html.unescape(re.sub(r"<[^>]+>", "", domain_match.group(1))).strip()
    category = html.unescape(re.sub(r"<[^>]+>", "", domain_match.group(2))).strip()
    title_match = re.search(r'<small class="registry-title">Заголовок: (.*?)</small>', row, re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1))) if title_match else ""
    ads_match = re.search(r'data-ads="(\d+)"', row)
    count = int(ads_match.group(1)) if ads_match else 0
    if count:
        observation = f"В нашей выборке из 97 фраз сайт встретился в рекламе по {count} из них. Это не все его объявления и не число заявок."
    else:
        observation = "В нашей выборке из 97 фраз рекламу сайта не встретили; это не доказывает, что её нет."
    if domain in {p["domain"] for p in PROFILES}:
        next_step = f'<a href="#{profile_id(domain)}">Читать понятный разбор компании ↓</a>'
    else:
        next_step = "Отчёт Keys.so по этому домену не открывали: цифр позиций и расходов здесь нет."
    explanation = (
        '<small class="registry-reader-note"><b>Что это значит:</b> '
        + tag(observation + " " + practical_angle(category, title))
        + " " + next_step + "</small>"
    )
    target = '<td data-label="Сайт">'
    if target not in row:
        return row
    return row.replace(target, target + explanation, 1)


def main() -> None:
    page = PAGE.read_text(encoding="utf-8")
    if 'id="profiles"' in page:
        raise SystemExit("Profiles already present: refusing to duplicate content")
    page = page.replace(
        '<a href="#compare">Сайт и реклама рядом</a>',
        '<a href="#profiles">10 разборов компаний</a><a href="#compare">Примеры объявлений</a>',
        1,
    )
    page = page.replace(
        '<section class="story-section" id="compare">',
        build_profiles() + '<section class="story-section" id="compare">',
        1,
    )
    for p in PROFILES:
        domain = p["domain"]
        old = f'<td><b>{domain}</b><a href="https://www.keys.so/ru/report?domain={domain}"'
        new = f'<td><b>{domain}</b><a href="#{profile_id(domain)}">Что это значит для «Спектра» ↓</a><a href="https://www.keys.so/ru/report?domain={domain}"'
        page = page.replace(old, new, 1)
    page = re.sub(r'<tr data-ads="\d+".*?</tr>', explain_registry_row, page, flags=re.S)
    page = page.replace('competitors.css?v=20261102', 'competitors.css?v=20261102b', 1)
    page = page.replace('competitors.js?v=20261102', 'competitors.js?v=20261102b', 1)
    PAGE.write_text(page, encoding="utf-8")
    print("Added 10 detailed profiles and notes to 68 registry rows")


if __name__ == "__main__":
    main()
