#!/usr/bin/env python

import glob
import os

all_fn=glob.glob("q_*_master.tex")
all_fn.sort()

for fn in all_fn:
    f=open(fn,"r")
    ln=f.readlines()
    f.close()

    os.system("rm "+fn.strip().replace("_master.tex","_v*.tex"))

    count=0
    for l in ln:
        if "***VERSION***" in l:
            count+=1
            start,end=list(map(int,l.split("***")[2].split(",")))
    if count>1:
        print("So far supports only one!")
        exit()

    for i in range(start, end+1):
        version=str(i).zfill(2)
        out=""
        for l in ln:
            if "***VERSION***" in l:
                sp=l.replace("***VERSION",version).split("***")
                out+=sp[0]+sp[-1]
            else:
                out+=l
        f=open(fn.strip().replace("_master.tex","_v"+version+".tex"),"w")
        f.write(out)
        f.close()
        
