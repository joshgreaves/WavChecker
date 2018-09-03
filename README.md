# Wav Tester
Used to check the header information in a wav file.

## Usage
Clone repository, then simply run:
`python main.py myfile.wav`, replacing `myfile.wav` with the name of your wav file.

For colorful output, install colorama `pip install colorama`

## Example
Input:
```
python main.py test.wav
```
Output:
```
Check 1,  ChunkID == RIFF:      	Success
Check 2,  ChunkSize:            	Success
Check 3,  Format == WAVE:       	Success
Check 4,  Subchunk ID == 'fmt ':	Success
Check 5,  Subchunk 1 size == 16:	Success
Check 6,  Audio Format:         	Success
Check 7,  Num Channels:         	Success
Check 8,  Sample Rate:          	Success
Check 9,  Byte Rate:            	Success
Check 10, Block Align:          	Success
Check 11, Bits per sample:      	Success
Check 12, Subchunk 2 ID:        	Success
Check 13, Subchunk 2 Size:      	Success

Result: 13/13
wav format:     	0x0001 WAVE_FORMAT_PCM
num channels:   	1
sample rate:    	44100
byte rage:      	88200
block align:    	2
bits per sample:	16
```
