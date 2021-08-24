import argparse
import os
import base64
import cryptography
from cryptography import fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

parser = argparse.ArgumentParser(description='Encrypt a file')
parser.add_argument('-f', '--file', help='File to encrypt', required=True)
parser.add_argument('-k', '--key', help='Key to use for encryption', required=True)
parser.add_argument('-e', '--encrypt', help='Encrypt the file', action='store_true')
parser.add_argument('-d', '--decrypt', help='Decrypt the file', action='store_true')
parser.add_argument('-s', '--sneaky', help='Do not append .enc to filename', action='store_true')
args = parser.parse_args()
args = parser.parse_args()

salt = b"F@qa4,C.>%?+j[8W2ff\?s558'pF/.Kz"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=cryptography.hazmat.backends.default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(args.key.encode()))
f = fernet.Fernet(key)

if not os.path.isfile(args.file):
    print("File does not exist")
    exit()

if not args.encrypt and not args.decrypt:
    print("No action specified")
    exit()

if args.encrypt:
    with open(args.file, 'rb') as file:
        try:
            data = file.read()
        except Exception as e:
            print("error reading file: {}".format(e))
            exit(1)
    encrypted = f.encrypt(data)
    with open(args.file, 'wb') as file:
        file.write(encrypted)
    if not args.sneaky:
        os.rename(args.file, args.file + '.enc')
    print("enctypted")


if args.decrypt:
    with open(args.file, 'rb') as file:
        data = file.read()
    try:
        decrypted = f.decrypt(data)
    except cryptography.fernet.InvalidToken:
        print("Incorrect key")
        exit(1)
    with open(args.file, 'wb') as file:
        file.write(decrypted)
    outpath = args.file.replace('.enc', '')
    os.rename(args.file, outpath)
    print("decrypted")
