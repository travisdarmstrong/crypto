#!/usr/bin/python
import os, argparse, logging
import sys


alphabet = 'abcdefghijklmnopqrstuvwxyz'
ignore = """ ,.;#$!"'*-?\r\n"""
LOGFILENAME = "logfile.log"
replacement = alphabet
logger = None
look_for_words = ['me', 'my', 'mine', 'your', 'yours', 'our', 'ours', 'his', 'him', 'her', 'hers', 'the', 'and', 'what', 'for', 'that', 'they', 'them', 'how', 'why', 'when']

parser = argparse.ArgumentParser(description = 'Encode and Decode shift and replacement ciphers')
parser.add_argument('-s', '--shift', type=int, help='Shift cipher (every letter is shifted forward by this value)')
parser.add_argument('-us', '--unshift', type=int, help='Unshift cipher (every letter is shifted backward by this value)')
parser.add_argument('-find', '--find_shift', action='store_true', help='Find the shift cipher value (iterate through all shift values 1 to 26)')
parser.add_argument('-sr', '--set_replacement', help='Set Replacement cipher string (must be 26 characters. ignore values with *')
parser.add_argument('-r', '--replace', action='store_true', help='Encode text using replacement cipher. Set the replacement cipher with --sr')
parser.add_argument('-b', '--atbash', action='store_true', help='Replace using reverse alphabet (atbash)')
parser.add_argument('-ss', '--shift_series', help='Shift by a series (1245632, etc). repeats if the string is longer than the series')
parser.add_argument('-uss', '--unshift_series', help='Un-Shift a series (1245632, etc). repeats if the string is longer than the series')
parser.add_argument('-q', help='The input string')
parser.add_argument('-in', '--input', help='Input file to read (can use instead of --q. will read line-by-line through the file. ignore lines by starting with "#"')
parser.add_argument('-out', '--output', help='Output converted text to file')
args = parser.parse_args()

def log_init():
	global logger
	logger = logging.getLogger('cryptologger')
	fileformatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(message)s")
	streamformatter = logging.Formatter("%(levelname)s - %(message)s")
	streamhandler = logging.StreamHandler()
	filehandler = logging.FileHandler(LOGFILENAME)
	streamhandler.setFormatter(streamformatter)
	filehandler.setFormatter(fileformatter)
	streamhandler.setLevel(logging.WARNING)
	filehandler.setLevel(logging.INFO)
	logger.addHandler(filehandler)
	logger.addHandler(streamhandler)
	logger.setLevel(logging.INFO)

# Shift single letter
def get_shifted(c, offset):
	old_position = alphabet.find(c.lower())
	if old_position == -1:
		logger.error("can't shift {}".format(c))
		return c
	new_position_raw = old_position + offset
	new_position = new_position_raw % len(alphabet)
	shifted_letter = alphabet[new_position].upper() if c.isupper() else alphabet[new_position]
	return shifted_letter

# encode input string with shift cipher
def shift(q, offset):
	result = []
	for rawline in q:
		line = rawline.strip()
		if line.startswith('#'):
			logger.debug("comment found: {}".format(line))
			result.append(line)
			continue
		tmp = ''
		for c in line:
			if c in ignore:
				tmp += c
			else:
				tmp += get_shifted(c,offset)
		result.append(tmp)
	return result

# try all possible shifts to reverse engineer a caesar shift
def find_shift(q):
	result = []
	for offset in range(1,len(alphabet)):
		shifted_string = shift(q, -offset)
		if findwords(shifted_string):
			shifted_string.append('<---')
		result.append("({})\t{}".format(offset, shifted_string))
	return result

# look for common words in the shifted string
def findwords(q):
	result = False
	for line in q:
		words = line.split(' ')
		for word in words:
			if word in look_for_words:
				print("Word '{}' found".format(word))
				result = True
	return result


# decode using atbash cipher
def atbash(c):
	set_replacement(alphabet[::-1])
	return replace(c)

# decode using a variable shift series
# each letter is shifted by a different amount
# pattern repeats
def shift_series(q, series, decode=False):
	shift_val=turn_series_into_values(series, decode)
	idx = 0
	result = []
	for rawline in q:
		line = rawline.strip()
		if line.startswith('#'):
			logger.debug("comment found: {}".format(line))
			result.append(line)
			continue
		tmp = ''
		for c in line:
			if c in ignore:
				tmp += c
			else:
				logger.debug("shifting '{}' by '{}'".format(c, shift_val[idx]))
				tmp += get_shifted(c,shift_val[idx])
				idx = (idx + 1) % len(shift_val)
		result.append(tmp)
	return result

def turn_series_into_values(series, decode=False):
	logger.info("series entered as '{}' {}".format(series, "" if decode is False else "decoding"))

	shift_by = []
	invert = -1 if decode is True else 1
	logger.debug("invert = {}".format(invert))
	for s in series:
		shift_value = int(s) * invert
		shift_by.append(shift_value)
	logger.info("shift by (array) = '{}'".format(shift_by))
	return shift_by


# set the replacement cipher
def set_replacement(xr):
	# xr must be same length as alphabet (26 characters)
	# unknown letter replacements should be a *
	global replacement
	if len(xr) != len(alphabet):
		logger.error("replacement ciphertext '{}' is not the same length as the alphabet '{}'".format(xr, alphabet))
		if len(xr)<len(alphabet):
			xr = xr + '*'*(len(alphabet)-len(xr))
		else:
			xr = xr[:len(alphabet)]
	replacement = xr

# encode a character with replacement cipher
def get_replacement(c):
	position = alphabet.find(c.lower())
	replaced_letter = replacement[position].upper() if c.isupper() else replacement[position]
	logger.debug("{} ({}) replaced with {} ({})".format(c, position, replaced_letter, position))
	return replaced_letter

# encode the text in replacement cipher
def replace(q):
	result = []
	for rawline in q:
		line = rawline.strip()
		if line.startswith('#'):
			logger.debug("comment found: {}".format(line))
			result.append(line)
			continue
		tmp = ''
		for c in line:
			if c in ignore:
				tmp += c
			else:
				tmp += get_replacement(c)
		result.append(tmp)
	return result

# read the input file
def read_input(fname):
	result = ''
	if not os.path.exists(fname):
		msg = "path {} does not exist".format(fname)
		print msg 
		return msg
	with open(fname, 'r') as f:
		text = f.readlines()
		return text

# write results to output file
def write_output(fname, text):
	with open(fname, 'w') as f:
		f.write('\r\n'.join(text))

if __name__=='__main__':
	log_init()
	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
	q=""
	result = []
	if args.q is not None:
		logger.info("input text '{}'".format(args.q))
		q = [args.q]
	if args.input is not None:
		logger.info("reading file {}".format(args.input))
		q = read_input(args.input)
	if args.shift is not None:
		logger.info("shifting '{}' by {}".format(q, args.shift))
		result = shift(q, args.shift)
	if args.unshift is not None:
		logger.info("un-shifting '{}' by {}".format(q, args.unshift))
		result = shift(q, -args.unshift)
	if args.find_shift:
		logger.info("finding shift for '{}'".format(q))
		result = find_shift(q)
	if args.atbash:
		logger.info("using atbash (reverse alphabet) for '{}'".format(q))
		result = atbash(q)
	if args.shift_series is not None:
		logger.info("shifting '{}' by series '{}'".format(q, args.shift_series))
		result = shift_series(q, args.shift_series)
	if args.unshift_series is not None:
		logger.info("un-shifting '{}' by series '{}'".format(q, args.unshift_series))
		result = shift_series(q, args.unshift_series, True)
	if args.set_replacement is not None:
		set_replacement(args.set_replacement)
		result = "{}\r\n{}".format(alphabet, replacement)
	if args.replace:
		result = replace(q)
	if args.output is not None:
		logger.info("putting results in '{}'".format(args.output))
		write_output(args.output, result)
	else:
		for r in result:
			print r
	logger.info("Results:{}".format(result))


