import os
import re

# Author: triggerderler

search_pattern = re.compile(r'[\w\d]{50,}')
ignore_patterns = ["discord.com/api/webhooks", "cdn.discordapp.com/attachments"]
ignore_folders = ["boş-kalmamalı"]  # Görmezden gelinecek klasör adları
http_request_pattern = "PerformHttpRequest"
output_file = "results.txt"  # Sonuçların yazılacağı dosya adı

def write_results(results):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(results)
        print(f"İşlem başarılı: Sonuçlar '{output_file}' dosyasına yazıldı.")
    except Exception as e:
        print(f"Sonuçlar dosyası oluşturulurken hata oluştu: {e}")

def scan_file(file_path):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, 1):
                if any(pattern in line for pattern in ignore_patterns):
                    continue
                
                folder_path = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
                
                if search_pattern.search(line):
                    results.append(f"Klasör yolu: {folder_path}\nSatırın bulunduğu dosya: {file_name}\nBulunan satır:\n{line.strip()}\n\n")
                
                if http_request_pattern in line:
                    results.append(f"Klasör yolu: {folder_path}\nSatırın bulunduğu dosya: {file_name}\nBulunan satır:\n{line.strip()}\n\n")

    except Exception as e:
        print(f"Dosya taranırken hata oluştu: {file_path}. Hata: {e}")
    
    return results

def scan_directory(directory):
    if not os.path.exists(directory): 
        print(f"Uyarı: Belirtilen dizin bulunamadı: '{directory}'")
        return 

    all_results = []
    for root, dirs, files in os.walk(directory):
        if any(ignore_folder in root for ignore_folder in ignore_folders):
            continue
        
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                results = scan_file(file_path)
                all_results.extend(results)

    write_results(all_results)

if __name__ == "__main__":
    resource_directory = r"C:\FiveM\server-data\resources"
    scan_directory(resource_directory)

    input("Tarama tamamlandı. Kapatmak için bir tuşa basın...")
