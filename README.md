# Bitcoin Core Authenticated RPC Proxy

Purpose: share a synced full node among students learning bitcoind capabilities
and bitcoin-cli RPC usage, without requiring students to sync the node themselves.

## Install

1. clone repo
2. `pip install -r requirements.txt`

## Run

There is a bitcoin.conf included in this repo with RPC ports and password
which the local proxy will connect to. The proxy's external ports match
the default for Bitcoin Core networks, making it simpler to access remotely
with bitcoin-cli.

Networks supported: `main`, `testnet`, `signet`, `regtest`

- Start Bitcoin Core: `bitcoind -conf=/path/to/repo/rpc-auth-proxy/etc/bitcoin.conf`
  - Optionally add `-signet`, etc for different network
- Start proxy server: `python src/server.py main`
  - Optionally replace `main` with `signet`, etc.

## Adding Users

There is an included utility for adding users. Hashed passwords are saved by
default in a JSON file at `~/.rpc-auth-proxy-passwords.json`. Provide a password
with `-p` or the script will generate one for you:

```sh
~/rpc-auth-proxy$ python src/users.py newuser1
Password for newuser1: lYDk7mbTiN60
~/rpc-auth-proxy$ python src/users.py newuser2 -p hunter2
Password for newuser2: hunter2
```

## Remote Access

Users must have `bitcoin-cli` installed locally but they do not need to run their
own node. They provide their unique credentials with each RPC as well as the
IP address (or hostname) of the server.

Example:

```sh
$ bitcoin-cli -rpcconnect=34.172.95.104 -rpcuser=newuser1 -rpcpassword=lYDk7mbTiN60 getblockcount
817037
```

## Security Precautions

**This is NOT a secure system and should be used for educational purposes only.**

- SSL is not supported so `rpcpassword` is sent over the internet unencrypted
- Users are welcome to create wallets but keep in mind other users can access them
  - Wallets can be encrypted with a second wallet password, but even then security is poor
- Certain RPC methods are like `invalidateblock` and `stop` are disallowed to prevent users from disrupting the service
  - Users may still be able to disrupt service with "safe" commands like `scantxoutset`



