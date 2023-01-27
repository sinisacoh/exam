#!/usr/bin/env python

import glob
import os

def main():

    os.system("rm -rf fig ; mkdir fig ; cp -rf ../fig/* fig/")

    # read in all solutions
    all_solut={}
    allf=glob.glob("a_*_v*.tex")
    allf.sort()    
    for fn in allf:
        f=open(fn,"r")
        ln=f.read()
        f.close()
        all_solut[fn]=ln

    # read in all grading schemes
    all_grad={}
    allf=glob.glob("g_*.tex")
    allf.sort()    
    for fn in allf:
        f=open(fn,"r")
        ln=f.read()
        f.close()
        all_grad[fn]=ln

    # place in solutions to the tex file
    allf=glob.glob("../__tmp__*.tex")
    allf.sort()    
    for fn in allf:
        f=open(fn,"r")
        ln=f.readlines()
        f.close()

        out=""
        for l in ln:
            if "%PLACEHERESOLUTIONLATER++" in l:
                aan=l.split("++")[-1].strip().replace("q_","a_")
                out+=r"{\color{red}  {\bf Solution to the problem:} "+"\n\n"
                if aan in all_solut.keys():
                    out+=all_solut[aan]
                else:
                    out+=r"{\it SOLUTION WILL BE ADDED LATER.}"
                aangra=l.split("++")[-1].strip().replace("q_","g_").split("_v")[0]+".tex"
                if aangra in all_grad.keys():
                    out+="\n\n"+r"{\bf Grading scheme:}"+"\n\n"
                    out+=all_grad[aangra]
                out+=r"}"+"\n"
                out+="\n"
            else:
                out+=l


        sol_fn_basis=fn.replace("../","").replace("__tmp__","__tmp_solution__").replace(".tex","")
                
        ff=open(sol_fn_basis+".tex","w")
        ff.write(out)
        ff.close()

        os.system("pdflatex "+sol_fn_basis)
        os.system("mv "+sol_fn_basis+".pdf "+sol_fn_basis.replace("__tmp_solution__","solution_")+".pdf")

                
main()
