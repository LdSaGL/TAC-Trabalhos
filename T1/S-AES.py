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

O algoritmo vai fazer:

KeyExpansion: gera K1 e K2.
AddRoundKey com K0.
SubNibbles.
ShiftRows.
MixColumns.
AddRoundKey com K1.
SubNibbles.
ShiftRows.
AddRoundKey final com K2.
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

def bin_to_base64(bin_str):
    """
    Converts a binary string to its base64 representation.
    """
    import base64
    # Convert binary string to bytes
    byte_array = int(bin_str, 2).to_bytes((len(bin_str) + 7) // 8, byteorder='big')
    # Encode bytes to base64
    return base64.b64encode(byte_array).decode('utf-8')

def assemble_state(msg):
    """
    Assembles the state from the binary message.
    The state is a 2x2 matrix represented as a list of lists.
    """
    state = []
    for i in range(0, len(msg), 16):
        substate = []
        # Divide o bloco de 16 bits em 4 nibbles (4 bits cada)
        # e organiza em uma matriz 2x2
        substate.append([msg[i:i+4], msg[i+8:i+12]]) # Primeiro nibble e Terceiro nibble
        substate.append([msg[i+4:i+8], msg[i+12:i+16]]) # Segundo nibble e Quarto nibble
        state.append(substate)
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
    parsed_key = [key[i:i+4] for i in range(0, len(key), 4)]
    
    state[0][0] = format(int(state[0][0], 2) ^ int(parsed_key[0], 2), '04b')
    state[1][0] = format(int(state[1][0], 2) ^ int(parsed_key[1], 2), '04b')
    state[0][1] = format(int(state[0][1], 2) ^ int(parsed_key[2], 2), '04b')
    state[1][1] = format(int(state[1][1], 2) ^ int(parsed_key[3], 2), '04b')

def sub_nibbles(state):
    """
    Replaces each nibble in the state with its corresponding value from the S-Box.
    """
    for i in range(2):
        for j in range(2):
            state[i][j] = sbox[int(state[i][j], 2)]
     
def shift_rows(state):
    """
    Shifts the rows of the state matrix.
    The first row is unchanged, the second row is shifted left by 1, 
    """
    aux = state[1][0]
    state[1][0] = state[1][1]
    state[1][1] = aux

def mix_columns(state):
    """
    Mixes the columns of the state matrix using Galois Field multiplication.
    This function is not implemented in this simplified version.
    
    diff_matrix = [[1,4],
                   [4,1]]
    """
    gf4_mul_by_4 = {
        0x0: 0x0, 0x1: 0x4, 0x2: 0x8, 0x3: 0xC,
        0x4: 0x3, 0x5: 0x7, 0x6: 0xB, 0x7: 0xF,
        0x8: 0x6, 0x9: 0x2, 0xA: 0xE, 0xB: 0xA,
        0xC: 0x5, 0xD: 0x1, 0xE: 0xD, 0xF: 0x9
    }

    a = int(state[0][0], 2)
    b = int(state[0][1], 2)
    c = int(state[1][0], 2)
    d = int(state[1][1], 2)

    a_new = a ^ gf4_mul_by_4[c]
    c_new = gf4_mul_by_4[a] ^ c
    b_new = b ^ gf4_mul_by_4[d]
    d_new = gf4_mul_by_4[b] ^ d

    state[0][0] = format(a_new, '04b')
    state[1][0] = format(c_new, '04b')
    state[0][1] = format(b_new, '04b')
    state[1][1] = format(d_new, '04b')


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

# Entrada de dados
print("AES Simplificado")
msg = text_to_bin(input("Digite a mensagem: "))
print("Mensagem em binário: ", msg) # Mostra a mensagem em binário

key = '1001011001011010'  # Chave K0
print("Chave K0: ", key) # Mostra a chave utilizada

keys = key_expansion(key) # Gera as chaves K1 e K2
print("Chaves K1 e K2: ", keys[1:]) # Mostra as chaves geradas

state = assemble_state(msg) # Monta o estado
print("Estados: ", state) # Mostra a lista de estados

for i in range(len(state)):
    print('#' * 20)
    print("Estado ", i, ":") 
    print('#' * 20)

    # Aplica o algoritmo para cada estado
    add_round_key(state[i], keys[0])
    print('Add Round Key K0:')
    print(state[i])
    sub_nibbles(state[i])
    print('##### Rodada 1 #####')
    print('Sub Nibbles:')
    print(state[i])
    shift_rows(state[i])
    print('Shift Rows:')
    print(state[i])
    mix_columns(state[i])
    print('Mix Columns:')
    print(state[i])
    add_round_key(state[i], keys[1])
    print('Add Round Key K1:')
    print(state[i])
    sub_nibbles(state[i])
    print('##### Rodada 2 #####')
    print('Sub Nibbles:')
    print(state[i])
    shift_rows(state[i])
    print('Shift Rows:')
    print(state[i])
    add_round_key(state[i], keys[2])
    print('Add Round Key K2:')
    print(state[i])

states_bin = ''.join([''.join(row) for substate in state for row in substate])
states_hex = bin_to_hex(states_bin)
states_base64 = bin_to_base64(states_bin)

print("Mensagem cifrada: ", states_bin)
print("Mensagem cifrada em hexadecimal: ", states_hex)
print("Mensagem cifrada em base64: ", states_base64)