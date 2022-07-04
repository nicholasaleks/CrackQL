import graphql
import re
import csv
import textwrap

try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

def get_root_type(query_data):
	first = query_data.split('\n', 1)[0]
	return first

def get_operation(query_data):
	first = query_data.split('\n', 1)[1]
	last = first[:first.rfind('\n')]
	return textwrap.dedent(last)

def get_variable_type(query_data, variable):
	# Check for header variable names against query payload
	regex = r"\{\{.*" + re.escape(variable) + r".*\|(...)\}\}"
	try:
		return re.search(regex, query_data).group(1)
	except:
		return False

def get_csv_row_count(csv_input, delimiter):
	csv_line_count = -1
	with open(csv_input, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter)
		for row in reader:
			if any(row):
				csv_line_count+=1

	return csv_line_count

def get_variables(csv_input, delimiter):
	with open(csv_input, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter)
		list_of_column_names = []
		for row in reader:
			list_of_column_names = row
			break
	return list_of_column_names

def to_str(text):
    """Custom filter"""
    return '"{}"'.format(text)

def to_int(text):
    """Custom filter"""
    return int(text)


def to_float(text):
    """Custom filter"""
    return float(text)

