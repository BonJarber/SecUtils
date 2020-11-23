#! /bin/bash
# To view the changes do:
# diff original.txt_cleaned <(sort original.txt) | more

regexes=(
    "[^0-9A-Za-z=/_.-]" # Ignore noisy characters
    ".{100}" # Ignore lines with more than 100 characters (overly specific)
    "[0,1,3-9][1-9][0-9]{2}" # Ignore lines with 4 or more consecutive digits (likely an id) but keep recent years
    "[0,1,3-9][1-9][0-9]$" # Ignore lines where the last 3 or more characters are digits (likely an id)
    "[A-Fa-f0-9]{32}" # Likely MD5 hash or similar
    "[0-9]+[A-Z0-9]{5,}" # Number followed by 5 or more numbers and uppercase letters (almost all noise)
    "\/.*\/.*\/.*\/.*\/.*\/.*\/" # Ignore lines more than 6 directories deep (overly specific)
    "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}" # Ignore UUIDs
    "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{8}" # Ignore GUIDs
    "[0-9]+[a-zA-Z]+[0-9]+[a-zA-Z]+[0-9]+" # Ignore multiple numbers and letters mixed together (likley noise)
    "\.([ot]tf|aac|ajax|all|apk|avif?|axd|bmp|cs[sv]|docx?|eot|exe|flv|gifv?|i[cs]o|jpe?g|lock|m4[av]|map|mp[34]|msi|og[gmv]|pdf|png|svg|swf|ttf|wav|webm|woff2?)($|\?)" # Ignore low value filetypes
)

[[ $1 == "" ]] && exit

wordlist=$1

runiq="sort -u"
which runiq >/dev/null && runiq="$(which runiq) -"

echo "[+] Cleaning ${wordlist}"
original_size=$(wc -l < ${wordlist})

# Build command
tr ' ' '\n' <<< ${regexes[@]} | grep -vEf - "${wordlist}" | $runiq >${wordlist}_cleaned

# Calculate changes
new_size=$(wc -l < ${wordlist}_cleaned)
removed=$((original_size-new_size))

echo "[-] Removed ${removed} lines"
echo "[+] Wordlist is now ${new_size} lines"
echo "[+] Done"
