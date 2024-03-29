import yaml
import os
import pandas as pd

def load_config(filepath):
	"""Return dictionary with settings"""
	with open(filepath) as file:
		config = yaml.full_load(file)
		return config

def load_data(data_dir, filename):
	"""Read csv-only file from data_dir/filename"""
	filepath = os.path.join(data_dir, filename)
	df = pd.read_csv(filepath, header=0)
	return df