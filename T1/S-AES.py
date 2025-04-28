"""
Implementar o algoritmo AES simplificado em Python.

Blocos de 16 bits
2 rodadas

Op. Básicas:
AddRoundKey
SubNibbles (S-Box fixa)
ShiftRows
MixColumns (GF(2^4))
KeyExpansion
"""

def text_to_bin(text):
    """
    Converts a string of text into its binary representation.
    Each character is represented by its 8-bit ASCII binary equivalent.
    """
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_hex(bin_str):
    """
    Converts a binary string to its hexadecimal representation.
    """
    return hex(int(bin_str, 2))

def assemble_state(msg):
    """
    Assembles the state from the binary message.
    The state is a 2x2 matrix represented as a list of lists.
    """
    state = []
    for i in range(0, len(msg), 16):
        state.append([msg[i:i+4], msg[i+8:i+12]]) # Primeiro nibble e Terceiro nibble
        state.append([msg[i+4:i+8], msg[i+12:i+16]]) # Segundo nibble e Quarto nibble
    return state

def key_expansion(key):
    """
    Expands the 16-bit key into three round keys for the simplified AES algorithm.
    """
    rcon_1 = '10000000'
    rcon_2 = '00110000'
    
    w0 = key[0:8]
    w1 = key[8:16]
    
    # Rotaciona w1, aplica S-Box e XOR com rcon_1
    g_w1 = format(int(sbox[int(w1[4:], 2)] + sbox[int(w1[:4], 2)],2) ^ int(rcon_1, 2), '08b')
    
    # w2 = w0 XOR g_w1  
    w2 = format(int(w0, 2) ^ int(g_w1, 2), '08b')
    
    # w3 = w1 XOR w2
    w3 = format(int(w1, 2) ^ int(w2, 2), '08b')
    
    # Rotaciona w3, aplica S-Box e XOR com rcon_2
    g_w3 = format(int(sbox[int(w3[4:], 2)] + sbox[int(w3[:4], 2)],2) ^int(rcon_2, 2), '08b')
    
    # w4 = w2 XOR g_w3
    w4 = format(int(w2, 2) ^ int(g_w3, 2), '08b')
    
    # w5 = w3 XOR w4
    w5 = format(int(w3, 2) ^ int(w4, 2), '08b')

    return [w0+w1, w2+w3, w4+w5]
 
def add_round_key(state, key):
    """
    Adds the round key to the state using XOR operation.
    Each nibble of the state is XORed with the corresponding nibble of the key.
    """
    return

"""
S-Box (Entrada -> Saída)
Mapear uma saida para todas as entradas de 4 bits 
    0x0	0x9 -> 1001
    0x1	0x4 -> 0100
    0x2	0xA -> 1010
    0x3	0xB -> 1011
    0x4	0xD -> 1101
    0x5	0x1 -> 0001
    0x6	0x8 -> 1000
    0x7	0x5 -> 0101
    0x8	0x6 -> 0110
    0x9	0x2 -> 0010
    0xA	0x0 -> 0000
    0xB	0x3 -> 0011
    0xC	0xC -> 1100
    0xD	0xE -> 1110
    0xE	0xF -> 1111
    0xF	0x7 -> 0111
"""
sbox = ['1001', '0100', '1010', '1011', '1101', '0001', '1000', '0101', '0110', '0010', '0000', '0011', '1100', '1110', '1111', '0111']

"""
# Entrada de dados
print("AES Simplificado")
msg = input("Digite a mensagem: ")
key = text_to_bin(input("Digite a chave (2 caracteres ASCII): "))
key = '1001011001011010'  # Chave de exemplo
keys = key_expansion(key)
"""

msg = 'oqa'
print(assemble_state(text_to_bin(msg)))