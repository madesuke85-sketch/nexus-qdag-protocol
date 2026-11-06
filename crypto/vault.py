import hashlib, os
class PostQuantumVault:
    def __init__(self, seed_secret=None):
        self.secret = seed_secret or hashlib.sha3_256(os.urandom(32)).hexdigest()
        self.raw_quantum_pubkey = hashlib.sha3_512(self.secret.encode()).hexdigest() * 2
        self.address = "NXQ_" + hashlib.sha3_256(self.raw_quantum_pubkey.encode()).hexdigest()[:32]
        self.core_balance = 0.0
        self.pocket_cash = 0.0

    def lock_to_pocket_cash(self, amount):
        if amount > self.core_balance: return False, "Saldo tidak cukup!"
        self.core_balance -= amount
        self.pocket_cash += amount
        return True, "Sukses"

    def sign_transaction(self, recipient, amount, fee=0.01):
        payload = f"{self.address}:{recipient}:{amount}:{fee}"
        sig = hashlib.sha3_256((payload + self.secret).encode()).hexdigest()
        return {"sender": self.address, "recipient": recipient, "amount": float(amount), "fee": float(fee), "revealed_pubkey": self.raw_quantum_pubkey, "zk_sig": sig}

    @staticmethod
    def verify_tx(tx):
        expected_addr = "NXQ_" + hashlib.sha3_256(tx["revealed_pubkey"].encode()).hexdigest()[:32]
        return expected_addr == tx["sender"]
