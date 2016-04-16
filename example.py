#!/usr/bin/env python3

from pycode import *

def main():
    tp= Program(units='mm', safe=10, feedrate=80)

    tp.add(Tool, 1.6)
    
    tp.add(Safe)

    tp.add(Comment, 'Start Oberflaeche')
    tp.add(Fill, Point(-0.8, -0.8, 10), Point(60+0.8, 24+0.8, 10))
    tp.add(Comment, 'Ende Oberflaeche')
    
    tp.add(Comment, 'Start Rand aussen')
    tp.add(Move, Point(-0.8, -0.8))
    for depth in ifrange(10,0,10):
        tp.add(Box,
               Point(-0.8, -0.8, depth),
               Point(60+0.8, 24+0.8, depth))
    tp.add(Safe)
    tp.add(Comment, 'Ende Rand aussen')

        
    tp.add(Comment, 'Start PCB Vertiefung')
    for depth in ifrange(10, 8, 2):
        tp.add(Fill, Point( 0, 0, depth), Point(10, 24, 8)) #Links
        tp.add(Safe)
        
        tp.add(Fill, Point(50, 0, depth), Point(60, 24, 8)) #Rechts
        tp.add(Safe)
    
        tp.add(Fill, Point(10, 3, depth), Point(50, 21, 8)) #Mitte
        tp.add(Safe)
    tp.add(Comment, 'Ende PCB Vertiefung')

    tp.add(Comment, 'Start Aussparung Mitte')
    for depth in ifrange(8, 2, 6):
        tp.add(Fill, Point(10, 4, depth), Point(50, 20, depth))
        tp.add(Safe)
    tp.add(Comment, 'Ende Aussparung Mitte')


    for mh in ((5.5, 3.5), (5.5, 24-3.5), (60-5.5, 24-3.5), (60-5.5, 3.5)):
        cx,cy=mh
        
        tp.add(Comment, 'Start Magnet Loch {},{}'.format(cx,cy))
        for depth in ifrange(8, 3, 5):
            tp.add(Move, Point(cx-2.5, cy-2.5+0.8))
            tp.add(Dive, depth)
            tp.add(Line, Point(posX=cx+2.5))
            tp.add(Line, Point(posX=cx+2.5-0.8))
            tp.add(Line, Point(posY=cy+2.5-0.8))
            tp.add(Line, Point(posX=cx+2.5))
            tp.add(Line, Point(posX=cx-2.5))
            tp.add(Line, Point(posX=cx-2.5+0.8))
            tp.add(Line, Point(posY=cy))
            tp.add(Line, Point(posX=cx+2.5-0.8))
            
            tp.add(Safe)
        tp.add(Comment, 'Ende Magnet Loch {},{}'.format(cx, cy))

    tp.add(Move, Point(0,0))
        
    print (tp)
    
if __name__ == '__main__':
    main()
