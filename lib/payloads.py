import config
import requests
import sys

from lib.common import print_output
from lib.parser import indent

def generate_payload(batch_operations, root_type):
	operation_body = indent(batch_operations, 4)
	return root_type  + operation_body + '\n}'

def send_payload(url, payload, batches_sent, total_requests_to_send, verbose=False):
	print_output('[+] Sending batch {batches_sent} of {total_requests_to_send} to {url}...'.format(
		batches_sent=batches_sent,
		total_requests_to_send=total_requests_to_send,
		url=url
	), verbose)

	try:
		response = requests.post(
			url,
			headers=config.HEADERS,
			cookies=config.COOKIES,
			verify=False,
			timeout=60,
			json={'query':payload}
		)
		return response.json()

	except Exception as e:
		print('Error: {e}'.format(e=e))
		sys.exit(1)