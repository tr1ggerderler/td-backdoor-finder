import os
import re
import requests

# Author: triggerderler

search_pattern = re.compile(r'[\w\d]{50,}')
hex_list_pattern = re.compile(r"(?:'[\da-fA-F]{2}',\s*){10,}")
find_pattern = ["PerformHttpRequest"]  # Aratılacak şüpheli fonksiyonlar

ignore_patterns = ["discord.com/api/webhooks", "cdn.discordapp.com/attachments"]  # Görmezden gelinecek dizinler
ignore_folders = ["bob74_ipl"]  # Görmezden gelinecek klasör adları
output_file = "results.txt"  # Sonuçların yazılacağı dosya

CURRENT_VERSION = "1.0.0"
REPO_OWNER = "triggerderler"
REPO_NAME = "td-backdoor-finder"

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
            folder_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_results = []

            for line_num, line in enumerate(lines, 1):
                if ignore_patterns and any(pattern in line for pattern in ignore_patterns):
                    continue

                if search_pattern.search(line) or hex_list_pattern.search(line):
                    file_results.append(f"Satır {line_num}: {line.strip()}\n")

                if any(pattern in line for pattern in find_pattern):
                    file_results.append(f"Satır {line_num}: {line.strip()}\n")

            if file_results:
                results.append(f"Klasör yolu: {folder_path}\nSatırın bulunduğu dosya: {file_name}\n")
                results.extend(file_results)
                results.append("\n")

    except Exception as e:
        print(f"Dosya taranırken hata oluştu: {file_path}. Hata: {e}")
    
    return results

def scan_directory(directory):
    if not os.path.exists(directory): 
        print(f"Uyarı: Belirtilen dizin bulunamadı: '{directory}'")
        return 

    print("Bu biraz zaman alabilir, lütfen bekleyin...")

    all_results = []
    for root, dirs, files in os.walk(directory):
        if ignore_folders != [""] and any(ignore_folder in root for ignore_folder in ignore_folders):
            continue
        
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                results = scan_file(file_path)
                all_results.extend(results)

    write_results(all_results)

def check_version():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        if latest_version != CURRENT_VERSION:
            print(f"Yeni sürüm mevcut: {latest_version}. Lütfen güncelleyin.")
        else:
            print("Yazılımınız güncel.")
    except requests.exceptions.RequestException as e:
        print(f"Sürüm kontrolü başarısız: {e}")

if __name__ == "__main__":
    check_version()  # Sürüm kontrolünü çalıştır
    resource_directory = r"C:\Users\burak\Desktop\QBcore\server\resources"
    scan_directory(resource_directory)

    input("Kapatmak için bir tuşa basın...")
