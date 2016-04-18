#!/usr/bin/env python3

import math

def ifrange (start, end, steps):
    for i in range(steps):
        yield (end-start)*i/float(steps)+start
        
    yield end

class Point (object):
    def __init__ (self, posX=None, posY=None, posZ=None):
        self.posX=posX
        self.posY=posY
        self.posZ=posZ

    def __getitem__(self, key):
        if key in ['X', 'Y', 'Z']:
            return getattr(self, 'pos' + key)
        
    def __str__ (self):
        return (' '.join(a+str(self[a])
                         for a in ['X', 'Y', 'Z']
                         if self[a] is not None))

class Move (object):
    def __init__ (self, toolpath, end):
        self.end= end
        self.cmd= 'G00'

    def __str__ (self):
        return(self.cmd + ' '+ str(self.end))

class Line(Move):
    def __init__ (self, toolpath, end):
        self.end= end
        self.cmd= 'G01'

class Dive(Move):
    def __init__ (self, toolpath, depth):
        self.end= Point(posZ=depth)
        self.cmd= 'G01'

class Safe(Move):
    def __init__ (self, toolpath):
        self.end= Point(posZ=toolpath.safe)
        self.cmd='G00'

class Comment(object):
    def __init__(self, toolpath, cmt):
        self.comment= cmt

    def __str__(self):
        return ('('+self.comment+')')
        
class Tool(object):
    def __init__ (self, toolpath, diameter, number=1, spinspeed=3000):
        self.diameter= diameter
        self.toolpath= toolpath
        self.number= number
        self.spinspeed= spinspeed

        toolpath.tool= self

    def __str__(self):
        return('(Change to {}{} diameter tool)\nT{}\nM03 S{}'
               .format(self.diameter, self.toolpath.units,
                       self.number, self.spinspeed))

class Box(object):
    def __init__ (self, parpath, start, end):
        self.subpath= Path(parpath.safe, parpath.units)

        self.subpath.add(Line, Point(start.posX, start.posY))
        self.subpath.add(Line, Point(posZ=start.posZ))
        
        self.subpath.add(Line, Point(posX= end.posX))
        self.subpath.add(Line, Point(posY= end.posY))
        self.subpath.add(Line, Point(posX= start.posX))
        self.subpath.add(Line, Point(posY= start.posY))

    def __str__ (self):
        return str(self.subpath)
    
class Fill(object):
    def __init__ (self, parpath, istart, iend, rovlp=0.2):
        self.subpath= Path(parpath.safe, parpath.units)

        radius= parpath.tool.diameter/2*(1-rovlp)
        
        start=Point(istart.posX + radius,
                    istart.posY + radius)
        
        end=Point(iend.posX - radius,
                  iend.posY - radius)
        
        numlnx= math.ceil((end.posX - start.posX)/(radius*2))+1
        numlny= math.ceil((end.posY - start.posY)/(radius*2))+1
        
        lnsx= list(ifrange(start.posX, end.posX, numlnx))
        lnsy= list(ifrange(start.posY, end.posY, numlny))

        boxes= math.ceil(min(numlnx, numlny)/2.0)
        
        for i in range(boxes):
            self.subpath.add(Box,
                             Point(lnsx[i], lnsy[i], istart.posZ),
                             Point(lnsx[numlnx-i], lnsy[numlny-i], istart.posZ))

        
        if numlnx > numlny:
            self.subpath.add(Safe)
        
            self.subpath.add(Line,
                             Point(start.posX, (start.posY+end.posY)/2))
            
            self.subpath.add(Dive, istart.posZ)        
            
            self.subpath.add(Line,
                             Point(posX=end.posX))
        else:
            self.subpath.add(Safe)
        
            self.subpath.add(Line,
                             Point((start.posX+end.posX)/2, start.posY))

            self.subpath.add(Dive, istart.posZ)
            
            self.subpath.add(Line,
                             Point(posY=end.posY))
            
            
    def __str__(self):
        return str(self.subpath)
    
class Path(object):
    def __init__ (self, safe, units='mm'):
        self.units= units
        self.safe= safe

        self.tool=None

        self.path=[]

    def add (self, cmd, *args, **kwargs):
        self.path.append(cmd(self, *args, **kwargs))

    def __str__ (self):
        s= '\n'.join(map(str,self.path))

        return (s)
        
class Program(Path):
    def __init__ (self, safe, feedrate, units='mm'):
        self.units= units
        self.safe= safe

        self.tool=None

        self.path=[]

        self.path.append({'mm':'G21','in':'G20'}[units])
        self.path.append('G90')
        self.path.append('G94 F'+str(feedrate))

    def __str__ (self):
        s= '\n'.join(map(str,self.path+['M05', 'M02']))

        return (s)
            
