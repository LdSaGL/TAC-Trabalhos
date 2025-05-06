import time
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Função auxiliar: padding de 128 bits (AES exige blocos de 16 bytes)
def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

# Mensagem a ser cifrada
plaintext = b"AES e top demais!"  # 16 bytes

# Chave e IV fixos
key   = b'0123456789abcdef' # 16 bytes = 128 bits
iv    = b'abcdef9876543210' # 16 bytes
nonce = b'uniqueNONCE12345' # 16 bytes

# Pad a mensagem
padded = pad(plaintext)

# Modos e resultados
results = {}

# Modos com seus objetos
modes_dict = {
    'ECB': modes.ECB(),
    'CBC': modes.CBC(iv),
    'CFB': modes.CFB(iv),
    'OFB': modes.OFB(iv),
    'CTR': modes.CTR(nonce)
}

# Execução
print("Mensagem original:", plaintext.decode())
print("\nCriptografias com diferentes modos:\n")

for mode_name, mode_obj in modes_dict.items():
    cipher = Cipher(algorithms.AES(key), mode_obj, backend=default_backend())
    encryptor = cipher.encryptor()
    
    start = time.time()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    elapsed = time.time() - start

    results[mode_name] = {
        'hex': ciphertext.hex().upper(),
        'base64': base64.b64encode(ciphertext).decode(),
        'tempo': elapsed
    }

# Mostrar resultados
for mode, data in results.items():
    print(f"{mode}:\n  HEX   -> {data['hex']}\n  BASE64 -> {data['base64']}\n  TEMPO -> {data['tempo']:.6f} segundos\n")
