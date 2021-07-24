#!/usr/bin/env bash
lat=144.4951;
lon=50.1391;
#lat=151.0098;
#lon=48.7847;
lat=-20.5293
lon=21.0439
proj='JG';
globe='/home/pi/Desktop/globe.ps';
finished_globe='/home/pi/Desktop/globe.png';

start_lat=-20.5293
start_lon=21.0439

end_start_lat=-18.4356
end_start_lon=22.8053
mul=10

end_lat=`echo "scale=4; $start_lat - $end_start_lat" | bc`;
end_lat=`echo "scale=4; $end_lat * $mul" | bc`;
end_lat=`echo "scale=4; $start_lat - $end_lat" | bc`;

end_lon=`echo "scale=4; $start_lon - $end_start_lon" | bc`;
end_lon=`echo "scale=4; $end_lon - $mul" | bc`;
end_lon=`echo "scale=4; $start_lon - $end_lon" | bc`;



echo $end_lon;
#end_lat=(expr $start_lat - $end_lat);
gmt pscoast -Rg -$proj$lat/$lon/6i -Bag -Dc -A5000 -Gforestgreen -Sblue3 -BWSne+t"ISS" -P -K > $globe;
gmt psxy -R -$proj -O -K -Wfat,100/25/30/4  <<END >> /home/pi/Desktop/globe.ps
$start_lat $start_lon
$end_lat $end_lon
END
gmt psimage /home/pi/Desktop/ISSIcon.png -Dg$lat/$lon+w1i -Rg -$proj -O >> $globe;
#png
gmt psconvert -A+s4c -TgG $globe;
#jpeg
#gmt psconvert -A+s4c -TjG $globe;
gpicview $finished_globe;

#gmt pssolar -I-7.93/37.079+d2016-02-04T10:01:00
#gmt pscoast -Rd -W0.1p -JQ0/14c -Ba -BWSen -Dl -A1000 -P -K > /home/pi/Desktop/solar.ps
#gmt pssolar -R -J -W1p -Tdc -O >> /home/pi/Desktop/solar.ps

#works
#gmt pssolar -R -J -Gyellow -Tc > /home/pi/Desktop/someplot.ps
#works but probably not right
#gmt pssolar -R -$proj$lat/$lon/60/6i -Gyellow -Tc > /home/pi/Desktop/someplot.ps

echo TopLeft | gmt pstext -R1/10/1/10 -JX10 -F+cTL -P > /home/pi/Desktop/text.ps


ps=../example_26.ps

# first do an overhead of the east coast from 160 km altitude point straight down
latitude=41.5
longitude=-74.0
altitude=160.0
tilt=0
azimuth=0
twist=0
Width=0.0
Height=0.0

PROJ=-JG${longitude}/${latitude}/${altitude}/${azimuth}/${tilt}/${twist}/${Width}/${Height}/4i

gmt pscoast -Rg $PROJ -X1i -B5g5/5g5 -Glightbrown -Slightblue -W0.25p -Dl -N1/1p,green -N2,0.5p -P -K \
	-Y5i > $ps
# now point from an altitude of 160 km with a specific tilt and azimuth and with a wider restricted
# view and a boresight twist of 45 degrees

tilt=55
azimuth=210
twist=45
Width=30.0
Height=30.0

PROJ=-JG${longitude}/${latitude}/${altitude}/${azimuth}/${tilt}/${twist}/${Width}/${Height}/5i

gmt pscoast -R $PROJ -B5g5/5g5 -Glightbrown -Slightblue -W0.25p -Ia/blue -Di -Na -O -X1i -Y-4i \
	-U/-1.75i/-0.75i/"Example 26 in Cookbook" >> $ps
pwd
rm -f gmt.his*
#sudo apt autoremove
