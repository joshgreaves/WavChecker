import argparse

try:
    from colorama import Fore, Style

    SUCCESS = Fore.GREEN + "Success" + Style.RESET_ALL
    FAILURE = Fore.RED + "Failure" + Style.RESET_ALL
    WARNING = Fore.YELLOW + "Warning" + Style.RESET_ALL
except ImportError:
    SUCCESS = ""
    FAILURE = ""
    WARNING = ""

CHECK1 = "Check 1,  ChunkID == RIFF:      "
CHECK2 = "Check 2,  ChunkSize:            "
CHECK3 = "Check 3,  Format == WAVE:       "
CHECK4 = "Check 4,  Subchunk ID == 'fmt ':"
CHECK5 = "Check 5,  Subchunk 1 size == 16:"
CHECK6 = "Check 6,  Audio Format:         "
CHECK7 = "Check 7,  Num Channels:         "
CHECK8 = "Check 8,  Sample Rate:          "
CHECK9 = "Check 9,  Byte Rate:            "
CHECK10 = "Check 10, Block Align:          "
CHECK11 = "Check 11, Bits per sample:      "
CHECK12 = "Check 12, Subchunk 2 ID:        "
CHECK13 = "Check 13, Subchunk 2 Size:      "

WAVE_FORMATS = {
    0x0001: "0x0001 WAVE_FORMAT_PCM",
    0x0003: "0x0003 WAVE_FORMAT_IEEE_FLOAT",
    0x0006: "0x0006 WAVE_FORMAT_ALAW",
    0x0007: "0x0007 WAVE_FORMAT_MULAW",
    0xFFFE: "0xFFFE WAVE_FORMAT_EXTENSIBLE"
}


def check(data):
    audio_format = int.from_bytes(data[20:22], byteorder='little')
    num_channels = int.from_bytes(data[22:24], byteorder='little')
    sample_rate = int.from_bytes(data[24:28], byteorder='little')
    byte_rate = int.from_bytes(data[28:32], byteorder='little')
    block_align = int.from_bytes(data[32:34], byteorder='little')
    bits_per_sample = int.from_bytes(data[34:36], byteorder='little')

    num_successes = 0
    num_checks = 13

    # 'RIFF'
    print(CHECK1, end="\t")
    if data[:4] == "RIFF".encode('ascii'):
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Chunk Size (Size of file - first 8 bytes)
    print(CHECK2, end="\t")
    chunk_size = int.from_bytes(data[4:8], byteorder='little')
    if chunk_size + 8 == len(data):
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE + " (Header val: %d, Actual size: %d)" % (chunk_size, len(data) - 8))

    # Format = 'WAVE'
    print(CHECK3, end="\t")
    if data[8:12] == "WAVE".encode('ascii'):
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Subchunk 1 ID = 'fmt '
    print(CHECK4, end="\t")
    if data[12:16] == "fmt ".encode('ascii'):
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Subchunk 1 Size
    print(CHECK5, end="\t")
    chunk_size = int.from_bytes(data[16:20], byteorder='little')
    if chunk_size == 16:
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Audio Format
    print(CHECK6, end="\t")
    if audio_format == 0x0001:
        print(SUCCESS)
        num_successes += 1
    else:
        print(WARNING + " (Only able to handle 0x0001 = WAVE_FORMAT_PCM, found " + hex(audio_format) + ")")

    # Num Channels
    print(CHECK7, end="\t")
    if num_channels == 1 or num_channels == 2:
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE + " (channels = " + str(num_channels) + ")")

    # Sample Rate
    print(CHECK8, end="\t")
    if sample_rate == 44100:
        print(SUCCESS)
        num_successes += 1
    else:
        print(WARNING + " (Unexpected Sample Rate = %.2fkHz)" % (sample_rate / 1000))

    # Byte Rate
    # == SampleRate * NumChannels * BitsPerSample/8
    print(CHECK9, end='\t')
    if byte_rate == sample_rate * num_channels * bits_per_sample / 8:
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE + " (Unkown Byte Rate = %d)" % byte_rate)

    # Block Align
    # == NumChannels * BitsPerSample/8
    print(CHECK10, end='\t')
    if block_align == num_channels * bits_per_sample / 8:
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Bits Per Sample
    print(CHECK11, end='\t')
    if bits_per_sample == 16:
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE + " (Bits per sample = %d)" % bits_per_sample)

    # Subchunk 2 ID
    print(CHECK12, end='\t')
    if data[36:40] == "data".encode('ascii'):
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Subchunk 2 Size
    print(CHECK13, end='\t')
    subchunk2_size = int.from_bytes(data[40:44], byteorder='little')
    if subchunk2_size == len(data) - 44:
        print(SUCCESS)
        num_successes += 1
    else:
        print(FAILURE)

    # Print results
    print("\nResult: ", end="")
    if num_successes == num_checks:
        print(Fore.GREEN, end="")
    else:
        print(Fore.RED, end="")
    print(("%d/%d" % (num_successes, num_checks)) + Style.RESET_ALL)
    print("wav format:     \t" +
          (WAVE_FORMATS[audio_format] if audio_format in WAVE_FORMATS else "0x{:04x} Unknown".format(audio_format)))
    print("num channels:   \t%d" % num_channels)
    print("sample rate:    \t%d" % sample_rate)
    print("byte rage:      \t%d" % byte_rate)
    print("block align:    \t%d" % block_align)
    print("bits per sample:\t%d" % bits_per_sample)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check an WAV file is correctly specified")
    parser.add_argument("file", type=str, help="wav file to check")
    args = parser.parse_args()
    with open(args.file, 'rb') as f:
        bin_data = f.read()
    check(bin_data)
