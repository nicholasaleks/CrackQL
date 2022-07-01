from optparse import OptionParser
from version import VERSION
from lib.verifications import verify_url, verify_query, verify_inputs

import sys


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


	print('[*] Validating url, query operation and inputs...')

	# Verify Target GraphQL Endpoint

	if not verify_url(options.url):
		sys.exit(1)

	# Verify GraphQL Operation (mock data)

	if not verify_query(options.query):
		sys.exit(1)

	# Verify Input CSV exists and is correct csv format

	if not verify_inputs(options.query, options.input_csv, options.delimiter):
		sys.exit(1)

	# **TODO** Measure CSV Input Size and Potentially Shared for better processing 

	print('[*] Generating & parsing batch queries...')

	# Count CSV lines

	# Execution loop = CSV_LINE_COUNT / BATCH_SIZE
















































































if __name__ == '__main__':
    main()