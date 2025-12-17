# 🌟 AI Yorum Analiz Uygulaması

Amazon ürün sayfalarındaki yorumları otomatik olarak toplayan, yabancı dilleri Türkçeye çeviren ve BERT tabanlı yapay zeka ile duygu analizi yapan PyQt5 arayüzlü masaüstü uygulaması.

Amaç: Bir ürünün yorumlarını hızlıca analiz edip, genel memnuniyet seviyesini **0–100 arası bir “AI Puanı”** ile özetlemek.

---

## 🚀 Özellikler

- 🔍 **Amazon ürün sayfasından yorumları otomatik toplar**  
- 🌍 **İngilizce, Almanca, Fransızca vb. dilleri otomatik algılar**
- 🔁 **M2M100 çok dilli çeviri modeli ile Türkçeye çevirir**
- 🧠 **BERT tabanlı Türkçe duygu analizi**  
  - Pozitif / Negatif / Nötr sınıflandırma  
- 📊 Her yorum için 0–100 arası skor üretir, ortalamayı alır
- ⭐ **Site puanı + sentiment ortalamasını birleştirerek** hibrit “AI puanı” hesaplar
- 🎨 Modern koyu temalı, kullanıcı dostu **PyQt5 arayüz**

---

## 🧩 Mimarinin Kısa Özeti

- **`scraper.py`**  
  Playwright kullanarak Amazon ürün sayfasına gider, yorumları ve site puanını çeker.

- **`translator_hf.py`**  
  `facebook/m2m100_418M` modelini kullanarak farklı dillerden Türkçeye çeviri yapar.

- **`analyzer.py`**  
  - `langdetect` ile dil tespiti  
  - Gerekirse çeviri çağrısı (`translator_hf.py` subprocess)  
  - `savasy/bert-base-turkish-sentiment-cased` ile duygu analizi  
  - Bayesian smoothing + site puanı ile final skoru üretir

- **`app.py`**  
  PyQt5 arayüzü; kullanıcıdan linki alır, arka planda scraping + analiz yapar, sonucu ekranda gösterir.

---

## 📚 Kullanılan Kütüphaneler

Kurulumdan önce aşağıdaki kütüphanelerin yüklü olduğundan emin olun:

```bash
pip install PyQt5
pip install playwright
pip install torch
pip install transformers
pip install langdetect
```
🛠️ Kurulum
1️⃣ Python kurulumunu yap

Proje Python 3.10 ile geliştirilmiştir. Önerilen sürüm: 3.10.x

Python indirme sayfası:
<img width="1128" height="270" alt="522823961-bdeeafa6-f5ae-47d6-8557-468fae0b7dc3" src="https://github.com/user-attachments/assets/f9f120f7-8968-4288-97f5-5954080d9939" />

2️⃣ Proje dosyalarını aynı klasöre yerleştir

Aşağıdaki dosyalar aynı klasörde olmalıdır:
app.py
scraper.py
analyzer.py
translator_hf.py
Örnek klasör yapısı:
<img width="853" height="383" alt="522824769-c183ed63-cf9d-407b-8d07-b83301fc84c8" src="https://github.com/user-attachments/assets/7405e322-a5a7-4cd7-a570-7a16da6698db" />

3️⃣ Gerekli kütüphaneleri yükle

Windows’ta Başlat menüsünden Komut İstemi (CMD) aç:
<img width="783" height="671" alt="522825418-94f5c26f-2b6a-4bfb-aa98-163df76b3e1f" src="https://github.com/user-attachments/assets/c6015747-b74f-491d-ac0a-ef20692d1632" />
Ardından sırayla şu komutları gir:

pip install PyQt5
pip install playwright
pip install torch
pip install transformers
pip install langdetect
python -m playwright install

Not:
Komutları yazarken kırmızı hata mesajı görürseniz, ilgili kütüphane yüklenmemiş demektir.
İnternet bağlantınızı kontrol edip komutu tekrar çalıştırın.
Örnek:
<img width="976" height="511" alt="522826204-64c73f4b-c13a-445c-bb72-2e04eb0f8d6f" src="https://github.com/user-attachments/assets/94f57107-1056-4da0-a315-71b0bed6d860" />

4️⃣ Uygulamayı çalıştır

CMD’de proje klasörüne geçin ve:
python app.py
komutunu çalıştırın. PyQt5 penceresi açılacaktır.

👁️ Arayüz
1️⃣ Giriş Ekranı
Uygulama açıldığında ilk karşınıza gelen ekran:
![522827689-51efaa24-12fb-47fe-a132-3f85b970059a](https://github.com/user-attachments/assets/777531a5-1d17-40ac-8717-31a1454963a1)
Buraya analiz etmek istediğiniz Amazon ürün sayfasının linkini yapıştırıp
“Analize Başla” butonuna tıklıyorsunuz.

2️⃣ Yükleme Ekranı
Yorum sayısına göre süresi değişen analiz aşaması:
![522828312-cb791917-a97f-4d99-9c7a-11efefc880cd](https://github.com/user-attachments/assets/0da9082d-876d-4fa7-add5-52f2a06aedd1)
Burada Playwright yorumları topluyor, çeviri + sentiment modeli devreye giriyor.

3️⃣ Sonuç Ekranı
Analiz tamamlandığında:
![522828675-d75b042f-c71b-4d22-a72d-8dcbcfdf245e](https://github.com/user-attachments/assets/8f766755-457e-415e-a88a-dea6b2472bd0)
Ürünün AI Puanı (% olarak)
Toplam okunan yorum sayısı
Sitedeki yıldız puanı
En pozitif ve en negatif yorumlardan örnekler
görüntülenir.

📌 Gelecek Geliştirmeler (İdealar)
Hepsiburada ve diğer e-ticaret siteleri için ek scraper desteği
Batch çeviri ile daha hızlı M2M100 entegrasyonu
Farklı sentiment modelleri (örneğin çok dilli)
Sonuçları CSV/Excel olarak dışa aktarma
