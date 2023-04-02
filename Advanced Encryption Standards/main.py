import sbox_generation, shift_rows, round_key_generation, mix_columns_matrix,sys


def xor_key(a, b):

    n, m = len(a), len(a[0])

    for i in range(n):
        for j in range(m):
            a[i][j] = a[i][j]^b[i][j]
            
    return a

def create_bin_to_num_matrix(inp):
    return [list(map(lambda x: int(x, 2), row)) for row in inp]

def encrypt(inp, key):

    inp = create_bin_to_num_matrix(round_key_generation.create_str_to_bin_matrix(round_key_generation.create_hex_to_bin_str(inp, len(inp))))

    aes_keymat = round_key_generation.aes_keymat(key, 0)
    inp = xor_key(inp, aes_keymat)
    print("After Round 0 of encryption: %s" % round_key_generation.create_matrix_to_str(inp))
    # print(inp)
    for round in range(1, 11):
        # inp = Substitution_Box.substitution(inp)
        # for row in inp: print(row)
        inp = sbox_generation.sbox_transform(inp)
        # print("After Substitution",inp,"\n");
        # print(type(inp[0][0]))
        inp = shift_rows.ShiftRow(inp)
        # print("After Shift Row",inp,"\n");
        if round != 10:
            inp = mix_columns_matrix.mixColumns_new(inp)
        # print("After mix column", inp, "\n");
        if(round == 10): # did this because inp values in string format becuase in round 10 mixcolumn is not performed to make values in decimal format
            for i in range(4):
                for j in range(4):
                    inp[i][j] = int(inp[i][j], 16)
        # for row in inp: print(row)
        # print(key)
        aes_keymat = round_key_generation.aes_keymat(key, round)
        # print(aes_keymat)
        temp = ""
        for i in range(4):
            for j in range(4):
                str = hex(aes_keymat[i][j])
                temp = temp + str[2:]
        inp = xor_key(inp, aes_keymat)
        print("After Round %d of encryption: %s, key %s" % (round, round_key_generation.create_matrix_to_str(inp), temp))
        # print();
    return round_key_generation.create_matrix_to_str(inp)

# inp = 128 bit hex string output = 128 bit hex string

def decrypt(inp: str, key: str) -> str:
    print(f"Cipher text = {inp}")
    cracked_mssg = "WRONG ANSWER"

    inp = create_bin_to_num_matrix(round_key_generation.create_str_to_bin_matrix(round_key_generation.create_hex_to_bin_str(inp, len(inp))))

    aes_keymat = round_key_generation.aes_keymat(key, 10)
    inp = xor_key(inp, aes_keymat)
    # print(f"After Round 0 of decryption: {key_expansion.create_matrix_to_str(inp)}")
    for round in range(1, 11):
        inp = shift_rows.InverseShiftRow(inp)
        # print("After inverse shift row", inp, "\n")
        inp = sbox_generation.inv_sbox_transform(inp)
        # for row in inp:
        #     print(row)
        for i in range(4):
            for j in range(4):
                inp[i][j] = int(inp[i][j], 16)
        temp = ""
        for i in range(4):
            for j in range(4):
                str = hex(aes_keymat[i][j])
                temp = temp + str[2:]
        print("After Round %d of encryption: %s, key %s" % (round, round_key_generation.create_matrix_to_str(inp), temp))
        aes_keymat = round_key_generation.aes_keymat(key, 10 - round)
        # print(aes_keymat)
        inp = xor_key(inp, aes_keymat)
        
        if round == 10:
            cracked_mssg = round_key_generation.create_matrix_to_str(inp)
            print(f"After Round {round} of decryption: {round_key_generation.create_matrix_to_str(inp)}")
        if round != 10:
            inp = mix_columns_matrix.inverse_MixColumns(inp)
            for i in range(4):
                for j in range(4):
                    inp[i][j] = int(inp[i][j], 16)
        # print("after mix column", inp, "\n")
    return [round_key_generation.create_matrix_to_str(inp), cracked_mssg]




def main():
    key = "0abcdef1234567890abcdef123456789"
    #............Plain text 1...............
    inp = "3e43ea9085aff2163c91b9722c5b49f1"
    cipher = encrypt(inp, key)
    print("\n---------------------------------\n")
    cipher2 = decrypt(cipher, key) 
    print(inp, " ", cipher2[1])
    if(inp == cipher2[1]):
        print("True")
    else:
        print("False")

    #...........Plain text 2...............
    inp = "0abc12f1a34567890abcdef123422788"
    cipher = encrypt(inp, key)
    print("\n---------------------------------\n")
    cipher = "ae43ea9085aff2163c91b9722c5b49f1"
    cipher2 = decrypt(cipher, key) 
    print(inp, " ", cipher2[1])
    if(inp == cipher2[1]):
        print("True")
    else:
        print("False")

if __name__ == "__main__":
    main()

    # import subprocess

    # package_name = "pyglet"

    # # Install the package using pip
    # subprocess.check_call(["pip", "install", package_name])

    # import pyglet

    # # Load the animation
    # animation = pyglet.image.load_animation('tenor.gif')

    # # Get the dimensions of the animation
    # width = animation.get_max_width()
    # height = animation.get_max_height()

    # # Create a window
    # window = pyglet.window.Window(width=width, height=height)

    # # Create a sprite for the animation
    # sprite = pyglet.sprite.Sprite(animation)

    # # Set the background color to white
    # pyglet.gl.glClearColor(1, 1, 1, 1)

    # # Define the on_draw event handler
    # @window.event
    # def on_draw():
    #     window.clear()
    #     sprite.draw()

    # # Start the event loop
    # pyglet.app.run()
