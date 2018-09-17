
# Bid on '.eth' ENS names with Python

[![Join the chat at https://gitter.im/ens-py/Lobby](https://badges.gitter.im/ens-py/Lobby.svg)](https://gitter.im/ens-py/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Access the Ethereum Name Service Auction using this python library.
Note: **this is a work in progress**

Using this library is not a way to skip learning how ENS works. If you are registering a name, a
small misunderstanding can cause you to lose **all** your deposit.
Go [read about ENS](http://docs.ens.domains/en/latest/userguide.html) first.
Your funds are your responsibility.

## Beta-quality warning

This is a preview for developers, and an invitation for contributions. Please do not use this in
production until this warning is removed, especially when putting funds at risk. Examples of funds
being at risk include: sending ether/tokens to resolved addresses and participating in name
auctions.

If you supply the a domain with type `bytes`, it will be assumed to be UTF-8 encoded, like in
[Ethereum contracts](https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI#argument-encoding).

## Setup

```
pip install ensauction
```

Any issues? See [Setup details](#setup-details)

## Usage

All examples in Python 3

### Auctions for names ending in .eth

#### Get auction status

Example with domain 'payment.eth':

```py
from ensauction.auto import ethnames
from ensauction.registrar import Status

status = ethnames.status('payment.eth')
```

If you get an error here, like:
> UnhandledRequest: No providers responded to the RPC request:\
 method:eth_getBlockByNumber\
 params:['latest', False]
 
Then you are not connected to your node.
See below [how to manually connect to your node](#optionally-a-custom-web3-provider).

Otherwise, continue...

```py
# if you forget to strip out .eth, ens.py will do it for you
assert ethnames.status('payment') == status

# these are the possible statuses

assert status in (
  Status.Open,
  Status.Auctioning,
  Status.Owned,
  Status.Forbidden,
  Status.Revealing,
  Status.NotYetAvailable
  )


# if you get the integer status from another source, you can compare it directly

assert Status.Owned == 2
```

#### Start auctions

```py
# start one auction (which tips people off that you're interested)

ethnames.start('you_saw_him_repressin_me_didnt_ya')


# start many auctions (which provides a bit of cover)

ethnames.start(['exchange', 'tickets', 'payment', 'trading', 'registry'])
```

#### Bid on auction

Bid on a 'trading.eth' with 5211 ETH, and secret "I promise I will not forget my secret":

```py
from web3.auto import w3

ethnames.bid(
      'trading',
      Web3.toWei('5211', 'ether'),
      "I promise I will not forget my secret",
      transact={'from': w3.eth.accounts[0]}
      )
```
(if you want to "mask" your bid, set a higher value in the transact dict)

#### Reveal your bid

You must **always** reveal your bid, whether you won or lost.
Otherwise you will lose the full deposit.

Example of revealing your bid on 'registry.eth' with 0.01 ETH, and secret
"For real, though: losing your secret means losing ether":

```py
ethnames.reveal(
      'registry',
      Web3.toWei('0.01', 'ether'),
      "For real, though: losing your secret means losing ether",
      transact={'from': w3.eth.accounts[0]}
      )
```

#### Claim the name you won

aka "Finalize" auction, which makes you the owner in ENS.

```py
ethnames.finalize('gambling')
```

#### Get detailed information on an auction

Find out the owner of the auction Deed --
see [docs on the difference](http://docs.ens.domains/en/latest/userguide.html#managing-ownership)
between owning the name and the deed

```py
deed = ethnames.deed('ethfinex')

assert deed.owner() == '0x9A02ed4Ca9AD55b75fF9A05DeBb36D5eb382E184'
```

When was the auction completed? (a timezone-aware datetime object)

```py
close_datetime = ethnames.close_at('ethfinex')

assert str(close_datetime) == '2017-06-05 08:10:03+00:00'
```

How much is held on deposit?

```py
from decimal import Decimal
from web3 import Web3

deposit = ethnames.deposit('ethfinex')

assert Web3.fromWei(deposit, 'ether') == Decimal('0.01')
```

What was the highest bid?

```py
top_bid = ethnames.top_bid('ethfinex')

assert Web3.fromWei(top_bid, 'ether') == Decimal('201709.02')
```

## Setup details

### If Python 2 is your default, or you're not sure

In your shell
```
if pip --version | grep "python 2"; then
  python3 -m venv ~/.py3venv
  source ~/.py3venv/bin/activate
fi
```

### Now, with Python 3

In your shell: `pip install ensauction`

*ensauction.py* requires an up-to-date Ethereum blockchain, preferably local.
If your setup isn't working,
try running `geth --fast` until it's fully-synced. I highly recommend using the default IPC
communication method, for speed and security.

### "No matching distribution found for ensauction"

If you are seeing something like:
```
Collecting ensauction
  Could not find a version that satisfies the requirement ensauction (from versions: )
No matching distribution found for ensauction
```

It is most likely that you are in Python 2.
Retry the first Setup section, to make sure you're in Python 3

### Use a custom web3 provider

In Python:

```
from ensauction.registrar import Registrar
from ens import ENS
from web3 import IPCProvider 

ns = ENS(IPCProvider('/your/custom/ipc/path'))
reg = Registrar(ns)
```



## Developer Setup

```
git clone git@github.com:carver/ensauction.py.git
cd ensauction.py/

python3 -m venv venv
. venv/bin/activate

pip install -e .
pip install -r requirements-dev.txt
```

### Testing Setup

Re-run flake on file changes:

```
$ when-changed -s -1 -r ensauction/ tests/ -c "clear; echo; echo \"running flake - $(date)\"; warn()
{
notify-send -t 5000 'Flake8 failure ⚠⚠⚠⚠⚠' 'flake8 on ensauction.py failed'
}
if ! git diff | flake8 --diff | grep "\.py"; then if ! flake8 ensauction/ tests/; then warn; fi else warn; fi; echo done"
```

### Why does ensauction.py require python 3?

*Short version*

It turns out that the distinction between `str` and `bytes` is important. If
you want to write code for the future (Ethereum), don't use a language from the past.

*Long version*

Interacting with the EVM requires clarity on the bits you're using. For example, a sha3 hash expects
to receive a series of bytes to process. Calculating the sha3 hash of a string is (or should be)
a Type Error; the hash algorithm doesn't know what to do with
a series of characters, aka Unicode code points. As the caller, you need to know which thing you're
calculating the hash of:
1. a series of bytes: `b'[ c$o!\x91\xf1\x8f&u\xce\xdb\x8b(\x10.\x95tX'`
2. the bytes represented by a string in hex format: `'0x5b2063246f2191f18f2675cedb8b28102e957458'`
3. the bytes generated by encoding a string using utf-8: **Oops, the bytes from #1 cannot be read using utf-8!**
4. the bytes generated by encoding a string using utf-16: `'⁛④Ⅿ\uf191⚏칵诛ဨ键塴'`

Python 3 doesn't let you ignore a lot of these details. That's good, because precision in dealing
with the EVM is critical.

If you are resistant -- I get it, I've been there. It is not intuitive for most people. But it's
seriously worth it to [learn about
encoding](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/) 
if you're going to develop on top of Ethereum. Your ETH depends on it!

### Release setup

For Debian-like systems:
```
apt install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
