# Fernet

Port of [Fernet-rb](https://github.com/fernet/fernet-rb) from ruby.

Fernet allows you to easily generate and verify **HMAC based authentication
tokens** for issuing API requests between remote servers. It also **encrypts**
the message so it can be used to transmit secure data over the wire.

## Installation

This library requires either the M2Crypto library or the Pycrypto lib. By default Pycrypto
is configured as a dependency since M2Crypto requires the presence of SWIG for compilation.
If M2Crypto (>=0.21.1) is installed it will be used, otherwise Pycrypto (>=2.6.1) will
be used.

pip install fernet  # TODO review, https://github.com/heroku/fernet-py/issues/1 suggests this is not possible

    pip install -e git+https://github.com/italian-licorice/fernet-py.git#egg=fernet-py

From local source checkout

    python -m pip install -r requirements.txt
    # pip install pycryptodome==3.7.2  # Needed for Py 2.7, as pycryptodome-3.23.0 missing 64-bit Windows binary (only has 32-bit)
    # TODO python -m pip install -e .

## Installation on Heroku

If you want to use M2Crypto you can try this buildpack which supports building the M2Cryto package:
  https://github.com/guybowden/heroku-buildpack-python-paybox

## Usage

Both client and server must share a secret.

You want to encode some data in the token as well, for example, an email
address can be used to verify it on the other end.


```python
import fernet
token = fernet.generate(secret, 'scottp@heroku.com')
```

On the server side, the receiver can use this token to verify whether it's
legit:

```python
verifier = fernet.verifier(secret, token)
if verifier.valid():
    operate_on(verifier.message) # the original, decrypted message
```


### Demo

```python
Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> import fernet
>>> secret = os.urandom(32) # pseudo-random 32 bytes, needs to be 32 bytes in length
>>> token = fernet.generate(secret, 'scottp@heroku.com')
>>> token
'gAAAAABp95bqUC-v-Nu3lYtV2ETSB5zaGu00KQmNckaxY90E5vDKqwg237h8mNvg5gUz-synkFYAfmWeRgo_Yyi-D9ZzpbJgn523m9PwKx3YYEQbrEFEvIw='
>>> verifier = fernet.verifier(secret, token)
>>> if verifier.valid():
...     print(verifier.message) # the original, decrypted message
...
scottp@heroku.com
```

### Global configuration

It's possible to configure fernet via the `Configuration` class. To do so, put
this in an initializer:

```python
# default values shown here
import fernet.Configuration
fernet.Configuration.enforce_ttl = true
fernet.Configuration.ttl         = 60
```

## Tests

Note tests require the Fernet spec and samples, in a git checkout issue:

    git submodule update --init

Run ```tests.sh``` to run the unit tests. I.e.:

    python -m unittest discover -s test

Note that one test checking for bad padding in a token will
fail when running with Pycrypto.

Current results/failure with pycryptodome:

```
(py2venv) C:\code\py\enc\fernet-py>python -m unittest discover -s test
.Resulting message: ?
F.....................
======================================================================
FAIL: test_invalid_tokens (acceptance.test_verify.TestVerifySpec)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\code\py\enc\fernet-py\test\acceptance\test_verify.py", line 47, in test_invalid_tokens
    print("Resulting message: %s" % verifier.message)
AssertionError: InvalidToken not raised

----------------------------------------------------------------------
Ran 23 tests in 0.045s

FAILED (failures=1)
```
