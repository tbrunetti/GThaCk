# GThaCk
(**GT**ha**C**k)
Code to hack through, manipulate, and extract information from GTC files

## Table of Contents
---------------------
1.  [Introduction and Overview](#introduction-and-overview)
2.  [Software Requirements and Dependencies](#software-requirements-and-dependencies)
3.  [Installation](#installation)
4.  [General Usage](#general-usage)
	* method: [manipulateGTCs](https://github.com/tbrunetti/GThaCk/wiki/manipulateGTCs_wiki)
	* method: [createSampleSheet](https://github.com/tbrunetti/GThaCk/wiki/createSampleSheet_wiki)
	* method: [getIntensities](https://github.com/tbrunetti/GThaCk/wiki/getIntensities_wiki)
	* method: [sampleInformation](https://github.com/tbrunetti/GThaCk/wiki/sampleInformation_wiki)
	* method: [query](https://github.com/tbrunetti/GThaCk/wiki/query_wiki)

### Introduction and Overview
-----------------------------
GThaCk is a program that allows users to extract all data contained a gtc file without the use of GenomeStudio or Beeline.  Additionally, it allows users to manipulate the contents within a gtc file by making a copy of the file, while always maintaining the integrity of the original file. The manipulating of sample metadata and calls is primarily useful for validating software requirements and use cases/edge cases.


### Software Requirements and Dependencies
------------------------------------------
*  Python >=3.6
*  numpy  
*  pandas
*  matplotlib (for methods: sampleInformation, getIntensities) 
*  seaborn  (for methods: sampleInformation, getIntensities)
*  IlluminaBeadArrayFiles
	--note: This is very similar to the base Illumina code forked from (https://github.com/Illumina/BeadArrayFiles), however, I have modified it to be compatible with Python version 3.6 and updated the code with some updates to be compatible with GThaCk.  Since GThaCk is built upon this code, the same copyright and licensing of this software need to be applied in addition to the one listed for the GThaCk repo.  Where conflicts between the licences persist, the Illumina license should take precedence.  They can be found (here)[https://github.com/Illumina/BeadArrayFiles] and [here](https://github.com/Illumina/GTCtoVCF).

### Installation
-----------------
To install this software either download or clone this repository
```
git clone https://github.com/tbrunetti/GThaCk.git
```
The go to the modules directory and move the IlluminaBeadArrayFiles.tar.gz to the site-packages directory of your python3 library and unpack it.
```
cd modules
mv IlluminaBeadArrayFiles.tar.gz ~/.local/lib/python3.XX/site-packages/
cd ~/.local/lib/python3.XX/site-packages
tar -zxvf IlluminaBeadArrayFiles
```


### General Usage
-----------------
Every function has the same 2 requirements: the bpm file specified using `--bpm`  and the directory of the location of the gtcs specified using `--gtcDir` in addition to specific argument required or optionally specified for that particular method.  For more information please visit the table of options for each method listed in the [wiki here](https://github.com/tbrunetti/GThaCk/wiki)
```
python3 gtcFuncs.py {method} --bpm /path/to/manifest.bpm --gtcDir /path/to/gtcLocations/
```
For help on all the options available and what they do, please run the following or see the full table of options located on the [wiki](https://github.com/tbrunetti/GThaCk/wiki):
```
python3 gtcFuncs.py -h
```


