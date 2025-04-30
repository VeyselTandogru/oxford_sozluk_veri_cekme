import json
import os

# İngilizce ve Türkçe verileri oku
with open("C1.json", "r", encoding="utf-8") as f_en, open("C1_Turkce.json", "r", encoding="utf-8") as f_tr:
    en_data = json.load(f_en)
    tr_data = json.load(f_tr)

# Eğer merged.json dosyası varsa onu da oku, yoksa boş liste olarak başla
if os.path.exists("merged.json"):
    with open("merged.json", "r", encoding="utf-8") as f_merged:
        existing_data = json.load(f_merged)
else:
    existing_data = []

# Yeni verileri oluştur
new_merged_data = []
for en_item, tr_item in zip(en_data, tr_data):
    merged_item = {
        "kelime": en_item.get("kelime"),
        "kategori": en_item.get("kategori"),
        "dil_bilgisi": en_item.get("dil_bilgisi"),
        "örnekler": en_item.get("örnekler"),
        "turkceKelime": tr_item.get("kelime"),
        "turkceKategori": tr_item.get("kategori"),
        "turkceDilBilgisi": tr_item.get("dil_bilgisi"),
        "turkceÖrnekler": tr_item.get("ornekler")
    }
    new_merged_data.append(merged_item)

# Eski ve yeni verileri birleştir
combined_data = existing_data + new_merged_data

# Sonuçları merged.json'a yaz
with open("merged.json", "w", encoding="utf-8") as f_out:
    json.dump(combined_data, f_out, ensure_ascii=False, indent=4)

print("✅ Yeni veriler mevcut 'merged.json' dosyasına eklendi.")
