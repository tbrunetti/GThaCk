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
    import seaborn as sns
    import matplotlib.pyplot as plt 
    import numpy as np
    import sys

    logging.getLogger('getIntensities')

    gtcDir = self.gtcDir
    bpm = self.bpm
    outDir = self.outDir
    fileOutName = self.fileOutName
    prefix = self.prefix

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

    
    intensities_per_sample = {}

    for gtc in input_gtc_list:
        data = extractInformation.getGtcInfo(gtc=os.path.join(gtcDir, gtc))
        try:
            assert data[101] == manifest.manifest_name
            intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())] = {}
            intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())]['sex'] = data[1007].decode()

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
            logger.warning("Sample {}, {} does not have a matching bpm for the manifest you are supplying. Skipping sample.".format(data[10], gtc))
            continue
            

    allIntesities = pandas.DataFrame(intensities_per_sample)
    allIntensities_transpose = allIntesities.T
    if os.path.exists(outDir) == False:
        os.mkdir(outDir)
    allIntensities_transpose.to_csv(os.path.join(outDir, fileOutName), index = True, sep = '\t')


    allIntensities_transpose['sampleGroup'] = "samples"

    images = list(allIntensities_transpose)
    images.pop(images.index('sex'))
    images.pop(images.index('sampleGroup'))
    
    for i in images:
        mean = allIntensities_transpose[i].astype(int).mean()
        upperStdSix = mean + (allIntensities_transpose[i].astype(int).std()*6)
        lowerStdSix = mean - (allIntensities_transpose[i].astype(int).std()*6)
        upperStdThree = mean + (allIntensities_transpose[i].astype(int).std()*3)
        lowerStdThree = mean - (allIntensities_transpose[i].astype(int).std()*3)

        removeOutliers = allIntensities_transpose.loc[(allIntensities_transpose[i].astype(int) > lowerStdThree) & 
            (allIntensities_transpose[i].astype(int) < upperStdThree)]

        fig, axs = plt.subplots(ncols=3)

        sns.boxplot(x='sampleGroup', y=i, data = allIntensities_transpose, showfliers=False, color='white', ax=axs[0])
        sns.stripplot(x='sampleGroup', y=i, data = allIntensities_transpose, hue='sex', palette="colorblind", ax=axs[0]).set_title(str(i) + '\n across all samples', fontsize=10)
        axs[0].tick_params(axis='y', which='major', labelsize=8)

        plotDevs = sns.boxplot(x='sampleGroup', y=i, data = allIntensities_transpose, showfliers=False, color='white', ax=axs[1])
        plotDevs = sns.stripplot(x='sampleGroup', y=i, hue='sex', data = allIntensities_transpose, palette="colorblind", ax=axs[1])
        axs[1].set_ylabel('')
        axs[1].legend_.remove()
        plotDevs.axhline(upperStdThree, ls='--', color='blue')
        plotDevs.axhline(lowerStdThree, ls='--', color='blue')
        plotDevs.axhline(upperStdSix, ls=':', color='orange')
        plotDevs.axhline(lowerStdSix, ls=':', color='orange')
        plotDevs.axhline(mean, ls='-.', color = 'green', linewidth=2)
        axs[1].tick_params(axis='y', which='major', labelsize=8)
        plotDevs.set_title(str(i) + '\n across all samples \n annotated mean and std devs', fontsize=10)
        
        sns.boxplot(x='sampleGroup', y=i, data = removeOutliers, showfliers=False, color='white', ax=axs[2])
        sns.stripplot(x='sampleGroup', y=i, data = removeOutliers, hue='sex', palette="colorblind", ax=axs[2]).set_title(str(i) + '\n across all samples \n with < 3 std devs from mean', fontsize=10)
        axs[2].set_ylabel('')
        axs[2].tick_params(axis='y', which='major', labelsize=8)

        axs[0].legend(loc=0)
        axs[1].legend(loc=0)
        axs[2].legend(loc=0)
        plt.setp(axs)
        
        fig.set_size_inches(11, 7)
        fig.savefig(prefix + str(i) + "Plots.png")

        del removeOutliers
        del plotDevs
        del fig
        del axs


def getIntensitiesRecursive(self):
    import extractInformation
    import pandas
    import seaborn as sns
    import matplotlib.pyplot as plt 
    import numpy as np
    import sys
    from pathlib import Path
    from os import fspath

    logger.getLogger('getIntensitiesRecursive')

    gtcDir = self.gtcDir
    bpm = self.bpm
    outDir = self.outDir
    fileOutName = self.fileOutName
    prefix = self.prefix

    # reading in manifest more than once carries lot of overhead
    manifest = BeadPoolManifest(bpm)

    input_gtc_list = [fspath(gtc) for gtc in Path(gtcDir).rglob('*.gtc')]

    #detect which probes are available based on bpm input
    controls = manifest.control_config.decode().split('\n')
    # checks if split leaves an empty string, if yes, pop off
    if len(manifest.control_config.decode().split('\n')[-1]) == 0:
        controls.pop(len(controls)-1)

    # list of control probes in order
    tmp = [controls[i].split(":")[3].split(',', 1)[1] for i in range(0, len(controls))]
    intensity_probes = [i.replace(',', '_').replace(' ', '_') for i in tmp]

    
    intensities_per_sample = {}

    for gtc in input_gtc_list:
        data = extractInformation.getGtcInfo(gtc)
        try:
            assert data[101] == manifest.manifest_name
            intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())] = {}
            intensities_per_sample['{}-{}-{}'.format(data[11].decode(), data[12].decode(), data[10].decode())]['sex'] = data[1007].decode()

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
            logger.warning("Sample {}, {} does not have a matching bpm for the manifest you are supplying. Skipping sample.".format(data[10], gtc))
            continue
            

    allIntesities = pandas.DataFrame(intensities_per_sample)
    allIntensities_transpose = allIntesities.T
    if os.path.exists(outDir) == False:
        os.mkdir(outDir)
    allIntensities_transpose.to_csv(os.path.join(outDir, fileOutName), index = True, sep = '\t')


    allIntensities_transpose['sampleGroup'] = "samples"

    images = list(allIntensities_transpose)
    images.pop(images.index('sex'))
    images.pop(images.index('sampleGroup'))
    
    for i in images:
        mean = allIntensities_transpose[i].astype(int).mean()
        upperStdSix = mean + (allIntensities_transpose[i].astype(int).std()*6)
        lowerStdSix = mean - (allIntensities_transpose[i].astype(int).std()*6)
        upperStdThree = mean + (allIntensities_transpose[i].astype(int).std()*3)
        lowerStdThree = mean - (allIntensities_transpose[i].astype(int).std()*3)

        removeOutliers = allIntensities_transpose.loc[(allIntensities_transpose[i].astype(int) > lowerStdThree) & 
            (allIntensities_transpose[i].astype(int) < upperStdThree)]

        fig, axs = plt.subplots(ncols=3)

        sns.boxplot(x='sampleGroup', y=i, data = allIntensities_transpose, showfliers=False, color='white', ax=axs[0])
        sns.stripplot(x='sampleGroup', y=i, data = allIntensities_transpose, hue='sex', palette="colorblind", ax=axs[0]).set_title(str(i) + '\n across all samples', fontsize=10)
        axs[0].tick_params(axis='y', which='major', labelsize=8)

        plotDevs = sns.boxplot(x='sampleGroup', y=i, data = allIntensities_transpose, showfliers=False, color='white', ax=axs[1])
        plotDevs = sns.stripplot(x='sampleGroup', y=i, hue='sex', data = allIntensities_transpose, palette="colorblind", ax=axs[1])
        axs[1].set_ylabel('')
        axs[1].legend_.remove()
        plotDevs.axhline(upperStdThree, ls='--', color='blue')
        plotDevs.axhline(lowerStdThree, ls='--', color='blue')
        plotDevs.axhline(upperStdSix, ls=':', color='orange')
        plotDevs.axhline(lowerStdSix, ls=':', color='orange')
        plotDevs.axhline(mean, ls='-.', color = 'green', linewidth=2)
        axs[1].tick_params(axis='y', which='major', labelsize=8)
        plotDevs.set_title(str(i) + '\n across all samples \n annotated mean and std devs', fontsize=10)
        
        sns.boxplot(x='sampleGroup', y=i, data = removeOutliers, showfliers=False, color='white', ax=axs[2])
        sns.stripplot(x='sampleGroup', y=i, data = removeOutliers, hue='sex', palette="colorblind", ax=axs[2]).set_title(str(i) + '\n across all samples \n with < 3 std devs from mean', fontsize=10)
        axs[2].set_ylabel('')
        axs[2].tick_params(axis='y', which='major', labelsize=8)

        axs[0].legend(loc=0)
        axs[1].legend(loc=0)
        axs[2].legend(loc=0)
        plt.setp(axs)
        
        fig.set_size_inches(11, 7)
        fig.savefig(prefix + str(i) + "Plots.png")

        del removeOutliers
        del plotDevs
        del fig
        del axs