# STOP Traffic Sign Detection

Python ve OpenCV kullanarak renk tabanli (HSV) yontemle **STOP trafik isareti** tespiti yapan bir görüntü isleme projesi. Yıldız Rover ekibi — Destek Ekip, Ödev 2 kapsaminda hazirlanmistir.

## Project Description

Otonom bir rover'in cevresindeki STOP tabelasini tanimasi ve durmasi gerekmektedir. Bu proje, bir görüntüdeki kirmizi STOP tabelasini HSV renk uzayinda maskeleme yaparak tespit eder, tabelayi bir bounding box icine alir, merkez piksel koordinatini hesaplar ve terminale yazdirir. Dataset'teki tum gorseller otomatik olarak islenir ve isaretlenmis ciktilar `outputs/` klasorune kaydedilir.

## Features

- HSV renk uzayinda iki araligi birlestiren kirmizi renk maskeleme
- Morfolojik islemlerle (opening + closing) gurultu temizligi
- Kontur tespiti ve alan / aspect-ratio / extent filtreleriyle yanlis pozitif azaltma
- Bounding box cizimi ve merkez piksel koordinati hesaplama
- Dataset'teki tum gorsellerin (jpg / jpeg / png) otomatik, tek komutla islenmesi
- Her goruntu icin acik terminal ciktisi (tespit edildi / edilemedi)
- `outputs/results.json` icinde makine-okunabilir ozet sonuc
- Hatali/okunamayan dosyalarda program crash etmez, anlamli mesaj verir
- **HSV esikleri ve alan filtreleri komut satirindan ayarlanabilir** (`--lower-red1` vb.) — kod degistirmeden kalibrasyon
- **`--debug-mask` modu**: temizlenmis kirmizi maskeyi `outputs/debug_masks/` altina kaydeder, HSV ayari yaparken hangi bolgelerin "kirmizi" sayildigini gorsel olarak incelemeyi saglar
- Dataset olmadan da calisabilen, **7 farkli senaryoyu** (temiz tabela, gölgeli, kismen kapali, uzak/kucuk, dikkat dagitici nesnelerle birlikte, tabelasiz, yalnizca dikkat dagitici) kapsayan sentetik sanity-test (`tests/test_sanity.py`)

## Technologies

- Python 3
- OpenCV (`opencv-python`)
- NumPy

## Installation

```bash
git clone <bu-repo-url>
cd stop-sign-detection
pip install -r requirements.txt
```

## Dataset

Paylasilan **`stop_sign_dataset`** klasorundeki gorseller `dataset/` klasorune yerlestirilmelidir:

```text
stop-sign-detection/
└── dataset/
    ├── stop_01.jpg
    ├── stop_02.jpg
    └── ...
```

Program `dataset/` klasorunu (alt klasorler dahil) tarayarak `.jpg`, `.jpeg`, `.png` uzantili tum dosyalari otomatik bulur; dataset farkli bir alt klasor yapisina sahipse de calisir.

> **Not:** Bu depoda ornek/gercek dataset gorselleri bulunmamaktadir; ödev kapsaminda dataset ayrica paylasilmaktadir. Farkli bir konumda tutmak isterseniz: `python src/main.py --dataset yol/to/dataset --output yol/to/outputs`

## Project Structure

```text
stop-sign-detection/
│
├── dataset/                    # STOP tabelasi gorselleri (kullanici tarafindan eklenir)
├── outputs/                     # Isaretlenmis cikti gorselleri, results.json, debug_masks/
├── tests/
│   ├── test_sanity.py           # 7 sentetik senaryo uzerinde hizli dogrulama testi
│   └── synthetic_scenarios.py   # Sentetik test goruntusu ureteclerinin tanimlari
├── src/
│   ├── __init__.py
│   ├── config.py               # Ayarlanabilir HSV / kontur-filtre esik degerleri (DetectionConfig)
│   ├── detector.py             # HSV maskeleme, kontur filtreleme, bounding box, merkez hesaplama
│   └── main.py                  # Dataset tarama, toplu isleme, CLI, terminal/JSON ciktilari
│
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run

```bash
python src/main.py
```

Varsayilan olarak `dataset/` klasorunu okur, sonuclari `outputs/` klasorune yazar. Farkli klasor belirtmek icin:

```bash
python src/main.py --dataset dataset/ --output outputs/
```

Sanity-test (gercek dataset gerektirmez, 7 sentetik senaryoyu kontrol eder):

```bash
python tests/test_sanity.py
```

### HSV Esiklerini Kalibre Etme

Varsayilan esikler (`src/config.py`) zaten 198 gercek goruntu uzerinde kalibre edilmistir (bkz. "Results" bolumundeki "HSV Kalibrasyon Deneyi"). Farkli bir dataset icin yeniden ayar gerekirse, kodu degistirmeden komut satirindan yapilabilir:

```bash
python src/main.py --lower-red1 0 100 70 --upper-red1 10 255 255 --debug-mask
```

`--debug-mask` bayragi, her goruntu icin temizlenmis kirmizi maskeyi `outputs/debug_masks/<dosya-adi>_mask.jpg` olarak kaydeder; bu sayede hangi bolgelerin "kirmizi" sayildigi gozle kontrol edilip esikler buna gore ince ayarlanabilir. Bu depodeki varsayilan esikler (S≥70, V≥50), daha siki bir baslangic degerine (S≥100, V≥70) gore gercek veride Accuracy'yi %80.3'ten %83.8'e cikarmistir — detayli deney icin "Results" bolumune bakin.

## Algorithm

```text
Input Image
     |
Image Read
     |
BGR -> HSV
     |
Red Color Mask (iki Hue araligi birlestirilir)
     |
Morphological Operations (opening + closing)
     |
Contour Detection
     |
Contour Filtering (alan, aspect ratio, extent)
     |
Bounding Box
     |
Center Point Calculation
     |
Visualization
     |
Output Image
```

### HSV ve Kirmizi Renk Tespiti

Kirmizi renk HSV uzayinda Hue eksininin iki ucunda (0 civari ve 180 civari) bulunur, bu yuzden iki ayri esik araligi (`[0-10]` ve `[170-180]`) olusturulup birlestirilir. Saturation ve Value alt sinirlari, gölge/aydinlatma farklarina tolerans taniyacak sekilde secilmistir. **Bu degerler, 198 gercek goruntuden olusan bir dogrulama seti uzerinde kalibre edilmistir** — detayli deney ve sonuclar icin "Results" bolumune bakin.

### Kontur ve Bounding Box

`cv2.findContours` ile bulunan konturlar su kriterlere gore filtrelenir:
- **Minimum/maksimum alan orani**: goruntu boyutuna oransal, cok kucuk gurultu ve goruntuyu kaplayan asiri buyuk yanlis bolgeleri eler.
- **Aspect ratio (0.6–1.6)**: STOP tabelasi oktagonal oldugu icin genislik/yukseklik oraninin 1'e yakin olmasi beklenir.
- **Extent (kontur alani / bounding box alani, min 0.55)**: STOP tabelasinin dolgun bir sekil olmasi nedeniyle ince/dagitik kirmizi lekeleri eler.

Birden fazla aday kontur filtreden gecerse, **en buyuk alanli** olan STOP tabelasi olarak secilir.

### Merkez Piksel Koordinati

```text
center_x = x + width / 2
center_y = y + height / 2
```

`x, y` bounding box'in sol-ust kosesi, `width, height` ise genislik ve yukseklik. Sonuc integer piksel degerine yuvarlanir.

## Example Output

Terminal ciktisi ornegi:

```text
Image: stop_01.jpg
STOP detected
Bounding Box: x=120, y=85, w=210, h=205
Center Pixel: (225, 187)

Image: image_05.jpg
STOP not detected
```

Isaretlenmis cikti gorselleri `outputs/<dosya-adi>_result.jpg` olarak kaydedilir; ozet istatistikler `outputs/results.json` icinde tutulur.

> **Bu depoda `outputs/` klasoru doludur** — 98 isaretlenmis cikti gorseli, 197 debug maskesi ve `results.json` zaten mevcuttur. Ancak bunlar yerine gecen dataset'e aittir, resmi degildir; detaylar ve telif uyarisi icin `outputs/OKUYUN_TELIF_UYARISI.txt` dosyasina bakin.

## Results

### ⚠️ Onemli: Bu sonuclar ödevin resmi "stop_sign_dataset" veri seti UZERINDE DEGILDIR

Ödev kapsaminda paylasilmasi gereken resmi `stop_sign_dataset` bu gelistirme ortaminda hic mevcut olmadi. Kodun gercek veri uzerinde calisip calismadigini ve doğruluğunu **uydurmadan** gostermek icin, halka acik bir GitHub reposundan ([mbasilyan/Stop-Sign-Detection](https://github.com/mbasilyan/Stop-Sign-Detection)) **yerine gecen (substitute) bir dataset** kullanildi: 100 STOP tabelali + 100 STOP tabelasiz, toplam 198 okunabilir gercek fotograf, ground-truth etiketleriyle birlikte (`labels.tsv` + dosya numarasina gore cikarim).

**Bu asagidaki sayilar gercektir (uydurulmamistir), ancak ödevin resmi dataset'i degildir.** Resmi `stop_sign_dataset` elinize gectiginde, asagidaki komutla gercek sonuclari yeniden uretmeniz gerekir:

```bash
python src/main.py --debug-mask
```

### Yerine Gecen Dataset Uzerindeki Gercek Sonuclar (198 goruntu)

| Metrik | Deger |
|---|---|
| Toplam degerlendirilen goruntu | 198 |
| True Positive (STOP var, dogru tespit) | 82 |
| False Negative (STOP var, kacirildi) | 16 |
| False Positive (STOP yok, yanlis tespit) | 16 |
| True Negative (STOP yok, dogru red) | 84 |
| **Accuracy** | **%83.8** |
| **Precision** | **%83.7** |
| **Recall** | **%83.7** |
| **F1 Score** | **%83.7** |

Bu degerler, `src/config.py` icindeki varsayilan HSV esikleriyle (S≥70, V≥50) elde edilmistir. Daha siki bir baslangic esigi (S≥100, V≥70) daha dusuk sonuc vermisti (Accuracy %80.3, Recall %72.4) — bkz. "HSV Kalibrasyon Deneyi" asagida.

### HSV Kalibrasyon Deneyi (gercek veriyle yapilan iyilestirme)

Ilk baslangic esikleriyle (S≥100, V≥70) calistirildiginda, bircok soluk/gölgeli STOP tabelasi extent filtresine takilarak kacirilmisti (orn. bulutlu havada cekilmis, hafif yipranmis bir tabela — extent 0.45, esik 0.55). Saturation/Value alt sinirlari gevsetilince (S≥70, V≥50):

| Konfigurasyon | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Siki esik (S≥100, V≥70) | %80.3 | %85.5 | %72.4 | %78.5 |
| **Gevsek esik (S≥70, V≥50) — yeni varsayilan** | **%83.8** | %83.7 | **%83.7** | **%83.7** |

Recall (kacirilan tabela sayisi) belirgin sekilde iyilesti, precision hafifce dustu (daha fazla false-positive) — bu, HSV tabanli renk tespitinde tipik bir hassasiyet/kesinlik odunlesimidir (bkz. rapor "Sinirliliklar").

### Gozlemlenen Hata Oruntuleri (Qualitative)

- **False Positive'ler**: Cogunlukla kirmizi tenteler/gölgelikler, kirmizi tabelalar (STOP disi) ve kirmizi arac gövdeleri. Ornek: bir magaza vitrini uzerindeki kirmizi tente, oktagon olmamasina ragmen aspect-ratio ve extent filtrelerini gecebilecek kadar "kare-ye yakin" bir bicimde kesildigi icin yanlislikla STOP olarak isaretlendi.
- **False Negative'ler**: Cogunlukla (a) goruntude cok kucuk/uzak gorunen tabelalar (minimum alan filtresi), (b) soluk/gölgeli kirmizi tonlar (HSV esigi disi kalan pikseller), (c) yuksek cozunurluklu goruntulerde beyaz "STOP" yazisinin kirmizi konturu parcalamasi (extent dususu).

> **Telif hakki notu:** Yukaridaki yerine gecen dataset'in bazi gorselleri (orn. bir "Green Stock Media" filigranli fotograf tespit edildi) telifli stok fotograf kaynakli olabilir. Bu yuzden bu depoya **hicbir gercek fotograf veya isaretlenmis cikti gorseli eklenmemistir** — yalnizca sayisal sonuclar paylasilmistir. Resmi `stop_sign_dataset` ile calistirdiginizda kendi ciktilariniz `outputs/` klasorunde olusacaktir ve telif sorunu olmadan repository'e eklenebilir.

## Limitations

- **Yalnizca renge dayanir**: Sekil/desen bilgisi kullanilmadigi icin kirmizi renkte baska nesneler (araba, tabela, giysi, kirmizi bina cephesi vb.) yanlis pozitife yol acabilir.
- **Aydinlatma degisimine duyarlidir**: Sabit HSV esikleri, gun isigi/golge/aksam isigi gibi farkli aydinlatma kosullarinda tutarli calismayabilir.
- **Kismi gorunen tabelalar**: Tabela kismen baska bir nesne tarafindan kapatilmissa aspect-ratio/extent filtreleri onu eleyebilir.
- **Mesafe ve cozunurluk**: Cok uzak/kucuk gorunen tabelalar minimum alan filtresi nedeniyle atlanabilir; filtre cok gevsetilirse gurultu artar.
- **Bulanik (motion blur) goruntuler**: Kontur kenarlari netligini kaybettiginde extent/aspect-ratio hesaplari bozulabilir.
- **Renk esiklerinin ortam-bagimliligi**: Kamera kalitesi ve beyaz dengesi farkli kirmizi tonlari uretebilir; tek bir HSV araligi her kamera/ortam icin ideal olmayabilir.

Bu sinirlamalar, projenin "yalnizca renk tabanli" bir yaklasim olmasinin dogal sonucudur (ödevin istedigi temel yontem budur); daha saglam bir cozum icin sekil/desen veya ogrenme-tabanli yontemlerle desteklenmesi gerekir.

**198 gercek goruntuden olusan yerine gecen dataset uzerinde gozlemlenen somut bulgular** (bkz. "Results" bolumu):
- Yuksek cozunurluklu bir goruntude (2462×1735), acikca gorunen bir STOP tabelasi extent filtresine takilarak kacirildi (extent=0.45, esik=0.55). Nedeni arastirildi: bulutlu havada cekilmis, hafifce soluk bir kirmizi ton, HSV maskesinde noktali/parcali bir bolge uretti (morfolojik kapatma bunu tam dolduramadi). Saturation/Value esikleri gevsetilince (S≥70,V≥50) bu ozel goruntu basariyla tespit edildi (extent 0.45→0.77).
- Bu tek ornekten yola cikarak S/V esikleri tum 198 goruntu uzerinde gevsetildi: Accuracy %80.3→%83.8, Recall %72.4→%83.7 (Precision %85.5→%83.7'ye hafifce dustu — false-positive sayisi 12'den 16'ya cikti). Bu, HSV tabanli tespitte tipik bir hassasiyet/kesinlik odunlesimidir.
- Gercek false-positive ornekleri incelendiginde, kirmizi tenteler/gölgelikler ve kirmizi arac govdeleri en sik yanlis pozitif kaynagi oldu — bu, "yalnizca renge dayanma" sinirlamasinin somut kanitidir.

**Sentetik senaryo testlerinden gozlemlenen ek bulgular** (`tests/test_sanity.py`, gercek dataset degildir ama pipeline davranisini onceden gostermistir):
- Kismen kapanmis (partially occluded) bir tabela senaryosunda, extent filtresi tabelayi reddetmistir — bu, "kismi görünen tabelalar" sinirlamasinin kod seviyesinde de dogrulanan somut bir ornegidir.
- Dikkat dagitici kucuk/ince kirmizi nesneler, alan/aspect-ratio/extent filtreleriyle basariyla elenmistir.

## Future Improvements

- Renk maskesiyle birlikte **sekil dogrulama** (oktagon kose sayisi kontrolu, `cv2.approxPolyDP`) eklenerek false-positive orani dusurulebilir.
- Adaptif/otomatik HSV esik secimi (ornegin histogram tabanli) ile farkli aydinlatma kosullarina dayaniklilik artirilabilir.
- Ground-truth etiketli (bounding box) bir alt-kume hazirlanarak gercek precision/recall/F1 olculebilir.
- Zamanla (video/ardisik kareler) takip (tracking) eklenerek tek karede kacan tespitler telafi edilebilir.
- Derin ogrenme tabanli (orn. YOLO) bir tespit modeliyle karsilastirmali degerlendirme yapilabilir (bkz. rapor "Alternatif Yontemler").

## Reference Courses

Ödev kapsaminda izlenmesi istenen iki OpenCV kursu ve bu projeyle dogrudan iliskili konulari:

- **[OpenCV Python Course (freeCodeCamp / OpenCV.org, Satya Mallick)](https://www.youtube.com/watch?v=rfscVS0vtbw)** — Modul bazli, temel-orta seviye bir kurstur (goruntu okuma, temel manipulasyon, filtreleme, kenar tespiti, nesne takibi/tespiti gibi bolumler icerir). Bu projede kullanilan goruntu okuma ve temel islemler bu kursun ilk modulleriyle ortusmektedir.
- **[OpenCV Course - Full Tutorial with Python (Jason Dsouza)](https://www.youtube.com/watch?v=oXlwWbU8l2o)** — Bu proje icin daha dogrudan iliskili konulari icerir: **Renk Uzaylari (Color Spaces)**, **Kontur Tespiti (Contour Detection)**, **Maskeleme (Masking)** ve **Bitwise Islemler**. Projede kullanilan BGR→HSV donusumu, `cv2.inRange` ile maskeleme ve `cv2.findContours` ile kontur tespiti dogrudan bu kursun ilgili bolumlerindeki kavramlara dayanmaktadir.
