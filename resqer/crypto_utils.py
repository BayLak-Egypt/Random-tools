from Crypto.Cipher import AES
import base64
import os
def encrypt(key: bytes, data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext
def decrypt(key: bytes, data: bytes) -> bytes:
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
def generate_key(length=16) -> bytes:
    if length not in [16, 24, 32]:
        raise ValueError("AES key must be 16, 24, or 32 bytes")
    return os.urandom(length)
def bytes_to_binary(data: bytes) -> str:
    return ''.join(format(b, '08b') for b in data)
def binary_to_bytes(binary: str) -> bytes:
    return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
def binary_to_dots_spaces(binary: str) -> str:
    return ''.join(' ' if b=='1' else '.' for b in binary)
def dots_spaces_to_binary(dots_spaces: str) -> str:
    return ''.join('1' if c==' ' else '0' for c in dots_spaces)