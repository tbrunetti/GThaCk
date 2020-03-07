import struct
from io import BytesIO
import os
import sys
import argparse
import logging

class GtcFunctions:

    def __init__(self, bpm, gtcDir, outDir):
        self.logger = logging.getLogger("classObject")
        self.bpm = bpm
        self.gtcDir = gtcDir
        self.outDir = outDir

        logger.debug('New object initialized')

    def manipulateUpdate(self, snpUpdateFile, overrides):
        import manipulateGTC
        
        logger = logging.getLogger('manipulateGTC')
        logger.debug('Running module: manipulateGTC')

        self.snpUpdateFile = snpUpdateFile
        self.overrides = overrides
        manipulateGTC.manipulate_gtc(bpm=self.bpm, gtcDir=self.gtcDir, outDir=self.outDir, snpsToUpdate=self.snpUpdateFile, overrides=self.overrides)

   
    def extractSampleInfo(self):
        import getSampleInfo
        
        logger = logging.getLogger('extractSampleInfo')
        logger.debug('Running module: extractSampleInfo')

    
    def getIntensities(self):
        import getIntensities

        logger = logging.getLogger('getIntensities')
        logger.debug('Running module: getIntensities')

    
    def getCallperSample(self):
        logger = logging.getLogger('getCallperSample')
        logger.debug('Running module: getCallperSample')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Functions and methods for gtc files')
    parser.add_argument('method', choices=['manipulateGTCs', 'getIntensities', 'sampleInformation'])
    parser.add_argument('--bpm', required=True, type=str, help='Full path to bead pool manifest file (.bpm); must be same one used to generate gtc')
    parser.add_argument('--gtcDir', type=str, default=os.getcwd(), help='Full path to location of directory/folder containing gtc files to process (files must end in .gtc)')
    parser.add_argument('--outDir', default=os.getcwd(), type=str,help='Full path to directory or folder to output results')
    parser.add_argument('--snpUpdates', default=None, type=str, help='Full path to file containing snps to update')
    parser.add_argument('--modDir', default=os.path.join(os.getcwd(), 'modules'), type=str, help='Full path to module files .py from github; default is current working directory with modules folder appended')
    parser.add_argument('--logName', default='gtcFuncs.log', type=str, help='Name of log file to output')
    parser.add_argument('--overrides', default=None, type=str, help='a tab-delimited text file, one snp per line, of snp name and allele change.  Ex: rs12248560.1    [T/A], will update allele rs12248560.1 to have alleles T and A instad of what is listed on the bpm')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=os.path.join(args.outDir, args.logName))
    logger = logging.getLogger('Initialization')

    sys.path.insert(1, args.modDir)

    if args.method == 'manipulateGTCs':
        logger.info('method manipulateGTCs selected \n creating new object of class GtcFunctions')
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.manipulateUpdate(args.snpUpdates, args.overrides)
    
    elif args.method == 'getIntensities':
        logger.info('method getIntensities selected \n creating new object of class GtcFunctions')
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.getIntensities()
    
    elif args.method == 'sampleInformation':
        logger.info('method sampleInformation selected \n creating new object of class GtcFunctions')
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.extractSampleInfo()
    
    else:
        logger.critical('method {} does not exist!'.format(args.method))