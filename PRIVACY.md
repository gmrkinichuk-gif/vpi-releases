# VPI Privacy Notice

Applies to the public VPI release (`VPI-Setup-<version>-EU-Public.exe`, `VPI-<version>-EU-Public.zip` and the two `.wotmod` files in them) published at <https://github.com/gmrkinichuk-gif/vpi-releases/releases>. The English text governs; a Ukrainian translation follows. Last reviewed: 28 November 2026.

## 1. Who is responsible

VPI is made by Vladyslav Kinichuk (metronom_). Questions and privacy requests: [GitHub Issues of vpi-releases](https://github.com/gmrkinichuk-gif/vpi-releases/issues). Issues are public; do not post account IDs, private data, credentials or logs containing personal information. Ask for a private contact channel if needed. VPI has no account system, no analytics, no advertising and no telemetry.

## 2. Data that stays on your computer

VPI stores its settings, personal battle history and update-check state locally in `mods/configs/vpi-index/` in your game folder. Those files are not uploaded. The installer writes VPI packages and, where needed, a locally generated compatibility page into the game folders; the mod also writes diagnostic messages to the game's logs.

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

- `POST /v1/ratings` with up to 30 public player identities (nickname and account ID when available; otherwise a nickname for exact lookup). This includes your own account in the hangar, players in the battle interface and loading screen, post-battle results and visible contacts. Bots and identities hidden by the Anonymizer are skipped while hidden; a real identity revealed by the game in post-battle results may be looked up.
- `GET /v1/catalog` for the vehicle table (tier, class, role, hit points, view range).

When enabled, the service uses its own application ID to retrieve public account and vehicle statistics from the Wargaming Public API. It sends public account IDs or nicknames as needed for those lookups, calculates VPI and returns ratings and battle counts to the requesting mod. The purpose is to provide the optional ratings feature and to protect the service against excessive requests.

The ratings service is designed to keep at most 100 player identities in memory at a time. Pending, failed and ready records have time limits of 20, 15 and 60 seconds respectively; in-flight requests and response delivery can retain temporary references until they finish. No player-statistics database or permanent copy is maintained by VPI. The non-player vehicle catalogue is cached in memory for up to 24 hours. The VPI application and its configured reverse proxy do not keep access logs of requests, URLs, bodies, player IDs, nicknames or IP addresses. A keyed hash of the source address is used for rate limiting and kept only in memory until its idle rate-limit buckets refill (approximately three minutes for a fully used identity quota). The mod caches up to 100 received ratings in memory for 10 minutes. Turning the ratings feature off stops new ratings requests and clears its local ratings cache; requests already in flight may finish and server records expire according to their normal limits.

The ratings service may be enabled, temporarily disabled or restricted for maintenance, capacity, upstream availability or compliance reasons. While it is disabled, it does not query Wargaming for ratings or create new player rating records, and the mod shows ratings as unavailable. Enabling ratings in the mod does not guarantee service availability. VPI is an independent, unofficial project; this notice does not claim endorsement or written approval from Wargaming.

## 4. Update check

Only in the hangar, at most once every 6 hours after a successful check (a failed check is retried after an hour), VPI asks the public GitHub API (`https://api.github.com/repos/gmrkinichuk-gif/vpi-releases/releases/latest`) which VPI release is the latest. The request carries no token and no personal data apart from what any web request reveals to GitHub (your IP address and the header `User-Agent: VPI-mod/<version>`); see [GitHub's Privacy Statement](https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement). VPI downloads and installs nothing. Turn it off with "Notify about updates" in VPI settings. Clicking the update line opens the releases page in your browser.

## 5. What VPI never does

VPI does not collect or transmit your password, e-mail, payment data, chat, replay files or unrelated personal files. VPI does not sell personal data or use it for advertising. The ratings and update-check data flows to Wargaming and GitHub are described above. HTTPS traffic is also handled by the hosting and network infrastructure needed to operate the service. The public build contains no Wargaming application ID, no access token and no code that calls the Wargaming API directly.

## 6. Your choices

Turn off the optional ratings feature at any time on **Дані EU / EU data**, or turn off update checks separately. With the game closed, delete `mods/configs/vpi-index/` to erase locally stored VPI data. For privacy questions or requests concerning your data, use the contact route in section 1 without posting personal information publicly. Your statutory rights, including applicable rights to access, correct or erase personal data and to object to processing or complain to a competent supervisory authority, are not limited by this notice.

---

# Повідомлення про приватність VPI

Стосується публічного релізу VPI (`VPI-Setup-<версія>-EU-Public.exe`, `VPI-<версія>-EU-Public.zip` і двох `.wotmod` у них), опублікованого на <https://github.com/gmrkinichuk-gif/vpi-releases/releases>. Чинним є англійський текст, нижче переклад. Перевірено 28 листопада 2026 року.

## 1. Хто відповідає

VPI створює Vladyslav Kinichuk (metronom_). Питання та запити щодо приватності: [GitHub Issues репозиторію vpi-releases](https://github.com/gmrkinichuk-gif/vpi-releases/issues). Звернення там публічні; не публікуйте ID акаунтів, приватні дані, облікові дані або журнали з персональною інформацією. За потреби попросіть приватний канал зв’язку. У VPI немає облікових записів, аналітики, реклами й телеметрії.

## 2. Дані, які лишаються на вашому комп’ютері

VPI зберігає налаштування, власну історію боїв та стан перевірки оновлень локально в `mods/configs/vpi-index/` у теці гри. Ці файли не завантажуються на сервер. Інсталятор записує пакети VPI та, за потреби, локально створену сторінку сумісності в теки гри; мод також записує діагностичні повідомлення в журнали гри.

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

- `POST /v1/ratings` з не більш ніж 30 публічними ідентичностями гравців (нік та ID акаунта, якщо доступний; інакше нік для точного пошуку). Це ваш акаунт в ангарі, гравці в інтерфейсі бою та на екрані завантаження, у післябойових результатах і видимі контакти. Боти та ідентичності, приховані Anonymizer, пропускаються, доки вони приховані; справжня ідентичність, яку гра відкриває в післябойових результатах, може бути використана для запиту.
- `GET /v1/catalog` для таблиці техніки (рівень, клас, роль, міцність, огляд).

Коли сервіс увімкнено, він отримує публічну статистику акаунтів і техніки через Wargaming Public API зі своїм ідентифікатором застосунку. Для цього він передає публічні ID акаунтів або ніки за потреби, обчислює VPI та повертає рейтинги й кількість боїв моду, який їх запросив. Мета — надання необов’язкової функції рейтингів і захист сервісу від надмірної кількості запитів.

Сервіс рейтингів розрахований на утримання не більш ніж 100 ідентичностей гравців одночасно в пам’яті. Записи в очікуванні, невдалі та готові мають строки 20, 15 і 60 секунд відповідно; поточні запити та передавання відповіді можуть утримувати тимчасові посилання до їх завершення. VPI не веде базу статистики гравців і не зберігає постійних копій. Каталог техніки без даних гравців кешується в пам’яті до 24 годин. Застосунок VPI та налаштований для нього зворотний проксі не ведуть журналів доступу із запитами, URL, тілами запитів, ID, ніками чи IP-адресами. Для обмеження частоти використовується ключований хеш адреси джерела, який зберігається лише в пам’яті, доки після простою не відновляться ліміти (приблизно три хвилини для повністю використаної квоти ідентичностей). Мод кешує до 100 отриманих рейтингів у пам’яті на 10 хвилин. Вимкнення функції рейтингів зупиняє нові запити й очищає локальний кеш рейтингів; поточні запити можуть завершитися, а серверні записи спливають за звичайними лімітами.

Сервіс рейтингів може бути увімкнений, тимчасово вимкнений або обмежений через технічне обслуговування, навантаження, доступність джерела статистики чи вимоги щодо відповідності правилам. Поки сервіс вимкнений, він не звертається до Wargaming по рейтинги та не створює нових рейтингових записів гравців, а мод показує рейтинги як недоступні. Увімкнення рейтингів у моді не гарантує доступності сервісу. VPI є незалежним неофіційним проєктом; це повідомлення не стверджує, що Wargaming схвалив його або надав письмовий дозвіл.

## 4. Перевірка оновлень

Лише в ангарі, не частіше ніж раз на 6 годин після вдалої перевірки (невдалу VPI повторює через годину), VPI запитує публічний API GitHub (`https://api.github.com/repos/gmrkinichuk-gif/vpi-releases/releases/latest`), який реліз VPI останній. Запит не містить токена й персональних даних, крім того, що бачить GitHub у будь-якому вебзапиті (ваша IP-адреса й заголовок `User-Agent: VPI-mod/<версія>`); див. [Privacy Statement GitHub](https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement). VPI нічого не завантажує й не встановлює. Вимкнути: «Повідомляти про оновлення» в налаштуваннях VPI. Клік по рядку оновлення відкриває сторінку релізів у браузері.

## 5. Чого VPI ніколи не робить

VPI не збирає та не передає ваш пароль, електронну пошту, платіжні дані, чат, файли реплеїв чи сторонні особисті файли. VPI не продає персональні дані й не використовує їх для реклами. Передавання даних для рейтингів і перевірки оновлень до Wargaming та GitHub описане вище. HTTPS-трафік також обробляється хостинговою та мережевою інфраструктурою, необхідною для роботи сервісу. Публічна збірка не містить ідентифікатора застосунку Wargaming, токенів доступу й коду, що звертається до Wargaming API напряму.

## 6. Ваш вибір

Вимкнути необов’язкову функцію рейтингів можна будь-коли на сторінці **Дані EU**, а перевірку оновлень — окремо. При закритій грі видаліть `mods/configs/vpi-index/`, щоб стерти локальні дані VPI. З питань приватності та запитів щодо ваших даних використовуйте спосіб зв’язку з розділу 1, не публікуючи особистої інформації. Це повідомлення не обмежує ваших законних прав, зокрема застосовних прав на доступ, виправлення чи видалення персональних даних, заперечення проти обробки та подання скарги до компетентного наглядового органу.
