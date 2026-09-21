# Claude Web Workflow

**Claude ile uçtan uca site yapımı: hangi model ne yapar, hangi skill ne zaman çağrılır, hangi MCP sunucusu bağlanır — ve sonucun "yapay zekâ işi" gibi durmasını engelleyen önlemler.**

[![check](https://github.com/turuncfatih/claude-web-workflow/actions/workflows/check.yml/badge.svg)](https://github.com/turuncfatih/claude-web-workflow/actions/workflows/check.yml)
[![licence](https://img.shields.io/badge/lisans-MIT-blue.svg)](LICENSE)

[🇬🇧 English](README.md) · 🇹🇷 Türkçe

"İşte landing page yapan bir prompt" değil. Boş klasörden yayındaki hızlı,
güvenli, bulunabilir siteye kadar tüm hat: Opus / Sonnet / Haiku arasındaki iş
bölümü, her aşamadaki skill'ler, tasarım için Stitch, karar için Artifact, soğuk
inceleme için ikinci bir model, ve sonucu kimse görmeden denetleyen roller.

```
14 bölüm · 8 ajan tanımı · 1 çalışan script · 1 uçtan uca yürüyüş
```

> **Kardeş repolar.**
> [Claude Mobile Workflow](https://github.com/turuncfatih/claude-mobile-workflow) — aynı akışın React Native hali.
> [Agent Team Playbook](https://github.com/turuncfatih/agent-team-playbook) — ajan ekibi tasarlamanın genel yöntemi.
> [AgentForge](https://github.com/turuncfatih/agentforge) — orkestrasyon makinesi, .NET ile.

---

## Bu repo neden var

### Sorun, web sitesi yapmanın zor olması değil

Zor olmaktan çıktı. Artık herkes bir landing page tarif edip on dakikada çalışan
HTML alabiliyor. Bu gerçekten yeni bir şey, ve sorun da tam burada: **darboğaz
üretmekten yargılamaya kaydı.**

O on dakikadan çıkan şey genelde **doğrudur**. Derlenir. Responsive'dir. Başlıkları
ve alt metinleri vardır. Ve çok az değer taşır, çünkü:

| Varsayılan olarak aldığın | Sana maliyeti |
|---|---|
| Diğer bütün üretilmiş sayfalar gibi duran bir sayfa | Ziyaretçi iki saniyede birinin önemseyip önemsemediğine karar veriyor. Jenerik tasarım, önemsemeyen bir işletme demek |
| Herhangi bir şirkete ait olabilecek metin | "Kaliteli hizmet, ihtiyacınıza özel" — bir rakibin de söylemeyeceği hiçbir şey söylemiyor |
| Uydurulmuş sayılar ve referanslar | Bir işletmenin sitesindeki uydurma istatistik bir üslup sorunu değildir |
| Sayfanın çizilip çizilmediğini kimse kontrol etmedi | Derleme geçti. Bu, sayfanın çalışmasıyla aynı şey değil |
| Yapısal veri yok, tarama yolu yok | Doğru ve görünmez |
| 6 MB'lık hero görseli ve üç takip script'i | Müşterilerinin gerçekten sahip olduğu bağlantıda yavaş |

Bunların hiçbiri **yetenek** sorunu değil. Bir model iyi metin yazabilir,
düşünülmüş bir sayfa tasarlayabilir, geçerli schema üretebilir. **Bunlar süreç
sorunu** — hiçbir şeyi yakalayan bir adım yoktu, çünkü işi bir ajan üretti ve
bittiğini de aynı ajan ilan etti.

### Neden süreç, neden sadece daha iyi bir prompt değil

Daha iyi bir prompt ilk taslağı iyileştirir. Bir geri besleme döngüsü kurmaz.

Sonucu gerçekten değiştiren üç şey metinsel değil, yapısal:

1. **Yazandan başka biri inceler.** Kendi çıktısını inceleyen ajan, o sorunu
   üreten kör noktayı taşıyor. Kendi pull request'ini merge etmeme sebebinle
   aynı sebep.
2. **Bir şey hayır diyebilir.** Yayını durduramayan inceleme, yorumdur. Bir rol
   veto taşıyor, ve olgulara dayanıyor — derlendi ya da derlenmedi.
3. **Deterministik kısımlar script'tir, yargı değil.** Karakter saymak, JSON-LD
   doğrulamak, yasak bir kalıbı bulmak — bir regex bunu anında, bedava ve her
   seferinde aynı şekilde yapıyor. Modele sormak daha yavaş, para yiyor, ve arada
   kendisiyle çelişiyor.

Bu reponun bütün şekli bu. Geri kalanı detay.

### Neden özellikle bu araçlar

Her seçim kendi bölümünde savunuluyor, kısa hali:

| Seçim | Sebep |
|---|---|
| **Statik site** | Pazarlama sitesi belgedir. Belgelerin çalışma anında framework'e ihtiyacı yok, ve sıfır JavaScript performans sorununu ayarlanacak bir şey olmaktan çıkarıp **ortadan kaldırıyor**. Buradaki hiçbir şey özellikle Astro'ya bağlı değil |
| **Cloudflare Pages** | CDN, TLS, DDoS koruması ve preview URL'leri çözülmüş problemler. `_headers` ve `_redirects` repoda duruyor, yani normalde sunucu yapılandırması olacak şey diff'te incelenebiliyor |
| **Ana oturumda Opus** | Yanlış bir plan kendinden sonraki her adımı çöpe atıyor. Projedeki en geri alınamaz karar, ve doğru yapması en ucuz olan |
| **Alt ajanlarda Sonnet** | Net bir spesifikasyonla uygulama icradır. Buna frontier fiyatı ödemek hiçbir şey kazandırmıyor |
| **İllüstrasyon için görsel modeli, ikon için ikon kütüphanesi** | Üretilen ikon setleri çizgi kalınlığı ve stilde kayıyor, ve karışık ikonlar sayfayı kimsenin tasarlamadığının en bariz işareti |
| **Düzen için Stitch** | Bir düzeni yazıyla tarif etmek, sana dilin en kolay tarif ettiği düzeni veriyor — üretilen sayfaların birbirine benzemesinin sebebi bu. Üç seçeneğe tepki vermek bunu kırıyor |

### Bu sana aslında ne veriyor

Daha hızlı çıktı değil. Hızlı çıktıyı zaten alabiliyorsun.

- Ziyaretçinin başka bir firma adı koyamayacağı bir sayfa
- Her iddiasının, bir rakibin gerçekten itiraz edebileceği türden olduğu bir metin
- Bitti denmeden önce **çizildiği doğrulanmış** bir site
- Yapısal veri ve tarama yolu — yani bulunabilir bir iş
- Site hâlâ küçükken, bedavaya eklenmiş güvenlik header'ları ve CSP
- Açıklayabildiğin bir maliyet, çünkü harcama işin prestijine değil kararın geri
  alınabilirliğine göre dağılıyor

Zaten bir inceleme adımın, bir doğrulayıcın ve bir maliyet modelin varsa burada
az şey bulursun. Mevcut sürecin "üret, bak, yayınla" ise, eksik yarısı bu.

---

## Akılda kalması gereken tek şey

Üretilmiş bir site genelde **doğrudur**. Derlenir, responsive'dir, başlıkları
vardır — ve ziyaretçi iki saniyede kimsenin bir şeye karar vermediğini anlar. Bu
bir güven sorunudur ve doğrulukla çözülmez.

Bu yüzden tüm akış tek bir sorunun etrafında kurulu:

> **Bu sayfa, başka bir firmanın adını koysan yine çalışır mıydı?**

Cevap evet ise henüz hiçbir şeye karar verilmemiş demektir.
[5. bölüm](docs/05-not-looking-ai-made.md) bunun işaretlerini, önlemlerini ve
bunu zorlayan rolleri anlatıyor.

---

## Hangi model ne yapar

| Nerede | Model | Ne oraya ait |
|---|---|---|
| **Ana oturum** | Opus, yüksek efor | Planlama, yönlendirme, tasarım yönü, son karar |
| **Alt ajanlar** | Sonnet | Uygulama, metin, doğrulama — spesifikasyona karşı icra |
| **Dar, mekanik iş** | Haiku | Sınıflandırma, çıkarım, araç çıktısını raporlama |
| **Tamamen deterministik** | *bir script* | Sayma, doğrulama, karşılaştırma — model bile değil |

Altındaki kural:

> **Muhakeme seviyesi, kararın geri alınabilirliğine göre seçilir — işin
> prestijine göre değil.**

Geliştirici ajan **en üst katman değildir**. Net bir spesifikasyon varsa uygulama
icradır; geri alınamaz düşünme zaten yukarıda yapılmıştır. Geliştiricin Opus
istiyorsa sebebi genelde zayıf spesifikasyondur, ve modeli yükseltmek bunu
gizler. [1. bölüm](docs/01-model-division-of-labour.md).

---

## Hangi araç ne için

| İş | Nerede | Neden |
|---|---|---|
| Repo işi, ajanlar, derleme | **Claude Code** | Dosyaların, rollerin ve araçların onda |
| Arayüz düzen yönleri | **Stitch** (MCP) | Tepki verilecek bir şey — medyan düzene düşmemek için |
| Yönler arasında karar | **Artifact** | Üç yön, tek anahtar, gönderilebilir bir link |
| İllüstrasyon, avatar, OG görseli | **Bir görsel modeli** | Claude görsel üretmez |
| Arayüz ikonları | **Bir ikon kütüphanesi** | Üretilen ikon setleri kayar — karışık ikon en bariz işaretlerden |
| Çok büyük metin yığını okuma | **Uzun bağlamlı bir model** | Karar değil, özet getir |
| Toplu sınıflandırma | **Ucuz bir model ya da script** | Hacim bir maliyet sorunudur, yetenek sorunu değil |
| Bitmiş metnin soğuk incelemesi | **Onu yazmayan herhangi bir model** | Ortak kör nokta yok |

Son satır atlanan satırdır. Kendi çıktısını inceleyen model, o çıktıyı üreten kör
noktayı taşır — yapısal olarak kendi işini onaylayan ajanla aynı hata.
[13. bölüm](docs/13-which-ai-for-what.md).

---

## Ekip

Sekiz rol, artı ana oturum. **Tek yazar. İki veto, türleri farklı.**

| Rol | Artefakt | Yazar mı? | Model | Veto |
|---|---|:---:|---|:---:|
| *ana oturum* | Plan ve son karar | ✗ | **Opus** | — |
| `designer` | Tasarım spesifikasyonu | ✗ | **Opus** | ✗ |
| `content-writer` | Sayfa metni | ✗ | Sonnet | ✗ |
| `web-dev` | Çalışan sayfalar | ✅ | Sonnet | ✗ |
| `design-critic` | "Bu şablon gibi duruyor" | ✗ | Sonnet | ✗ |
| `slop-auditor` | "Bunu makine yazmış gibi" | ✗ | Sonnet | ✗ |
| `seo-auditor` | "Bunu kimse bulamaz" | ✗ | Haiku | ✗ |
| `security-reviewer` | "Bu yayına çıkamaz" | ✗ | **Opus** | ✅ yargı |
| `release-verifier` | "Bu çalışmıyor" | ✗ | Sonnet | ✅ olgu |

```
ana oturum planlar
   ├─ designer ───────┐   (paralel)
   └─ content-writer ─┤
                      ▼
                 web-dev  ← repoya dokunan tek rol
                      ▼
      [ script'ler: build · slop_check.py ]
                      ▼
            release-verifier   ── OLGU VETOSU, tek başına ve ilk
                      ▼
   ┌──────────┬──────────────┬─────────────────┐   (paralel)
   ▼          ▼              ▼                 ▼
design-critic  slop-auditor  seo-auditor  security-reviewer
                                          ── YARGI VETOSU
                      ▼
       ana oturum: yayınla · revize et · insana devret
```

Sekiz, playbook'un kendi 3–6 sınırını aşıyor — bu yüzden
[agents/README.md](agents/README.md) bunu açıkça savunuyor: hangi yedi rolün
birleştirildiği ve bu dört eleştirmenin neden ayrı kaldığı yazılı.

---

## Slop denetimi

Bağımlılıksız, gerçekten çalışan bir script:
[`scripts/slop_check.py`](scripts/slop_check.py)

```bash
python3 scripts/slop_check.py dist/
```

```
HIGH  (10)
  bad.html  [slop-phrase]        "in today's fast-paced world"
  bad.html  [unsourced-number]   "99%" in: We are trusted by thousands…
  bad.html  [structure]          2 <h1> elements, expected exactly 1
MEDIUM (2)
  bad.html  [structure]          title is 65 chars (max 60)
LOW   (1)
  bad.html  [uniform-rhythm]     5 paragraphs, length spread 0.22 — too even
```

Sıfırdan farklı kodla çıkar, yani CI'a girer. Yasak kalıpları (İngilizce **ve
Türkçe**), kaçamak dil yoğunluğunu, üçleme refleksini, kaynaksız sayıları,
paragraf uzunluğu tekdüzeliğini ve yapısal SEO'yu denetler.

**Listeleri büyümek için var.** Gözünden kaçan her işaret script'e bir satır
olarak eklenir, ve bir daha kaçmaz. Script'ten sağ çıkan metin `slop-auditor`
ajanına gider — regex'in yapamayacağını o yapar: iddia somut mu, ve bir rakip
bunun tersini söyleyebilir mi.

---

## Bölümler

| # | Bölüm | |
|---|---|---|
| 0 | [Kurulum](docs/00-setup.md) | Boş klasörden. `CLAUDE.md`, en çok iş gören dosya |
| 1 | [Hangi model ne yapar](docs/01-model-division-of-labour.md) | Opus / Sonnet / Haiku, aşama aşama, maliyet dağılımıyla |
| 2 | [Skills haritası](docs/02-skills-map.md) | Hangi aşamada hangi skill |
| 3 | [MCP sunucuları](docs/03-mcp-servers.md) | Stitch, tarayıcı otomasyonu, hosting — ve neyi bağlamamalı |
| 4 | [Tasarım akışı](docs/04-design-flow.md) | Brief → üç yön → tepki → spesifikasyon |
| 5 | [**Makine işi gibi durmamak**](docs/05-not-looking-ai-made.md) | ★ İşaretler, önlemler, bunu zorlayan roller |
| 6 | [Görsel varlıklar](docs/06-visual-assets.md) | İkon, avatar, kilitli stil çıpası, revizyon döngüsü |
| 7 | [SEO ve GEO](docs/07-seo-geo-flow.md) | Sayfa sıralamak ve cevaplarda alıntılanmak |
| 8 | [Performans](docs/08-performance.md) | LCP / INP / CLS ve en başta verilen kararlar |
| 9 | [Güvenlik](docs/09-security.md) | Sızan anahtarlar, formlar, header'lar, üçüncü taraf script'ler |
| 10 | [Doğrulama](docs/10-verification.md) | Önce script, sonra ajan. İki veto, üç değil |
| 11 | [Cloudflare'e yayın](docs/11-shipping-cloudflare.md) | Pages, `_headers`, `_redirects`, önbellek, WAF |
| 12 | [Artifact ile tasarım incelemesi](docs/12-artifacts-for-design-review.md) | Üç yön, tek anahtar, toplantı yerine link |
| 13 | [Hangi yapay zekâ ne için](docs/13-which-ai-for-what.md) | Claude, görsel modelleri, uzun bağlam, ucuz katman |

**5 ve 1 ile başla.** Sonra [yürüyüşe](walkthrough/) geç.

---

## Kullanım

```bash
git clone <repo-url> && cd claude-web-workflow

# ekip
cp agents/*.md ~/.claude/agents/

# denetim
cp scripts/slop_check.py <projen>/scripts/

# tasarım MCP sunucusu
claude mcp add --transport http stitch https://stitch.googleapis.com/mcp
```

Sonra [yürüyüşü](walkthrough/) bir kez baştan sona uygula.

Buradaki teknik detaylar Cloudflare Pages üzerinde statik bir Astro sitesine ait.
**Roller ve sıra taşınır, stack detayları taşınmaz.** `CLAUDE.md`'yi kendi
projene göre yaz, şekli koru.

> Bölüm içerikleri ve ajan tanımları İngilizce yazıldı — kopyalanabilir olmaları
> ve uluslararası okuyucuya açık kalmaları için.

---

**Lisans** · MIT — ajanları kopyala, script'i kopyala, yöntemi kopyala.
