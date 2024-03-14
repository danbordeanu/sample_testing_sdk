## Synopsis

This will provide a clear and reproductible way of testing the HPC-API.

## Motivation

- HPC-API endpoints tested automatically using jenkins.
- predictable way to report and reproduce issues.
- execute performance testing against endpoints.

## Installation

### Dependencies

The HPC-API-UAT framework depends on python libraries:

- requests (wrapper for rest-api requests)
- paramiko (wrapper for ssh used to executed remote commands)
- multi-mechanize (multi threaded performance test and html/xml generator)

```bash
pip install requests
pip install requests-requests-toolbelt
pip install requests-oauthlib
pip install paramiko
pip install multi-mechanize

```

Or, use  **--proxy** variable for pip.


### Execution

In ordet to run all tests suite the **run_tests.py** file must be called:

```bash
python2 run_tests.py
```

The run_tests.py file is just a wrapper for the tests cases located in tests directory

```python
POST_login = LoginTest(parser)
POST_logout = LogoutTest(parser, POST_login.getTicket())
```

The results of the tests will be published in html format in **html** directory and the log
execution files will be located in **log** directory.

## Framework capabilities

- rest-api handling.
- html reports.
- console reports
- remote code execution.
- configuration parser.
- sending emails with results.
- performance testing using multi-mechanize custom made lib.

## How to create a UAT test

**!!!NB!!!** all tests are located in **tests** directory and are called by **run_tests.py** wrapper.

Every test has 3 main functions:

- init variables (endpoint, test name, username/password, test results)

```python
class LoginTest:
    def __init__(self, parser):
        self.parser = parser
        self.suite_name = 'Login'
        self.test_name = []
        self.result = []
        self.url = parser.config_params('hpcapi')['url']
        self.user_a = parser.config_params('users')['user_c']
        self.password_a = base64.b64decode(parser.config_params('users')['password_c'])

```

- login, for every test we need to login (the login function will return the ticket)

```python
do_login = login.login(self.url + '/' + 'login', self.user_a, self.password_a)
```

- do the actual test, for example evaluate the presence of .com string in the ticket

```python
assert type(ticket) is str, 'ticket is not str: {0}'.format(ticket)
```

- appending the results

```python
self.result.append(self.success)
self.result.append(self.failure)

```

- generating the html results

```python
report.report_testcase(self.suite_name, zip(self.test_name, self.result))
report.report_testcasehtml(self.suite_name, zip(self.test_name, self.result))
```

## Running performance tests with multi-mechanize

Multi-mechanize is just a wrapper for python requests library that will create threads and generate nice html reports.

### Tests

Each test is located in test_login_load  and (atm) is just executing basic REST-API requests.

```python
    def run(self):
        ticket = 'bla-bla-123'
        dirname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        r = requests.post(self.url + '/file/create' + '?ticket=' + ticket,
                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                   'Accept': 'application/json'}, data={'name': dirname})
        r.raw.read()
```

This test will create dirs using the HPC-API. 

### Execute a performance test

In ordet to start the test, multi-mechanize must be installed. See dependencies list.

```bash
multimech-run test_login_load
```

Don't forget to modify the config.cfg file (there params for howe many threads and for how long the script will be running)

```bash
[global]
run_time = 60
rampup = 10
results_ts_interval = 10
progress_bar = on
xml_report = on
console_logging = on

[user_group-1]
threads = 4
script = login.py
```

## Feature and TODO's of the framework

- extend the tests to cover all HPC-API endpoints.
- send alerts and notifications using Sentry grid.
- performance testing to be improved and to use the test cases.
