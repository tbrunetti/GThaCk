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

   
    def createSampleSheet(self, sampleSheetUpdates, pseudoInstID, pseudoMrn, fileOutName, config):
        import sampleSheet

        logger = logging.getLogger('createSampleSheet')
        logger.debug('Running module: createSampleSheet')
        print('Running module: createSampleSheet')
        self.sampleSheetUpdates = sampleSheetUpdates
        self.config = config
        self.pseudoInstID = pseudoInstID
        self.pseudoMrn = pseudoMrn
        sampleSheet.baseData(self)
        sampleSheet.updateHeader(self)
        sampleSheet.generateSampleSheet(outDir = self.outDir, fileName = fileOutName)


    def extractSampleInfo(self, fileOutName, prefix, flag):
        import getSampleInfo
        
        logger = logging.getLogger('extractSampleInfo')
        logger.debug('Running module: extractSampleInfo')
        print('Running module: extractSampleInfo')
        self.fileOutName = fileOutName
        self.prefix = prefix
        if flag:
            getSampleInfo.reportSampleInfoRecursive(self)
        else:
            getSampleInfo.reportSampleInfo(self)

 
    def getIntensities(self, fileOutName, prefix, flag):
        import getIntensities

        logger = logging.getLogger('getIntensities')
        logger.debug('Running module: getIntensities')
        print('Running module: getIntensities')
        self.fileOutName = fileOutName
        self.prefix = prefix
        if flag:
            getIntensities.getIntensitiesRecursive(self)
        else:
            getIntensities.getIntensities(self)
    
    
    def getCallperSample(self):
        logger = logging.getLogger('getCallperSample')
        logger.debug('Running module: getCallperSample')
        print('Running module: getCallperSample')


    def allCombos(self, snpFile):
        import itertools
        import pandas
        '''
        snpFile='test_combos_slocob1_cyp2c19.txt'
        phenoFile='/home/brunettt/Downloads/software/github_repos/GThaCk/phenotype_cyp2c19_slco1b1.txt'
        geneName = []
        snpName = []
        allCombos = []
        with open(snpFile) as allSnps:
            for line in allSnps:
                allCombos.append(line.strip().split(':')[1:-1][0].split(','))
                snpName.append(line.strip().split(':')[0])
                geneName.append(line.strip().split(':')[-1])

        allCases = itertools.product(*allCombos)
        snps = pandas.DataFrame(list(allCases), columns=snpName)
        
        phenoTables = {}
        tmpDFsetup = []
        geneName = ''
        with open(phenoFile) as pheno:
            for line in pheno:
                if line.strip().startswith('>'):
                    if len(tmpDFsetup) != 0:
                        header = tmpDFsetup[0]
                        tmpDFsetup.pop(0)
                        phenoTables[geneName] = pandas.DataFrame(tmpDFsetup, columns=header)
                    geneName = line.strip()[1:]
                    tmpDFsetup = []
                    continue
                elif line.strip().startswith('>') == False:
                    tmpDFsetup.append(line.strip().split('\t'))
            # make sure the last table from EOF gets pushed to dataframe
            header = tmpDFsetup[0]
            tmpDFsetup.pop(0)
            phenoTables[geneName] = pandas.DataFrame(tmpDFsetup, columns=header)


        # match phenotype to combinatoric set of snps
        for idx,row in snps.iterrows():
            for key,value in phenoTables.items():
                possibleSNPs = list(phenoTables[key])[:-2] # returns a list of all rsIDs to grab for gene of interest
                genotypesGene = list(row[possibleSNPs])
                a = zip(possibleSNPs, list(row[possibleSNPs]))
                phenoTables[key].loc[possibleSNPs[]]

        '''

    def query():
        pass
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Functions and methods for gtc files')
    parser.add_argument('method', choices=['manipulateGTCs', 'getIntensities', 'sampleInformation', 'createSampleSheet', 'allCombos'])
    parser.add_argument('--bpm', required=True, type=str, help='Full path to bead pool manifest file (.bpm); must be same one used to generate gtc')
    parser.add_argument('--gtcDir', type=str, default=os.getcwd(), help='Full path to location of directory/folder containing gtc files to process (files must end in .gtc) -- will not recursively go into subdirectories')
    parser.add_argument('--outDir', default=os.getcwd(), type=str,help='Full path to directory or folder to output results.  If it path does not exist, program will attempt to create it')
    parser.add_argument('--updates', default=None, type=str, help='Full path to file containing snps and/or metadata to update')
    parser.add_argument('--overrides', default=None, type=str, help='a tab-delimited text file to temporary update the snp listed in the bpm file (not GTC!), one snp per line, of snp name and allele change.  Ex: rs12248560.1    [T/A], will update allele rs12248560.1 to have alleles T and A instead of what is listed on the bpm')
    parser.add_argument('--sampleSheetUpdates', default=None, type=str, help='Path and name of samplesheet updates.  Tab-delimited with following headers required: patientName, DOB, sex, mrn, instrumentID -- GThaCk wiki for help')
    parser.add_argument('--config', default=None, type=str, help='Path and name to configuration file -- see GThaCk wiki for help')
    parser.add_argument('--prefix', default='', type=str, help='String prefix for saving images generated by sampleInformation')
    parser.add_argument('--fileOutName', default=None, type=str, help='[default: method=createSampleSheet -> sampleSheet.csv\n method=sampleInformation -> allSampleInfo.txt\n] Name of output file to write results, will be created in directory --outDir')
    parser.add_argument('--modDir', default=os.path.join(os.getcwd(), 'modules'), type=str, help='Full path to module files .py from github; default is current working directory with modules folder appended')
    parser.add_argument('--logName', default='gtcFuncs.log', type=str, help='Name of log file to output, will be created in directory --outDir')
    parser.add_argument('--pseudoInstID', default='7000000000,9999999999', type=str, help='A comma-separated pair of 2 integers with the minimum and maximum range to select instrument ID.  Both integers must be 10 digits.')
    parser.add_argument('--pseudoMrn', default='2000000,7999999', type=str, help='A comma-separated pair of 2 integers with the minimum and maximum range to select MRN.  Both integers must be 7 digits.')
    parser.add_argument('--recursive', action='store_true', help="if flag is set, gtc files will be found recursively from base --gtcDir; only valid for methods: getIntensities and sampleInformation")
   
    # ONLY FOR allCombos if implemented
    parser.add_argument('--snpFile', default=None, type=str, help='A file with snpID followed by possible combinations and gene association')
 

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
        if str(args.pseudoInstID.split(',')[0])[0] == '0' or str(args.pseudoInstID.split(',')[1])[0] == '0' or len(str(args.pseudoInstID.split(',')[0])) != 10 or len(str(args.pseudoInstID.split(',')[1])) != 10:
            parser.error('Please make sure pseudoInstID does not have ints beginning with 0 or are not integers of length 10')
        if str(args.pseudoMrn.split(',')[0])[0] == '0' or str(args.pseudoMrn.split(',')[1])[0] == '0' or len(str(args.pseudoMrn.split(',')[0])) != 7 or len(str(args.pseudoMrn.split(',')[1])) != 7:
            parser.error('Please make sure pseudoMrn does not have ints beginning with 0 or are not integers of length 7')
        if args.fileOutName == None:
            args.fileOutName = 'sampleSheet.csv'

        logger.info('method createSampleSheet selected \n creating new object of class GtcFunctions')
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.createSampleSheet(args.sampleSheetUpdates, args.pseudoInstID, args.pseudoMrn, args.fileOutName, args.config)


    elif args.method == 'getIntensities':
        logger.info('method getIntensities selected \n creating new object of class GtcFunctions')
        if args.fileOutName == None:
            args.fileOutName = 'controlProbeIntensityValues.txt'
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.getIntensities(args.fileOutName, args.prefix, args.recursive)
    
    elif args.method == 'sampleInformation':
        logger.info('method sampleInformation selected \n creating new object of class GtcFunctions')
        if args.fileOutName == None:
            args.fileOutName = 'allSampleInfo.txt'
        analysisObj = GtcFunctions(args.bpm, args.gtcDir, args.outDir)
        analysisObj.extractSampleInfo(args.fileOutName, args.prefix, args.recursive)
    
    else:
        logger.critical('method {} does not exist!'.format(args.method))
        print('method {} does not exist!'.format(args.method))
        sys.exit()
