from freeGPT import AsyncClient
from asyncio import run
import os
import time
import random

async def main():
    dont_exit = True

    sourcefolder = input("file folder: ")
    sourcefile = input("textfile: ")
    outputsuffix = input("result suf: ") or "simp"
    aimodel = input("use gpt 4? ") or "gpt3"

    if aimodel != "gpt3":
        aimodel = "gpt4"
        print("Using GPT4...")
    else:
        print("Using GPT3...")

    cwd = os.getcwd()
    folderpath = '%s/%s' % (cwd, sourcefolder)
    sourcefilepath = "%s/%s" % (folderpath,sourcefile)
    filename = sourcefile.split(".txt")[0]


    sourcefile = open(sourcefilepath, "r").read()
    fulltext = str(sourcefile).strip('\\n')
    fulltext = fulltext.split("##")
    simplifiedtext = []

    donefolder = "%s/done" % cwd
    donefilename = "%s_%s.txt" % (filename,outputsuffix)
    transcribedlines = []    
    transcribedfilepath = "%s/%s" % (donefolder,donefilename)
    if donefilename in os.listdir(donefolder):
        transcribedfile = open(transcribedfilepath, "r").read()
        transcribedlines = transcribedfile.split("\n")

    ts = time.time()
    textfilepath = "%s/part/%s_%s_part.txt" % (cwd, filename,outputsuffix)
    completedfilepath = "%s/output/%s-%s-%s.txt" % (cwd,filename,outputsuffix,ts) 

    with open(textfilepath, "a+") as fh:
        fh.write("Transcript for %s: \n" % filename) 

    print("partial text: %s" % textfilepath)
    print("progress text: %s" % transcribedfilepath)
    print("completed text: %s" % completedfilepath)

    for text in fulltext:
        textlines = text.split('\n')
        for textline in textlines:
            if textline in transcribedlines:
                print(">> DONE: %s... SKIPPING." % textline[0:48])
                time.sleep(0.1)
                continue
            partialtext = ""
            if textline=="##":
                simplifiedtext.append("##")
                exit()
            elif len(textline)>0:
                prompt = 'Break down each sentence and simplify it into several concise sentences, but make it clearer and coherent by using common words to form an engaging paragraph. do not make a list. here is the text: "%s"' % textline
                print(f"??: {textline}")

                try:
                    promptresult = await AsyncClient.create_completion(aimodel, prompt)
                    print(f">>: {promptresult} \n")
                    partialtext = f"{promptresult}"
                    simplifiedtext.append(partialtext)
                    with open(transcribedfilepath, "a+") as fh:
                        fh.write("%s\n" % textline)
                    with open(textfilepath, "a+") as fh:
                        fh.write("%s\n" % partialtext)
                except Exception as e:
                    print(e)
                    print(f"🤖: {e}")
                    exit()

                naptime = random.randint(4, 9)
                print("wait %ds." % naptime)
                time.sleep(naptime) 
            elif len(textline)==0:
                print("skipping empty line...")
            else:
                print("wait 3s.")
                time.sleep(3)

        allsimplifiedtext = "\n".join(simplifiedtext)
        with open(completedfilepath, "a+") as fh:
            fh.write(allsimplifiedtext) 
               
run(main())