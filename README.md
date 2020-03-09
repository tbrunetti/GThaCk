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



### Usage
----------
