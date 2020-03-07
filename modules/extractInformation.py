from IlluminaBeadArrayFiles import *
import struct
from io import BytesIO

'''
function: getGtcInfo(gtc)
description:
input:
output:
'''

def getGtcInfo(gtc):
    data = {}
    genotype_calls = GenotypeCalls(gtc)
    print(genotype_calls)
    
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_AUTOCALL_DATE] = genotype_calls.get_autocall_date(
        )  # key:201
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_AUTOCALL_VERSION] = genotype_calls.get_autocall_version(
        )  # key:300
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_B_ALLELE_FREQS] = genotype_calls.get_ballele_freqs(
        )  # key:1012 - per SNP on all SNPs on chip
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_BASE_CALLS] = genotype_calls.get_base_calls(
        )  # key:1003 - per SNP on all SNPs on chip (options: A/C/T/G/-/I/D)
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_CALL_RATE] = genotype_calls.get_call_rate(
        )  # key:1006 - per sample -- total number of valid SNPs with genotype calls divided by total SNPs clustered.  If a SNP has been zeroed out in the cluster file, it is not considered in the tatal # clustered snps; confirmed same value as in BCP
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_CLUSTER_FILE] = genotype_calls.get_cluster_file(
        )  # key:100
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_CONTROLS_X] = genotype_calls.get_control_x_intensities(
        )  # key:500 - 92 values
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_CONTROLS_Y] = genotype_calls.get_control_y_intensities(
        )  # key:501 - 92 values
    data[
        GenotypeCalls._GenotypeCalls__ID_GC10] = genotype_calls.get_gc10(
        )  # key:1009 - per samples - confirmed same as BCP
    data[GenotypeCalls._GenotypeCalls__ID_GC50] = (
        genotype_calls.get_gc50(), genotype_calls.get_num_calls(),
        genotype_calls.get_num_no_calls(),
        genotype_calls.get_num_intensity_only()
        )  # key:1011 - per sample
    data[GenotypeCalls.
        _GenotypeCalls__ID_GENDER] = genotype_calls.get_gender(
        )  # key:1007 - calculated from chip NOT from sample manifest
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_GENOTYPE_SCORES] = genotype_calls.get_genotype_scores(
        )  # key:1004
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_GENOTYPES] = genotype_calls.get_genotypes(
        )  # key:1002
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_IMAGING_DATE] = genotype_calls.get_imaging_date(
        )  # key:200
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_LOGR_DEV] = genotype_calls.get_logr_dev(
        )  # key:1008 - the standard deviation of the log(r ratio) across all snps. Essentially estimates noise per sample; confirmed same as in BCP
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_NORMALIZATION_TRANSFORMS] = genotype_calls.get_normalization_transforms(
        )  # key:400
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_NUM_SNPS] = genotype_calls.get_num_snps(
        )  # key:1
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_PERCENTILES_X] = genotype_calls.get_percentiles_x(
        )  # key:1014 - 3 values
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_PERCENTILES_Y] = genotype_calls.get_percentiles_y(
        )  # key:1015 - 3 values
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_PLOIDY] = genotype_calls.get_ploidy(
        )  # key:2 - per sample
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_PLOIDY_TYPE] = genotype_calls.get_ploidy_type(
        )  # key:3 - per sample
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_RAW_X] = genotype_calls.get_raw_x_intensities(
        )  # key:1000 - per SNP
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_RAW_Y] = genotype_calls.get_raw_y_intensities(
        )  # key:1001 - per SNP
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_SAMPLE_NAME] = genotype_calls.get_sample_name(
        )  # key:10
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_SAMPLE_PLATE] = genotype_calls.get_sample_plate(
        )  # key:11
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_SAMPLE_WELL] = genotype_calls.get_sample_well(
        )  # key:12
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_SCANNER_DATA] = genotype_calls.get_scanner_data(
        )  # key:1005
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_SLIDE_IDENTIFIER] = genotype_calls.get_slide_identifier(
        )  # key:1016 - Illumina barcode (not the RxCx part)
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_SNP_MANIFEST] = genotype_calls.get_snp_manifest(
        )  # key:101 - name of cluster file used
    data[
        GenotypeCalls.
        _GenotypeCalls__ID_LOGR_RATIOS] = genotype_calls.get_logr_ratios(
        )  # key:1013 per SNP, the log(R ratio), 0 = perfect single copy while above and below indicate copy number anomoalies

    return data