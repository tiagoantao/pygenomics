# -*- coding: utf-8 -*-
'''
.. module: genomics.popgen.ne2
   :synopsis: This module provides code to work with NeEstimator2.
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>
'''

import pprint


class Record(object):
    '''Holds information from a NeEstimator2 OUTPUT file.

    @ivar freqs_used  Frequencies used as a cutoff. The list
                       might include None (no cutoff)

    @ivar  ld          List of LD data
                       Composed of a list (size = cutoffs) dictionary with
                       HMean
                       IndepComp
                       OvRSquare
                       ExpRSquareSample
                       EstNe
                       ParaNe
                       IGNORING JACKNIFE for now
    @ivar  het         List of Het data
                       Composed of a list (size = cutoffs) dictionary with
                       HMean
                       IndepAlleles
                       WeiMeanD
                       EstNeb
                       IGNORING PARAMETRIC AND JACKNIFE For now
    @ivar  coanc       List of Coanc data
                       Composed of a SINGLE dictionary with
                       HMean
                       OvF1
                       EstNeb
                       IGNORING PARAMETRIC AND JACKNIFE For now
    @ivar  temporal    List of temporal info.
                       Composed of dict with
                       sampleId1
                       sampleId2
                       generation1
                       generation2
                       results
                       results it itself another dictionary with the
                       method as key (Pollak,Nei/Tajima,Jorde/Ryman) and
                       a content of a dict per cutoff of
                           HMean
                           IndepAlleles
                           Fk
                           Fline
                           Ne

    '''

    def __init__(self):
        self.freqs_used = []
        self.ld = []
        self.het = []
        self.coanc = []
        self.temporal = []

    def __str__(self):
        myRep = ""
        pp = pprint.PrettyPrinter()
        myRep += "LD\n"
        for elem in self.ld:
            myRep += pp.pformat(elem)
            myRep += "\n"
        myRep += "HetExcess\n"
        for elem in self.het:
            myRep += pp.pformat(elem)
            myRep += "\n"
        myRep += "Coanc\n"
        for elem in self.coanc:
            myRep += pp.pformat(elem)
            myRep += "\n"
        for elem in self.temporal:
            myRep += "Samples: %d %d\n" % (elem["sampleId1"],
                                           elem["sampleId2"])
            myRep += "Generations: %d %d\n" % (elem["generation1"],
                                               elem["generation2"])
            for stat, result in elem["results"].items():
                myRep += stat
                myRep += " "
                myRep += pp.pformat(result)
                myRep += "\n"
            myRep += "\n"
        return myRep


def _getVals(guard, line, fun=float):
    """Gets a line of values from Ne2 output and converts it.

    @param guard String that splits text from values (typically =)
    @param line Line to parse
    @param fun Function to convert string, typically but int also common
    """
    vals = []
    line = line[line.find(guard) + len(guard):]
    toks = filter(lambda x: x != "", line.split(" "))
    if fun == float:
        fun = lambda x: None if x == "0+" or x == "Infinite" else float(x)
    vals = [fun(x) for x in toks]
    return vals


def _readTemp(results, f):
    method = f.readline().strip().rstrip()[1:-1]
    cutCases = []
    results[method] = cutCases
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for val in vals:
        cutCases.append({"HMean": val})
    #l = f.readline().rstrip()
    #vals = _getVals("=", l, int)
    #for i in range(len(vals)):
    #    cutCases[i]["IndepAlleles"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        cutCases[i]["Fk"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        cutCases[i]["Fline"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        cutCases[i]["Ne"] = vals[i]

    l = f.readline().rstrip()
    l = f.readline().rstrip()
    l = f.readline().rstrip()
    vals = _getVals("c", l)
    for i in range(len(vals)):
        cutCases[i]["ParaTemp"] = [vals[i]]
    l = f.readline().rstrip()  # 0.975
    vals = _getVals(" ", l)
    for i in range(len(vals)):
        cutCases[i]["ParaTemp"].append(vals[i])
    l = f.readline().rstrip()
    l = f.readline().rstrip()


def _doTemporal(rec, f):
    """Parse Temporal part."""
    f.readline()  # First empty line
    l = f.readline()  # freqs
    if len(rec.freqs_used) == 0:
        rec.freqs_used = _getVals("Used", l.rstrip())
    l = f.readline()
    while l != "":
        l = l.rstrip()
        if l.find("=======") > -1:
            l = f.readline().rstrip()
            if l.startswith("Samples"):
                tempCalc = {}
                rec.temporal.append(tempCalc)
                l = l[7:].strip()
                toks = l.split("&")
                tempCalc["sampleId1"] = int(toks[0][:toks[0].find("[")])
                tempCalc["sampleId2"] = int(toks[1][:toks[1].find("[")])
                l = f.readline().rstrip()[11:].strip()
                toks = l.split("&")
                tempCalc["generation1"] = float(toks[0].rstrip())
                tempCalc["generation2"] = float(toks[1].rstrip())
                l = f.readline()
                l = f.readline()
                # Independent alleles TBD
                tempCalc["results"] = {}
                l = f.readline()
                while l.find("-----") > -1:
                    _readTemp(tempCalc["results"], f)
                    l = f.readline()
            else:
                return
        else:
            l = f.readline()


def _doLD(rec, f):
    "Parse LD."
    myLDs = []
    l = f.readline().rstrip()
    while l.find("Harmonic") == -1:
        l = f.readline().rstrip()
    vals = _getVals("=", l)
    for val in vals:
        myLDs.append({"HMean": val})
    l = f.readline().rstrip()
    vals = _getVals("=", l, int)
    for i in range(len(vals)):
        myLDs[i]["IndepComp"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        myLDs[i]["OvRSquare"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        myLDs[i]["ExpRSquareSample"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        myLDs[i]["EstNe"] = vals[i]
    l = f.readline().rstrip()  # Empty
    l = f.readline().rstrip()  # 95% CIs for Ne^
    l = f.readline().rstrip()  # 0.025
    vals = _getVals("c", l)
    for i in range(len(vals)):
        myLDs[i]["ParaNe"] = [vals[i]]
    l = f.readline().rstrip()  # 0.975
    vals = _getVals(" ", l)
    for i in range(len(vals)):
        myLDs[i]["ParaNe"].append(vals[i])
    rec.ld.append(myLDs)


def _doExcess(rec, f):
    """Parse Heterozygosity Excess."""
    myHets = []
    l = f.readline().rstrip()
    while l.find("Harmonic") == -1:
        l = f.readline().rstrip()
    vals = _getVals("=", l)
    for val in vals:
        myHets.append({"HMean": val})
    l = f.readline().rstrip()
    vals = _getVals("=", l, int)
    for i in range(len(vals)):
        myHets[i]["IndepAlleles"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        myHets[i]["WeiMeanD"] = vals[i]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    for i in range(len(vals)):
        myHets[i]["EstNeb"] = vals[i]
    rec.het.append(myHets)


def _doCoanc(rec, f):
    """Parse coancestry."""
    myCoanc = {}
    l = f.readline().rstrip()
    while l.find("Harmonic") == -1:
        l = f.readline().rstrip()
    vals = _getVals("=", l)
    myCoanc["HMean"] = vals[0]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    myCoanc["OvF1"] = vals[0]
    l = f.readline().rstrip()
    vals = _getVals("=", l)
    myCoanc["EstNeb"] = vals[0]
    rec.coanc.append(myCoanc)


def parse(f):
    """Parses a NeEstimator2 output file.

       @param f File descriptor
    """
    rec = Record()
    l = f.readline()
    while l != "":
        if len(rec.freqs_used) == 0 and l.find("Lowest Allele") > -1:
            rec.freqs_used = _getVals("Used", l.rstrip())
        if l.find("LINKAGE DISEQUILIBRIUM METHOD") > -1:
            _doLD(rec, f)
        if l.find("HETEROZYGOTE EXCESS METHOD") > -1:
            _doExcess(rec, f)
        if l.find("MOLECULAR COANCESTRY METHOD") > -1:
            _doCoanc(rec, f)
        if l.find("TEMPORAL METHOD") > -1:
            _doTemporal(rec, f)
        l = f.readline()
    return rec
