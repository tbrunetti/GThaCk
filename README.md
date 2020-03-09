# GThaCk
(**GT**ha**C**k)
Code to hack through, manipulate, and extract information from GTC files

## Table of Contents
---------------------
1.  [Introduction and Overview](#introduction-and-overview)
2.  [Software Requirements and Dependencies](#software-requirements-and-dependencies)
3.  [Installation](#installation)
4.  [Usage](#usage)
	* method: manipulateGTCs
	* method: getIntensities
	* method: sampleInformation

### Introduction and Overview
-----------------------------
GThaCk is a program that allows users to extract all data contained a gtc file without the use of GenomeStudio or Beeline.  Additionally, it allows users to manipulate the contents within a gtc file by making a copy of the file, while always maintaining the integrity of the original file. The manipulating of sample metadata and calls is primarily useful for validating software requirements and use cases/edge cases.


### Software Requirements and Dependencies
------------------------------------------
*  Python >=3.6
*  numpy
*  IlluminaBeadArrayFiles
	--note: This is the base of Illumina code forked from ..... however, I have modified it to be compatible with Python version 3.6 and updated the code with some updates to be compatible with GThaCk

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


### Usage
----------
Every function has the same 2 requirements: the bpm file and the directory of the location of the gtcs

For help on all the options available and what they do, please run the following or see the table at the bottom of the page:
```
python3 gtcFuncs.py -h
```


**method: manipulateGTCs**  
The minimum command required to manipulate gtc files is the following:
```
python3 gtcFuncs.py manipulateGTCs --bpm /path/to/manifest.bpm --gtcDir /path/to/gtcLocations/ --updates myUpdates.txt
```
An example of the format of myUpdates.txt can be see [here](https://github.com/tbrunetti/GThaCk/blob/develop/examples/example_gtcManipulationFile_input.txt) in [examples/example_gtcManipulationFile_input.txt](https://github.com/tbrunetti/GThaCk/blob/develop/examples/example_gtcManipulationFile_input.txt)
	*  tab-delimited text file
	_For sample update and metadata line:_
	*  first column = must start with the character ">" for each new sample directly followed by the name of the base gtc 
	*  second column = name of new gtc to be created
	*  third column = comma-separate list of keyword in gtc to update.  Keywords must be followed by "=" (no spaces before or after).  Possible keywords are the following: sampleName, sentrixBarcode, plateName, well, and sex.  Only use keywords that need to be updated.  Any keywords not listed will inherit the value of the base gtc file.
	_For snp updates_
	*  one snp per line
	*  first column = the name of the snp list in bpm file
	*  second column = the alleles to change it to.  Must always be an allele pair.
	*  The snps are update for the sample until the next sample is reached as determined by the next ">" character of metadata
	
Another option that is available exclusively to the method manipulateGTCs is the `--override` argument.  If a snp call needs to be updated in the bpm it can be made using this argument using an overrides file.  This **does not** create an updated bpm file, it is merely used so that a gtc can pass validation due to misrepresentation of a wrong allele(s).  The bpm file is updated within the scope of the running program, however, it will not write out a new bpm, only the original bpm will persist.  An example of an override file can be seen [here](https://github.com/tbrunetti/GThaCk/blob/develop/examples/override.txt) in [examples/override.txt](https://github.com/tbrunetti/GThaCk/blob/develop/examples/override.txt).  

Here is an example of how that would look like on the command line:
```
python3 gtcFuncs.py manipulateGTCs --bpm /path/to/manifest.bpm --gtcDir /path/to/gtcLocations/ --updates examples/example_gtcManipulationFile_input.txt --overrides examples/override.txt --outDir /path/to/output/Directory/
```

**method: getIntensities**

**method: sampleInformation**


