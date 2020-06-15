from IlluminaBeadArrayFiles import *
import logging
import os


'''
function: getIntensities(gtcDir, bpm, outDir)
description:
input:
output:
'''
def getIntensities(self):
    import extractInformation
    import pandas
    
    gtcDir = self.gtcDir
    bpm = self.bpm
    outDir = self.outDir
    fileOutName = self.fileOutName
    prefix = self.prefix

    # SOMEWHERE NEED TO CALL METHOD: extractionInformation.py
    # reading in manifest more than once carries lot of overhead
    manifest = BeadPoolManifest(bpm)


    input_gtc_list = [
        gtc for gtc in os.listdir(gtcDir) if gtc.endswith(".gtc")
    ]

    #detect which probes are available based on bpm input
    controls = manifest.control_config.decode().split('\n')
    # checks if split leaves an empty string, if yes, pop off
    if len(manifest.control_config.decode().split('\n')[-1]) == 0:
        controls.pop(len(controls)-1)

    # list of control probes in order
    tmp = [controls[i].split(":")[3].split(',', 1)[1] for i in range(0, len(controls))]
    intensity_probes = [i.replace(',', '_').replace(' ', '_') for i in tmp]

    '''
    intensities_per_sample = {}

    for gtc in input_gtc_list:
        data = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, gtc))
        try:
            assert data[101] == manifest.manifest_name
            intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())] = {}
            intensityIndex = 0
            for i in range(0, len(data[500])):
                if i%4 == 0:
                    intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())][intensity_probes[intensityIndex] + '_1X'] = data[500][i]
                    intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())][intensity_probes[intensityIndex] + '_1Y'] = data[501][i]
                    intensityIndex += 1
                else:
                    continue
        except AssertionError:
            print("Sample {}, {} does not have a matching bpm for the manifest you are supplying. Skipping sample.".format(data[10], gtc))
            sys.stdout.flush()
            continue
            

    allIntesities = pandas.DataFrame(intensities_per_sample)
    allIntensities_transpose = allIntesities.T
    if os.path.exists(outDir) == False:
        os.mkdir(outDir)
    allIntensities_transpose.to_csv(os.path.join(outDir, fileOutName), index = True, sep = '\t')

