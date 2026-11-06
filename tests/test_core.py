import unittest
import sys
import os

# Hubungkan direktori modul
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.dag import FixedPoint, QuantizedAIProof, DAGBlock
from crypto.vault import PostQuantumVault
from transport.acoustic import AcousticTransceiver

class TestNexusProtocol(unittest.TestCase):
    def test_fixed_point_math(self):
        """Memastikan pembulatan integer deterministik tidak berubah bit-nya"""
        a = FixedPoint.from_float(2.5)
        b = FixedPoint.from_float(4.0)
        res = FixedPoint.mul(a, b)
        self.assertEqual(FixedPoint.to_float(res), 10.0)

    def test_quantum_vault_signature(self):
        """Memastikan verifikasi hash-commitment kunci pasca-kuantum bekerja"""
        vault = PostQuantumVault()
        tx = vault.sign_transaction("NXQ_REKAN_TEST", 10.0)
        self.assertTrue(PostQuantumVault.verify_tx(tx))

    def test_ai_quantized_training(self):
        """Memastikan AI circuit menghasilkan loss konvergen dan zk-proof"""
        proof = QuantizedAIProof.train_and_prove("test_seed_hash_12345")
        self.assertTrue(proof["valid"])
        self.assertTrue(len(proof["zk_proof"]) == 64)

if __name__ == '__main__':
    print("[*] MENJALANKAN AUTOMATED AUDIT TEST SUITE...")
    unittest.main()
