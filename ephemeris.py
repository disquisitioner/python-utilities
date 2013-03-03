#!/usr/bin/python

# Basic ephemeris program (experimental), exploring the capabilities of
# the PyEphem library, which is based on a C library from XEphem.
#
# Author: David Bryant (djbryant@gmail.com)
# Version: 0.2
# Date: February 16, 2013

import ephem
import argparse
import math

#  BODY  | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  | PHASE |
#--------+-----+- ------+--------+-------------+-------------+-------+-------+
#Sun     | No  |   ---  |   ---  | 02/21 06:54 | 02/21 18:55 |  ---  |  ---  |
#Jupiter | Yes | ddd:mm | ddd:mm | mm/dd hh:mm | mm/dd hh:mm | -28.6 | 0.375 |

# Function to pretty print planet info
def print_planet(name,body,location,now):
    body.compute(location)
    if body.alt < 0:
        # print "{:7s}: Not visible".format(name)
        print_visinfo(name,body,location,now)
    else:
        print "{:7s}: is visible now: alt = {}, az = {}, mag = {}".format(name,body.alt,body.az,body.mag)

# Function to format date + time
def fmt_datetime(dttm):
    return "{:02d}/{:02d} {:02d}:{:02d}".format(dttm.month,dttm.day,dttm.hour,dttm.minute)

# Function to format angle (in radians) as dd:mm
def fmt_angle(a):
    a = 180 * a / math.pi # convert radians to degrees
    deg = int(a)
    min = int( ((a - deg) * 60) + 0.5)
    return "{:3d}:{:02d}".format(deg,min)

# Function to handle displaying rise/set information
def print_visinfo(body,location,now):
    body.compute(location)
    # Handle the case when the body is above the horizon (so already rose)
    if body.alt > 0:
        body_rise = ephem.localtime(location.previous_rising(body))
        body_set  = ephem.localtime(location.next_setting(body))
        # Location-based rise/set modifies body attributes, so need to recompute
        body.compute(location)

        r_time = fmt_datetime(body_rise)
        s_time = fmt_datetime(body_set)
        print "{:7s} | Yes | {} | {} | {} | {} | {:5.1f} |".format(body.name, 
            fmt_angle(body.alt),fmt_angle(body.az), r_time, s_time, body.mag)
    else:
        # If the body isn't visible either it hasn't yet risen today, or it already set today
        body_rise = ephem.localtime(location.next_rising(body))
        body_set  = ephem.localtime(location.next_setting(body))
        # Location-based rise/set modifies body attributes, so need to recompute
        body.compute(location)
        r_time = fmt_datetime(body_rise)
        s_time = fmt_datetime(body_set)

        now_tp = now.tuple()
        if body_rise.year == now_tp[0] and body_rise.month == now_tp[1] and body_rise.day == now_tp[2]:
            rise_when = "today"
        else:
            rise_when = "tomorrow"
        if body_set.year == now_tp[0] and body_set.month == now_tp[1] and body_set.day == now_tp[2]:
            set_when = "today"
        else:
            set_when = "tomorrow"
        print "{:7s} | No  |   ---  |   ---  | {} | {} |  ---  |".format(body.name,r_time,s_time)


# ----- Main program functionality starts here -----
# Create the argument parser
parser = argparse.ArgumentParser()

# Arguments supported
#  --now    OPTIONAL, just display current observing info  (up/set, alt, az, etc.)
#  --daily  OPTIONAL, just display daily observing info (rise, set, etc.)

parser.add_argument("--now",
     help="Display only current observing info (up/set, alt, az, etc.)",
     action="store_true")
parser.add_argument("--daily",
     help="Display only daily observing info (rise, set, etc.)",
     action="store_true")

# Parse command line arguments
args = parser.parse_args()


# Get current local time
now = ephem.now()

# Observer at Los Gatos, CA
losgatos = ephem.Observer()
#losgatos.lon = '-121.9676'
#losgatos.lat = '37.1367'
losgatos.lon = '-121.99'
losgatos.lat = '37.2276'
losgatos.elevation = 400
losgatos.date = now
location_name = 'Los Gatos, CA'


print "***** Currently at {} ({})*****".format(location_name,ephem.localtime(losgatos.date))

# First do Sun and Moon
s = ephem.Sun(losgatos)
m = ephem.Moon(losgatos)
# Observer-based rise/set calculations modifies the body involved, so need to create
# 'disposable' ones we don't mind having modififed
s_loc = ephem.Sun(losgatos)
m_loc = ephem.Moon(losgatos)


print "\n*** Sun and Moon ***"
print "  BODY  | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |"
print "--------+-----+--------+--------+-------------+-------------+-------+"
print_visinfo(s_loc,losgatos,now)
print_visinfo(m_loc,losgatos,now)
print "--------+-----+--------+--------+-------------+-------------+-------+"

print "\n*** Lunar Phase information: ***"
prev_new = ephem.previous_new_moon(now)
next_new = ephem.next_new_moon(now)
next_first = ephem.next_first_quarter_moon(now)
next_full = ephem.next_full_moon(now)
next_last = ephem.next_last_quarter_moon(now)

phase = m.moon_phase
lunation = (now-prev_new)/(next_new-prev_new)
# Elaborate on most recent lunar phase

print "Current lunar illumination is {:0.1f}%, lunation is {:0.4f}".format(phase*100,lunation)
if lunation < 0.25:
    print "Was just New Moon at {} UT".format(ephem.previous_new_moon(now))
elif lunation < 0.5:
    print "Was just First Quarter at {} UT".format(ephem.previous_first_quarter_moon(now))
elif lunation < 0.75:
    print "Was just Full Moon at {} UT".format(ephem.previous_full_moon(now))
else:
    print "Was just Last Quarter at {} UT".format(ephem.previous_last_quarter_moon(now))

print "New Moon     : {} UT ({} Local time)".format(next_new,ephem.localtime(next_new))
print "First Quarter: {} UT ({} Local time)".format(next_first,ephem.localtime(next_first))
print "Full Moon    : {} UT ({} Local time)".format(next_full,ephem.localtime(next_full))
print "Last Quarter : {} UT ({} Local time)".format(next_last,ephem.localtime(next_last))

print "\n*** Planets ***"
mercury = ephem.Mercury()
venus   = ephem.Venus()
mars    = ephem.Mars()
jupiter = ephem.Jupiter()
saturn  = ephem.Saturn()
uranus  = ephem.Uranus()
neptune = ephem.Neptune()
pluto   = ephem.Pluto()

print "  BODY  | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |"
print "--------+-----+--------+--------+-------------+-------------+-------+"
print_visinfo(mercury,losgatos,now)
print_visinfo(venus,losgatos,now)
print_visinfo(mars,losgatos,now)
print_visinfo(jupiter,losgatos,now)
print_visinfo(saturn,losgatos,now)
print_visinfo(uranus,losgatos,now)
print_visinfo(neptune,losgatos,now)
print_visinfo(pluto,losgatos,now)
print "--------+-----+--------+--------+-------------+-------------+-------+"

# Look for conjunctions
bodies = [s, m, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto ]
n = len(bodies)
count = 0
threshold = 15.0 * math.pi / 180.0  # 15 degrees

for i in range(n):
    for j in range(i+1,n):
        sep = ephem.separation( (bodies[i].az,bodies[i].alt), (bodies[j].az,bodies[j].alt) )
        if sep < threshold:
            if count == 0:
                print "\n*** Close Approaches (may not be visible) ***"
            print "{:7s} to {:7s} = {} (dd:mm)".format(bodies[i].name,bodies[j].name, fmt_angle(sep))
            count = count + 1

