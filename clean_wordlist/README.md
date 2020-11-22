## clean_wordlist.sh
Runs a series of regexes against a wordlist to remove noisy lines such as those that contain UUID's, image filetypes, etc.

Specify your wordlist and the script will output you a new version with the suffix "_cleaned"

Usage:
```sh
./clean_wordlist.sh <wordlist>
```

To view the changes you can do:
```sh
diff original.txt_cleaned <(sort original.txt) | more
```
