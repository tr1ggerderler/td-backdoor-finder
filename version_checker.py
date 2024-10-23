import urllib.request
import json

CURRENT_VERSION = "1.0.0"  # Mevcut sürümünüzü buraya yazın
REPO_OWNER = "triggerderler"  # Proje sahibi
REPO_NAME = "td-backdoor-finder"  # Proje adı

def check_version():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            latest_release = json.loads(data)
            latest_version = latest_release["tag_name"]
            print(f"En son sürüm: {latest_version}")
            if latest_version != CURRENT_VERSION:
                print(f"Yeni sürüm mevcut: {latest_version}. Lütfen güncelleyin.")
            else:
                print("Yazılımınız güncel.")
    except urllib.error.URLError as e:
        print(f"Sürüm kontrolü başarısız: {e}")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

if __name__ == "__main__":
    check_version()
