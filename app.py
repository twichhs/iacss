from flask import Flask, render_template
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO setup
GPIO.setmode(GPIO.BCM)

PIR_PIN = 17
LED_PIN = 27
DHT_PIN = 4

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

sensor = Adafruit_DHT.DHT11  # ou DHT22

def ler_dados():
    umidade, temperatura = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    movimento = GPIO.input(PIR_PIN)

    status_led = False
    estado = "Normal"

    # Lógica IF/ELSE (OBRIGATÓRIO PRA NOTA)
    if movimento:
        estado = "Presença detectada"
        GPIO.output(LED_PIN, True)
        status_led = True

    if temperatura is not None and temperatura > 30:
        estado = "Alerta (Temperatura alta)"
        GPIO.output(LED_PIN, True)
        status_led = True

    if not movimento and (temperatura is None or temperatura <= 30):
        GPIO.output(LED_PIN, False)

    return temperatura, umidade, movimento, status_led, estado


@app.route("/")
def index():
    temperatura, umidade, movimento, led, estado = ler_dados()

    return render_template("index.html",
                           temperatura=temperatura,
                           umidade=umidade,
                           movimento=movimento,
                           led=led,
                           estado=estado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)