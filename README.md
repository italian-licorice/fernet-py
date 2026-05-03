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

TODO doc submodule checkout

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
verifer = fernet.verifier(secret, token)
if verifier.valid():
    operate_on(verifier.message) # the original, decrypted message
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

Run ```tests.sh``` to run the unit tests. I.e.:

    python -m unittest discover -s test

Note that one test checking for bad padding in a token will
fail when running with Pycrypto.
