# client.py
import requests

filename = r"C:\Users\JO\Desktop\Muzammil\FAST_API\stock_app\img.jpg"
files = {'my_file': (filename, open(filename, 'rb'))}
json = {'first': "Hello", 'second': "World"}

response = requests.post(
    'http://192.168.0.82:8005/inventory/upload_image',
    files=files,
    data={'first': "Hello", 'second': "World"}
)
print(response.json())