#!/usr/bin/env python3

# Copyright (c) 2016 Leonard Göhrs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

    def new_relative (self, r=None, angle=None, dx=None, dy=None, dz=None):
        newX= self.posX
        newY= self.posY
        newZ= self.posZ

        if r is not None and angle is not None:
            arad= math.radians(angle)

            newX+=r*math.cos(arad)
            newY+=r*math.sin(arad)

        if dx is not None:
            newX+=dx

        if dy is not None:
            newY+=dy

        if dz is not None:
            newZ+=dz

        return Point(newX, newY, newZ)

    def __add__(self, other):
        kwargs=[('pos'+a, self[a] + other[a])
                for a in ['X', 'Y', 'Z']
                if self[a] is not None]

        return (Point(**dict(kwargs)))

    def __neg__(self):
        kwargs=[('pos'+a, -self[a])
                for a in ['X', 'Y', 'Z']
                if self[a] is not None]

        return (Point(**dict(kwargs)))

    def __sub__(self, other):
        return (self + -other)
    
    def __getitem__(self, key):
        if key in ['X', 'Y', 'Z']:
            return getattr(self, 'pos' + key)

    def __str__ (self):
        return (' '.join(a+'{0:.4f}'.format(self[a])
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

class Arc(object):
    def __init__(self, toolpath, start, center, end, direction='CW'):
        self.cmd= {'CW': 'G02', 'CCW' : 'G03'}[direction]
        self.end= end
        self.relcenter= center - start

    def __str__(self):
        rcs= str(self.relcenter)

        for r in [('X', 'I'), ('Y', 'J'), ('Z', 'K')]:
            rcs=rcs.replace(r[0], r[1])
        
        return('{} {} {}'.format(self.cmd, str(self.end),rcs))

class Circle(Arc):
    def __init__(self, toolpath, start, center, direction='CW'):
        super().__init__(toolpath, start, center, start, direction)
    
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
