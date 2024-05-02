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

# Configuration des broches du capteur SR04
TRIGGER_PIN = 23
ECHO_PIN = 24

# Initialisation de Firebase
firebase = firebase.FirebaseApplication(FIREBASE_URL, None)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # vitesse du son (343 m/s)
    return distance

def main():
    setup()

    try:
        while True:
            distance = get_distance()
            print("Distance: {:.2f} cm".format(distance))

            # Envoyer la distance à Firebase
            firebase.put('/', 'distance', distance)

            time.sleep(5)  # Attendre 5 secondes avant de mesurer à nouveau
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()