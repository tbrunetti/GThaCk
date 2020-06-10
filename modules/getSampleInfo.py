import os
import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
    fileOutName = self.fileOutName

    nameMatch = open(os.path.join(outDir, fileOutName), 'w')
    manifest = BeadPoolManifest(bpm)
    input_gtc_list = [gtc for gtc in os.listdir(gtcDir) if gtc.endswith(".gtc")]

    header = ['BTID', 'plate', 'well', 'gtcName', 'sampleID', 'callRate', 'gc10', 'sex', 'logrDev']
    nameMatch.write('\t'.join(header) + '\n')
    
    for sampleGtc in input_gtc_list:
        try:
            names = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, sampleGtc))
            assert manifest.manifest_name.decode() == names[101].decode()
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
    
    summaryData = pandas.read_table(nameMatch.name)
    nameMatch.close()

    summaryData['sampleGroup'] = "samples"

    images = ['callRate', 'gc10', 'logrDev']
    for i in images:
        mean = summaryData[i].mean()
        upperStdSix = mean + (summaryData[i].std()*6)
        lowerStdSix = mean - (summaryData[i].std()*6)
        upperStdThree = mean + (summaryData[i].std()*3)
        lowerStdThree = mean - (summaryData[i].std()*3)

        removeOutliers = summaryData.loc[(summaryData[i].astype(float) > lowerStdThree) & 
            (summaryData[i].astype(float) < upperStdThree)]

        fig, axs = plt.subplots(ncols=3)

        sns.boxplot(x='sampleGroup', y=i, data = summaryData, showfliers=False, color='white', ax=axs[0])
        sns.stripplot(x='sampleGroup', y=i, data = summaryData, hue='sex', palette="colorblind", ax=axs[0]).set_title(str(i) + ' across all samples', fontsize=10)
        axs[0].set_yticklabels(np.round(axs[0].get_yticks(),3), size = 8)

        plotDevs = sns.boxplot(x='sampleGroup', y=i, data = summaryData, showfliers=False, color='white', ax=axs[1])
        plotDevs = sns.stripplot(x='sampleGroup', y=i, hue='sex', data = summaryData, palette="colorblind", ax=axs[1])
        axs[1].set_ylabel('')
        axs[1].legend_.remove()
        plotDevs.axhline(upperStdThree, ls='--', color='blue')
        plotDevs.axhline(lowerStdThree, ls='--', color='blue')
        plotDevs.axhline(upperStdSix, ls=':', color='orange')
        plotDevs.axhline(lowerStdSix, ls=':', color='orange')
        plotDevs.axhline(mean, ls='-.', color = 'green', linewidth=2)
        plotDevs.set_title(str(i) + ' across all samples \n annotated mean and std devs', fontsize=10)
        axs[1].set_yticklabels(np.round(axs[1].get_yticks(),3), size = 8) 

        sns.boxplot(x='sampleGroup', y=i, data = removeOutliers, showfliers=False, color='white', ax=axs[2])
        sns.stripplot(x='sampleGroup', y=i, data = removeOutliers, hue='sex', palette="colorblind", ax=axs[2]).set_title(str(i) + ' across all samples \n with < 3 std devs from mean', fontsize=10)
        axs[2].set_ylabel('')
        axs[2].set_yticklabels(np.round(axs[2].get_yticks(), 3), size = 8) 

        axs[0].legend(loc=0)
        axs[1].legend(loc=0)
        axs[2].legend(loc=0)
        plt.setp(axs)

        fig.set_size_inches(11, 7)
        fig.savefig(str(i)+"Plots.png")

        del removeOutliers
      
    