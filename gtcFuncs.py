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
        print('Running module: manipulateGTC')

        self.snpUpdateFile = snpUpdateFile
        self.overrides = overrides
        manipulateGTC.manipulate_gtc(self)

   
    def createSampleSheet(self, sampleSheetUpdates, fileOutName, config):
        import sampleSheet

        logger = logging.getLogger('createSampleSheet')
        logger.debug('Running module: createSampleSheet')
        print('Running module: createSampleSheet')
        self.sampleSheetUpdates = sampleSheetUpdates
        self.config = config
        sampleSheet.baseData(self)
        sampleSheet.updateHeader(self)
        sampleSheet.generateSampleSheet(outDir = self.outDir, fileName = fileOutName)


    def extractSampleInfo(self):
        import getSampleInfo
        
        logger = logging.getLogger('extractSampleInfo')
        logger.debug('Running module: extractSampleInfo')
        print('Running module: extractSampleInfo')
        getSampleInfo.reportSampleInfo(self)

 
    def getIntensities(self):
        import getIntensities

        logger = logging.getLogger('getIntensities')
        logger.debug('Running module: getIntensities')
        print('Running module: getIntensities')

        getIntensities.getIntensities(self)
    
    
    def getCallperSample(self):
        logger = logging.getLogger('getCallperSample')
        logger.debug('Running module: getCallperSample')
        print('Running module: getCallperSample')



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Functions and methods for gtc files')
    parser.add_argument('method', choices=['manipulateGTCs', 'getIntensities', 'sampleInformation', 'createSampleSheet'])
    parser.add_argument('--bpm', required=True, type=str, help='Full path to bead pool manifest file (.bpm); must be same one used to generate gtc')
    parser.add_argument('--gtcDir', type=str, default=os.getcwd(), help='Full path to location of directory/folder containing gtc files to process (files must end in .gtc)')
    parser.add_argument('--outDir', default=os.getcwd(), type=str,help='Full path to directory or folder to output results.  If it path does not exist, program will attempt to create it')
    parser.add_argument('--updates', default=None, type=str, help='Full path to file containing snps and/or metadata to update')
    parser.add_argument('--sampleSheetUpdates', default=None, type=str, help='')
    parser.add_argument('--config', default=None, type=str, help='')
    parser.add_argument('--fileOutName', default='sampleSheet.csv', type=str, help='')
    parser.add_argument('--modDir', default=os.path.join(os.getcwd(), 'modules'), type=str, help='Full path to module files .py from github; default is current working directory with modules folder appended')
    parser.add_argument('--logName', default='gtcFuncs.log', type=str, help='Name of log file to output')
    parser.add_argument('--overrides', default=None, type=str, help='a tab-delimited text file, one snp per line, of snp name and allele change.  Ex: rs12248560.1    [T/A], will update allele rs12248560.1 to have alleles T and A instead of what is listed on the bpm')
    args = parser.parse_args()

    if os.path.isdir(args.outDir) == False:
        print('\nOutput directory {} does not exists'.format(args.outDir))
        
        try:
            print('Attempting to create new output directory {}'.format(args.outDir))
            os.mkdir(args.outDir)
            print('Successfully created {}'.format(args.outDir))
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=os.path.join(args.outDir, args.logName))
            logger = logging.getLogger('Initialization')

        except:
            print('\n Please check path for --outDir argument')
            raise OSError('Error, problem with path {}. Please check path exists' % args.outDir)
            
    
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=os.path.join(args.outDir, args.logName))
        logger = logging.getLogger('Initialization')
        if any(files.endswith('.gtc') for files in os.listdir(args.outDir)) and (args.method != 'createSampleSheet'):
            logger.critical('Output directory contains files with extension .gtc.  Please move these files to a new directory or create a new directory without gtc files.')
            print('\nOutput directory contains files with extension .gtc.  Please move these files to a new directory or create a new directory without gtc files.')
            sys.exit()
        logger.debug('Output directory can be used!')



    sys.path.insert(1, args.modDir)


    if args.method == 'manipulateGTCs':
        logger.info('method manipulateGTCs selected \n creating new object of class GtcFunctions')
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.manipulateUpdate(args.updates, args.overrides)
    
    elif args.method == 'createSampleSheet':
        if args.config == None:
            parser.error('method createSampleSheet requires argument --config')
        logger.info('method createSampleSheet selected \n creating new object of class GtcFunctions')
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.createSampleSheet(args.sampleSheetUpdates, args.fileOutName, args.config)


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
        print('method {} does not exist!'.format(args.method))
        sys.exit()