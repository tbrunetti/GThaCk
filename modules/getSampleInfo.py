import os
from IlluminaBeadArrayFiles import *

'''
function: getSampleInfo(bpm, gtcDir, outDir)
description: gets sample level information for all gtcs in a directory
input:
output:
'''
def reportSampleInfo(self):
    import extractInformation

    bpm = self.bpm
    gtcDir = self.gtcDir
    outDir = self.outDir

    nameMatch = open(os.path.join(outDir, 'sentrixMap.txt'), 'w')
    manifest = BeadPoolManifest(bpm)
    input_gtc_list = [gtc for gtc in os.listdir(gtcDir) if gtc.endswith(".gtc")]

    header = ['BTID', 'plate', 'well', 'gtcName', 'sampleID', 'callRate', 'gc10', 'sex', 'logrDev']
    nameMatch.write('\t'.join(header) + '\n')
    
    for sampleGtc in input_gtc_list:
        try:
            names = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, sampleGtc))
            assert manifest.manifest_name == names[101]
            nameMatch.write(names[10].decode() + '\t' + 
                names[11].decode() + '\t' + names[12].decode() + '\t' + 
                sampleGtc + '\t' +
                '{}-{}-{}'.format(names[11].decode(), names[12].decode(), names[10].decode()) + 
                '\t' + str(names[1006]) + '\t' + str(names[1009]) + '\t' +
                str(names[1007].decode()) + '\t' + str(names[1008]) + '\n')

        except AssertionError:
            print("Error, sample {} in gtc {} does not have matching manifest/bpm file. Sample manifest is listed as {}.  Skipping sample.".format(
             names[10], sampleGtc, names[101]))

    nameMatch.flush()
    nameMatch.close()
