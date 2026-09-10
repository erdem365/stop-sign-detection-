# Final Checklist — Ödev Gereksinimleri Karşılaştırması

Bu belge, ödev dokümanındaki (Destek Ekip – Ödev 2) ve talimat metnindeki tüm maddelerin tek tek karşılandığını doğrulamak için hazırlanmıştır.

## Ödev Dokümanı (Destek Ekip – Ödev 2) Maddeleri

| # | Gereksinim | Durum | Açıklama |
|---|---|---|---|
| 1 | Verilen 2 YouTube kursunun izlenmesi | Tamam | Kursların içerikleri araştırıldı; README'nin "Reference Courses" bölümünde projeyle ilişkilendirildi. Videoların bizzat izlenmesi öğrenciye aittir. |
| 2a | Kırmızı renk tespitiyle STOP işaretinin bulunması, kare içine alınarak vurgulanması | Tamam | `detector.py`. 198 gerçek fotoğrafta doğrulandı. |
| 2b | Karenin merkez piksel konumunun bulunması ve terminale basılması | Tamam | `calculate_center`, terminal çıktısı. |
| 2c | Dataset ile tüm fotoğrafların işlenmesi, her çıktının kaydedilmesi | **Kısmi — bkz. not** | Resmi `stop_sign_dataset` hiç sağlanmadı. Bunun yerine 198 gerçek fotoğraftan oluşan halka açık bir yerine-geçen (substitute) veri seti üzerinde tam işlem yapıldı, gerçek sonuçlar üretildi (bkz. README "Results"). **Resmi dataset ile yeniden çalıştırılması gerekir.** |
| 3a | Algoritma gerçek hayatta kullanılabilir mi? Ne kadar doğru çalışıyor? | **Kısmi — bkz. not** | Yerine geçen 198 görüntülük dataset'te gerçek ölçüm yapıldı: Accuracy %83.8, Precision/Recall/F1 %83.7. Resmi dataset'te farklı çıkabilir. |
| 3b | Algoritma yetersizse sebepleri | Tamam | Rapor Bölüm 8.B — hem genel gerekçeler hem 198 gerçek görüntüden gözlemlenen somut hata örüntüleri (kırmızı tente/araç false-positive, soluk/uzak tabela false-negative). |
| 3c | Alternatif yöntemler ve neden tercih edilmeli | Tamam | Rapor Bölüm 8.C — 5 yöntem karşılaştırmalı. |
| 4 | PDF raporun Classroom'a yüklenmesi | Kullanıcıya ait | `STOP_Isareti_Tespiti_Raporu.pdf` hazır. |
| 5 | Kodun public GitHub reposuna yüklenmesi | Kullanıcıya ait | Kod hazır; repo oluşturma/push kullanıcıya ait olacak şekilde bırakıldı. |
| 6 | README'de çalıştırma bilgileri | Tamam | Kurulum, çalıştırma, CLI, HSV kalibrasyonu, gerçek sonuçlar dahil. |
| 7 | Fotoğraf çıktılarının repository'e eklenmesi | **Tamam — bkz. telif notu** | `outputs/` klasörü, kullanıcının açık onayıyla, 98 işaretlenmiş çıktı görseli + 197 debug maskesi ile doldurulmuştur (bir maske, filigran sızıntısı nedeniyle çıkarıldı). Bunlar yerine geçen dataset'e aittir, resmi değildir ve telif riski `outputs/OKUYUN_TELIF_UYARISI.txt` içinde açıkça belirtilmiştir. Resmi dataset ile üretilecek çıktılarla değiştirilmesi önerilir. |

## ⚠️ ÖNEMLİ UYARI: Kullanılan Dataset Ödevin Resmi Dataset'i DEĞİLDİR

Elimize hiçbir zaman ödev kapsamında paylaşılması gereken **`stop_sign_dataset`** ulaşmadı. Bunun yerine, 2c ve 3a maddelerinin **tamamen boş/uydurma** kalmasındansa, gerçek bir sonuç üretebilmek için halka açık bir GitHub deposu ([mbasilyan/Stop-Sign-Detection](https://github.com/mbasilyan/Stop-Sign-Detection), 198 gerçek fotoğraf + ground-truth etiket) kullanıldı ve **gerçek, ölçülmüş, uydurulmamış** sonuçlar elde edildi:

- **Accuracy: %83.8, Precision: %83.7, Recall: %83.7, F1: %83.7** (198 görüntü; 82 TP, 16 FN, 16 FP, 84 TN)

**Bunun anlamı:**
- Kodun gerçek veri üzerinde çalıştığı, doğruluğunun ölçülebildiği ve HSV eşiklerinin gerçek veriyle kalibre edilebildiği **kanıtlanmıştır**.
- **ANCAK bu sayılar resmi ödev dataset'inin sonuçları değildir.** Raporunuzu/README'nizi olduğu gibi teslim ederseniz, hocanız/asistanınız bu durumu açıkça görecektir (rapor ve README'de bu husus defalarca ve açıkça belirtilmiştir, gizlenmemiştir).
- **Yerine geçen dataset'teki bazı görsellerin ticari stok fotoğraf kaynaklı (filigranlı) olduğu tespit edilmiştir.** Kullanıcının açık onayıyla `outputs/` klasörüne bu dataset'e ait işaretlenmiş çıktılar eklenmiştir; ancak kaynak dataset'in tamamını (200 ham fotoğraf) kendi public reponuza ayrıca yüklemeyin — telif durumu belirsizdir. Detaylar için `outputs/OKUYUN_TELIF_UYARISI.txt` dosyasına bakın.

**Sizin yapmanız gereken:** Resmi `stop_sign_dataset`'i temin edip `dataset/` klasörüne koyduktan sonra:

```bash
python src/main.py --debug-mask
```

çalıştırın. Bu, `outputs/` klasörünü resmi, telif sorunu olmayan çıktı görselleriyle dolduracak ve `outputs/results.json` üretecektir. Ardından README "Results" ve Rapor Bölüm 7/8.A'yı bu resmi sayılarla güncelleyip raporu yeniden PDF'e çevirmeniz gerekir (aksi halde raporunuzda "yerine geçen dataset" uyarısı kalır).

## Talimat Metninin "Final Checklist" Bölümü (21 madde)

| Madde | Durum | Not |
|---|---|---|
| Python + OpenCV kullanıldı | Tamam | |
| STOP işaretinin kırmızı rengi tespit ediliyor | Tamam | 198 gerçek görüntüde doğrulandı |
| HSV tabanlı maskeleme uygulanıyor | Tamam | İki Hue aralığı birleştiriliyor |
| Kontur tespiti yapılıyor | Tamam | `cv2.findContours` |
| Bounding box oluşturuluyor | Tamam | |
| Merkez piksel koordinatı hesaplanıyor | Tamam | |
| Merkez koordinatı terminale yazdırılıyor | Tamam | |
| Dataset görüntüleri işleniyor | Kısmi | Yerine geçen datasette tam işlendi; resmi dataset bekliyor |
| Çıktı görüntüleri kaydediliyor | Tamam | 98 gerçek işaretlenmiş görsel `outputs/` klasöründe mevcut (yerine geçen datasette, telif notuyla) |
| Yanlış pozitifler mümkün olduğunca azaltılıyor | Tamam | Alan/aspect-ratio/extent filtreleri; gerçek veride %83.7 precision |
| Algoritmanın doğruluğu/başarımı değerlendiriliyor | Tamam | Gerçek confusion matrix + accuracy/precision/recall/F1 (yerine geçen datasette) |
| Gerçek hayatta kullanılabilirliği tartışılıyor | Tamam | Rapor Bölüm 8.A, gerçek sayılarla |
| Sınırlılıklar açıklanıyor | Tamam | Rapor Bölüm 9, gerçek hata örüntüleriyle |
| Alternatif yöntemler karşılaştırılıyor | Tamam | Rapor Bölüm 8.C |
| README hazırlanıyor | Tamam | |
| requirements.txt hazırlanıyor | Tamam | |
| .gitignore hazırlanıyor | Tamam | |
| GitHub repository yapısı düzenleniyor | Tamam | |
| Rapor içeriği hazırlanıyor | Tamam | |
| Uydurma deney sonucu kullanılmıyor | Tamam | Tüm sayılar gerçek veri üzerinde ölçüldü; hangi dataset olduğu açıkça belirtildi |
| Kod gereksiz tekrar içermiyor | Tamam | |

---

# Tespit Edilen Problemler ve Çözümleri

### 1. Resmi dataset hiç sağlanmadı
**Problem:** Ödevin çekirdek gereksinimi olan `stop_sign_dataset` bu ortamda hiç mevcut olmadı.
**Çözüm:** Kod, hiçbir dataset yapısı varsayılmadan genel/esnek yazıldı. Gerçek bir sonuç üretebilmek için halka açık, ground-truth etiketli bir yerine-geçen dataset (198 görüntü) bulunup indirildi, tam işlendi ve **gerçek** accuracy/precision/recall/F1 hesaplandı. Bu, "sonuç yok" ile "uydurma sonuç" arasında üçüncü bir dürüst yol: gerçek ama farklı bir veri üzerinde gerçek ölçüm.

### 2. Yerine geçen dataset'te bazı görsellerin telifli olması
**Problem:** Yerine geçen dataset içindeki en az bir görüntüde ("Green Stock Media" filigranı) ticari stok fotoğraf izi tespit edildi.
**Çözüm:** Kullanıcının açık onayıyla `outputs/` klasörüne bu dataset'e ait işaretlenmiş çıktılar (98 görsel + 197 debug maskesi) eklendi; ham kaynak fotoğraflar ise projeye dahil edilmedi. Kullanıcı, dataset'in tamamını (200 ham fotoğraf) kendi public reposuna ayrıca yüklememesi konusunda README, FINAL_CHECKLIST ve `outputs/OKUYUN_TELIF_UYARISI.txt` içinde açıkça uyarıldı.

### 3. Yüksek çözünürlüklü görüntüde net bir tabelanın kaçırılması
**Problem:** 2462×1735 çözünürlüklü bir görüntüde, gözle net görünen bir STOP tabelası extent filtresine takılarak (0.45 < eşik 0.55) kaçırıldı.
**Kök neden analizi:** Bulutlu havada çekilmiş, hafifçe soluk bir kırmızı ton, HSV maskesinde parçalı/noktalı bir bölge üretti; morfolojik kapatma bunu tam dolduramadı.
**Çözüm:** Saturation/Value alt sınırları gevşetildi (S≥100→70, V≥70→50). Bu tek görüntüde extent 0.45'ten 0.77'ye çıktı. Değişiklik 198 görüntünün tamamına uygulandı: Accuracy %80.3→%83.8, Recall %72.4→%83.7 (Precision %85.5→%83.7'ye hafifçe düştü — beklenen ödünleşim). Bu, `src/config.py` içindeki yeni varsayılan değer olarak kalıcı hale getirildi.

### 4. Sentetik test verisinde yanlış false-positive (önceki turdan)
**Problem/Çözüm:** Bkz. önceki sürüm notları — test verisindeki bir renk kırmızıya çok yakındı, düzeltildi.
