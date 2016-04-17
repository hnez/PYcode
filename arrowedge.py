#!/usr/bin/env python3

from pycode import *

def main():
    pr= Program(units='mm', safe=2, feedrate=150)

    pr.add(Tool, 1.6)
    
    pr.add(Safe)

    pr.add(Move, Point(0,-1))
    pr.add(Dive, 0)

    pr.add(Line, Point(posX=8))
    pr.add(Line, Point(posY=-3))
    pr.add(Line, Point(posX=6))
    pr.add(Line, Point(9, -6))
    pr.add(Line, Point(12, -3))
    pr.add(Line, Point(posX=10))
    pr.add(Line, Point(posY=1))
    pr.add(Line, Point(posX=0))
    pr.add(Line, Point(posY=-1))
    

    
    pr.add(Safe)

    print (pr)
        
if __name__ == '__main__':
    main()
