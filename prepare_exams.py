#!/usr/bin/env python

import sys,os
import glob
import loc
import random

TEMPLATE="template.tex"

random.seed(0)

def main():
    # create template file
    f=open(TEMPLATE,"r")
    template=f.read()
    f.close()

    # get all questions
    all_questions={}
    for fn in glob.glob("q_*_v*.tex"):
        f=open(fn,"r")
        quest=f.read()
        f.close()

        qi=fn.split("_")[1]
        qj=fn.split("_")[2].split(".")[0].replace("v","")

        if qi not in all_questions.keys():
            all_questions[qi]=[]

        all_questions[qi].append({"filename":fn,"content":quest})

    sortkeys=list(all_questions.keys())
    sortkeys.sort()

    os.system("rm "+loc.EXAM_NAME.strip()+"__version_*.pdf")

#    info = ""    
    # go over all versions of the text
    for i in range(1,loc.NUM_OF_EXAM_VERSIONS+1):
        txt=""
#        info+=str(i).strip()+":"
        # go over all questions
        for q in sortkeys:
            # pick one of the versions
            choose_version=random.randint(0,len(all_questions[q])-1)
#            info+=str(q).strip()+"_"+str(choose_version).strip()+","
            txt+="\n\n\n"
            if "QQQQQ" in all_questions[q][choose_version]["content"]:
                txt+=all_questions[q][choose_version]["content"].replace("QQQQQ",r"\textbf{Problem "+q.strip()+"}").lstrip().rstrip()
            else:
                txt+=r"\textbf{Problem "+q.strip()+r" } "
                txt+=all_questions[q][choose_version]["content"].lstrip().rstrip()
            txt+="\n"+r"\vspace{0.1cm}"+"\n\n"

            txt+=r"%PLACEHERESOLUTIONLATER++"+all_questions[q][choose_version]["filename"].strip()+"\n"
            
            txt+="\n\n\n"
            
#        info+="\n"
        
        ff=open("__tmp__"+str(i)+".tex","w")
        ff.write(template.replace("AAAAA",txt).replace("BBBBB",str(i)))
        ff.close()

#    f=open("info.txt","w")
#    f.write(info)
#    f.close()

    for i in range(1,loc.NUM_OF_EXAM_VERSIONS+1):
        os.system("pdflatex __tmp__"+str(i))
        os.system("mv __tmp__"+str(i)+".pdf "+loc.EXAM_NAME.strip()+"__version_"+str(i)+".pdf")


main()
