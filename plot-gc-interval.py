#Name	     plot-gc-interval.py
#Purpose:    Creates scatter plot of glat vs glong for observing time period specified by user
#Usage:      python plot_gc.py -az 180 -alt 70 -day 2021-09-25 -time 09:00 -hours 8.5
#Reference:  https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html#sphx-glr-generated-examples-coordinates-plot-obs-planning-py

import numpy as np
import astropy.units as u
from astropy.time import Time
from datetime import datetime
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Galactic
import matplotlib.pyplot as plt

#Read data provided by user
import argparse
parser = argparse.ArgumentParser(description='plot_gc.py')
parser.add_argument("-alt", "--alt", help="Enter altitude in degrees", type=float)
parser.add_argument("-az", "--az", help="Enter azimuth in degrees", type=float)
parser.add_argument("-day", "--day", help="Enter day like 2021-09-12", type=str)
parser.add_argument("-time", "--time", help="Enter starting local time like 09:00", type=str)
parser.add_argument("-hours", "--hours", help="Enter duration in decimal hours like 4.5", type=float)
args = parser.parse_args()
altitude=args.alt
azimuth=args.az
startday=args.day
starttime=args.time
duration=args.hours

#Program uses information below for calculations
LATITUDE=+41.867; LONGITUDE=-87.630
Chicago = EarthLocation(lat=LATITUDE*u.deg, lon=LONGITUDE*u.deg, height=0*u.m)
print("Latitude",LATITUDE,"Longitude",LONGITUDE)

time_zone=-5.0                # -5 for DST (summer) and -6 for ST (winter)
utcoffset = time_zone*u.hour
start_time=startday+" "+starttime
print("Local Starting Time "+start_time)
print("Time correction in hours "+str(time_zone)+"  where -5 for DST-summer and -6 for ST-winter")

#Create arrays to represent altitude and azimuth.  
alt_array=[altitude]
azi_array=[azimuth]
npoints=500
for i in range(npoints-1):  
    alt_array.append(altitude)
    azi_array.append(azimuth)

hour=np.linspace(0,duration,npoints)*u.hour
times=Time(start_time)-utcoffset+hour
frame=AltAz(obstime=times,location=Chicago)
aa=SkyCoord(alt=alt_array*u.deg,az=azi_array*u.deg,obstime=times,location=Chicago,frame='altaz')
gc=aa.transform_to(Galactic)

#Plot data
ax=plt.axes()
ax.set_title("Altitude, Azimuth, "+str(altitude)+", "+str(azimuth))
ax.scatter(gc.l*u.deg,gc.b*u.deg)
ax.set_xticks([0,40,80,120,160,200,240,280,320,360])
ax.set_yticks([-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90])
plt.xlabel('Galactic Longitude (degrees)')
plt.ylabel('Galactic Latitude (degrees)')

#Generate a line passing through galactic latitude of zero degrees
x=[0];y=[0]
for i in range(360):
    x.append(i)
    y.append(0)
ax.scatter(x,y,marker=".")
plt.grid()
plt.show()
exit()
