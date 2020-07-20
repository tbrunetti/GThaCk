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
    import logging

    logger = logging.getLogger('reportSampleInfo')

    bpm = self.bpm
    gtcDir = self.gtcDir
    outDir = self.outDir
    fileOutName = self.fileOutName
    if self.prefix != '':
        prefix = self.prefix + "_"
    else:
        prefix = self.prefix

    nameMatch = open(os.path.join(outDir, fileOutName), 'w')
    manifest = BeadPoolManifest(bpm)
    input_gtc_list = [gtc for gtc in os.listdir(gtcDir) if gtc.endswith(".gtc")]

    header = ['BTID', 'plate', 'well', 'gtcName', 'sampleID', 'callRate', 'gc10', 'sex', 'logrDev', 'location']
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
                str(names[1007].decode()) + '\t' + str(names[1008]) + '\t' + gtcDir + '\n')

        except AssertionError:
            print("Error, sample {} in gtc {} does not have matching manifest/bpm file. Sample manifest is listed as {}.  Skipping sample.".format(
             names[10], sampleGtc, names[101])) 
            logger.warning('Error, sample {} in gtc {} does not have matching manifest/bpm file. Sample manifest is listed as {}.  Skipping sample.'.format(
             names[10], sampleGtc, names[101]))

    nameMatch.flush()
    
    summaryData = pandas.read_table(nameMatch.name)
    nameMatch.close()

    summaryStatsTable = summaryData.groupby('plate').agg(totalSamples=pandas.NamedAgg(column="plate", aggfunc='count'),
        totalUniqueWells=pandas.NamedAgg(column='well', aggfunc='nunique'), 
        totalUniqueBTID=pandas.NamedAgg(column='BTID', aggfunc='nunique'), 
        meanCallrate=pandas.NamedAgg(column='callRate', aggfunc='mean'), 
        stdDevCallrate=pandas.NamedAgg(column='callRate', aggfunc='std'), 
        minCallrate=pandas.NamedAgg(column='callRate', aggfunc='min'), 
        maxCallrate=pandas.NamedAgg(column='callRate', aggfunc='max'), 
        medianCallrate=pandas.NamedAgg(column='callRate', aggfunc="median"), 
        varianceCallrate=pandas.NamedAgg(column='callRate', aggfunc="var"),
        meanGC10=pandas.NamedAgg(column='gc10', aggfunc='mean'), 
        stdDevGC10=pandas.NamedAgg(column='gc10', aggfunc='std'), 
        minGC10=pandas.NamedAgg(column='gc10', aggfunc='min'), 
        maxGC10=pandas.NamedAgg(column='gc10', aggfunc='max'), 
        medianGC10=pandas.NamedAgg(column='gc10', aggfunc="median"), 
        varianceGC10=pandas.NamedAgg(column='gc10', aggfunc="var"),
        meanLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='mean'), 
        stdDevLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='std'), 
        minLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='min'), 
        maxLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='max'), 
        medianLogRdev=pandas.NamedAgg(column='logrDev', aggfunc="median"), 
        varianceLogRdev=pandas.NamedAgg(column='logrDev', aggfunc="var"))

    summaryStatsTable.to_csv(os.path.join(outDir, prefix + 'summaryStatsTable.txt'), sep='\t', index=True)
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
        axs[0].tick_params(axis='y', which='major', labelsize=8)


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
        axs[1].tick_params(axis='y', which='major', labelsize=8)


        sns.boxplot(x='sampleGroup', y=i, data = removeOutliers, showfliers=False, color='white', ax=axs[2])
        sns.stripplot(x='sampleGroup', y=i, data = removeOutliers, hue='sex', palette="colorblind", ax=axs[2]).set_title(str(i) + ' across all samples \n with < 3 std devs from mean', fontsize=10)
        axs[2].set_ylabel('')
        axs[2].tick_params(axis='y', which='major', labelsize=8)

        axs[0].legend(loc=0)
        axs[1].legend(loc=0)
        axs[2].legend(loc=0)
        plt.setp(axs)

        fig.set_size_inches(11, 7)
        fig.savefig(os.path.join(outDir, prefix + str(i)+"Plots.png"))

        del removeOutliers
      

def reportSampleInfoRecursive(self):
    import extractInformation
    from pathlib import Path
    from os import fspath
    import logging

    logger = logging.getLogger('reportSampleInfoRecursive')

    bpm = self.bpm
    gtcDir = self.gtcDir
    outDir = self.outDir
    fileOutName = self.fileOutName
    if self.prefix != '':
        prefix = self.prefix + "_"
    else:
        prefix = self.prefix

    nameMatch = open(os.path.join(outDir, fileOutName), 'w')
    manifest = BeadPoolManifest(bpm)
    input_gtc_list = [fspath(gtc) for gtc in Path(gtcDir).rglob('*.gtc')]
 
    header = ['BTID', 'plate', 'well', 'gtcName', 'sampleID', 'callRate', 'gc10', 'sex', 'logrDev', 'location']
    nameMatch.write('\t'.join(header) + '\n')
    
    for sampleGtc in input_gtc_list:
        try:
            names = extractInformation.getGtcInfo(gtc=sampleGtc)
            assert manifest.manifest_name.decode() == names[101].decode()
            nameMatch.write(names[10].decode() + '\t' + 
                names[11].decode() + '\t' + names[12].decode() + '\t' + 
                sampleGtc.split('/')[-1] + '\t' +
                '{}-{}-{}'.format(names[11].decode(), names[12].decode(), names[10].decode()) + 
                '\t' + str(names[1006]) + '\t' + str(names[1009]) + '\t' +
                str(names[1007].decode()) + '\t' + str(names[1008]) + '\t' + '/'.join(sampleGtc.split('/')[:-1]) + '\n')

        except AssertionError:
            print("Error, sample {} in gtc {} does not have matching manifest/bpm file. Sample manifest is listed as {}.  Skipping sample.".format(
             names[10], sampleGtc, names[101]))
            logger.warning("Error, sample {} in gtc {} does not have matching manifest/bpm file. Sample manifest is listed as {}.  Skipping sample.".format(
             names[10], sampleGtc, names[101]))

    nameMatch.flush()
    
    summaryData = pandas.read_table(nameMatch.name)
    nameMatch.close()

    summaryStatsTable = summaryData.groupby('plate').agg(
        totalSamples=pandas.NamedAgg(column="plate", aggfunc='count'),
        totalUniqueWells=pandas.NamedAgg(column='well', aggfunc='nunique'),
        totalUniqueBTID=pandas.NamedAgg(column='BTID', aggfunc='nunique'),
        meanCallrate=pandas.NamedAgg(column='callRate', aggfunc='mean'),
        stdDevCallrate=pandas.NamedAgg(column='callRate', aggfunc='std'),
        minCallrate=pandas.NamedAgg(column='callRate', aggfunc='min'),
        maxCallrate=pandas.NamedAgg(column='callRate', aggfunc='max'),
        medianCallrate=pandas.NamedAgg(column='callRate', aggfunc="median"),
        varianceCallrate=pandas.NamedAgg(column='callRate', aggfunc="var"),
        meanGC10=pandas.NamedAgg(column='gc10', aggfunc='mean'),
        stdDevGC10=pandas.NamedAgg(column='gc10', aggfunc='std'),
        minGC10=pandas.NamedAgg(column='gc10', aggfunc='min'),
        maxGC10=pandas.NamedAgg(column='gc10', aggfunc='max'),
        medianGC10=pandas.NamedAgg(column='gc10', aggfunc="median"),
        varianceGC10=pandas.NamedAgg(column='gc10', aggfunc="var"),
        meanLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='mean'),
        stdDevLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='std'),
        minLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='min'),
        maxLogRdev=pandas.NamedAgg(column='logrDev', aggfunc='max'),
        medianLogRdev=pandas.NamedAgg(column='logrDev', aggfunc="median"),
        varianceLogRdev=pandas.NamedAgg(column='logrDev', aggfunc="var"))

    summaryStatsTable.to_csv(os.path.join(outDir, prefix + 'summaryStatsTable.txt'),sep='\t',index=True)

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
        axs[0].tick_params(axis='y', which='major', labelsize=8)


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
        axs[1].tick_params(axis='y', which='major', labelsize=8)


        sns.boxplot(x='sampleGroup', y=i, data = removeOutliers, showfliers=False, color='white', ax=axs[2])
        sns.stripplot(x='sampleGroup', y=i, data = removeOutliers, hue='sex', palette="colorblind", ax=axs[2]).set_title(str(i) + ' across all samples \n with < 3 std devs from mean', fontsize=10)
        axs[2].set_ylabel('')
        axs[2].tick_params(axis='y', which='major', labelsize=8)

        axs[0].legend(loc=0)
        axs[1].legend(loc=0)
        axs[2].legend(loc=0)
        plt.setp(axs)

        fig.set_size_inches(11, 7)
        fig.savefig(os.path.join(outDir, prefix + str(i)+"Plots.png"))

        del removeOutliers
