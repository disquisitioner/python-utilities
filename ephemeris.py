#!/usr/bin/python

# Basic ephemeris program (experimental), exploring the capabilities of
# the PyEphem library, which is based on a C library from XEphem.
#
# Author: David Bryant (djbryant@gmail.com)
# Version: 1.0
# Date: March 3, 2013

import ephem
import argparse
import math

# Here's the output table we want to generate:
#
#       BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |
#-------------------+-----+--------+--------+-------------+-------------+-------+
#Sun                | No  |   ---  |   ---  | 02/21 06:54 | 02/21 18:55 |  ---  |
#Jupiter            | Yes | ddd:mm | ddd:mm | mm/dd hh:mm | mm/dd hh:mm | -28.6 |

# Short lists of additional cities of interest not known to PyEphem
_mycity_data = {
    'Los Gatos': ('37.2276', '-121.99', 400),  # California USA
    'Manaus': ('-3.12854', '-60.00018', 41.4),  # Amazonas, Brazil
    }

# And a utility function to look up a city in our additional list
def additional_city(name):
    try:
        data = _mycity_data[name]
    except KeyError:
        raise KeyError('Unknown city: %r' % (name,))
    o = ephem.Observer()
    o.name = name
    o.lat, o.lon, o.elevation = data
    o.compute_pressure()
    return o


# Function to fully display a datetime object (the way I like to see it :-)
def fmt_fulldatetime(dttm):
    return "{:02d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        dttm.month,dttm.day,dttm.year,
        dttm.hour,dttm.minute,dttm.second)

# Function to format a datetime object just as day/mo + hr:min
def fmt_datetime(dttm):
    return "{:02d}/{:02d} {:02d}:{:02d}".format(dttm.month,dttm.day,dttm.hour,dttm.minute)

# Function to format angle (in radians) as dd:mm
def fmt_angle(a):
    a = 180 * a / math.pi # convert radians to degrees
    deg = int(a)
    min = int( ((a - deg) * 60) + 0.5)
    return "{:3d}:{:02d}".format(deg,min)

# Function to format a Date object the way I like to see it
def fmt_date(date):
    d = date.tuple()
    return "{:02d}/{:02d}/{:02d} {:02d}:{:02d}:{:04.1f}".format(
        d[1],d[2],d[0],d[3],d[4],d[5])

# Function to generate the output table entry for a body at a specific location.  Note
# that the location object contains the specific time of interest (location.date)
def print_visinfo(body,location):
    body.compute(location) # Compute the viewing details
    # Handle the case when the body is above the horizon (so already rose)
    if body.alt > 0:
        # Body might have risen yesterday (is circumpolar)
        try:
            body_rise = ephem.localtime(location.previous_rising(body))
            r_time = fmt_datetime(body_rise)
        except ephem.CircumpolarError:
            r_time = "already up "

        # Body might not set today (is circumpolar)
        try:
            body_set  = ephem.localtime(location.next_setting(body))
            s_time = fmt_datetime(body_set)
        except ephem.CircumpolarError:
            s_time = "doesn't set"
        # Location-based rise/set modifies body attributes, so need to recompute
        body.compute(location)
        print "{:.<19.19s}| Yes | {} | {} | {} | {} | {:5.1f} |".format(body.name, 
            fmt_angle(body.alt),fmt_angle(body.az), r_time, s_time, body.mag)
    else:
        # If the body isn't visible either it hasn't yet risen today, or it already set today
        body_rise = ephem.localtime(location.next_rising(body))
        body_set  = ephem.localtime(location.next_setting(body))
        # Location-based rise/set modifies body attributes, so need to recompute
        body.compute(location)
        r_time = fmt_datetime(body_rise)
        s_time = fmt_datetime(body_set)
        print "{:.<19.19s}| No  |   ---  |   ---  | {} | {} |  ---  |".format(body.name,r_time,s_time)


# ----- Main program functionality starts here -----

# Create the argument parser
parser = argparse.ArgumentParser()

# Arguments supported
#  -c,--city  OPTIONAL, specifies the city of the observer
#  -d,--date  OPTIONAL, specifies the date and time (in UT) for the observation

parser.add_argument("-c","--city",help="City of the observer",
	default="Los Gatos")
parser.add_argument("-d","--date",help="Specify date and time in UT ('yyyy/mm/dd hh:mm') for the observer")

args = parser.parse_args()

# Look up the observer's city using both the list built into PyEphem and our own
# private one defined here
try:
    site = ephem.city(args.city)
except KeyError:
    try:
        site = additional_city(args.city)
    except:
        print "City '{}' not found in global or local list".format(args.city)
        exit(0)
        

# Get current time and use that for our observer.  Note that the result of
# ephem.now() is a time in UT so it isn't location dependent.  However, the 
# times displayed by ephem.localtime() will be converted to whatever time and
# timezone the clock on your computer is set to.  This might confuse you if
# you specify an observer location in a time zone other than where you are now,
# but if you think about it carefully you'll see that the information displayed
# is correct.
if args.date:
    now = ephem.Date(args.date)
else:
    now = ephem.now()

site.date = now

# Generate the output information
print "***** Currently at {} ({}) *****".format(site.name,
    fmt_fulldatetime(ephem.localtime(site.date)))

# First do Sun and Moon
s = ephem.Sun(site)
m = ephem.Moon(site)
# Observer-based rise/set calculations modifies the body involved, so need to create
# 'disposable' ones we don't mind having modififed
s_loc = ephem.Sun(site)
m_loc = ephem.Moon(site)


print "\n*** Sun and Moon ***"
print "       BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |"
print "-------------------+-----+--------+--------+-------------+-------------+-------+"
print_visinfo(s_loc,site)
print_visinfo(m_loc,site)
print "-------------------+-----+--------+--------+-------------+-------------+-------+"

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
    print "Was just New Moon at {} UT".format(fmt_date(ephem.previous_new_moon(now)))
elif lunation < 0.5:
    print "Was just First Quarter at {} UT".format(fmt_date(ephem.previous_first_quarter_moon(now)))
elif lunation < 0.75:
    print "Was just Full Moon at {} UT".format(fmt_date(ephem.previous_full_moon(now)))
else:
    print "Was just Last Quarter at {} UT".format(fmt_date(ephem.previous_last_quarter_moon(now)))

print "New Moon     : {} UT ({} Local time)".format(
    fmt_date(next_new),fmt_fulldatetime(ephem.localtime(next_new)))
print "First Quarter: {} UT ({} Local time)".format(
    fmt_date(next_first),fmt_fulldatetime(ephem.localtime(next_first)))
print "Full Moon    : {} UT ({} Local time)".format(
    fmt_date(next_full),fmt_fulldatetime(ephem.localtime(next_full)))
print "Last Quarter : {} UT ({} Local time)".format(
    fmt_date(next_last),fmt_fulldatetime(ephem.localtime(next_last)))

print "\n*** Planets ***"
mercury = ephem.Mercury()
venus   = ephem.Venus()
mars    = ephem.Mars()
jupiter = ephem.Jupiter()
saturn  = ephem.Saturn()
uranus  = ephem.Uranus()
neptune = ephem.Neptune()
pluto   = ephem.Pluto()

print "       BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |"
print "-------------------+-----+--------+--------+-------------+-------------+-------+"
print_visinfo(mercury,site)
print_visinfo(venus,site)
print_visinfo(mars,site)
print_visinfo(jupiter,site)
print_visinfo(saturn,site)
print_visinfo(uranus,site)
print_visinfo(neptune,site)
print_visinfo(pluto,site)
print "-------------------+-----+--------+--------+-------------+-------------+-------+"

# Look for conjunctions

# M45 (The Pleiades) is close enough to the ecliptic that we'll include it in
# conjunction searches.

# Create a body for M45 (The Pleiades) by parsing its attributes in XEphem format
m45_x = "M45,f|U,3:47:0,24:07:0,1.6,2000,0"
m45 = ephem.readdb(m45_x)
m45.compute(site) # Compute observation values for our specified site

bodies = [s, m, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto, m45 ]
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


# Handle special objects such as comets
print "\n*** Special Objects ***"
print "       BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |"
print "-------------------+-----+--------+--------+-------------+-------------+-------+"
panstarrs_x = "C/Pan-STARRS,h, 3/10.1691/2013,84.2072,65.6659,333.6512,1.000033,0.301546, 1/01/2000,5.5,4,0"
panstarrs = ephem.readdb(panstarrs_x)
print_visinfo(panstarrs,site);

ison_x = "C/ISON,h,11/28.7929/2013,61.882,295.7335,345.5117,1.000004,0.012501, 1/01/2000,6,4,0"
ison = ephem.readdb(ison_x)
print_visinfo(ison,site)
print "-------------------+-----+--------+--------+-------------+-------------+-------+"
