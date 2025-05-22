import requests

# URL endpoint API yang ingin diakses
url = 'https://jsonplaceholder.typicode.com/comments'

# Parameter (berdasarkan dokumentasi jsonplaceholder)
params = {
    'postId': 1  # Misalnya ambil komentar dari post dengan ID 1
}

# Mengirim request GET tanpa header Authorization karena tidak dibutuhkan
response = requests.get(url, params=params)

# Mengecek status code dan menampilkan hasil
if response.status_code == 200:
    data = response.json()
    print("Data berhasil diambil:")
    for comment in data:
        print(
            f"ID: {comment['id']} - Email: {comment['email']} - Komentar: {comment['body'][:30]}...")
else:
    print(f"Gagal mengambil data. Status code: {response.status_code}")
    print(response.text)
