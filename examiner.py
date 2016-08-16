import pickle
import pprint
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to examine", type=str)
with open(parser.parse_args().file, "r+b") as cp_file:
	data = pickle.load(cp_file)
	pprint.pprint(data)