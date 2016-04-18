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
    pr= Program(units='mm', safe=16, feedrate=100)

    pr.add(Tool, 1.6)

    pr.add(Safe)
    pr.add(Comment, 'Start of contour')

    rd=0.8
    
    pr.add(Move, Point(-rd,-rd))
    pr.add(Dive, 0)
    
    pr.add(Line, Point(posX=10+rd))
    pr.add(Line, Point(posY=3-rd))
    pr.add(Line, Point(posX=50-rd))
    pr.add(Line, Point(posY=-rd))
    pr.add(Line, Point(posX=60+rd))
    
    pr.add(Line, Point(posY=24+rd))
    
    pr.add(Line, Point(posX=50-rd))
    pr.add(Line, Point(posY=21+rd))
    pr.add(Line, Point(posX=10+rd))
    pr.add(Line, Point(posY=24+rd))
    pr.add(Line, Point(posX=-rd))

    pr.add(Line, Point(posY=-rd))

    pr.add(Safe)
    pr.add(Move, Point(10+rd, 3-rd))
    pr.add(Dive, 0)
    pr.add(Line, Point(10, 3))

    pr.add(Safe)
    pr.add(Move, Point(10+rd, 21+rd))
    pr.add(Dive, 0)
    pr.add(Line, Point(10, 21))
    
    pr.add(Safe)
    pr.add(Move, Point(50-rd, 3-rd))
    pr.add(Dive, 0)
    pr.add(Line, Point(50, 3))

    pr.add(Safe)
    pr.add(Move, Point(50-rd, 21+rd))
    pr.add(Dive, 0)
    pr.add(Line, Point(50, 21))
    
    
    pr.add(Safe)
    pr.add(Comment, 'End of contour')

    print (pr)
    
if __name__ == '__main__':
    main()
