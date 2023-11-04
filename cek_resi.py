import argparse
import requests

def response_data():
  api_url = f"https://api.binderbyte.com/v1/track?api_key=7355af5dd29cf5cf36854c280018d6faed94c4990b9430c57feb0c31b9119d02&courier={args.kurir}&awb={args.nomor_resi}"
  response = requests.get(api_url)
  
  if response.status_code == 200:
    return response.json()
  else:
    exit("Data tidak ditemukan!")

def status_detail():
  print('\nDetail paket: \n' + '='*12 + '\n')
  data = response_data().get("data")["summary"]
  datas = response_data().get("data")["detail"]
  history = response_data().get("data")["history"]

  awb = data["awb"]
  courier = data["courier"]
  service = data["service"]
  status = data["status"]
  date = data["date"]
  desc = data["desc"]
  weight = data["weight"]
  
  origin = datas["origin"]
  destination = datas["destination"]
  shipper = datas["shipper"]
  receiver = datas["receiver"]
  
  print("No.resi :", awb)
  print("Kurir :", courier)
  print("Layanan :", service)
  print("Status :", status)
  print("Waktu :", date)
  print("Deskripsi :", desc)
  print("Berat :", weight)
  print("\nLokasi :", origin)
  print("Tujuan :", destination)
  print("Pengirim :", shipper)
  print("Penerima :", receiver)
  
  print("\nHistori Paket :\n" + "="*15)
  for history_packet in history:
    print("\nTanggal :",history_packet.get("date"))
    print("Status :", history_packet.get("desc"))
    print("Lokasi :", history_packet.get("location"))

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Scrape informasi nomor resi")
  parser.add_argument("--kurir", required=True, help="Nama kurir (contoh: jne)")
  parser.add_argument("--nomor_resi", required=True, help="Nomor resi")
  
  args = parser.parse_args()
  status_detail()