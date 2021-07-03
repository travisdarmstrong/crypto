# crypto
cryptography tools

- Shift Cipher
- Substitution Cipher
- Atbash Cipher
- Series Shift
- Reading from / Writing to File
- Ignored Characters


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

### Finding a shift value
Quick brute-force way to search shift values from 1 to 25 
`python crypto.py -find -q {input string}`
Every shift from 1 to 25 will be output. Additionally, those strings will be searched for some common (English) words, and if the shifted string contains the word, a marker will be printed to draw attention to the string.

For example, `python crypto.py -find -q "ymnx nx f yjxy"` will output

```(1)	xlmw mw e xiwx
(2)	wklv lv d whvw
(3)	vjku ku c vguv
(4)	uijt jt b uftu
(5)	this is a test <---
(6)	sghr hr z sdrs
(7)	rfgq gq y rcqr
(8)	qefp fp x qbpq
(9)	pdeo eo w paop
(10)	ocdn dn v ozno
(11)	nbcm cm u nymn
(12)	mabl bl t mxlm
(13)	lzak ak s lwkl
(14)	kyzj zj r kvjk
(15)	jxyi yi q juij
(16)	iwxh xh p ithi
(17)	hvwg wg o hsgh
(18)	guvf vf n grfg
(19)	ftue ue m fqef
(20)	estd td l epde
(21)	drsc sc k docd
(22)	cqrb rb j cnbc
(23)	bpqa qa i bmab
(24)	aopz pz h alza
(25)	znoy oy g zkyz
```

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

## Ignored substitutions
If only the partial ciphertext is known, put an asterisk "\*" in place, and the character will not be replaced.

`python crypto.py -r -sr "x***x***x*****x*****x*****" -q "this is a test"` will return `thxs xs x txst`

# [Atbash Cipher](https://en.wikipedia.org/wiki/Atbash)
The Atbash Cipher is an implementation of the Substitution Cipher where the alphabet is reversed

## Usage
`python crypto.py -b -q "this is a test"`

`python crypto.py --atbash -q "this is a test"`

returns `gsrh rh z gvhg`

# Shift Series
An implementation of the Shift Cipher where the shift value changes. The user provides a series of numbers, which are converted from characters to integers. Each letter is shifted by the value. The series is repeated to the length of the input string.
## Usage
`python crypto.py -ss {series} -q {input string}`

`python crypto.py -ss 123 -q "aaaaaaaaaaaaaaaaa"` returns `bcdbcdbcdbcdbcdbc`

# Using Files

## Input File
input string can be read from a text file using the `-in` argument
## Usage
Lines that start with "#" will not be changed, only written as is.
If the text file looks like this:

> \# this line is ignored
> 
> this is a test

`python crypto.py -b -in ~/tmp/input.txt` 
returns:  
`# this line is ignored`  
`gsrh rh z gvhg`

## Output File
the output can be sent to a text file instead of the terminal  
`python crypto.py -b -in ~/tmp/input.txt -out ~/tmp/output.txt`  
cat ~/tmp/output.txt  
> \# this line is ignored
> 
> gsrh rh z gvhg

# Ignored Characters
Punctuation characters that are not replaced in any of the methods:
`<space> ,.;#$!"'*-?\r\n`


