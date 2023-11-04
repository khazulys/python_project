import requests
import argparse
from tqdm import tqdm
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

def get_response_url():
  url = f"https://apkpure.com/id/search?q={args.download}&t=app"
  response = requests.get(url, headers={'User-Agent': ua.random})
  soup = BeautifulSoup(response.text, "html.parser")
  find = soup.find("p", attrs={"class":"p1"})
  try:
    download_link = soup.find("a", attrs={"class":"da is-download"})
    download_url = download_link.get("href")
  
    return download_url
  except AttributeError:
    keyword = find.text.replace(" ", "+").lower()
    second_url = f"https://apkpure.com/id/search?q={keyword}&t=app"
    response = requests.get(second_url, headers={'User-Agent': ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    
    download_link = soup.find("a", attrs={"class":"da is-download"})
    download_url = download_link.get("href")
    return download_url
    
def downloads_url():
  response= requests.get(get_response_url(), headers={"User-Agent": ua.random})
  soup = BeautifulSoup(response.text, "html.parser")
  find = soup.find("a", attrs={"class":"btn download-start-btn"})
  return find.get("href")
  
def main_download():
  filename = downloads_url().split("/")[-1]
  filenames = filename.split("?")[0]
  
  response = requests.get(downloads_url(), headers={"User-Agent": ua.random}, stream=True)
  if response.status_code == 200:
    total_size = int(response.headers.get("content-length", 0))
    
    with open(f"{filenames}.apk", "wb") as file, tqdm(
      desc=filenames,
      total=total_size,
      unit="B",
      unit_scale=True,
      unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
          file.write(data)
          bar.update(len(data))
    
    print("Unduhan selesai")
  else:
    print("Unduhan gagal")

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="APK Downloader")
  parser.add_argument("--download", required=True, help="Nama app (contoh: facebook)")
  
  args = parser.parse_args()
  main_download()
  #print(get_response_url())