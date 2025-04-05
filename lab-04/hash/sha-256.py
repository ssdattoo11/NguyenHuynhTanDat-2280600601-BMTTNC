import hashlib

def calculate_sha256_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

data_to_hash = input("Nhập chuỗi cần băm: ")
hash_value = calculate_sha256_hash(data_to_hash)
print ("Mã băm SHA-256 của chuỗi là: ", hash_value)