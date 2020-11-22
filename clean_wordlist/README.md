## clean_wordlist.sh
Runs a series of regexes against a wordlist to remove lines the following:

    - The following noisy characters `! ( , %`
    - More than 100 characters (these tend to be overly specific)
    - 4 or more consecutive digits (likely contains an id)
    - Where the last 3 or more characters are digits (likely an id)
    - 32 characters of just lowercase letters and numbers, likely to be an MD5 hash or similar
    - Number followed by 5 or more numbers and uppercase letters (almost always noisey id values)
    - More than 6 directories deep (these tend to be overly specific)
    - Containing UUIDs
    - Multiple numbers and letters mixed together (likley noise)
    - Ending in the following filetypes: `png, jpg, jpeg, gif, svg, bmp, ttf, avif, wav, mp4, aac, ajax, css, all`

### Usage:
Specify your wordlist and the script will output you a new version with the suffix "_cleaned"
```sh
./clean_wordlist.sh <wordlist>
```

To view the changes you can do:
```sh
diff original.txt_cleaned <(sort original.txt) | more
```
