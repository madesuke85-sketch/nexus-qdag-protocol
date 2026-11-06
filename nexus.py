import os
import sys
import json
import time
import hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.dag import FixedPoint, QuantizedAIProof, DAGBlock
from crypto.vault import PostQuantumVault
from transport.acoustic import AcousticTransceiver

def run_interactive():
    os.system("clear")
    print("=======================================================")
    print("      NEXUS-QDAG PROTOCOL - LIVE OPERATIONAL CONSOLE   ")
    print("=======================================================")
    
    vault = PostQuantumVault()
    vault.core_balance = 100.0
    dag = {}
    tips = []
    
    # Genesis Block
    genesis = DAGBlock(0, ["0"*64], [], {"zk_proof": "GENESIS_ZK", "valid": True}, epoch_anchor=True)
    dag[genesis.hash] = genesis
    tips.append(genesis.hash)
    
    while True:
        print(f"\n[STATUS] Alamat Node : {vault.address}")
        print(f"[STATUS] Saldo Core  : {vault.core_balance} NXQ | Pocket-Cash: {vault.pocket_cash} NXQ")
        print(f"[STATUS] Tinggi DAG  : #{len(dag)-1} Blok Terverifikasi | Tips Aktif: {len(tips)}")
        print("-" * 55)
        print("1. Uji Tambang AI & Cetak Blok Baru (Useful AI)")
        print("2. Uji Transaksi Kriptografi Kuantum (Kirim Koin)")
        print("3. Uji Gelombang Suara (Bikin WAV -> Bedah & Verifikasi)")
        print("4. Uji Simulasi Graf Paralel (Tambang 4 Blok)")
        print("0. Selesai & Keluar")
        print("-" * 55)
        cmd = input("Pilih Uji Coba [0-4]: ").strip()
        
        if cmd == "1":
            print("\n[*] [AI ENGINE] Menjalankan pelatihan tensor INT32...")
            parents = tips[:2] if len(tips) >= 2 else [tips[0]]
            seed = hashlib.sha3_256("".join(parents).encode()).hexdigest()
            proof = QuantizedAIProof.train_and_prove(seed)
            
            h = max([dag[p].height for p in parents]) + 1
            block = DAGBlock(h, parents, ["REWARD: 50 NXQ"], proof, epoch_anchor=(h%3==0))
            dag[block.hash] = block
            tips = [block.hash]
            vault.core_balance += 50.0
            
            print(f"[+] SUKSES: Blok #{block.height} Lahir!")
            print(f"    - Hash Blok    : {block.hash[:24]}...")
            print(f"    - AI Loss      : {proof['loss'] / 10000.0}")
            print(f"    - zk-Proof     : {proof['zk_proof'][:24]}...")
            print(f"    - BFT Anchor   : {'YA (Terkunci)' if block.epoch_anchor else 'TIDAK'}")
            
        elif cmd == "2":
            penerima = PostQuantumVault()
            print(f"\n[*] Membuat Dompet Penerima Baru: {penerima.address}")
            amt = 15.0
            tx = vault.sign_transaction(penerima.address, amt, fee=0.01)
            print(f"[*] Transaksi Ditandatangani dengan Kunci Kuantum...")
            if PostQuantumVault.verify_tx(tx):
                vault.core_balance -= (amt + 0.01)
                penerima.core_balance += amt
                print(f"[+] HASIL VERIFIKASI: 100% SAH & TEROTENTIKASI!")
                print(f"    - Saldo Pengirim Sekarang : {vault.core_balance} NXQ")
                print(f"    - Saldo Penerima          : {penerima.core_balance} NXQ")
            else:
                print("[!] GAGAL: Tanda tangan palsu!")
                
        elif cmd == "3":
            print("\n[*] Mengunci 10 NXQ ke Pocket-Cash...")
            vault.lock_to_pocket_cash(10.0)
            nonce = hashlib.sha3_256(os.urandom(8)).hexdigest()[:16]
            payload = {"from": vault.address, "to": "NXQ_REKAN_OFFLINE", "amt": 10.0}
            
            print(f"[*] Memodulasi ke suara 'qdag_airgap.wav' (17.5-19.0 kHz)...")
            wav_file = AcousticTransceiver.synthesize_wav(payload, nonce, "qdag_airgap.wav")
            print(f"[+] File suara tersimpan ({os.path.getsize(wav_file)} bytes).")
            
            print(f"[*] Membedah file suara dengan Nonce: {nonce}...")
            decoded, status = AcousticTransceiver.demodulate_wav(wav_file, nonce)
            if decoded and decoded.get("amt") == 10.0:
                print(f"[+] SUKSES BESAR: Data suara 100% COCOK & TERDEKODE!")
                print(f"    - Pengirim : {decoded['from']}")
                print(f"    - Nominal  : {decoded['amt']} NXQ")
            else:
                print(f"[!] Gagal: {status}")
                
        elif cmd == "4":
            print("\n[*] Menambang 4 Blok BlockDAG Berturut-turut...")
            for _ in range(4):
                parents = tips[:2] if len(tips) >= 2 else [tips[0]]
                seed = hashlib.sha3_256("".join(parents).encode()).hexdigest()
                proof = QuantizedAIProof.train_and_prove(seed)
                h = max([dag[p].height for p in parents]) + 1
                block = DAGBlock(h, parents, [], proof, epoch_anchor=(h%3==0))
                dag[block.hash] = block
                tips.append(block.hash)
                if len(tips) > 3: tips.pop(0)
                print(f"    -> Blok #{block.height} terbit | Induk: {len(block.parents)} | Hash: {block.hash[:16]}...")
            print(f"[+] Total Blok di Graf: {len(dag)} Blok terhubung sempurna!")
            
        elif cmd == "0":
            print("[*] Konsol ditutup.")
            break

if __name__ == '__main__':
    run_interactive()
