import json
import os
from deep_translator import GoogleTranslator

def translate_text(text, dest='tr'):
    """Metni belirtilen dile çevirir."""
    try:
        if isinstance(text, str) and text.strip():
            return GoogleTranslator(source='auto', target=dest).translate(text)
        return text
    except Exception as e:
        print(f"Çeviri hatası: {e} - Metin: {text}")
        return text

def translate_examples(examples, dest='tr'):
    """Örnek cümleleri çevirir."""
    if not examples:
        return []
    
    translated_examples = []
    for example in examples:
        if isinstance(example, str):
            translated_examples.append(translate_text(example, dest))
    
    return translated_examples

def translate_dictionary(input_file, output_file, dest='tr'):
    """JSON sözlük dosyasını çevirir."""
    try:
        # JSON dosyasını oku
        with open(input_file, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        
        # Her bir kelime girişini çevir
        translated_dict = []
        total = len(dictionary)
        
        for i, entry in enumerate(dictionary):
            print(f"İşlem: {i+1}/{total} - {entry.get('kelime', '')}")
            
            # Olası örnek alanları
            example_keys = ["Ã¶rnekler", "örnekler", "ornekler", "examples"]
            examples = []
            for key in example_keys:
                if key in entry and entry[key]:
                    examples = entry[key]
                    break
            
            # Kelimeyi çevir
            word = entry.get("kelime", "")
            translated_word = translate_text(word, dest) if word else ""
            
            translated_entry = {
                # Kelime çevrilir
                "kelime": translated_word,
                # Kategori aynı kalır
                "kategori": entry.get("kategori", ""),
                
                # Dil bilgisi Türkçe'ye çevrilir
                "dil_bilgisi": translate_text(entry.get("dil_bilgisi", ""), dest),
                
                # Örnekler Türkçe'ye çevrilir
                "ornekler": translate_examples(examples, dest)
            }
            
            translated_dict.append(translated_entry)
            
            # Her 10 girişte bir kaydet (işlem uzun sürebilir)
            if (i + 1) % 10 == 0 or i == total - 1:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(translated_dict, f, ensure_ascii=False, indent=4)
                print(f"Ara kayıt yapıldı: {i+1}/{total}")
        
        print(f"Çeviri tamamlandı. Toplam {len(translated_dict)} kelime çevrildi.")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    # Dosya yolları
    input_file = "C1.json"
    output_file = "C1_Turkce.json"
    
    # Dosya kontrolü
    if not os.path.exists(input_file):
        print(f"Hata: {input_file} dosyası bulunamadı!")
    else:
        print(f"Çeviri başlatılıyor: {input_file} -> {output_file}")
        translate_dictionary(input_file, output_file)
