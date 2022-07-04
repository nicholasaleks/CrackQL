CrackQL
=======
CrackQL is a GraphQL password brute-force and fuzzing utility.

<h1 align="center">
	<img src="https://github.com/nicholasaleks/CrackQL/blob/master/static/CrackQL-Banner.png?raw=true" alt="CrackQL"/>
	<br>
</h1>

CrackQL is a versatile GraphQL penetration testing tool that exploits poor rate-limit and cost analysis controls to brute-force credentials and fuzz operations.

## How it works?

CrackQL works by automatically batching a single GraphQL query or mutation into several alias operations. It determines the number of aliases to use based on the CSV input variables. After programmatically generating the batched GraphQL document, CrackQL then batches and sends the payload(s) to the target GraphQL API and parses the results and errors.

## Defense Evasion

Unlike [Burp Intruder](https://portswigger.net/burp/documentation/desktop/tools/intruder) which sends a request for each unique payload, CrackQL evades traditional API HTTP rate-limit monitoring defenses by using multiple alias queries to stuff large sets of credentials into single HTTP requests. To bypass query cost analysis defenses, CrackQL can be optimized into using a series of smaller batched operations (`-b`) as well as a time delay (`-D`).


## Attack Use Cases

CrackQL can be used for a wide range of GraphQL attacks since it programmatically generates payloads based on a list of dynamic inputs.

### Password Spraying Brute-forcing

CrackQL is perfect against GraphQL deployments that leverage in-band GraphQL authentication operations (such as the [GraphQL Authentication Module](https://www.graphql-modules.com/docs#authentication-module)). The below password spraying example works against [DVGA](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application) with the `sample-inputs/users-and-passwords.csv` dictionary.

*sample-queries/login.graphql*
```
mutation {
  login(username: {{username|str}}, password: {{password|str}}) {
    accessToken
  }
}
```

### Two-factor Authentication OTP Bypass

It is possible to use CrackQL to bypass two-factor authentication by sending all OTP (One Time Password) tokens

*sample-queries/otp-bypass.graphql*
```
mutation {
  twoFactor(otp: {{otp|int}}) {
    accessToken
  }
}
```

### User Account Enumeration

CrackQL can also be used for enumeration attacks to discover valid user ids, usernames and email addresses

*sample-queries/enumeration.graphql*
```
query {
  signup(email: {{email|str}}, password:{{password|str}}) {
    user {
      email
    }
  }
}
```

### Insecure Direct Object Reference

CrackQL could be used to iterate over a large number of potential unique identifiers in order to leak object information

*sample-queries/idor.graphql*
```
query {
  profile(uuid: {{uuid|int}}) {
    name
    email
    picture
  }
}
```

### General Fuzzing

CrackQL can be used for general input fuzzing operations, such as sending potential SQLi and XSS payloads.


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
Usage: python3 CrackQL.py -t http://example.com/graphql -q login.graphql -i users-and-passwords.csv

Options:
  -h, --help            Show this help message and exit
  -t URL, --target=URL  Target url with a path to the GraphQL endpoint
  -q QUERY, --query=QUERY  Input query or mutation operation with variable payload markers
  -i INPUTS_CSV, --input=INPUTS_CSV
                        Path to a csv list of arguments (i.e. usernames, emails, ids, passwords, otp_tokens, etc.)
  -d DELIMITER, --delimiter=DELIMITER  CSV input delimiter (default: ",")
  -o OUTPUT_JSON, --output-json=OUTPUT_JSON
                        Output results to a JSON file (default: results/[url]-[timestamp].json)
  -b BATCH_SIZE, --batch-size=BATCH_SIZE
                        Number of batch operations per GraphQL document request (default: 100)
  -a ALIAS_NAME, --alias-name=ALIAS_NAME
  -D DELAY, --delay=DELAY  Time delay in seconds between batch requests (default: 0)
  -v, --version         Print out the current version and exit.
```

## Maintainers
* [Nick Aleks](https://github.com/nicholasaleks)
* [Dolev Farhi](https://github.com/dolevf)
