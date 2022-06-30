CrackQL
=======
CrackQL is a GraphQL password brute-force and fuzzing utility.

<h1 align="center">
	<img src="https://github.com/nicholasaleks/CrackQL/blob/master/static/CrackQL-Banner.png?raw=true" alt="CrackQL"/>
	<br>
</h1>

CrackQL is a versatile GraphQL penetration testing tool that exploits poor rate-limit and cost analysis controls to brute-force credentials and fuzz operations.
It works by automatically batching a GraphQL query or mutation operation which executes dynamic inputs from a supplied dictionary into a single request.
CrackQL evades traditional API rate and ATO monitoring controls since it uses query batching to stuffed the entire set of credentials into a single HTTP request.


## Attack Use Cases

CrackQL is perfect against GraphQL deployments that leverage in-band GraphQL authentication operations (such as the [GraphQL Authentication Module](https://www.graphql-modules.com/docs#authentication-module))

### Password Spraying Brute-forcing

### Two-factor Authentication OTP Bypass

### User Account Enumeration

### Field Stuffing Information Disclosure

### General Fuzzing


## Installation

### Requirements
- Python3
- Requests
- GraphQL

### Clone Repository
`git clone git@github.com:nicholasaleks/CrackQL.git`


### Get Dependencies
`pip install -r requirements.txt`

### Run CrackQL
`python3 CrackQL.py -h`

```
Usage: CrackQL.py -t http://example.com/graphql -q query.graphql -i users_passwords.csv -b 10 -a alias

Options:
  -h, --help            show this help message and exit
  -t URL, --target=URL  target url with a path to the GraphQL endpoint
  -b BATCH_SIZE, --batch-size=BATCH_SIZE
                        Number of batch operations per GraphQL request
  -o OUTPUT_JSON, --output-json=OUTPUT_JSON
                        Output results to a file (JSON)
  -i INPUTS_CSV, --input=INPUTS_CSV
                        Path to a csv list of arguments (i.e. usernames, emails, ids, passwords, otp_tokens, etc.)
  -v, --version         Print out the current version and exit.
```
