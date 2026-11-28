# VPI Privacy Notice

Applies to the public VPI release (`VPI-Setup-<version>-EU-Public.exe`, `VPI-<version>-EU-Public.zip` and the two `.wotmod` files in them) published at <https://github.com/gmrkinichuk-gif/vpi-releases/releases>. The English text governs; a Ukrainian translation follows. Last reviewed: 27 November 2026.

## 1. Who is responsible

VPI is made by Vladyslav Kinichuk (metronom_). Questions and requests: [GitHub Issues of vpi-releases](https://github.com/gmrkinichuk-gif/vpi-releases/issues). VPI has no account system, no analytics, no advertising and no telemetry.

## 2. Data that stays on your computer

VPI writes only to `mods/configs/vpi-index/` in your game folder. Nothing from this folder is sent anywhere.

| File | Contents |
| --- | --- |
| `config.json` | Your VPI settings, including whether you agreed to public statistics. |
| `history-<account ID>.json` | Summaries of your own last battles per vehicle (VPI, tier, three main metrics, time) for the "Trend" and "session" views. |
| `update-check.json` | The latest VPI version seen on GitHub, its compatibility and the time of the check. |
| `install-state.json`, `build.json`, `legal/` | Installation details (build type, versions, hash of a page VPI wrote), licence documents. |

The installer works offline. "Remove VPI" deletes the VPI packages and installation files but keeps `config.json` and your history; delete the folder yourself to remove them.

## 3. Ratings from the VPI service (only after you agree)

Ratings are **off** until you switch them on in VPI settings, page **Дані EU / EU data** (`public_data_consent`). Without that consent the public build sends no player data anywhere.

With consent, VPI sends HTTPS requests to the official VPI service `https://vpi-ratings.duckdns.org` only:

- `POST /v1/ratings` with up to 30 pairs of *public account ID and nickname* of players the game shows you: your own account in the hangar, players in your battle and on its loading screen, in the post-battle results and contacts visible in your friends list. Players hidden by the Anonymizer and bots are skipped.
- `GET /v1/catalog` for the vehicle table (tier, class, role, hit points, view range).

The service looks up these public statistics through the Wargaming Public API with its own application ID and returns ratings. It keeps at most 100 player records in memory at a time, each for 15 to 60 seconds, and keeps no copy on disk. It does not log requests, URLs, bodies, IDs, nicknames or IP addresses; for rate limiting it uses a keyed hash of the source address that is never stored and expires within three minutes. The game keeps up to 100 received ratings in memory for 10 minutes. Switching consent off stops the requests and clears that memory at once.

Until Wargaming confirms its permission in writing, the service does not query Wargaming, and VPI shows no ratings from it.

## 4. Update check

At most once every 6 hours, and only in the hangar, VPI asks the public GitHub API (`https://api.github.com/repos/gmrkinichuk-gif/vpi-releases/releases/latest`) which VPI release is the latest. The request carries no token and no personal data apart from what any web request reveals to GitHub (your IP address and the header `User-Agent: VPI-mod/<version>`); see [GitHub's Privacy Statement](https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement). VPI downloads and installs nothing. Turn it off with "Notify about updates" in VPI settings. Clicking the update line opens the releases page in your browser.

## 5. What VPI never does

VPI does not read or send your password, e-mail, payment data, chat, replays or files outside its folder. It does not sell or share data. The public build contains no Wargaming application ID, no access token and no code that calls the Wargaming API directly.

## 6. Your choices

Withdraw consent at any time on **Дані EU / EU data**; delete `mods/configs/vpi-index/` to erase local data. Your statutory rights are not limited by this notice.

---

# Повідомлення про приватність VPI

Стосується публічного релізу VPI (`VPI-Setup-<версія>-EU-Public.exe`, `VPI-<версія>-EU-Public.zip` і двох `.wotmod` у них), опублікованого на <https://github.com/gmrkinichuk-gif/vpi-releases/releases>. Чинним є англійський текст, нижче переклад. Перевірено 27 листопада 2026 року.

## 1. Хто відповідає

VPI створює Vladyslav Kinichuk (metronom_). Питання й запити: [GitHub Issues репозиторію vpi-releases](https://github.com/gmrkinichuk-gif/vpi-releases/issues). У VPI немає облікових записів, аналітики, реклами й телеметрії.

## 2. Дані, які лишаються на вашому комп’ютері

VPI пише лише в `mods/configs/vpi-index/` у теці гри. Нічого з цієї теки нікуди не надсилається.

| Файл | Вміст |
| --- | --- |
| `config.json` | Ваші налаштування VPI, зокрема чи погодилися ви на публічну статистику. |
| `history-<ID акаунта>.json` | Підсумки ваших останніх боїв на кожній машині (VPI, рівень, три головні показники, час) для «Тренду» й «сесії». |
| `update-check.json` | Остання версія VPI на GitHub, її сумісність і час перевірки. |
| `install-state.json`, `build.json`, `legal/` | Дані встановлення (тип збірки, версії, хеш сторінки, яку записав VPI), ліцензійні документи. |

Інсталятор працює без мережі. «Видалити VPI» прибирає пакети й файли встановлення, але лишає `config.json` та історію; щоб видалити їх, видаліть теку самостійно.

## 3. Рейтинги від сервісу VPI (лише після вашої згоди)

Рейтинги **вимкнені**, доки ви не ввімкнете їх у налаштуваннях VPI на сторінці **Дані EU** (`public_data_consent`). Без цієї згоди публічна збірка нікуди не надсилає даних гравців.

Після згоди VPI надсилає HTTPS-запити лише до офіційного сервісу `https://vpi-ratings.duckdns.org`:

- `POST /v1/ratings` з не більш ніж 30 парами *публічний ID акаунта та нік* гравців, яких вам показує гра: ваш акаунт в ангарі, гравці вашого бою та його екрана завантаження, післябойових результатів і видимі контакти у списку друзів. Гравців, прихованих Anonymizer, і ботів пропущено.
- `GET /v1/catalog` для таблиці техніки (рівень, клас, роль, міцність, огляд).

Сервіс отримує цю публічну статистику через Wargaming Public API зі своїм ідентифікатором застосунку й повертає рейтинги. Він тримає в пам’яті не більше 100 записів гравців одночасно, кожен 15–60 секунд, і нічого не зберігає на диску. Він не журналює запити, URL, тіла, ID, ніки чи IP-адреси; для обмеження частоти використовує ключований хеш адреси джерела, який не зберігається й зникає щонайбільше за три хвилини. Гра тримає до 100 отриманих рейтингів у пам’яті 10 хвилин. Вимкнення згоди одразу зупиняє запити й очищає цю пам’ять.

До письмового підтвердження дозволу від Wargaming сервіс не звертається до Wargaming, і VPI не показує рейтингів від нього.

## 4. Перевірка оновлень

Не частіше ніж раз на 6 годин і лише в ангарі VPI запитує публічний API GitHub (`https://api.github.com/repos/gmrkinichuk-gif/vpi-releases/releases/latest`), який реліз VPI останній. Запит не містить токена й персональних даних, крім того, що бачить GitHub у будь-якому вебзапиті (ваша IP-адреса й заголовок `User-Agent: VPI-mod/<версія>`); див. [Privacy Statement GitHub](https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement). VPI нічого не завантажує й не встановлює. Вимкнути: «Повідомляти про оновлення» в налаштуваннях VPI. Клік по рядку оновлення відкриває сторінку релізів у браузері.

## 5. Чого VPI ніколи не робить

VPI не читає й не надсилає пароль, пошту, платіжні дані, чат, реплеї чи файли поза своєю текою. Не продає й не передає дані. Публічна збірка не містить ідентифікатора застосунку Wargaming, токенів доступу й коду, що звертається до Wargaming API напряму.

## 6. Ваш вибір

Згоду можна відкликати будь-коли на сторінці **Дані EU**; щоб стерти локальні дані, видаліть `mods/configs/vpi-index/`. Це повідомлення не обмежує ваших прав за законом.
