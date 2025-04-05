from blockchain import Blockchain
import datetime
import hashlib

class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.proof) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 4
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis block", "0", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while self.is_valid_proof(new_proof, previous_proof) is False:
            new_proof += 1
        return new_proof

    def hash(self, block):
        block_string = str(block.index) + str(block.timestamp) + str(block.transactions) + str(block.proof) + str(block.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def is_valid_proof(self, new_proof, previous_proof):
        guess = f'{previous_proof}{new_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty

    def create_block(self, proof, previous_hash):
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.datetime.now(),
            transactions=self.pending_transactions,
            proof=proof,
            previous_hash=previous_hash
        )
        self.pending_transactions = []
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            previous_proof = previous_block.proof
            current_proof = current_block.proof
            guess = f'{previous_proof}{current_proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:self.difficulty] != "0" * self.difficulty:
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

my_blockchain = Blockchain()

while True:
    print("\nChọn hành động:")
    print("1. Thêm giao dịch mới")
    print("2. Đào block mới")
    print("3. Hiển thị toàn bộ blockchain")
    print("4. Kiểm tra tính hợp lệ của blockchain")
    print("5. Thoát")

    choice = input("Nhập lựa chọn của bạn: ")

    if choice == '1':
        sender = input("Nhập người gửi: ")
        receiver = input("Nhập người nhận: ")
        while True:
            try:
                amount = float(input("Nhập số lượng: "))
                if amount <= 0:
                    print("Số lượng phải lớn hơn 0.")
                else:
                    break
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")
        my_blockchain.add_transaction(sender, receiver, amount)
        print("Giao dịch đã được thêm vào hàng chờ.")
    elif choice == '2':
        if not my_blockchain.pending_transactions:
            print("Không có giao dịch nào đang chờ xử lý để đào.")
        else:
            previous_block = my_blockchain.get_latest_block()
            previous_proof = previous_block.proof
            new_proof = my_blockchain.proof_of_work(previous_proof)
            previous_hash = previous_block.hash
            my_blockchain.add_transaction('Genesis', 'Miner', my_blockchain.mining_reward) # Phần thưởng cho người đào
            new_block = my_blockchain.create_block(new_proof, previous_hash)
            print("Block mới đã được đào thành công!")
    elif choice == '3':
        for block in my_blockchain.chain:
            print(f"Block #{block.index}")
            print("Timestamp:", block.timestamp)
            print("Transactions:", block.transactions)
            print("Proof:", block.proof)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)
            print()
    elif choice == '4':
        is_valid = my_blockchain.is_chain_valid(my_blockchain.chain)
        print("Is Blockchain Valid:", is_valid)
    elif choice == '5':
        print("Thoát chương trình.")
        break
    else:
        print("Lựa chọn không hợp lệ. Vui lòng thử lại.")