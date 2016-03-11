#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import system
import re

template = ''' $CONTRL RUNTYP=ENERGY DFTTYP=B3LYP MAXIT=200 MULT=1 COORD=ZMT $END 
 $BASIS GBASIS=N31 NGAUSS=6 NDFUNC=1 NPFUNC=1 $END
 $DATA
H2O2
C1
O
O 1 1.456229
H 1 0.970903 2 99.79
H 2 0.970903 1 99.79 3 {}
 $END'''

iname = '2.4-{}.inp'
oname = '2.4-{}.out'
origin = 118.16
step = 10

#for ang in range(0,360,step):
    #with open(iname.format(ang), 'w') as f:
        #f.write(template.format(origin+ang))
    #system('rm *dat; ./rungms {} |tee {}'.format(iname.format(ang),oname.format(ang)))

print('-----')
for ang in range(0,360,step):
    with open(oname.format(ang)) as f:
        for i in f:
            if re.search('TOTAL ENERGY =', i):
                print(ang,i[40:-1])
