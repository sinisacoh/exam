#!/usr/bin/env python

import glob
import subprocess

NLINES=10

all_fn=glob.glob("../q_*v*tex")
all_fn.sort()

for fn in all_fn:
    f=open(fn,"r")
    ln=f.readlines()
    f.close()

    found=False
    for l in ln:
        if r"\input{ten_lines.tex}" in l:
            found=True

    if found == True:
        o_fn=fn.replace("../","").replace("q_","a_")

        g=open("snippet_template.tex","r")
        qq=g.read()
        g.close()

        out=qq
        
        proc = subprocess.Popen(['python',
                                 'snippets/'+fn.replace("../","").replace(".tex",".py")],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        raw_out=proc.communicate()[0].decode("ascii").split("\n")
        if raw_out[-1]=="":
            raw_out=raw_out[:-1]

        if len(raw_out)>NLINES:
            print("too many lines in the output!!")
            exit()
                    
        for j in range(NLINES):
            ca=str(j+1).zfill(2)

            if j < len(raw_out):
                to_use=str(raw_out[j])
            else:
                to_use=""
                    
            out=out.replace("SNIPPET"+ca,to_use)
            
        f=open(o_fn,"w")
        f.write(out)
        f.close()
