import time
import datetime
import random

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

from w1thermsensor import W1ThermSensor

import dweepy

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# DS18B20 temperature sensor on 1-Wire bus
sensor = W1ThermSensor()

# Initialize library.
disp.begin()


def display_info(draw,font,seqno,maxt,mint):
	# Write lines of text.
	draw.text((x, top+font_h), 
		"Sample: {}".format(seqno),
		font=font, fill=255)
	draw.text((x, top+(2*font_h)),
		"Max: {:0.2f}".format(maxt), font=font, fill=255)
	draw.text((x, top+(3*font_h)),
		"Min: {:0.2f}".format(mint), font=font, fill=255)

# Function to calculate timezone offset
def local_time_offset(t=None):
    if t is None:
        t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone

# Function to generate ISO-8601 timestamp with timezone info
def create_timestamp():
	# Build ISO 8601 timestamp with local time but show current TZ offset
	# First figure out our timezone offset
	tzoffset = local_time_offset()
	if tzoffset < 0:
		tz_dir = '-'
		tz_delta = -1 * tzoffset
	else:
		tz_dir = '+'
		tz_delta = tzoffset

	tz_hoff = tz_delta / 3600
	tz_moff = (tz_delta % 3600) / 60

	# Then get local time
	lognow = time.localtime(time.time())

	timestamp = ( '{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}{6:}{7:02d}{8:02d}'.
		  format(lognow.tm_year,lognow.tm_mon,lognow.tm_mday,
		  lognow.tm_hour,lognow.tm_min,lognow.tm_sec,
		  tz_dir,tz_hoff,tz_moff) )
	return timestamp


# Function to publish our temperature reading via dweet.io
def report_dweet(tempF):
	timestamp = create_timestamp()
	# print "At: {} it is {} degrees".format(timestamp,tempF)
	try:
		dweepy.dweet_for('orangemoose-moosetemp',{
			'sensor': "Mooseometer",
			'value': tempF,
			'unit': "degrees F",
			'time': timestamp,
		});
	except Exception, e:
		print e



if __name__ == '__main__':
	# Clear display.
	disp.clear()
	disp.display()

	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	# Draw a black filled box to clear the image.
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	# Load default font.
	# font = ImageFont.load_default()
	font = ImageFont.load("pilfonts/helvR08.pil")
	font_h = 13

	# First define some constants to allow easy resizing of shapes.
	padding = 2
	top = padding
	bottom = height-padding
	x = padding
	seqno = 1
	maxt = -1000
	mint = 1000

	# Initialize random number generator
	random.seed()

	# Fetch our Orangemoose graphic
	om = Image.open('orangemoose.png').convert('1')
	(om_w,om_h) = om.size


	# loop and read temperature
	while True:
		# Read sensor
		tempF = sensor.get_temperature(W1ThermSensor.DEGREES_F)
		if tempF > maxt:
			maxt = tempF
		if tempF < mint:
			mint = tempF

		# Convert temperature to string and get its rendering extent
		tempFstr = "{:0.2f}".format(tempF)
		(tw,th) = draw.textsize(tempFstr,font=font)

		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)

		# Place Orangemoose randomly
		dx = int(random.random()*(disp.width-om_w))
		dy = int(random.random()*(disp.height-om_h-font_h-padding))
		image.paste(om,(dx,dy))

		# Add current temp
		x = dx + (om_w/2) - tw/2
		y = dy + om_h + padding
		draw.text((x, y),tempFstr, font=font, fill=255)

		# Display image.
		disp.image(image)
		disp.display()

		# Publish temperature via dweet.io
		report_dweet(tempF)

		# Wait until time for next sensor reading
		seqno += 1
		time.sleep(120)


