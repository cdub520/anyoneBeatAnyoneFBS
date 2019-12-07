# anyoneBeatAnyoneFBS
Using basic graph traversal you can prove definitively that anyone can beat anyone in college football.
# Basic Usage
xBeatY.py [team1] [team2] where team1 is any team in FBS with following the format of "Navy" or "Army" always uppercased first letter
# How it works
Based on a basic one way graph of all wins in FBS queried from a online API, a graph is constructed, then using a non-priority que verson of djykstras algorythm the shortest path between any two teams. Then you just follow the path a it returns the shortest path between any two teams if it exists.
# Thanks
https://gist.github.com/econchick/4666413 for the basic graph implementation and traversal
https://gist.github.com/mdsrosa/c71339cb23bc51e711d8 for the shortest path tracing function
https://api.collegefootballdata.com/api/ for the overwhelming amount of free data about college football
