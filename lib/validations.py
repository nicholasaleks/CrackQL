from graphql import parse
from lib.parser import get_variable_type
import requests
import csv

requests.packages.urllib3.disable_warnings()

def verify_url(url):
	'''
	Verifies that the GraphQL endpoint url is valid by running a simple test
	'''
	query = '''
      query {
        __typename
      }
    '''

	try:
		response = requests.post(
			url,
			verify=False,
			timeout=10,
			json={'query': query}
		).json()

		if response.get('data'):
			if response.get('data', {}).get('__typename', '') in ('Query', 'QueryRoot', 'query_root'):
				return True
			elif response.get('errors') and (any('locations' in i for i in response['errors']) or (any('extensions' in i for i in response))):
				return True
			elif response.get('data'):
				return True

	except Exception as e:
		print('Error: {e}'.format(e=e))
		return False


def verify_query(query, query_format='File'):
	'''
	Checks whether or not a GraphQL query is formatted correctly
	'''
	if query_format == 'File':
		with open(query, 'r') as file:
			data = file.read()
			try:
				ast = parse(data)
			except Exception as e:
				print('Error: Invalid GraphQL Operation \n{data} \n{e}'.format(data=data, e=e))
				return False
	elif query_format == 'String':
		try:
			ast = parse(query)
		except Exception as e:
			print('Error: Invalid GraphQL Operation \n{data} \n{e}'.format(data=data, e=e))
			return False
	return True


def verify_inputs(query, csv_input, delimiter):
	'''
	Validates CSV inputs to ensure they match payload jinja variables
	'''
	with open(csv_input, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter, skipinitialspace=True)
		list_of_column_names = []
		for row in reader:
			list_of_column_names = row
			break

		with open(query, 'r') as file:
			query_data = file.read()

			for variable in list_of_column_names:
				
				if not get_variable_type(query_data, variable):
					print('Error: CSV Header Payload "{variable}" not found in GraphQL operation \n{query_data}'.format(
						variable=variable,
						query_data=query_data,
						)
					)
					print('Please verify the GraphQL operation payloads match the csv header')
					return False

	return True