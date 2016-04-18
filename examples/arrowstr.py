#!/usr/bin/env python3

# Copyright Leonard Göhrs 2016.
# This documentation describes Open Hardware and is licensed under the
# CERN OHL v. 1.2.
# You may redistribute and modify this documentation under the terms of the
# CERN OHL v.1.2. (http://ohwr.org/cernohl). This documentation is distributed
# WITHOUT ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING OF
# MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A
# PARTICULAR PURPOSE. Please see the CERN OHL v.1.2 for applicable
# conditions

from pycode import *

def main():
    pr= Program(units='mm', safe=2, feedrate=150)

    pr.add(Tool, 1.6)
    
    pr.add(Safe)

    pr.add(Move, Point(0,-1))
    pr.add(Dive, 0)

    pr.add(Line, Point(posX=8))
    pr.add(Line, Point(posY=-3))
    pr.add(Line, Point(11, 0))
    pr.add(Line, Point(8, 3))
    pr.add(Line, Point(posY=1))
    pr.add(Line, Point(posX=0))
    pr.add(Line, Point(posY=-1))

    pr.add(Safe)

    print (pr)
        
if __name__ == '__main__':
    main()
