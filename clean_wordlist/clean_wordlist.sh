#! /bin/bash
# To view the changes do:
# diff original.txt_cleaned <(sort original.txt) | more

regexes=(
    "[\!(,%]" # Ignore noisy characters
    ".{100,}" # Ignore lines with more than 100 characters (overly specific)
    "[0-9]{4,}" # Ignore lines with 4 or more consecutive digits (likely an id)
    "[0-9]{3,}$" # Ignore lines where the last 3 or more characters are digits (likely an id)
    "[a-z0-9]{32}" # Likely MD5 hash or similar
    "[0-9]+[A-Z0-9]{5,}" # Number followed by 5 or more numbers and uppercase letters (almost all noise)
    "\/.*\/.*\/.*\/.*\/.*\/.*\/" # Ignore lines more than 6 directories deep (overly specific)
    "\w{8}-\w{4}-\w{4}-\w{4}-\w{12}" # Ignore UUIDs
    "[0-9]+[a-zA-Z]+[0-9]+[a-zA-Z]+[0-9]+" # Ignore multiple numbers and letters mixed together (likley noise)
    "\.(png|jpg|jpeg|gif|svg|bmp|ttf|avif|wav|mp4|aac|ajax|css|all)$" # Ignore low value filetypes
    "^$" # Ignores blank lines
)

wordlist=$1
echo "[+] Cleaning ${wordlist}"
original_size=$(cat ${wordlist} | wc -l)

# Build command
cmd="cat ${wordlist}"
for regex in "${regexes[@]}"; do
    cmd="${cmd} | grep -vE '${regex}'"
done

# Add sort, uniq, and save to new file
cmd="${cmd} | sort | uniq > ${wordlist}_cleaned"

# Execute command
eval $cmd

# Calculate changes
new_size=$(cat ${wordlist}_cleaned | wc -l)
removed=$((original_size-new_size))

echo "[-] Removed ${removed} lines"
echo "[+] Wordlist is now ${new_size} lines"
echo "[+] Done"
