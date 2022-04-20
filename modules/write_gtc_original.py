from IlluminaBeadArrayFiles import GenotypeCalls, BeadArrayUtility
import struct
from io import BytesIO
import logging

logger = logging.getLogger('write_gtc')
logger.debug('In module write_gtc.py')

def handle_int(value):
    return struct.pack("<i", value)

def handle_short(value):
    return struct.pack("<H", value)

def handle_char(value):
    return struct.pack("c", value)

def handle_byte(value):
    #print(value)
    return struct.pack("B", value)

def handle_float(value):
    return struct.pack("<f", value)

def handle_gc50(value):
    return struct.pack("<fiii", value[0], value[1], value[2], value[3])

def handle_percentiles(value):
    return struct.pack("<HHH", value[0], value[1], value[2])

def handle_string(value):
    assert len(value) <= 127
    return struct.pack("B", len(value)) + value

def handle_basecalls(value):
    return value

def handle_scanner_data(value):
    return handle_string(value.name) + handle_int(value.pmt_green) + handle_int(value.pmt_red) + handle_string(value.version) + handle_string(value.user)

def handle_normalization_transform(value):
    return struct.pack("<iffffff", value.version, value.offset_x, value.offset_y, value.scale_x, value.scale_y, value.shear, value.theta)


toc2handler = {}
toc2handler[GenotypeCalls._GenotypeCalls__ID_NUM_SNPS] = handle_int
toc2handler[GenotypeCalls._GenotypeCalls__ID_PLOIDY] = handle_int
toc2handler[GenotypeCalls._GenotypeCalls__ID_PLOIDY_TYPE] = handle_int
toc2handler[GenotypeCalls._GenotypeCalls__ID_SAMPLE_NAME] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_SAMPLE_PLATE] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_SAMPLE_WELL] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_CLUSTER_FILE] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_SNP_MANIFEST] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_IMAGING_DATE] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_AUTOCALL_DATE] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_AUTOCALL_VERSION] = handle_string
toc2handler[GenotypeCalls._GenotypeCalls__ID_NORMALIZATION_TRANSFORMS] = handle_normalization_transform
toc2handler[GenotypeCalls._GenotypeCalls__ID_CONTROLS_X] = handle_short
toc2handler[GenotypeCalls._GenotypeCalls__ID_CONTROLS_Y] = handle_short
toc2handler[GenotypeCalls._GenotypeCalls__ID_RAW_X] = handle_short
toc2handler[GenotypeCalls._GenotypeCalls__ID_RAW_Y] = handle_short
toc2handler[GenotypeCalls._GenotypeCalls__ID_GENOTYPES] = handle_byte
toc2handler[GenotypeCalls._GenotypeCalls__ID_BASE_CALLS] = handle_basecalls
toc2handler[GenotypeCalls._GenotypeCalls__ID_GENOTYPE_SCORES] = handle_float
toc2handler[GenotypeCalls._GenotypeCalls__ID_SCANNER_DATA] = handle_scanner_data
toc2handler[GenotypeCalls._GenotypeCalls__ID_CALL_RATE] = handle_float
toc2handler[GenotypeCalls._GenotypeCalls__ID_GENDER] = handle_char
toc2handler[GenotypeCalls._GenotypeCalls__ID_LOGR_DEV] = handle_float
toc2handler[GenotypeCalls._GenotypeCalls__ID_GC10] = handle_float
toc2handler[GenotypeCalls._GenotypeCalls__ID_GC50] = handle_gc50
toc2handler[GenotypeCalls._GenotypeCalls__ID_B_ALLELE_FREQS] = handle_float
toc2handler[GenotypeCalls._GenotypeCalls__ID_LOGR_RATIOS] = handle_float
toc2handler[GenotypeCalls._GenotypeCalls__ID_PERCENTILES_X] = handle_percentiles
toc2handler[GenotypeCalls._GenotypeCalls__ID_PERCENTILES_Y] = handle_percentiles
toc2handler[GenotypeCalls._GenotypeCalls__ID_SLIDE_IDENTIFIER] = handle_string

list_types = []
list_types.append(GenotypeCalls._GenotypeCalls__ID_NORMALIZATION_TRANSFORMS)
list_types.append(GenotypeCalls._GenotypeCalls__ID_CONTROLS_X)
list_types.append(GenotypeCalls._GenotypeCalls__ID_CONTROLS_Y)
list_types.append(GenotypeCalls._GenotypeCalls__ID_RAW_X)
list_types.append(GenotypeCalls._GenotypeCalls__ID_RAW_Y)
list_types.append(GenotypeCalls._GenotypeCalls__ID_GENOTYPES)
list_types.append(GenotypeCalls._GenotypeCalls__ID_BASE_CALLS)
list_types.append(GenotypeCalls._GenotypeCalls__ID_GENOTYPE_SCORES)
list_types.append(GenotypeCalls._GenotypeCalls__ID_B_ALLELE_FREQS)
list_types.append(GenotypeCalls._GenotypeCalls__ID_LOGR_RATIOS)


def write_gtc(data, handle):
    logger.debug('In sub-method of write_gtc.py, write_gtc(data, handle)')
    handle.write(b'g')
    handle.write(b't')
    handle.write(b'c')
    handle.write(handle_byte(5))

    num_entries = len(data)
    handle.write(handle_int(num_entries))
    offset = 8 + num_entries * 6;


    buffer = BytesIO()
    for toc_id in data:
        # write the toc ID
        handle.write(handle_short(toc_id))

        # write the data into the buffer
        if toc_id in list_types:
            handle.write(handle_int(offset + buffer.tell()))
            buffer.write(handle_int(len(data[toc_id])))
            for element in data[toc_id]:
                buffer.write(toc2handler[toc_id](element))
        else:
            if toc2handler[toc_id] == handle_int:
                handle.write(handle_int(data[toc_id]))
            else:
                handle.write(handle_int(offset + buffer.tell()))
                buffer.write(toc2handler[toc_id](data[toc_id]))
    buffer.seek(0)
    handle.write(buffer.read1(-1))