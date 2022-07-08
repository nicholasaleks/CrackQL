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
	'''
	Extracts the root operation type from the input query
	'''
	first = query_data.split('\n', 1)[0]
	return first

def get_operation(query_data):
	first = query_data.split('\n', 1)[1]
	last = first[:first.rfind('\n')]
	return textwrap.dedent(last)

def get_variable_type(query_data, variable):
	'''
	Identifies if jinja variables from CSV header exist in query
	'''
	regex = r"\{\{.*" + re.escape(variable) + r".*\|(str|int|float)\}\}"
	try:
		return re.search(regex, query_data).group(1)
	except:
		return False

def get_csv_row_count(csv_input, delimiter):
	'''
	Return to total number of rows in the CSV (minus header)
	'''
	csv_line_count = -1
	with open(csv_input, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter)
		for row in reader:
			if any(row):
				csv_line_count+=1

	return csv_line_count

def get_variables(csv_input, delimiter):
	'''
	Return the variable names from the header of CSV
	'''
	with open(csv_input, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter)
		list_of_column_names = []
		for row in reader:
			list_of_column_names = row
			break
	return list_of_column_names

def parse_data_response(response, raw_data, data_results, inputs, verbose=False):
	'''
	Packages the responses from the batched queries and returns both raw and formated data
	'''

	data_result = {}
	try:
		if 'data' in response and isinstance(response['data'], dict):
			raw_data.append(response['data'])
			for r in response['data'].items():
				name, data = r
				data_result[name] = {}
				data_result[name]['inputs'] = inputs
				data_result[name]['data'] = data
				data_results.append(data_result)
				data_result = {}
	except Exception as e:
		print(e)

	return (raw_data, data_results)

def parse_error_response(response, raw_errors, error_results, inputs, verbose=False):
	'''
	Packages the responses from the batched queries and returns both raw and formated errors
	'''
	error_result = {}
	try:
		if 'errors' in response and isinstance(response['errors'], list):
			for r in response['errors']:
				raw_errors.append(r)
				message = r.get('message')

				try:
					alias = r.get('path')[0]
				except:
					alias = 'undefined'


				error_result[alias] = {}
				error_result[alias]['inputs'] = inputs
				error_result[alias]['error'] = r['message']
				error_results.append(error_result)
				error_result = {}

	except Exception as e:
		print(e)

	return (raw_errors, error_results)



































