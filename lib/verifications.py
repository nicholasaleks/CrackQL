import requests

requests.packages.urllib3.disable_warnings()

def verify_url(url):

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

	except Exception as e:
		print('Error: {e}'.format(e=e))
		return False

