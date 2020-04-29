from IlluminaBeadArrayFiles import *
import struct
from io import BytesIO
import os
import sys
import logging
import pandas
import pympler
from pympler import muppy
from pympler import summary
#from multiprocessing import Process
import multiprocessing
import glob

'''
function: baseData(self)
description: extracts information from each gtc file in the directory to get all base metadata information formated into csv for sample sheet
input: gtcFunction object
output: does not return anything, however, a temporary file [data] csv is generated on the local system
'''
def checkConfig(config, gtcDir):
	logger = logging.getLogger('checkConfig')
	logger.debug('In module sampleSheet.py in baseData() in submodule checkConfig')

	totalGtcs = sum([1 for gtcFile in os.listdir(gtcDir) if gtcFile.endswith('.gtc')])
	
	configParams = {}
	with open(config, 'r') as baseParameters:
		for line in baseParameters:
			configParams[line.split(':')[0]] = [line.split(':')[1].rstrip()]

	try:
		assert ((totalGtcs - len(configParams['control_wells']) <= totalGtcs) and (totalGtcs - len(configParams['control_wells']) >= 0))
		return configParams, totalGtcs
		
	except AssertionError:
		print('There are not enough .gtc files to assign new values that are not controls')
		logger.critical('There are not enough .gtc files to assign new values that are not controls')
		sys.exit()

'''
function: baseData(self)
description: extracts information from each gtc file in the directory to get all base metadata information formated into csv for sample sheet
input: gtcFunction object
output: does not return anything, however, a temporary file [data] csv is generated on the local system
'''
def baseData(self):
	import extractInformation
	import random

	bpm=self.bpm
	gtcDir=self.gtcDir
	outDir=self.outDir
	sampleSheetUpdatesInput = self.sampleSheetUpdates
	config = self.config
	pseudoInstID = self.pseudoInstID
	pseudoMrn = self.pseudoMrn

	logger = logging.getLogger('generateSampleSheet')
	logger.debug('In method generateSampleSheet')

	
	def updateData(gtcFile, data, sampleSheetUpdates, default, exclude, gtcMatchFile):
		logger = logging.getLogger('updateData')
		logger.debug('In module sampleSheet.py in baseData() in submodule updateData')
		if sampleSheetUpdates == None:
			manifestGender = 'Unknown'
			if data[1007].decode() == 'F':
				manifestSex = 'Female'
			elif data[1007].decode() == 'M':
				manifestSex = 'Male'
			elif data[1007].decode() == 'U':
				manifestSex = "Unknown"
			colValues = [
				data[10].decode(),
				data[1016].decode(),
				gtcFile.split('_')[1][:-4],
				data[11].decode(),
				data[12].decode(),
				manifestSex,
				data[10].decode(),
				str(default['instID']),
				'',
				str(default['mrn']),
				'UNKNOWN, UNKNOWN',
				'00-00-0000',
				exclude,
				'validationPlate'
				]
			gtcMatchFile.write('\t'.join([gtcFile, data[10].decode(), data[12].decode(), manifestSex,
				str(default['instID']), str(default['mrn']), 'UNKNOWN, UNKNOWN', '00-00-0000']) + '\n')

		else:
			logger.debug('Updating {} in manifest sample sheet'.format(sampleSheetUpdates['patientName']))
			colValues = [
				data[10].decode(),
				data[1016].decode(),
				gtcFile.split('_')[1][:-4],
				data[11].decode(),
				data[12].decode(),
				sampleSheetUpdates['sex'],
				data[10].decode(),
				sampleSheetUpdates['instrumentID'],
				'',
				sampleSheetUpdates['mrn'],
				sampleSheetUpdates['patientName'],
				sampleSheetUpdates['DOB'],
				exclude,
				'validationPlate'
				]

			gtcMatchFile.write('\t'.join([gtcFile, data[10].decode(), data[12].decode(), sampleSheetUpdates['sex'],
				sampleSheetUpdates['instrumentID'], sampleSheetUpdates['mrn'], sampleSheetUpdates['patientName'],
				sampleSheetUpdates['DOB']]) + '\n')

		
		return colValues


	'''
	TODO:
	# add config of wells of control positions -- are always included in the exclude column (set to 1)
	# first x positions not controls update MRN, instrument ID
	# exclude = 1 except for controls and any updated IDs
	# exclude keyword and include keyword -- based on gtcID
	# print out a file with which gtc file is paired with
	# tab-delimited columns: patientName, DOB, sex, mrn, instrumentID as case-insensitive
	# sex needs to be coded as Male and Female not M and F
	# make sample sheet columns and order mutable based on config file
	'''
	manifest = BeadPoolManifest(bpm)
	gtcMatchData = open(os.path.join(outDir, 'gtcFiles_paired_sampleSheet.txt'), 'w')
	configParams, totalGtcs = checkConfig(config = config, gtcDir = gtcDir)
	if sampleSheetUpdatesInput != None:
		sampleSheetUpdates = pandas.read_table(sampleSheetUpdatesInput, dtype=str)
	else:
		sampleSheetUpdates = pandas.DataFrame()
	smplSheetcols = ['Sample_ID','SentrixBarcode_A','SentrixPosition_A','Sample_Plate','Sample_Well','Gender','Sample_Name','Instrument_ID','Race','MRN','Name','DOB','exclude','Notes']
	outputInfo = []

	randomInstIDs = random.sample(range(int(pseudoInstID.split(',')[0]), int(pseudoInstID.split(',')[1])), totalGtcs)
	randomMrns = random.sample(range(int(pseudoMrn.split(',')[0]), int(pseudoMrn.split(',')[1])), totalGtcs)

	

	def gtcProcessing(gtcFile, finalList):

		print('Pre-Processing Memory Leak Check for gtc {}:\n'.format(gtcFile))			
		#all_objects_in_gtc = muppy.get_objects()
		#print(summary.summarize(all_objects_in_gtc))
		if gtcFile.endswith('.gtc'):
			colValues = []
			data = extractInformation.getGtcInfo(os.path.join(gtcDir, gtcFile))
			if data[12].decode() in configParams['control_wells']:
				colValues = updateData(gtcFile=gtcFile, data=data, sampleSheetUpdates=None, default={'instID':randomInstIDs[0], 'mrn':randomMrns[0]}, exclude=0, gtcMatchFile=gtcMatchData)
				randomInstIDs.pop(0)
				randomMrns.pop(0)
			elif gtcFile in configParams['exclude_gtcs']:
				colValues = updateData(gtcFile=gtcFile, data=data, sampleSheetUpdates=None, default={'instID':randomInstIDs[0], 'mrn':randomMrns[0]}, exclude=1, gtcMatchFile=gtcMatchData)
				randomInstIDs.pop(0)
				randomMrns.pop(0)			
			elif len(sampleSheetUpdates.index) > 0:
				colValues = updateData(gtcFile=gtcFile, data=data, sampleSheetUpdates=sampleSheetUpdates.iloc[0].to_dict(), default=None, exclude=0, gtcMatchFile=gtcMatchData)
				sampleSheetUpdates.drop(0, inplace=True)
				sampleSheetUpdates.reset_index(drop=True, inplace=True)	
			else:
				colValues = updateData(gtcFile=gtcFile, data=data, sampleSheetUpdates=None, default={'instID':randomInstIDs[0], 'mrn':randomMrns[0]}, exclude=0, gtcMatchFile=gtcMatchData)
				randomInstIDs.pop(0)
				randomMrns.pop(0)
				
			singleSample = dict(zip(smplSheetcols, colValues))
			print('Post-Processing Memory Leak Check for gtc {}:\n'.format(gtcFile))			
			finalList.append(singleSample)

	dataManager = multiprocessing.Manager()
	finalList = dataManager.list()
	listOfJobs = []
	for gtcFile in enumerate(glob.glob(os.path.join(gtcDir, "*.gtc"))):
		print(gtcFile[1].split('/')[-1])
		#processes = multiprocessing.Process(target =gtcProcessing, args=(gtcFile, finalList))
		#listOfJobs.append(processes)
		#processes.start()

	#for eachJob in listOfJobs:
	#	eachJob.join()

	# convert a proxy list to normal list object for use in downstream code
	#convertedList = [i for i in finalList]

	try:
		assert len(sampleSheetUpdates.index) == 0
		dataManifest= pandas.DataFrame(convertedList)
		dataManifest.sort_values(by=['Sample_Well'], inplace=True)
		dataManifest.to_csv(os.path.join(outDir, '_tmp_data.csv'), index=False)
		gtcMatchData.flush()
		gtcMatchData.close()
		del dataManifest
	except AssertionError:
		print('Not all samples in sample update list were used in gtc file')
		logger.error('Not all samples in sample update list were used in gtc file')

'''
function: updateHeader(self)
description: generates the header portion of the sample sheet
input: gtcFunction object
output: nothing is returned, however, a temporary file [header] csv is generated on the local system
'''
def updateHeader(self):
	from datetime import datetime

	outDir = self.outDir
	bpm = self.bpm
	config = self.config
	gtcDir = self.gtcDir

	logger = logging.getLogger('updateHeader')
	logger.debug('In method updateHeader')

	configParams, totalGtcs = checkConfig(config=config, gtcDir=gtcDir)

	smplSheetcols = ['Sample_ID','SentrixBarcode_A','SentrixPosition_A','Sample_Plate','Sample_Well','Gender','Sample_Name','Instrument_ID','Race','MRN','Name','DOB','exclude','Notes']

	placeHolder = ['' for i in range(0, len(smplSheetcols))]
	placeHolder[0] = '[Header]'
	headerFile = open(os.path.join(outDir, '_tmp_headerFile.csv'), 'w')
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Institute Name'
	placeHolder[1] = configParams['institute_name'][0]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Investigator Name'
	placeHolder[1] = configParams['investigator_name'][0]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Project Name'
	placeHolder[1] = configParams['project_name'][0]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Date'
	placeHolder[1] =  datetime.today().strftime("%m/%d/%y")
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder = ['' for i in range(0, len(smplSheetcols))]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = '[Manifests]'
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'A'
	placeHolder[1] = bpm.split('/')[-1][:-4]
	placeHolder[2] = configParams['egt_cluster_file'][0]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder = ['' for i in range(0, len(smplSheetcols))]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = '[Data]'
	headerFile.write(','.join(placeHolder)+'\n')

	headerFile.flush()
	headerFile.close()

	del placeHolder


'''
function: generateSampleSheet(outDir, fileName)
description: combines the temorary [header] and [data] csv files to generate final manifest
input: path to output directory and the name of the final sample sheet
output: does not return anything, however, a final csv sample sheet is generated on the local system
'''
def generateSampleSheet(outDir, fileName):
	import subprocess
	
	logger = logging.getLogger('generateSampleSheet')
	logger.debug('In method generateSampleSheet()')

	finalFile = open(os.path.join(outDir, fileName), 'w')

	try:
		subprocess.check_call(['cat', os.path.join(outDir, '_tmp_headerFile.csv'), os.path.join(outDir, '_tmp_data.csv')],
			stdout=finalFile)
		finalFile.flush()
		finalFile.close()
	except subprocess.CalledProcessError:
		pass

	subprocess.run(['rm', os.path.join(outDir, '_tmp_headerFile.csv')])
	subprocess.run(['rm', os.path.join(outDir, '_tmp_data.csv')])