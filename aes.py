from collections import namedtuple
from Crypto.Cipher import AES
import base64
import os

# The block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
BLOCK_SIZE = 32

# TODO: Generate new keys for each session and share between parties secretly.
# The character used for padding used to ensure that your value is always a
# multiple of BLOCK_SIZE.
PADDING = b'|'
KEY = b'Sixteen byte key'
IV = b'Sixteen byte ivv'

def encrypt(privateInfo):
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING     
    # encrypt with AES, encode with base64
    EncodeAES = lambda c, s: c.encrypt(pad(s))
    # creates the cipher obj using the key
    cipher = AES.new(KEY, AES.MODE_EAX, IV)
    # encodes you private info!
    encoded = EncodeAES(cipher, privateInfo)
    return encoded


def decrypt(encryptedString, padLen=None):
    if padLen is None:
        DecodeAES = lambda c, e: c.decrypt(e).rstrip(PADDING)
    else:
        DecodeAES = lambda c, e: c.decrypt(e)[:-padLen]
    # Key is FROM the printout of 'secret' in encryption
    # below is the encryption.
    encryption = encryptedString
    cipher = AES.new(KEY, AES.MODE_EAX, IV)
    decoded = DecodeAES(cipher, encryption)
    return decoded
    
