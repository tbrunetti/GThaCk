from IlluminaBeadArrayFiles import *
import struct
from io import BytesIO
import os
import sys
import logging

'''
function: manipulate_gtc(self)
description: wrapper method to update metadata, snps, validate them and convert to bytes for writing
input: gtcFunction object
output: writes updated gtcs to output directory specified at runtime
'''
def manipulate_gtc(self):
    import extractInformation
    import write_gtc
    logger = logging.getLogger('manipulate_gtc')
    logger.debug('In method manipulate_gtc()')
    
    bpm=self.bpm
    gtcDir=self.gtcDir
    outDir=self.outDir
    snpsToUpdate=self.snpUpdateFile
    overrides=self.overrides


    '''
    function: updateMetaData(data, metaData)
    description: update sample metadata (not snps) pertaining to sampleName, sentrixBarcode, plateName, well
    input: data dictionary of a sample gtc and the metadata line pertaining to that sample
    output: data dictionary with update information listed in meta data lines
    '''
    def updateMetaData(data, metaData):
        import itertools

        logger = logging.getLogger('updateMetaData')
        logger.debug("In sub-method of manipulate_gtc() -- updateMetaData()")
        dataDict = {}

        metaDataUpdates = metaData.rstrip().split(',')
        for update in metaDataUpdates:
            if update.rstrip().split('=')[0] == 'sampleName':
                dataDict[10] = update.rstrip().split('=')[1].encode()
            elif update.rstrip().split('=')[0] == 'sentrixBarcode':
                dataDict[1016] = update.rstrip().split('=')[1].encode()
            elif update.rstrip().split('=')[0] == 'plateName':
                dataDict[11] = update.rstrip().split('=')[1].encode()
            elif update.rstrip().split('=')[0] == 'well':
                dataDict[12] = update.rstrip().split('=')[1].encode()
            else:
                logger.warning(
                    'MetaData {} does not exist; please make sure spelling is correct and case sensitive!  Ignoring...'
                    .format(update.rstrip().split('=')[0]))
                print('MetaData {} does not exist; please make sure spelling is correct and case sensitive!  Ignoring...'
                    .format(update.rstrip().split('=')[0]))
                sys.stdout.flush()

        for key, value in dataDict.items():
            data[key] = value

        return data

    
    '''
    function: snpUpdate(data, line)
    description: updates the snps in a gtc if the input text-file indicates a snp needs to be updated
    input: data dictionary and a snp line in the text-file for the gtc sample
    output: returns data dictionary for that sample with updated snp (update both base call in bytes and genotype)
    '''
    def snpUpdate(data, line):
        logger = logging.getLogger('snpUpdate')
        logger.debug("In sub-method of manipulate_gtc() -- snpUpdate()")
        
        loc = manifest.names.index(line.rstrip().split()[0])
        originalSnp = data[1003][loc]
        data[1003][loc] = str(line.rstrip().split()[1]).encode()
        if ((str(line.rstrip().split()[1])[0] != str(line.rstrip().split()[1])[1]) and (str(line.rstrip().split()[1])[0] != '-')):
            data[1002][loc] = 2
        elif (str(line.rstrip().split()[1])[0] == '-') and (str(line.rstrip().split()[1])[1] == '-'):
            data[1002][loc] = 0
        elif (str(line.rstrip().split()[1])[0] == str(line.rstrip().split()[1])[1]) and (str(line.rstrip().split()[1])[0] in ['A', 'T', 'G', 'C']) and (str(line.rstrip().split()[1])[1] in ['A', 'T', 'G', 'C']):
            if manifest.snps[loc].decode().find(str(line.rstrip().split()[1])[0]) != -1:
                data[1002][loc] = manifest.snps[loc].decode().find(str(line.rstrip().split()[1])[0])
            else:
                logger.warning('WARNING! {} allele possibilities do not match manifest.  {}={} and manifest={}. This snp will not be updated.'
                    .format(line.rstrip().split()[0],
                            line.rstrip().split()[0], originalSnp,
                            manifest.snps[loc]))
                print(
                    'WARNING! {} allele possibilities do not match manifest.  {}={} and manifest={}. This snp will not be updated.'
                    .format(line.rstrip().split()[0],
                            line.rstrip().split()[0], originalSnp,
                            manifest.snps[loc]))
                sys.stdout.flush()
                data[1003][loc] = originalSnp
        else:
            pass

        return data

    
    '''
    function: validateUpdate(originalGTC, outputName, outDir)
    description: a function to validate the manipulated gtc against the original gtc it is based off
    input: requires the orginal gtc, the name of the new gtc, and the output directory
    output: None - Raises an AssertionError if a gtc fail validation and records in the log file and standard out
    '''
    @staticmethod
    def validateUpdate(originalGTC, outputName, outDir):
        import extractInformation
        import write_gtc


        logger = logging.getLogger('validateUpdate')
        logger.debug("In sub-method of manipulate_gtc() -- validateUpdate()")

        original_genotype = GenotypeCalls(originalGTC)
        gtc_copy = GenotypeCalls(os.path.join(outDir,'{}.gtc'.format(outputName)),check_write_complete=False)
        
        try:
            assert gtc_copy.get_autocall_date() == original_genotype.get_autocall_date()
            assert gtc_copy.get_autocall_version() == original_genotype.get_autocall_version()
            #assert gtc_copy.get_base_calls() == genotype_calls.get_base_calls() -- do not activate, will def fail if snps are changed
            assert gtc_copy.get_cluster_file() == original_genotype.get_cluster_file()
            assert (gtc_copy.get_control_x_intensities() ==original_genotype.get_control_x_intensities()).all()
            assert (gtc_copy.get_control_y_intensities() ==original_genotype.get_control_y_intensities()).all()
            assert gtc_copy.get_num_no_calls() == original_genotype.get_num_no_calls()
            assert gtc_copy.get_gender() == original_genotype.get_gender()
            assert (gtc_copy.get_genotype_scores() ==original_genotype.get_genotype_scores()).all()
            #assert gtc_copy.get_genotypes() == genotype_calls.get_genotypes()  -- do not activate, will def fail if snps are changed
            assert gtc_copy.get_percentiles_x() == original_genotype.get_percentiles_x()
            assert (gtc_copy.get_raw_x_intensities() == original_genotype.get_raw_x_intensities()).all()

            all_genotypes = gtc_copy.get_genotypes()
            assert len(manifest.names) == len(all_genotypes)
            assert len(manifest.names) == len(gtc_copy.get_logr_ratios())
            assert len(manifest.names) == len(gtc_copy.get_ballele_freqs())

            logger.info(os.path.join(outDir, '{}.gtc'.format(outputName)) +' passed validation!')
            print(os.path.join(outDir, '{}.gtc'.format(outputName)) +' passed validation!')
            sys.stdout.flush()

        except AssertionError:
            logger.warning(os.path.join(outDir, '{}.gtc'.format(outputName)) +' failed validation -- please re-run this gtc')
            print(os.path.join(outDir, '{}.gtc'.format(outputName)) +' failed validation -- please re-run this gtc')
            sys.stdout.flush()
    
    '''
    function: snpOverride()
    description: will temporarily overwrite the original call in the bpm
    input: bpm manifest and a text-file gathered at run time containing snps name and override value
    output: returns an ephemeral bpm manifest used during the duration of the run only
    '''
    @staticmethod
    def snpOverride(manifest, overrides):
        logger = logging.getLogger('snpOverride')
        logger.debug('Opening snp override file...')
        
        with open(overrides, 'r') as snpsOverrides:
            for snp in snpsOverrides:
                snp = snp.split('\t')
                try:
                    logger.info('snp {} is being changed from {} to {}'.format(snp[0], manifest.snps[manifest.names.index(snp[0])].decode(), snp[1]))
                    manifest.snps[manifest.names.index(snp[0])] = snp[1].strip().encode()
                    logger.info('Success! Alleles of snp {} has been updated!'.format(snp[0]))
                except ValueError:
                    logger.error('Error! snp {} cannot be updated! Please check your input override file format.'.format(snp[0]))

        return manifest
    

###################################################################################################################
############### First analytic lines processed in manipulate_gtc(bpm, gtcDir, outDir, snpsToUpdate) ###############
###################################################################################################################
    logger.debug('Preparing to read in bpm file...')
    manifest = BeadPoolManifest(bpm)
    logger.debug('Successfully loaded BPM file')

    #######################
    # manifest overrides! #
    #######################
    if overrides == None:
        logger.debug('No overrides present')
    else:
        logger.debug('Override file present')
        manifest = snpOverride(manifest=manifest, overrides=overrides)
    
    gtc = ''
    total_gtcs = 0
    data = {}

    with open(snpsToUpdate) as updates:
        for line in updates:
            if line[0] == ">":
                total_gtcs += 1
                if total_gtcs == 1:
                    gtc = line.rstrip().split()[0][1:]
                    outputName = line.rstrip().split()[1]
                    data = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, gtc))
                    if len(line.rstrip().split()) == 3:  # means there is metadata to update
                        logger.info('Writing updated GTC to new GTC file...')
                        data = updateMetaData(data=data, metaData=line.rstrip().split()[2])
                else:
                    logger.info('Writing updated GTC to new GTC file...')
                    with open(os.path.join(outDir, '{}.gtc'.format(outputName)),"wb") as output_handle:
                        write_gtc.write_gtc(data, output_handle)

                    validateUpdate(originalGTC=os.path.join(gtcDir, gtc),
                                   outDir=outDir,
                                   outputName=outputName)

                    gtc = line.rstrip().split()[0][1:]
                    outputName = line.rstrip().split()[1]
                    data = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, gtc))
                    if len(line.rstrip().split()) == 3:  # means there is metadata to update
                        logger.info('Metadata found.  Updating metadata...')
                        data = updateMetaData(data=data, metaData=line.rstrip().split()[2])

            else:
                data = snpUpdate(data=data, line=line)

    # always the last gtc because out of lines in file at this point
    logger.info('Writing final updated GTC to new GTC file...')
    print('Writing final updated GTC to new GTC file...')
    sys.stdout.flush()
   
    with open(os.path.join(outDir, '{}.gtc'.format(outputName)),"wb") as output_handle:
        write_gtc.write_gtc(data, output_handle)

    validateUpdate(originalGTC=os.path.join(gtcDir, gtc),
                   outDir=outDir,
                   outputName=outputName)

    logger.info("All processing is finished!")
    print("All processing is finished!")
    sys.exit()