import requests
import argparse
from tqdm import tqdm

def send_requests(url_video):
  url = "https://tiktok-download-video-no-watermark.p.rapidapi.com/tiktok/info"
  data = {"url":url_video}
  headers = {
    "X-RapidAPI-Key": "4633877495msh33a460d911384a3p1e63fdjsnd7724771fb4d",
    "X-RapidAPI-Host": "tiktok-download-video-no-watermark.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=data)
  return response.json()

def collect_data():
  get_data = send_requests(args.download)
  
  video_id = get_data["data"].get("id")
  video_desc = get_data["data"].get("desc")
  author = get_data["data"].get("author_nickname")
  author_id = get_data["data"].get("author_unique_id")
  
  likes_count = get_data["data"]["statistics"].get("digg_count")
  comments_count = get_data["data"]["statistics"].get("comment_count")
  shares_count = get_data["data"]["statistics"].get("share_count")
  
  print("\nData video ditemukan\n" + "="*20)
  print("\nVideo id : %s" % (video_id))
  print("Deskripsi : %s" % (video_desc))
  print("Pembuat : %s" % (author))
  print("Username : %s" % (author_id))
  print("\nLike : %s" % (likes_count))
  print("Komentar : %s" % (comments_count))
  print("Share : %s \n" % (shares_count))

def start_download():
  get_data = send_requests(args.download)
  download_link = get_data["data"].get("video_link_nwm")
  
  video_id = get_data["data"].get("id")
  response = requests.get(download_link, stream=True)
  if response.status_code == 200:
    total_size = int(response.headers.get("content-length", 0))
    with open(f"{video_id}.mp4", "wb") as file, tqdm(
        desc=video_id,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
          file.write(data)
          bar.update(len(data))
          
    print("Unduhan selesai") 
  else:
    print("Unduhan gagal")
    
if __name__=="__main__":
  parser = argparse.ArgumentParser(description="TikTok Video Downloader")
  parser.add_argument("--download", required=True, help="Video Url")
  
  args = parser.parse_args()
  collect_data()
  start_download()