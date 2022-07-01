from graphql import parse
import requests
import csv
import re

requests.packages.urllib3.disable_warnings()

def verify_url(url):
	'''
	Verifies that the GraphQL endpoint url is valid by running a simple test
	'''
	try:
		response = requests.post(
			url,
			verify=False,
			timeout=10
		)
		if response.status_code in [404, 405, 500, 501, 502, 503, 504]:
			print('Error: GraphQL Endpoint [{url}] does not appear valid. Response Code: {code}.'.format(
				url=url,
				code=response.status_code
				)
			)
			print('Please verify the GraphQL endpoint is correct')
			return False
		else:
			return True

	except Exception as e:
		print('Error: {e}'.format(e=e))
		return False


def verify_query(query):
	with open(query, 'r') as file:
		data = file.read()
		try:
			ast = parse(data)
		except Exception as e:
			print('Error: Invalid GraphQL Operation \n{data} \n{e}'.format(data=data, e=e))
			return False
	return True


def verify_inputs(query, csv_input, delimiter):
	with open(csv_input, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter)

		list_of_column_names = []

		for row in reader:
			list_of_column_names = row
			break

		with open(query, 'r') as file:
			data = file.read()

			for variable in list_of_column_names:
				variable = variable.replace(' ', '')

				# Check for header variable names against query payload
				regex = r'\$' + re.escape(variable) + r'\|(...)\$"'

				try:
					re.search(regex, data).group(1)
				except Exception as e:
					print('Error: CSV Header Payload "{variable}" not found in GraphQL operation \n{data} \n{e}'.format(
						variable=variable,
						data=data,
						e=e
						)
					)
					print('Please verify the GraphQL operation payloads match the csv header')
					return False

	return True