import struct
from io import BytesIO
import os
import sys
import argparse
import pandas
#import write_gtc


class GtcFunctions:

    def __init__(self, bpm, gtcDir, outDir):
        self.bpm = bpm
        self.gtcDir = gtcDir
        self.outDir = outDir

    def manipulateUpdate(self, snpUpdateFile):
        import manipulateGTC
        print("manipulateUpdate")
        
        self.snpUpdateFile = snpUpdateFile
        manipulateGTC.manipulate_gtc(bpm=self.bpm, gtcDir=self.gtcDir, outDir=self.outDir, snpsToUpdate=self.snpUpdateFile)
        #manipulateGTC.manipulate_gtc(self)
   
    def extractSampleInfo(self):
        import getSampleInfo
        print("extractSampleInfo")
    
    def getIntensities(self):
        import getIntensities
        print("getIntensities")
    
    def getCallperSample(self):
        print("getCallperSample")



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Functions and methods for gtc files')

    parser.add_argument('method', choices=['manipulateGTCs', 'getIntensities', 'sampleInformation'])
    parser.add_argument('--gtcDir', type=str, default=os.getcwd(), help='Full path to location of directory/folder containing gtc files to process (files must end in .gtc)')
    parser.add_argument('--bpm', required=True, type=str, help='Full path to bead pool manifest file (.bpm); must be same one used to generate gtc')
    parser.add_argument('--outDir', default=os.getcwd(), type=str,help='Full path to directory or folder to output results')
    parser.add_argument('--snpUpdates', default=None, type=str, help="Full path to file containing snps to update")
    parser.add_argument('--modDir', default=os.path.join(os.getcwd(), "modules"), type=str, help="Full path to module files .py from github; default is current working directory with modules folder appended")
    args = parser.parse_args()

    sys.path.insert(1, args.modDir)

    if args.method == 'manipulateGTCs':
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.manipulateUpdate(args.snpUpdates)
    elif args.method == 'getIntensities':
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.getIntensities()
    elif args.method == 'sampleInformation':
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.extractSampleInfo()
    else:
        pass
    

    '''
    Uncomment commands below to activate
    '''

    #main(bpm=args.bpm, gtcDir=args.gtcDir, outDir=args.outDir)
    #manipulate_gtc(bpm=args.bpm, gtcDir=args.gtcDir, snpsToUpdate=args.snpUpdates, outDir=args.outDir)
    #getSampleInfo(bpm=args.bpm, gtcDir=args.gtcDir, outDir=args.outDir)
    #getControlsIntensity(gtcDir=args.gtcDir, bpm=args.bpm, outDir=args.outDir)
