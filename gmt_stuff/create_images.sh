#!/usr/bin/env bash
# "peachpuff" "snow3" 

arr=("darkgreen" "mediumseagreen" "limegreen" "palegreen" "springgreen" "lawngreen" "mediumspringgreen" "forestgreen" "rosybrown" "wheat" "tan" "lightbrown" "seagreen" "seagreen4" "palegreen4" "springgreen1" "springgreen2" "springgreen3" "springgreen4" "green3" "green4" "olivedrab4" "darkolivegreen4" "khaki4" "sienna4" "wheat4" "tan4");
arr2=("midnightblue" "navy" "navyblue" "cornflowerblue" "mediumblue" "royalblue" "blue" "darkblue" "steelblue" "skyblue" "lightsteelblue" "darkturquoise" "cyan" "aquamarine" "royalblue1" "royalblue2" "royalblue3" "royalblue4" "blue1" "blue2" "blue3" "blue4" "dodgerblue4" "steelblue1" "steelblue2" "steelblue3" "skyblue1" "skyblue2" "skyblue3" "lightsteelblue1" "lightsteelblue2" "lightsteelblue3" "cadetblue1" "cadetblue2" "cyan1" "cyan2" "cyan3" "aquamarine1" "aquamarine2" "aquamarine3" "aquamarine4");

for a in "${arr[@]}"
do
    for b in "${arr2[@]}"
    do
        gmt pscoast -R-8/63/15/55 -JM6i -P -Ba -G$a -S$b > ${a}_${b}.ps;
        #sleep .00001;
        gmt psconvert -A+s4c -Tg ${a}_${b}.ps;
        rm ${a}_${b}.ps;
        echo "${a}_${b}.png is finished";        
    done
done
