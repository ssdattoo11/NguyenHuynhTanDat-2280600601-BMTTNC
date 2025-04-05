from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
 
app = Flask(__name__)
#router routes for home page 

@app.route("/")
def home():
    return render_template('index.html')

#router routes for ceesar cypher
@app.route("/caesar")
def ceasar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['InputPlainText']
    key = int(request.form['InputKeyText'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text} <br/> Key: {key} <br/> encrypt text: {encrypted_text}"

@app.route("/decrypt", methods = ['POST'])
def caesar_decrypt():
    text = request.form['InputCipherText']
    key = int(request.form['InputKeyText'])
    Caesar = CaesarCipher()
    decrypted_text =  Caesar.decrypt_text(text, key)
    return f"text: {text} <br/> Key: {key} <br/> decrypted text: {decrypted_text}"

#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5050, debug = True)