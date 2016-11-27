python-utilities
================

Assorted utilities programs written in Python, mostly to make it easier to do interesting things with my Raspberry Pi.

Here's what is here currently...
* Kribensis -- A Python Dropbox client that supports easy file transfer from a local machine to Dropbox, or retrieval of a file from Dropbox.  See `kribensis_README.md` for more details.

* Ephemeris -- Uses the PyEphem package to calculate observational information for the Sun, Moon and planets for observers at any location.  See `ephemeris_README.md` for more details.

* Mooseometer -- Simple thermometer for Raspberry Pi using libraries to support reading temperature from a DS18B20 via the Onewire protocol and W1ThermSensor library.  The current temperature is displayed on an OLED using the Adafruit SSD1306 library. For fun, the data read is displayed along with the Orangemoose 'moose head' logo and is also uploaded to dweet.io using the dweepy library.  You'll find the logo image file 'orangemoose.png' here, along with a simple start/start script ('mminit') for launching the Mooseometer (which needs to be run as root so as to read data via GPIO).
