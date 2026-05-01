from flask import Flask, render_template
import adafruit_dht
import board
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO setup
GPIO.setmode(GPIO.BCM)

PIR_PIN = 17
LED_PIN = 27

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

dht = adafruit_dht.DHT11(board.D4)


def ler_dados():
    temperatura = None
    umidade = None
    movimento = False
    led = False
    estado = "Normal"

    # Leitura do DHT
    try:
        temperatura = dht.temperature
        umidade = dht.humidity
    except RuntimeError:
        pass
    except Exception as e:
        dht.exit()
        raise e

    # Leitura do PIR (SEMPRE fora do try)
    movimento = GPIO.input(PIR_PIN)

    # Lógica IF/ELSE
    if movimento:
        estado = "Presença detectada"
        GPIO.output(LED_PIN, True)
        led = True

    elif temperatura is not None and temperatura > 30:
        estado = "Alerta (Temperatura alta)"
        GPIO.output(LED_PIN, True)
        led = True

    else:
        GPIO.output(LED_PIN, False)
        led = False

    return temperatura, umidade, movimento, led, estado


@app.route("/")
def index():
    temperatura, umidade, movimento, led, estado = ler_dados()

    return render_template(
        "index.html",
        temperatura=temperatura,
        umidade=umidade,
        movimento=movimento,
        led=led,
        estado=estado
    )


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()
