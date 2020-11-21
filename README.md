# SecUtils
Random utilities from my security projects that might be useful to others

## clean_wordlist.sh
Runs a series of regexes against a wordlist to remove noisy lines such as those that contain UUID's, image filetypes, etc.

Specify your wordlist and the script will output you a new version with the suffix "_cleaned"

Usage:
```sh
./clean_wordlist.sh <wordlist>
```


## ports.json
```python
import json
with open('ports.json', 'r') as portfile:
  ports = json.load(portfile)

ports['22']['tcp']['name']
'ssh'

ports['22']['tcp']['desc']
'The Secure Shell (SSH) Protocol'
```
