# -*- coding: utf-8 -*-
import sys
import time
import json
import requests

#Import Blinka
import digitalio
import board
# Import Python Imaging Library
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import pools


if len(sys.argv) != 3 or (sys.argv[1] != "ethermine" and sys.argv[1] != "flexpool" and sys.argv[1] != "hiveon"):
    print("Usage: sudo python3 miner.py ethermine|flexpool|hiveon wallet")
    exit

pool = sys.argv[1]
wallet = sys.argv[2]
if wallet.startswith("0x"):
    wallet = wallet[2:]

value_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
                     width=135, height=240, x_offset=53, y_offset=40)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width   # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new('RGB', (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
big_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48)
small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)

font_height = font.getsize("a")[1]
big_font_height = big_font.getsize("a")[1]

red = "#FF0000"
green = "#00FF00"
blue = "#0000FF"
yellow = "#FFFF00"

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Add buttons as inputs
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input()

duration = 300
counter = duration

state = 0
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if counter == duration:
        try:
            miner_data = pools.mine_values(wallet) if pool == "ethermine" else pools.get_flexpool_values(wallet) if pool == "flexpool" else pools.get_hiveon_values(wallet)
            r = requests.get(value_api_url)
            data = json.loads(r.text)
            eth_value = data["ethereum"]["usd"]
        except:
            y = top
            draw.text((x,y),"ERROR LOADING DATA", font=font, fill=red)
            print("error")
            time.sleep(60)
            continue

    y = top

    if not buttonA.value:
        state = 1 if state == 0 else 0

    if state == 0:
        draw.text((x,y),"{:.5f}".format(miner_data["unpaid"]),font=big_font, fill=green if miner_data["workers"] >= 2 and miner_data["invalid_shares"] < 3 else red)
        y += big_font_height
        draw.text((x,y),"${:.2f}".format(miner_data["unpaid"]*eth_value), font=big_font, fill=green)
        y += big_font_height
        draw.text((x,y),"${:.2f}".format(eth_value), font=big_font, fill=green)
        draw.text((width-40,0), str(counter), font=small_font, fill=yellow)
    else:
        draw.text((x,y),"Unpaid: ", font=font, fill=blue)
        draw.text((x+font.getsize("Unpaid: ")[0],y), "{:.5f}".format(miner_data["unpaid"]), font=font, fill=green)
        y += font_height
        draw.text((x,y),"Value: ", font=font, fill=blue)
        draw.text((x+font.getsize("Value: ")[0],y+5), "${:.2f} ${:.2f}".format(eth_value*miner_data["unpaid"], eth_value), font=small_font, fill=green)
        y += font_height
        draw.text((x,y),"Workers: Mh/s (R/A):", font=font, fill=blue)
        y += font_height
        draw.text((x,y), "{}: {:.1f} / ".format(miner_data["workers"], miner_data["reported_hashrate"]), font=font, fill=green)
        draw.text((x+font.getsize("{} - {:.1f} / ".format(miner_data["workers"], miner_data["reported_hashrate"]))[0],y), "{:.1f}".format(miner_data["actual_hashrate"]), font=font, fill=green if miner_data["actual_hashrate"] >= miner_data["reported_hashrate"] else yellow)
        y += font_height
        draw.text((x,y),"Stale / Invalid: ", font=font, fill=blue)
        draw.text((x+font.getsize("Stale / Invalid: ")[0],y), str(miner_data["stale_shares"]), font=font, fill=green)
        draw.text((x+font.getsize("Stale / Invalid: {}".format(miner_data["stale_shares"]))[0],y), " / ", font=font, fill=blue)
        draw.text((x+font.getsize("Stale / Invalid: {} / ".format(miner_data["stale_shares"]))[0],y),str(miner_data["invalid_shares"]), font=font, fill=green if miner_data["invalid_shares"] == 0 else red)
        y += font_height
        draw.text((x,y), str(counter), font=small_font, fill=yellow)

    # Display image.
    disp.image(image, rotation)
    counter -= 1
    
    if counter == 0:
        counter = duration
    time.sleep(1)



