import logging

'''
function: getIntensities(gtcDir, bpm, outDir)
description:
input:
output:
'''
def getIntensities(gtcDir, bpm, outDir):

    # SOMEWHERE NEED TO CALL METHOD: extractionInformation.py
    # reading in manifest more than once carries lot of overhead
    manifest = BeadPoolManifest(bpm)


    input_gtc_list = [
        gtc for gtc in os.listdir(gtcDir) if gtc.endswith(".gtc")
    ]

    #TODO: detect which probes are available based on CSV input
    #TODO: use the names in CSV and then get a BCP mapping



    intensity_probes_X = [
        "STAINING_DNP_HIGH_1X", "STAINING_DNP_BGND_1X",
        "STAINING_BIOTIN_HIGH_1X", "STAINING_BIOTIN_BGND_1X", "EXTENSION_A_1X",
        "EXTENSION_T_1X", "EXTENSION_C_1X", "EXTENSION_G_1X",
        "TARGET_REMOVAL_1X", "HYBRIDIZATION_HYB_HIGH_1X",
        "HYBRIDIZATION_HYB_MEDIUM_1X", "HYBRIDIZATION_HYB_LOW_1X",
        "STRINGENCY_STRING_PM_1X", "STRINGENCY_STRING_MM_1X",
        "NSB_BGND_RED_1X", "NSB_BGNF_PURPLE_1X", "NSB_BGND_BLUE_1X",
        "NSB_BGND_GREEN_1X", "NON_POLYMORPHIC_NP_A_1X",
        "NON_POLYMORPHIC_NP_T_1X", "NON_POLYMORPHIC_NP_C_1X",
        "NON_POLYMORPHIC_NP_G_1X", "RESTORE_X"
    ]

    intensity_probes_Y = [
        "STAINING_DNP_HIGH_1Y", "STAINING_DNP_BGND_1Y",
        "STAINING_BIOTIN_HIGH_1Y", "STAINING_BIOTIN_BGND_1Y", "EXTENSION_A_1Y",
        "EXTENSION_T_1Y", "EXTENSION_C_1Y", "EXTENSION_G_1Y",
        "TARGET_REMOVAL_1Y", "HYBRIDIZATION_HYB_HIGH_1Y",
        "HYBRIDIZATION_HYB_MEDIUM_1Y", "HYBRIDIZATION_HYB_LOW_1Y",
        "STRINGENCY_STRING_PM_1Y", "STRINGENCY_STRING_MM_1Y",
        "NSB_BGND_RED_1Y", "NSB_BGNF_PURPLE_1Y", "NSB_BGND_BLUE_1Y",
        "NSB_BGND_GREEN_1Y", "NON_POLYMORPHIC_NP_A_1Y",
        "NON_POLYMORPHIC_NP_T_1Y", "NON_POLYMORPHIC_NP_C_1Y",
        "NON_POLYMORPHIC_NP_G_1Y", "RESTORE_Y"
    ]

    intensities_per_sample = {}

    for gtc in input_gtc_list:
        data = getGtcInfo(gtc=gtc)
        try:
            assert data[101] == manifest.manifest_name
            intensities_per_sample['{}-{}-{}'.format(data[11], data[12], data[10])] = {}
            intensityIndex = 0
            for i in range(0, len(data[500])):
                if i%4 == 0:
                    intensities_per_sample['{}-{}-{}'.format(data[11], data[12], data[10])][intensity_probes_X[intensityIndex]] = data[500][i]
                    intensities_per_sample['{}-{}-{}'.format(data[11], data[12], data[10])][intensity_probes_Y[intensityIndex]] = data[501][i]
                    intensityIndex += 1
                else:
                    continue
        except AssertionError:
            print("Sample {}, {} does not have a matching MEGA2 bpm. Skipping sample.".format(data[10], gtc))
            sys.stdout.flush()
            continue
            

    allIntesities = pandas.DataFrame(intensities_per_sample)
    allIntensities_transpose = allIntesities.T
    if os.path.exists(outDir) == False:
        os.mkdir(outDir)
    allIntensities_transpose.to_csv(os.path.join(outDir, 'intesities_per_sample.txt'), index = True, sep = '\t')
