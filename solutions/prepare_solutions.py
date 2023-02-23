#!/usr/bin/env python

import glob
import os

def do_all(include_grading_scheme):
    
    if include_grading_scheme is True:
        suffix="_scheme"
    else:
        suffix=""
        
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
    if include_grading_scheme is True:
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

        is_snippet=False
        is_blank_box=False

        out=""
        for il,l in enumerate(ln):

            if r"\input{ten_lines.tex}" in l:
                is_snippet=True

            if r"\input{blank_box.tex}" in l:
                is_blank_box=True

            if (is_snippet == False and is_blank_box == False) and "%PLACEHERESOLUTIONLATER++" in l:
                aan=l.split("++")[-1].strip().replace("q_","a_")
                out+=r"{\color{red}  {\bf Solution to the problem:} "+"\n\n"
                if aan in all_solut.keys():
                    out+=all_solut[aan]
                else:
                    out+=r"{\it SOLUTION WILL BE ADDED LATER.}"
                aangra=l.split("++")[-1].strip().replace("q_","g_").split("_v")[0]+".tex"
                out+=r"\vspace{1cm}"+"\n"
                if include_grading_scheme is True:
                    if aangra in all_grad.keys():
                        out+="\n\n"+r"{\bf Grading scheme:}"+"\n\n"
                        out+=all_grad[aangra]
                out+=r"}"+"\n"
                out+="\n"
            elif is_snippet==True and r"\input{ten_lines.tex}" in l:
                aan=None
                for j in range(il,len(ln)):
                    if "%PLACEHERESOLUTIONLATER++" in ln[j]:
                        aan=ln[j].split("++")[-1].strip().replace("q_","a_")
                        break
                if aan == None:
                    print("NOT FOUND!")
                    exit()
                out+=l.replace(r"\input{ten_lines.tex}",r"\input{"+aan+r"}")
            elif is_blank_box==True and r"\input{blank_box.tex}" in l:
                aan=None
                for j in range(il,len(ln)):
                    if "%PLACEHERESOLUTIONLATER++" in ln[j]:
                        aan=ln[j].split("++")[-1].strip().replace("q_","a_")
                        break
                if aan == None:
                    print("NOT FOUND!")
                    exit()
                f = open(aan.replace(".tex",".py"),"r")
                new_text = f.read()
                f.close()
                new_text = r"\begin{minted}{python}" + "\n" + new_text + r"\end{minted}" + "\n"
                out+=l.replace(r"\input{blank_box.tex}",new_text)
            else:
                out+=l

            if "%PLACEHERESOLUTIONLATER++" in l:
                is_snippet=False
                is_blank_box=False

                
        sol_fn_basis=fn.replace("../","").replace("__tmp__","__tmp_solution__").replace(".tex","")+suffix
                
        ff=open(sol_fn_basis+".tex","w")
        ff.write(out)
        ff.close()

        os.system("pdflatex -shell-escape "+sol_fn_basis)
        os.system("mv "+sol_fn_basis+".pdf "+sol_fn_basis.replace("__tmp_solution__","solution_")+".pdf")


def main():
    do_all(True)
    do_all(False)
        
main()
