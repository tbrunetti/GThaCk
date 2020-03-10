from IlluminaBeadArrayFiles import *
import struct
from io import BytesIO
import os
import sys
import logging
import pandas

'''
function: baseData(self)
description:
input: gtcFunction object
output:
'''
def baseData(self):
	import extractInformation

	bpm=self.bpm
	gtcDir=self.gtcDir
	outDir=self.outDir
	sampleSheetUpdates = self.sampleSheetUpdates

	logger = logging.getLogger('generateSampleSheet')
	logger.debug('In method generateSampleSheet')

	manifest = BeadPoolManifest(bpm)

	smplSheetcols = ['Sample_ID','SentrixBarcode_A','SentrixPosition_A','Sample_Plate','Sample_Well','Gender','Sample_Name','Instrument_ID','Race','MRN','Name','DOB','exclude','Notes']
	#dataManifest = pandas.DataFrame(columns = smplSheetcols)
	outputInfo = []
	
	for gtcFile in os.listdir(gtcDir):
		if gtcFile.endswith('.gtc'):
			data = extractInformation.getGtcInfo(os.path.join(gtcDir, gtcFile))
			colValues = [data[10].decode(),
						data[1016].decode(),
						gtcFile.split('_')[1][:-4],
						data[11].decode(),
						data[12].decode(),
						data[1007].decode(),
						data[10].decode(),
						'0000000000',
						'NA',
						'000',
						'UNKNOWN, UNKNOWN',
						'00-00-0000',
						'0',
						'validationPlate'
			 			]
			print(colValues)
			paired = zip(smplSheetcols, colValues)
			singleSample = dict(paired)
			outputInfo.append(singleSample)
			
	dataManifest= pandas.DataFrame(outputInfo)
	print(dataManifest)
	#dataManifest = pandas.concat([dataManifest, outputInfo], axis=0).reset_index()
	dataManifest.to_csv(os.path.join(outDir, '_tmp_data.csv'), index=False)

	def updateData(sampleSheetUpdates):
		pass


'''
function: updateHeader(self)
description:
input: gtcFunction object
output:
'''
def updateHeader(self):
	from datetime import datetime

	outDir = self.outDir
	bpm = self.bpm

	logger = logging.getLogger('updateHeader')
	logger.debug('In method updateHeader')

	smplSheetcols = ['Sample_ID','SentrixBarcode_A','SentrixPosition_A','Sample_Plate','Sample_Well','Gender','Sample_Name','Instrument_ID','Race','MRN','Name','DOB','exclude','Notes']

	placeHolder = ['' for i in range(0, len(smplSheetcols))]
	placeHolder[0] = '[Header]'
	headerFile = open(os.path.join(outDir, '_tmp_headerFile.csv'), 'w')
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Institute Name'
	placeHolder[1] = 'CCPM Biobank'
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Investigator Name'
	placeHolder[1] = 'Kathleen Barnes'
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Project Name'
	placeHolder[1] = 'CCPM-MEGAv1_validation_manifest1-8_PGX'
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'Date'
	placeHolder[1] =  datetime.today().strftime("%m/%d/%y")
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder = ['' for i in range(0, len(smplSheetcols))]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = '[Manifests]'
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = 'A'
	placeHolder[1] = bpm[:-4]
	placeHolder[2] = 'CCPM-MEGA-Ex_validation_07-21-17-1.egt'
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder = ['' for i in range(0, len(smplSheetcols))]
	headerFile.write(','.join(placeHolder) + '\n')

	placeHolder[0] = '[Data]'
	headerFile.write(','.join(placeHolder)+'\n')

	headerFile.flush()
	headerFile.close()


'''
function: generateSampleSheet(outDir, fileName)
description:
input:
output:
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