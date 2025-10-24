# Encrypt

Command line application to encrypt and decrypt any file with a password.

## Usage

```bash
# Using bash
./encrypt -f <file> -k <key> -e
./encrypt -f <file> -k <key> -d

# Using python
python3 encrypt -f <file> -k <key> -e
python3 encrypt -f <file> -k <key> -d
```

## Arguments

`-f` `--file` to encrypt, required  
`-k` `--key` key to use for encryption, required  
`-e` `--encrypt` encrypt the file, optional  
`-d` `--decrypt` decrypt the file, optional  
`-s` `--sneaky` do not append .enc to filename  

## Notes



## Considerations

- encrypt or decrypt must be specified
- you must have python and pip installed
- the cryptography package will be installed automatically if not found

## Security

### Brute Force Attack Estimates

This application uses PBKDF2 with 100,000 iterations, making each password guess take approximately 0.1 seconds on a modern CPU.

| Password Type | Entropy | Time to Crack |
|--------------|---------|---------------|
| 8 random lowercase | ~38 bits | Minutes to hours |
| 8 random alphanumeric | ~48 bits | Years |
| 12 random alphanumeric | ~71 bits | Millions of years |
| 16 random alphanumeric | ~95 bits | Billions of years |
| "password123" | Dictionary attack | Seconds |

### Recommendations

- **Minimum:** 12+ random characters (letters, numbers, symbols)
- **Alternative:** 4-5 word passphrase (e.g., "correct-horse-battery-staple")
- **Avoid:** Dictionary words, personal info, patterns, or common passwords

### Technical Details

- **Algorithm:** Fernet (AES-128-CBC + HMAC-SHA256)
- **Key Derivation:** PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Salt:** 32 random bytes generated per file using `secrets.token_bytes()`
- **Salt Storage:** Prepended to encrypted file (first 32 bytes)