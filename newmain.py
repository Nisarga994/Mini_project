import numpy as np
import streamlit as st
import cv2

def logistic_map(x, r, iterations):
    for i in range(iterations):
        x = r * x * (1 - x)
    return x

def encrypt_message(message,x, r, iterations):
    encrypted_msg = ""
    for char in message:
        x = logistic_map(x, r, iterations)
        encrypted_msg += chr(ord(char) + int(x * 255))
    return encrypted_msg

def decrypt_message(encrypted_msg,x, r, iterations):
    decrypted_msg = ""
    
    for char in encrypted_msg:
        x = logistic_map(x, r, iterations)
        decrypted_msg += chr(ord(char) - int(x * 255))
    return decrypted_msg

def text_to_hex(secret_msg):
    hexa_text = secret_msg.encode('utf-8').hex()
    return hexa_text

def hex_to_text(hexa_text):
    decrypt_bytes = bytes.fromhex(hexa_text)
    decrypted_text = decrypt_bytes.decode('utf-8')
    return decrypted_text

st.title("Image Steganography Using Chaos Function")

image_upload = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
passcode = st.text_input("Enter the password:",type='password')
secret_message = st.text_input("Enter the secret message:")


if image_upload:
    image = cv2.imdecode(np.frombuffer(image_upload.read(), np.uint8), cv2.IMREAD_COLOR)
    x_initial=st.slider("X(0) initial",0.0,1.0,0.5)
    parameter=st.slider("Parameter(r)",3.5,4.0,3.8)
    iterations=st.slider("Iterations",100,500,256)
    encrypted_msg =encrypt_message(secret_message,x_initial, parameter, iterations)
    hexa_text = text_to_hex(encrypted_msg)
    

    character_to_code = {}
    code_to_character = {}

    for i in range(255):
        character_to_code[chr(i)] = i
        code_to_character[i] = chr(i)

    n = 0
    m = 0

    for i in range(len(hexa_text)):
        image[n, m, 0] = character_to_code[hexa_text[i]]
        n += 1
        m += 1
    if st.button(label="encrypt"):
        st.image(image, caption="Encrypted Image")

    decrypt_msg = ""

    n = 0
    m = 0

    password = st.text_input("Enter the password for decryption:",type='password')

    if password == passcode:
        for i in range(len(hexa_text)):
            decrypt_msg += code_to_character[image[n, m, 0]]
            n += 1
            m += 1
        if st.button(label="decrypt"):
            decrypted_msg=hex_to_text(decrypt_msg)
            decrypt_text=decrypt_message(decrypted_msg,x_initial,parameter,iterations)
            st.write("Decrypted message is:", decrypt_text)
    else:
        st.write("Invalid password")
