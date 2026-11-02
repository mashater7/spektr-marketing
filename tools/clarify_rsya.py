"""Replace the confusing Moscow-only RSYA story with the actual evidence scope.

Run from repository root: python tools/clarify_rsya.py
Source: sources/44-keysso-рся-мобильный-директ.md and Keys.so's own
instruction on the meaning of parser region and detected ad records.
"""

from __future__ import annotations

import html
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "yandex" / "rsya.html"
DOCS = "https://help.keys.so/instrukciya_po_otchyotu_obyavleniya_v_rsya"

ADS = [
    ("rentaplazma", "rentaplazma.ru", 167, "LED-экраны, сенсорные панели, телевизоры", "Подходит для сравнения рекламы экранов. Все десять открытых записей сервис впервые обнаружил в Екатеринбурге, хотя тексты обещают доставку по Москве и области. По этой метке нельзя решить, где кампания показывалась.", "Экраны"),
    ("arendaattrakcionov", "arenda-attrakcionov.ru", 139, "Обогреватели, стенды и реквизит", "Это широкий прокат для событий. В десяти доступных объявлениях не нашлось предложения звука или света, поэтому не используем их как образец нашей основной услуги.", "Смежный прокат"),
    ("prointeractive", "pro-interactive.ru", 132, "Фотозоны, мастер-классы, кейтеринг", "События общие, но рекламируемая услуга другая. Не считаем эту компанию прямым конкурентом по звуку и свету только потому, что она встретилась в архиве.", "Другая услуга"),
    ("fvis", "fvis.ru", 118, "Техническое сопровождение, студия, трансляции", "Это близкий конкурент по комплексной технической части. В одном объявлении обещание выездной услуги ведёт на страницу студии: для «Спектра» проверяем, чтобы текст и страница говорили об одном.", "Близкий конкурент"),
    ("esmedia", "esmedia.ru", 110, "Экраны и оборудование для мероприятий", "Есть объявления с экранным оборудованием и доставкой по Москве и области. Запись, наблюдавшаяся 55 дней, показывает повторные находки сервисом, но не её заявки или прибыль.", "Экраны"),
    ("otido", "otido-group.ru", 20, "Шатры, сцены и техника", "Для «Спектра» полезны только пересекающиеся услуги. Долгое наблюдение объявлений о шатрах не доказывает, что реклама звука окупается.", "Смежные услуги"),
    ("lsmedia", "lsmedia-sound.ru", 19, "Звук, свет, доставка и монтаж", "Самый близкий текстовый пример в этих снимках: названы услуга и состав работ. Проверяем у себя ясное предложение, не копируя чужое объявление целиком.", "Близкий конкурент"),
    ("soundman24", "soundman24.ru", 17, "Звук и свет для частных мероприятий", "Доступные десять записей датированы 2024 годом. Они показывают прежние формулировки, но не подтверждают, что именно эти объявления работают сейчас.", "Близкий конкурент, старый снимок"),
]

NOT_OPENED = [
    "s-show.ru", "leaderstage.ru", "abk-production.ru", "livetechnics.ru",
    "sound-company.ru", "provaibeindastry.ru", "conferent.info",
    "covox-media.ru", "videostena.ru", "baby-theater.ru",
    "broadcaststudio.ru", "quiz.star-screens.ru", "zakazdj.ru",
    "techrezim.ru", "musprokat.ru", "arendaplazm.ru",
]


def safe(value: str) -> str:
    return html.escape(value, quote=True)


def company_card(item: tuple[str, str, int, str, str, str]) -> str:
    card_id, domain, total, offer, interpretation, tag = item
    asset = f"../assets/yandex-explained/{domain}-rsya.png"
    report = f"https://www.keys.so/ru/rsya/ads?domain={domain}"
    return (
        f'<article class="rsya-card" id="{card_id}"><div>'
        f'<p class="guide-kicker">{safe(tag)} · архив Keys.so: {total}</p>'
        f'<h3>{safe(domain)}</h3><p><b>О чём реклама:</b> {safe(offer)}.</p>'
        f'<p><b>Как читать:</b> {safe(interpretation)}</p>'
        f'<p class="guide-links"><a href="{report}" target="_blank" rel="noopener">Открыть отчёт в Keys.so ↗</a></p></div>'
        f'<details class="guide-details"><summary>Показать все 10 доступных объявлений {safe(domain)}</summary>'
        f'<a href="{asset}" target="_blank" rel="noopener" aria-label="Открыть полный снимок объявлений {safe(domain)}">'
        f'<img src="{asset}" alt="Десять доступных строк отчёта Keys.so для {safe(domain)}" loading="lazy"></a>'
        f'<p><a href="{asset}" target="_blank" rel="noopener">Открыть снимок в полном размере ↗</a></p>'
        f'</details></article>'
    )


def main() -> None:
    page = PAGE.read_text(encoding="utf-8")
    if 'id="show-all-rsya"' in page:
        raise SystemExit("RSYA page already clarified: refusing to duplicate work")
    before, rest = page.split('<header class="guide-hero">', 1)
    _, after = rest.split('<footer class="guide-footer">', 1)
    page = before + '''<header class="guide-hero"><p class="guide-kicker">ЯНДЕКС · РЕКЛАМА НА САЙТАХ И В ПРИЛОЖЕНИЯХ</p>
<h1>РСЯ: что показали объявления конкурентов</h1>
<p>Мы открыли 80 объявлений восьми компаний в архиве Keys.so. Ниже доступны все 80 снимков, а рядом — простое объяснение, что можно взять для рекламы «Спектра».</p></header>
<section class="guide-section" id="rsya-scope"><h2>Что именно мы проверили</h2>
<p>РСЯ — это объявления Яндекс Директа на сайтах и в приложениях сети, отдельно от рекламных строк в поиске. В прежний список для проверки попали 25 доменов. Демо Keys.so позволило открыть девять: по восьми мы увидели по 10 объявлений, по JackJack записей РСЯ сервис не нашёл. Остальные 16 из списка не открыли из-за лимита. Число 25 было нашей выборкой, а не числом конкурентов на рынке.</p>
<p class="guide-note"><b>Важная поправка:</b> раньше мы отсеивали объявления по столбцу «Регион показа» и писали «0 из 10 московских строк». Это была неверная логика: Keys.so указывает город, где его сборщик <em>впервые встретил</em> объявление. Этот город не раскрывает настройки географии рекламодателя. Поэтому RentaPlazma снова учитывается как пример рекламы экранов, но её охват в Москве и области по архиву не доказан. <a href="''' + DOCS + '''" target="_blank" rel="noopener">Как Keys.so собирает объявления ↗</a></p>
</section>
<section class="guide-section" id="rsya-examples"><h2>Три примера для быстрого просмотра</h2>
<p>Это первые примеры для обсуждения с клиентом. <a href="#all-rsya">Ниже можно открыть все 80 доступных объявлений восьми компаний ↓</a></p>
<div class="guide-two"><article><p class="guide-kicker">ЗВУК И СВЕТ</p><h3>LSmedia: доставка и монтаж</h3><p>В тексте названы техника и работы. Для «Спектра» это идея проверить понятное объявление про звук и свет с монтажом. Данных о заявках LSmedia нет.</p><a href="#lsmedia">Смотреть все 10 записей LSmedia ↓</a></article>
<article><p class="guide-kicker">ТЕХСОПРОВОЖДЕНИЕ</p><h3>Fresh Vision: предложение и страница</h3><p>Одно объявление обещает выездное сопровождение, а ссылка ведёт в раздел студии. Наше объявление должно вести на страницу той услуги, которую оно обещает.</p><a href="#fvis">Смотреть все 10 записей Fresh Vision ↓</a></article>
<article><p class="guide-kicker">ЭКРАНЫ</p><h3>ESmedia: конкретный состав услуги</h3><p>В объявлении перечислены виды экранов и сказано о доставке. Для «Спектра» это пример отдельного предложения об экранах, если мы можем подтвердить модели и условия монтажа.</p><a href="#esmedia">Смотреть все 10 записей ESmedia ↓</a></article></div>
<p class="guide-note">Эти тексты помогают придумать варианты объявлений, но не доказывают, что конкуренты на них заработали.</p></section>
<section class="guide-section" id="rsya-terms"><h2>Что означают числа в архиве</h2>
<div class="guide-table-wrap"><table><thead><tr><th>Надпись</th><th>Простое объяснение</th><th>Что нельзя из неё заключить</th></tr></thead><tbody>
<tr><td>«167 объявлений»</td><td>Столько записей сервис сохранил для домена; нам были доступны первые 10.</td><td>Что одновременно работали 167 кампаний или что они окупились.</td></tr>
<tr><td>«10 доступных»</td><td>Ограничение демо-просмотра. По восьми компаниям это 80 видимых записей.</td><td>Что мы изучили весь архив каждого конкурента.</td></tr>
<tr><td>«Регион показа»</td><td>Город первой находки объявления сборщиком Keys.so.</td><td>Что рекламодатель выбрал только этот город или исключил Москву.</td></tr>
<tr><td>«Дни в открутке»</td><td>Промежуток между первой и повторной находкой сервисом.</td><td>Количество показов людям, заявки или прибыль.</td></tr>
<tr><td>«0 записей» у JackJack</td><td>В базе РСЯ Keys.so этот домен не встретился.</td><td>Что у JackJack нет рекламы в поиске или никогда не было РСЯ.</td></tr>
</tbody></table></div><p><a href="''' + DOCS + '''" target="_blank" rel="noopener">Официальное объяснение полей Keys.so ↗</a> · <a href="https://help.keys.so/faq" target="_blank" rel="noopener">Почему архив может пропустить объявление ↗</a></p></section>
<section class="guide-section" id="all-rsya"><h2>Все 80 объявлений, которые удалось открыть</h2>
<p>Нажмите на компанию или откройте все снимки сразу. Это восемь изображений по десять записей; у каждой компании есть ссылка на живой отчёт Keys.so. Снимки показывают тексты и изображения, но не реальные показы, клики или заявки.</p>
<p><button class="guide-open-all" id="show-all-rsya" type="button">Показать все 80 объявлений</button></p>
<nav class="rsya-index" aria-label="Компании в архиве РСЯ">''' + ''.join(f'<a href="#{item[0]}">{safe(item[1])}</a>' for item in ADS) + '''</nav>
<div class="rsya-list">''' + ''.join(company_card(item) for item in ADS) + '''
<article class="rsya-card" id="jackjack"><div><p class="guide-kicker">ПО РСЯ В БАЗЕ НЕТ ЗАПИСЕЙ</p><h3>jackjack.ru</h3>
<p>Keys.so не нашёл записей РСЯ по этому домену. Это никак не отменяет объявления JackJack в <a href="search.html">рекламной выдаче поиска</a>: поиск и РСЯ — разные места показа. По нашей проверке нельзя утверждать, что компания никогда не использовала РСЯ.</p>
<p class="guide-links"><a href="https://www.keys.so/ru/rsya/ads?domain=jackjack.ru" target="_blank" rel="noopener">Проверить РСЯ в Keys.so ↗</a><a href="https://www.keys.so/ru/ads?domain=jackjack.ru&amp;db=msk" target="_blank" rel="noopener">Проверить поиск в Keys.so ↗</a></p></div>
<details class="guide-details"><summary>Показать ответ Keys.so по JackJack</summary><a href="../assets/yandex-explained/jackjack.ru-rsya.png" target="_blank" rel="noopener"><img src="../assets/yandex-explained/jackjack.ru-rsya.png" alt="Сообщение Keys.so: по jackjack.ru нет записей РСЯ" loading="lazy"></a></details></article>
</div></section>
<section class="guide-section guide-method" id="not-opened"><h2>Где остальные компании</h2>
<p>Ещё 16 доменов входили в первоначальный список 25, но их РСЯ-отчёты не открылись из-за дневного лимита. По ним нет проверенных десяти строк, поэтому мы не называем их объявлениями, которые проанализировали. Список 25 не охватывает весь рынок.</p>
<details class="guide-details"><summary>Показать 16 доменов без проверки РСЯ</summary><ul class="rsya-pending">''' + ''.join(f'<li><a href="https://www.keys.so/ru/rsya/ads?domain={safe(domain)}" target="_blank" rel="noopener">{safe(domain)} ↗</a></li>' for domain in NOT_OPENED) + '''</ul></details>
<p>Чтобы оценить рекламу именно для Москвы и области, нужны данные о настройках географии или наблюдение показов в нужном регионе. В чужом архиве таких настроек нет. <a href="competitors.html">Открыть общий реестр компаний и статус проверки →</a></p></section>
''' + '<footer class="guide-footer">' + after
    page = page.replace('guide.css?v=20261102d', 'guide.css?v=20261102e', 1)
    page = page.replace('guide.js?v=20261102c', 'guide.js?v=20261102d', 1)
    page = page.replace(
        'Что действительно нашли в московских строках, почему другие города не подходят для клиентского вывода и где посмотреть исходные снимки.',
        'Все доступные объявления конкурентов в РСЯ: 80 записей Keys.so, понятные выводы и ограничения архива.',
        1,
    )
    page = page.replace(
        '<title>Реклама в РСЯ: московские примеры — Спектр</title>',
        '<title>Реклама в РСЯ: все доступные объявления — Спектр</title>',
        1,
    )
    PAGE.write_text(page, encoding="utf-8")
    print("Clarified RSYA scope, parser regions, all 80 visible records, and 16 pending domains")


if __name__ == "__main__":
    main()
