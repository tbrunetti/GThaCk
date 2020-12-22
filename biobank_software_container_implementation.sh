#!/bin/bash

#SBATCH --time=1000
#SBATCH --ntasks=1
#SBATCH --mem=30000
#SBATCH --job-name=biobankSoftwareContainer
#SBATCH --output=biobankSoftwareContainer_07192020.log
#SBATCH --error=biobankSoftwareContainer_07192020.err
#SBATCH -p defq


module load singularity


singularity run -B /path/to/container/ \
	CCPM_Biobank_Freeze_and_Clinical_Validation_Software_v0.1.0_07192020.simg \
	python3 \
	/opt/GThaCk/gtcFuncs.py \
	sampleInformation \
	--bpm /path/to/my.bpm \
	--gtcDir /path/to/location/of/gtcs/ \
	--outDir /path/to/output/ \
	--modDir /opt/GThaCk/modules/ \
	--prefix sampleInfoTest \
	--logName testingSampleInfoContainer.log \
	--recursive

singularity run -B /path/to/container/ \
	CCPM_Biobank_Freeze_and_Clinical_Validation_Software_v0.1.0_07192020.simg /gtc_to_vcf.py \
	python3 \
	--manifest-file /path/to/my.csv \
	--gtc-paths /path/to/gtc/dir/ \
	--genome-fasta-file /opt/GTCtoVCF/scripts/37 \
	--output-vcf-path /path/to/vcf/output \
	--include-attributes GT GQ BAF LRR \
	--log-file GTCtoVCF.log \
	--unsquash-duplicates 

singularity run -B /path/to/container/ \
	CCPM_Biobank_Freeze_and_Clinical_Validation_Software_v0.1.0_07192020.simg \
	samtools view \
	mySortedFile.bam 
