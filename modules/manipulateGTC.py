from IlluminaBeadArrayFiles import *
import struct
from io import BytesIO
import os
import sys

'''
function: manipulate_gtc(bpm, gtcDir, snpsToUpdate, outDir)
description:
input:
output:
'''
def manipulate_gtc(bpm, gtcDir, outDir, snpsToUpdate):
    import extractInformation
    import write_gtc
    '''
    function: updateMetaData(data, metaData)
    description:
    input:
    output:
    '''
    def updateMetaData(data, metaData):
        import itertools
        # SOMEWHERE NEED TO CALL METHOD: extractionInformation.py

        dataDict = {}
        metaDataUpdates = metaData.rstrip().split(',')
        for update in metaDataUpdates:
            if update.rstrip().split('=')[0] == 'sampleName':
                dataDict[10] = update.rstrip().split('=')[1]
            elif update.rstrip().split('=')[0] == 'sentrixBarcode':
                dataDict[1016] = update.rstrip().split('=')[1]
            elif update.rstrip().split('=')[0] == 'plateName':
                dataDict[11] = update.rstrip().split('=')[1]
            elif update.rstrip().split('=')[0] == 'well':
                dataDict[12] = update.rstrip().split('=')[1]
            else:
                print(
                    'MetaData {} does not exist; please make sure spelling is correct and case sensitive!  Ignoring...'
                    .format(update.rstrip().split('=')[0]))
                sys.stdout.flush()

        for key, value in dataDict.items():
            data[key] = value

        return data

    
    '''
    function: snpUpdate(data, line)
    description:
    input:
    output:
    '''
    def snpUpdate(data, line):
        loc = manifest.names.index(line.rstrip().split()[0])
        print(loc)
        print(len(data[1003]))
        originalSnp = data[1003][loc]
        data[1003][loc] = str(line.rstrip().split()[1])
        if ((str(line.rstrip().split()[1])[0] != str(
                line.rstrip().split()[1])[1])
                and (str(line.rstrip().split()[1])[0] != '-')):
            data[1002][loc] = 2
        elif (str(line.rstrip().split()[1])[0] == '-') and (str(
                line.rstrip().split()[1])[1] == '-'):
            data[1002][loc] = 0
        elif (str(line.rstrip().split()[1])[0] == str(
                line.rstrip().split()[1])[1]) and (str(
                    line.rstrip().split()[1])[0] in [
                        'A', 'T', 'G', 'C'
                    ]) and (str(
                        line.rstrip().split()[1])[1] in ['A', 'T', 'G', 'C']):
            if manifest.snps[loc].find(str(line.rstrip().split()[1])[0]) != -1:
                data[1002][loc] = manifest.snps[loc].find(
                    str(line.rstrip().split()[1])[0])
            else:
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
    description:
    input:
    output:
    '''

    def validateUpdate(originalGTC, outputName, outDir):
        import extractInformation
        import write_gtc

        original_genotype = GenotypeCalls(originalGTC)
        gtc_copy = GenotypeCalls(os.path.join(outDir,
                                              '{}.gtc'.format(outputName)),
                                 check_write_complete=False)
        try:
            assert gtc_copy.get_autocall_date(
            ) == original_genotype.get_autocall_date()
            assert gtc_copy.get_autocall_version(
            ) == original_genotype.get_autocall_version()
            #assert gtc_copy.get_base_calls() == genotype_calls.get_base_calls()
            assert gtc_copy.get_call_rate() == original_genotype.get_call_rate(
            )
            assert gtc_copy.get_cluster_file(
            ) == original_genotype.get_cluster_file()
            assert (gtc_copy.get_control_x_intensities() ==
                    original_genotype.get_control_x_intensities()).all()
            assert (gtc_copy.get_control_y_intensities() ==
                    original_genotype.get_control_y_intensities()).all()
            assert gtc_copy.get_num_no_calls(
            ) == original_genotype.get_num_no_calls()
            assert gtc_copy.get_gender() == original_genotype.get_gender()
            assert (gtc_copy.get_genotype_scores() ==
                    original_genotype.get_genotype_scores()).all()
            #assert gtc_copy.get_genotypes() == genotype_calls.get_genotypes()
            assert gtc_copy.get_percentiles_x(
            ) == original_genotype.get_percentiles_x()
            assert (gtc_copy.get_raw_x_intensities() ==
                    original_genotype.get_raw_x_intensities()).all()

            all_genotypes = gtc_copy.get_genotypes()

            assert len(manifest.names) == len(all_genotypes)
            assert len(manifest.names) == len(gtc_copy.get_logr_ratios())
            assert len(manifest.names) == len(gtc_copy.get_ballele_freqs())
            print(
                os.path.join(outDir, '{}.gtc'.format(outputName)) +
                ' passed validation!')
            sys.stdout.flush()

        except AssertionError:
            print(
                os.path.join(outDir, '{}.gtc'.format(outputName)) +
                ' failed validation -- please re-run this gtc')
            sys.stdout.flush()

    manifest = BeadPoolManifest(bpm)
    manifest.snps[manifest.names.index(
        'rs12248560.1')] = '[T/C]'  # known mistake in bpm
    manifest.snps[manifest.names.index('newrs4986893')] = '[A/G]' # bpm strand flipping issue
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
                    if len(line.rstrip().split()
                           ) == 3:  # means there is metadata to update
                        print("Metadata found. Updating metadata...")
                        sys.stdout.flush()
                        data = updateMetaData(
                            data=data, metaData=line.rstrip().split()[2])
                else:
                    print('Writing updated GTC to new GTC file...')
                    sys.stdout.flush()
                    with open(
                            os.path.join(outDir, '{}.gtc'.format(outputName)),
                            "wb") as output_handle:
                        write_gtc.write_gtc(data, output_handle)

                    validateUpdate(originalGTC=os.path.join(gtcDir, gtc),
                                   outDir=outDir,
                                   outputName=outputName)

                    gtc = line.rstrip().split()[0][1:]
                    outputName = line.rstrip().split()[1]
                    data = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, gtc))
                    if len(line.rstrip().split()
                           ) == 3:  # means there is metadata to update
                        print("Metadata found. Updating metadata...")
                        sys.stdout.flush()
                        data = updateMetaData(
                            data=data, metaData=line.rstrip().split()[2])

            else:
                data = snpUpdate(data=data, line=line)

    # always the last gtc because out of lines in file at this point
    print('Writing final updated GTC to new GTC file...')
    sys.stdout.flush()
    with open(os.path.join(outDir, '{}.gtc'.format(outputName)),
              "wb") as output_handle:
        write_gtc.write_gtc(data, output_handle)

    validateUpdate(originalGTC=os.path.join(gtcDir, gtc),
                   outDir=outDir,
                   outputName=outputName)

    print("All processing is finished!")
    sys.exit()