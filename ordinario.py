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
PIN_AUDIO_SWITCHER = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_HDMI_SWITCHER_INPUT, GPIO.OUT)
GPIO.setup(PIN_HDMI_SPLIITER_OUTOUT, GPIO.OUT)
GPIO.setup(PIN_USB_SWITCHER, GPIO.OUT)
GPIO.setup(PIN_AUDIO_SWITCHER, GPIO.OUT)


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

def change_peripherals_intent():
    # Cambia HDMI
    handle_hdmi_switch_input()
    # Cambia USB
    handle_usb_intent()
    return jsonify(response_alexa('Cambiando HDMI y USB'))

def handle_hdmi_multiple_intent():
    # Cambia HDMI dos veces
    handle_hdmi_switch_input()
    time.sleep(1)
    handle_hdmi_switch_input()
    return jsonify(response_alexa('Cambiando HDMI dos veces'))

def audio_switch_intent():
    GPIO.output(PIN_AUDIO_SWITCHER, GPIO.LOW)
    time.sleep(1)
    GPIO.output(PIN_AUDIO_SWITCHER, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN_AUDIO_SWITCHER, GPIO.LOW)
    return jsonify(response_alexa('Cambiando Audio'))

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
        
        elif intent_name == 'CHANGEPERIFERICSINTENT':
            return change_peripherals_intent()
        
        elif intent_name == 'HANDLEHDMIMULTIPLEINTENT':
            return handle_hdmi_multiple_intent()
        
        elif intent_name == 'AUDIOSWITCHINTENT':
            return audio_switch_intent()

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        GPIO.cleanup()
