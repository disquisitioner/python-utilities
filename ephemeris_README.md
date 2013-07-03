# Ephemeris - Observing the Sun, Moon and Planets

As an amateur astronomer I like knowing what's going on in the night sky.  There are a number of web sites that will tell you bits and pieces of what I'd like to know, and an assortment of applications for mobile phones and tables that attempt to do so as well.  None of them was exactly what I was looking for, so I decided to write my own in Python.

Happily I discovered the excellent [PyEphem package](http://rodesmill.org/pyephem), which provides Python classes and functions atop the excellent [XEphem](http://www.clearskyinstitute.com/xephem) library by Elwood Downey.

## Usage 

Ephemeris needs to know the location for which you would like the observing information.  By default it will show you visibilty information at the current local time (based on the clock of your computer) but you can also specify a date and time to be used for the visibility calculations.

```
ephemeris.py [--city 'city'] [--date 'YYYY/MM/DD HH:MM']
```

## Sample Output
    ***** Currently at Los Gatos (03/09/2013 17:48:48) *****
    
    *** Sun and Moon ***
           BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |
    -------------------+-----+--------+--------+-------------+-------------+-------+
    Sun............... | Yes |   3:34 | 262:16 | 03/09 06:27 | 03/09 18:10 | -26.8 |
    Moon.............. | No  |   ---  |   ---  | 03/10 06:28 | 03/10 18:25 |  ---  |
    -------------------+-----+--------+--------+-------------+-------------+-------+
    
    *** Lunar Phase information: ***
    Current lunar illumination is 3.9%, lunation is 0.9407
    Was just Last Quarter at 03/04/2013 21:52:48.4 UT
    New Moon     : 03/11/2013 19:51:00.1 UT (03/11/2013 12:51:00 Local time)
    First Quarter: 03/19/2013 17:26:34.4 UT (03/19/2013 10:26:34 Local time)
    Full Moon    : 03/27/2013 09:27:18.2 UT (03/27/2013 02:27:18 Local time)
    Last Quarter : 04/03/2013 04:36:33.7 UT (04/02/2013 21:36:33 Local time)
    
    *** Planets ***
           BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |
    -------------------+-----+--------+--------+-------------+-------------+-------+
    Mercury........... | No  |   ---  |   ---  | 03/10 06:45 | 03/10 18:11 |  ---  |
    Venus............. | No  |   ---  |   ---  | 03/10 07:22 | 03/10 18:45 |  ---  |
    Mars.............. | Yes |  11:35 | 259:17 | 03/09 06:53 | 03/09 18:49 |   1.2 |
    Jupiter........... | Yes |  73:14 | 199:53 | 03/09 10:13 | 03/10 00:35 |  -2.1 |
    Saturn............ | No  |   ---  |   ---  | 03/09 22:10 | 03/10 09:55 |  ---  |
    Uranus............ | Yes |  20:23 | 256:52 | 03/09 07:16 | 03/09 19:34 |   5.9 |
    Neptune........... | No  |   ---  |   ---  | 03/10 06:47 | 03/10 17:44 |  ---  |
    Pluto............. | No  |   ---  |   ---  | 03/10 03:42 | 03/10 13:41 |  ---  |
    -------------------+-----+--------+--------+-------------+-------------+-------+
    
    *** Close Approaches (may not be visible) ***
    Sun     to Mercury =  11:20 (dd:mm)
    Sun     to Venus   =   4:21 (dd:mm)
    Sun     to Mars    =   8:33 (dd:mm)
    Moon    to Mercury =  12:29 (dd:mm)
    Moon    to Neptune =   8:46 (dd:mm)
    Mercury to Venus   =   7:60 (dd:mm)
    Mercury to Neptune =   6:30 (dd:mm)
    Venus   to Mars    =  12:41 (dd:mm)
    Venus   to Neptune =  12:15 (dd:mm)
    Mars    to Uranus  =   9:06 (dd:mm)
    
    *** Special Objects ***
           BODY        | VIS |   ALT  |   AZ   |    RISE     |     SET     |  MAG  |
    -------------------+-----+--------+--------+-------------+-------------+-------+
    C/Pan-STARRS...... | Yes |  14:30 | 251:41 | 03/09 07:36 | 03/09 19:06 |   0.5 |
    C/ISON............ | Yes |  65:56 |  95:48 | 03/09 11:49 | 03/10 04:33 |  15.6 |
    -------------------+-----+--------+--------+-------------+-------------+-------+
    
