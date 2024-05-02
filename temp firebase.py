import time
import board
import busio as io
import adafruit_mlx90614
import pyrebase

i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

config = {
  "apiKey": "database-secret",
  "authDomain": "project-id.firebaseapp.com",
  "databaseURL": "https://database-url.firebaseio.com",
  "storageBucket": "project-id.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

print("Send Data to Firebase Using Raspberry Pi")
print("----------------------------------------")
print()

while True:
  ambientString = "{:.2f}".format(mlx.ambient_temperature)
  objectString = "{:.2f}".format(mlx.object_temperature)

  ambientCelsius = float(ambientString)
  objectCelsius = float(objectString)

  print("Ambient Temp: {} °C".format(ambientString))
  print("Object Temp: {} °C".format(objectString))
  print()

  data = {
    "ambient": ambientCelsius,
    "object": objectCelsius,
  }
  db.child("mlx90614").child("1-set").set(data)
  db.child("mlx90614").child("2-push").push(data)

  time.sleep(2)