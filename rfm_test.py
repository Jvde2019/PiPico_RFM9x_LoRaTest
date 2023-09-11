# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of sending and recieving data with the RFM95 LoRa radio.
# Author: Tony DiCola
import board
import busio
import digitalio
import adafruit_rfm9x

#display
# Import all board pins.
from board import SCL, SDA
import busio
# Import the SSD1306 module.
import adafruit_ssd1306
# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Define radio parameters.
RADIO_FREQ_MHZ = 868.0
#RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)
# Or uncomment and instead use these if using a Feather M0 RFM9x board and the appropriate
# CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM9X_CS)
# RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 23

# Send a packet.  Note you can only send a packet up to 252 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
rfm9x.send(bytes("Hello world!\r\n", "utf-8"))
print("Sent Hello World message!")

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 252 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print("Waiting for packets...")

while True:
    packet = rfm9x.receive()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        #LED.value = False
        print("Received nothing! Listening again...")
    else:
        # Received a packet!
        #LED.value = True
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet))
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        packet_text = str(packet, "ascii")
        print("Received (ASCII): {0}".format(packet_text))
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))
        LED.value = True
        #rfm9x.send(bytes("Hello world!\r\n", "utf-8"))
        rfm9x.send(bytes(packet_text, "utf-8"))
        LED.value = False
        
        # Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
        display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
#         display.fill(0)
# 
#         display.show()
# 
# # Set a pixel in the origin 0,0 position.
#         display.pixel(0, 0, 1)
# # Set a pixel in the middle 64, 16 position.
#         display.pixel(64, 16, 1)
# # Set a pixel in the opposite 127, 31 position.
#         display.pixel(127, 31, 1)
#         display.show()
        display.fill(0)
#    button = 1  # Read button switch
        #pot = 100
        #msg = "Pot RAW: " + str(pot) +"   "
        display.text("RFM 9x LoRa-Test",0,0,2)
        #power = int(255 * pot / 65300)  # Range 0 to 255
        #msg = "Power: " + str(power)+"   "
        msg = "signal: "+str (rssi)+" dB"
        display.text(msg,0, 18,1)
        #display.text("  ? C", 90,20,1)   # No temperature sensor fitted
        display.text(packet_text,0,28,2)
#    deg(110,20)                   # Degree character
        #val = int(power * 100 / 255)  # Range 0 to 100 ('T')
#    showgraph(val)
#     if button == 1:  # This is the slow part of the loop
#         oled.text("1",6,34,1)
#         char(16, 30, up_arrow)    # Defined characters
#         char(34, 30, smiley)      # when button UP
#         char(54, 30, heart)
#         oled.text("True", 80,36,1)
#     else:
#         oled.text("0",6,34,1)
#         char(16, 30, down_arrow)  # Defined characters
#         char(34, 30, sad)         # when button pressed
#         char(54, 30, b_heart)
#         oled.text("False",80,36,1)
        display.show()
