import os
import re
import http.client

print(""" 
_____________________________________________________________________________________________________________________

                                      T D - B A C K D O O R - F İ N D E R
_____________________________________________________________________________________________________________________
""")

print("Author: triggerderler\n")


resource_directory = r"C:\Users\xxxx\Desktop\FiveM\server\resources" # Hedef klasörünü buraya yazın.

find_pattern = ["PerformHttpRequest"]  # Aratılacak şüpheli fonksiyonlar
ignore_patterns = ["discord.com/api/webhooks", "cdn.discordapp.com/attachments"]  # Görmezden gelinecek dizinler
ignore_folders = ["bob74_ipl"]  # Görmezden gelinecek klasör adları
output_file = "results.txt"  # Sonuçların yazılacağı dosya

search_pattern = re.compile(r'[\w\d]{50,}')
hex_list_pattern = re.compile(r"(?:'[\da-fA-F]{2}',\s*){10,}")

def write_results(results):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(results)
        print(f"İşlem başarılı: Sonuçlar '{output_file}' dosyasına yazıldı.\n")
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

    print("Bu biraz zaman alabilir, lütfen bekleyin...\n")

    all_results = []
    for root, dirs, files in os.walk(directory):
        if ignore_folders and any(ignore_folder in root for ignore_folder in ignore_folders):
            continue
        
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                results = scan_file(file_path)
                all_results.extend(results)

    write_results(all_results)




def check_version():
    local_version = get_local_version()
    github_version = get_version()
    version_info_url = "https://github.com/tr1ggerderler/td-backdoor-finder"
    
    if github_version and local_version:
        if local_version != github_version:
            print(f"Uyarı: Eski bir versiyon kullanıyorsunuz! Lütfen güncelleyin. (Yerel: {local_version}, Güncel: {github_version})\n")
            print(f"Github: {version_info_url}\n")
        else:
            print(f"Sürümünüz güncel! {github_version}\n")

def get_version():
    try:
        conn = http.client.HTTPSConnection("raw.githubusercontent.com")
        conn.request("GET", "/tr1ggerderler/td-backdoor-finder/main/version.txt")
        response = conn.getresponse()

        if response.status == 200:
            return response.read().decode('utf-8').strip()
        else:
            print(f"Versiyon dosyası alınamadı. HTTP Durumu: {response.status}")
            return None
    except Exception as e:
        print(f"Versiyon dosyası okunurken hata oluştu: {e}")
        return None

def get_local_version():
    try:
        with open("version.txt", 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Hata: 'version.txt' dosyası bulunamadı.")
        return None
    except Exception as e:
        print(f"Yerel versiyon dosyası okunurken hata oluştu: {e}")
        return None

if __name__ == "__main__":

    check_version()

    scan_directory(resource_directory)

    input("Kapatmak için [ENTER] tuşuna basın...")
