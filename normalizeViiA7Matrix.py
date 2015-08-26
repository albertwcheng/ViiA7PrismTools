#!/usr/bin/env python

from sys import *
from getopt import getopt

def printUsageAndExit(programName):
    print >> stderr,programName,"[-g GeneName,SampleName] [options]... ViiA7File"
    print >> stderr,"[Options]"
    print >> stderr,"-o SampleName,...  Only output these samples"
    print >> stderr,"-x GeneName,...  Only output these genes"
    exit(1)

if __name__=='__main__':
    programName=argv[0]
    
    geneNormalizers=dict()
    outputTheseSamplesOnly=[]
    outputTheseGenesOnly=[]
    showHeader=False
    
    try:
        opts,args=getopt(argv[1:],"g:o:x:h",[])
        filename,=args
        for o,v in opts:
            if o=='-g':
                geneName,sampleName=v.split(",")
                geneNormalizers[geneName]=sampleName
            elif o=='-o':
                outputTheseSamplesOnly.extend(v.split(","))
            elif o=='-x':
                outputTheseGenesOnly.extend(v.split(","))
            elif o=='-h':
                showHeader=True
    except:
        printUsageAndExit(programName)


    geneNormFactors=dict()

    fil=open(filename)
    for lin in fil:
        lin=lin.rstrip("\r\n")
        fields=lin.split("\t")
        if len(fields)<10:
            continue


        if fields[0]=="Well":
            try:
                sampleNameCol=fields.index("Sample Name")
            except:
                print >> stderr,"Error: Sample Name col not found on Well row. Abort"
                exit(1)

            try:
                geneNameCol=fields.index("Target Name")
            except:
                print >> stderr,"Error: Target Name col not found on Well row. Abort"
                exit(1)

            try:
                RQCol=fields.index("RQ")
            except:
                print >> stderr,"Error: RQ Col not found on Well row. Abort"
                exit(1)

            try:
                RQMinCol=fields.index("RQ Min")
            except:
                print >> stderr,"Error: RQ Min Col not found on Well row. Abort"
                exit(1)

            try:
                RQMaxCol=fields.index("RQ Max")
            except:
                print >> stderr,"Error: RQ Max Col not found on Well row. Abort"
                exit(1)
        else:
            try:
                sampleName=fields[sampleNameCol]
                geneName=fields[geneNameCol]
                if geneNormalizers[geneName]==sampleName:
                    geneNormFactors[geneName]=float(fields[RQCol])
            except:
                continue
                    
                    
        
    fil.close()

    #print >> stderr,geneNormFactors


    fil=open(filename)
    for lin in fil:
        lin=lin.rstrip("\r\n")
        fields=lin.split("\t")
        if len(fields)<10:
            continue
        if fields[0]=="Well":
            if showHeader:
                print >> stdout,"\t".join(fields)
        else:
            geneName=fields[geneNameCol]
            sampleName=fields[sampleNameCol]
            if (len(outputTheseSamplesOnly)==0 or sampleName in outputTheseSamplesOnly) and (len(outputTheseGenesOnly)==0 or geneName in outputTheseGenesOnly):
                #now we can output this row
                try:
                    RQ=float(fields[RQCol])
                    RQMin=float(fields[RQMinCol])
                    RQMax=float(fields[RQMaxCol])
                    try:
                        normF=geneNormFactors[geneName]
                        RQ/=normF
                        RQMin/=normF
                        RQMax/=normF
                    except:
                        pass

                    fields[RQCol]=str(RQ)
                    fields[RQMinCol]=str(RQMin)
                    fields[RQMaxCol]=str(RQMax)
                except:
                    pass

                print >> stdout,"\t".join(fields)



    fil.close()
