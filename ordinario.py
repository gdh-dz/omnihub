import logging
from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# Constants for GPIO pins
PIN_HDMI_SWITCHER_INPUT = 22
PIN_HDMI_SPLIITER_OUTOUT = 27
PIN_USB_SWITCHER = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_HDMI_SWITCHER_INPUT, GPIO.OUT)
GPIO.setup(PIN_HDMI_SPLIITER_OUTOUT, GPIO.OUT)
GPIO.setup(PIN_USB_SWITCHER, GPIO.OUT)

def response_alexa(speech, end_session=True):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "shouldEndSession": end_session
        }
    }

def handle_hdmi_switch_input():
    GPIO.output(PIN_HDMI_SWITCHER_INPUT, GPIO.LOW)
    time.sleep(1)
    GPIO.output(PIN_HDMI_SWITCHER_INPUT, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN_HDMI_SWITCHER_INPUT, GPIO.LOW)
    return jsonify(response_alexa('Cambiando HDMI'))

def handle_usb_intent():
    GPIO.output(PIN_USB_SWITCHER, GPIO.LOW)
    time.sleep(1)
    GPIO.output(PIN_USB_SWITCHER, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN_USB_SWITCHER, GPIO.LOW)
    return jsonify(response_alexa('Cambiando USB'))

def handle_hdmi_output_intent():
    GPIO.output(PIN_HDMI_SPLIITER_OUTOUT, GPIO.LOW)
    time.sleep(1)
    GPIO.output(PIN_HDMI_SPLIITER_OUTOUT, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN_HDMI_SPLIITER_OUTOUT, GPIO.LOW)
    return jsonify(response_alexa('Cambiando Pantallas'))
@app.route('/', methods=['POST'])
def gpio_control():
    data = request.json
    if data['request']['type'] == 'IntentRequest':
        intent_name = data['request']['intent']['name']
        
        if intent_name == 'HDMISWITCHINPUT':
            return handle_hdmi_switch_input()
        
        elif intent_name == 'USBINTENT':
            return handle_usb_intent()
        
        elif intent_name == 'HDMIOUTPUTINTENT':
            return handle_hdmi_output_intent()

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        GPIO.cleanup()
