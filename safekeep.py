import os
import base64
import getpass

#Vigenère Cipher
def _encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def _decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

#File Handling
def pwd_close(pwd, fname):
    with open(f"./{fname}", "rb") as f:
        data = f.read().decode("utf-8")

    new_name = f"encoded_{fname}.txt"
    
    with open(f"./{new_name}", "wb") as f:
        f.write( bytes(_encode(pwd, data), "utf-8") )

    os.system(f"copy /b img.png+{new_name} new.png")
    os.remove(f"./{new_name}")

def pwd_open(key, fname):
    with open(f"./{fname}", "rb") as f:
        data = f.read().decode("utf-8")
        
    with open(f"./decoded_{fname}", "wb") as f:
        f.write( bytes(_decode(key, data), "utf-8") )
        
#User Interaction
def run():
    prompt = input("Open or Close? ")
    pwd = getpass.getpass()
    fname = input("File Name: ")

    if prompt.lower() == "o" or prompt.lower() == "open":
        pwd_open(pwd, fname)
    elif prompt.lower() == "c" or prompt.lower() == "close":
        pwd_close(pwd, fname)
    else:
        print("Invalid")

run()
