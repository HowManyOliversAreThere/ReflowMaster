import network
import urequests
from umqtt.simple import MQTTClient
from machine import Pin

import SECRET

def run():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SECRET.ssid, SECRET.password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

    relay_in = Pin(SECRET.pin, Pin.IN)
    STATES = (b'off', b'on')
    state = relay_in.value()

    client = MQTTClient(SECRET.user, server=SECRET.server)
    client.connect()
    print("Connected to server %s!" % SECRET.server)

    channel = b'cmnd/%s/power' % SECRET.topic
    client.publish(channel, STATES[state])

    while True:
        new_state = relay_in.value()
        if new_state != state:
            state = new_state
            client.publish(channel, STATES[state])
            print("Set state: %s" % state)
