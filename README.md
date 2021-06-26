# crypto
cryptography tools

# [Shift Cipher](https://en.wikipedia.org/wiki/Caesar_cipher)
Each letter is replaced with a letter a fixed number of positions away in the alphabet.

## Usage
### Shifting forward
`python crypto.py -s {N} -q {input string}`

Each letter in the input string will be replaced with one *N* positions forward in the alphabet

`python crypto.py -s 5 -q "this is a test"`
will output `ymnx nx f yjxy`

### Shifting backward
`python crytpo.py -us {N} -q {input string}`
Each letter will be replaced with one *N* positions backward in the alphabet
`python crypto.py -us 5 -q "ymnx nx f yjxy"` will output `this is a test`

Note: There is no difference between using `-us` to shift backwards, or using `-s` with a negative number for N

`python crypto.py -us 5 -q "ymnx nx f yjxy"` and `python crypto.py -s -5 -q "ymnx nx f yjxy"` will return the same thing

# [Replacement / Substitution Cipher](https://en.wikipedia.org/wiki/Substitution_cipher)
Each letter is replaced with a letter defined in a replacement ciphertext

## Usage
`python crypto.py -sr {ciphertext} -r -q {input text}`

{ciphertext} must be exactly the same number of characters as the alphabet (26). If it is too short, '\*' will be appended to the end to pad the length. If it is too long, it will be truncated.

`-r` is simply a flag. The ciphertext must be provided with `-sr`

`python crypto.py -sr "zyxwvutsrqponmlkjihgfedcba" -r -q "this is a test"` will return `gsrh rh z gvhg`

This example replacement string will simply reverse the alphabet, also called an Atbash. "a" will be replaced with "z", "b" with "y", and so on.

Reversing the cipher is done by providing the same replacement string:
`python crypto.py -sr "zyxwvutsrqponmlkjihgfedcba" -r -q "gsrh rh z gvhg"` returns `this is a test`


# [Atbash Cipher](https://en.wikipedia.org/wiki/Atbash)
The Atbash Cipher is an implementation of the Substitution Cipher where the alphabet is reversed

## Usage
`python crypto.py -b -q "this is a test"`

`python crypto.py --atbash -q "this is a test"`

returns `gsrh rh z gvhg`

# Shift Series
An implementation of the Shift Cipher where the shift value changes. The user provides a series of numbers, which are converted from characters to integers. Each letter is shifted by the value. The series is repeated to the length of the input string.
