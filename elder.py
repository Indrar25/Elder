
from web3 import Web3

# Konfigurasi
KAIA_RPC = "https://klaytn.api.onfinality.io/public"
TOKEN_ADDRESS = "0x8755d2e532b1559454689bf0e8964bd78b187ff6"
PRIVATE_KEYS_FILE = "wallets.txt"  # file berisi private key per baris
OUTPUT_FILE = "token.txt"

# ABI ERC20 dasar
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

# Inisialisasi Web3 dan kontrak token
w3 = Web3(Web3.HTTPProvider(KAIA_RPC))
token = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=ERC20_ABI)

# Baca private keys dan derive wallet address
with open(PRIVATE_KEYS_FILE, "r") as f:
    private_keys = [line.strip() for line in f if line.strip()]

# Tulis ke file output
with open(OUTPUT_FILE, "w") as out:
    out.write("=== Daftar Wallet yang Dicek ===\n")
    for pk in private_keys:
        try:
            acct = w3.eth.account.from_key(pk)
            out.write(f"{acct.address}\n")
        except Exception as e:
            out.write(f"INVALID PRIVATE KEY: {pk} | ERROR: {str(e)}\n")

    out.write("\n=== Hasil Pengecekan Airdrop ===\n")

    print("Hasil pengecekan airdrop:")
    for pk in private_keys:
        try:
            acct = w3.eth.account.from_key(pk)
            checksum_wallet = Web3.to_checksum_address(acct.address)
            balance = token.functions.balanceOf(checksum_wallet).call()

            if balance > 0:
                balance_normal = balance / 1e18
                formatted_balance = "{:.2f}".format(balance_normal)
                print(f"[+] {checksum_wallet} menerima airdrop: {formatted_balance}")
                out.write(f"{checksum_wallet} | MENERIMA: {formatted_balance}\n")
            else:
                print(f"[-] {checksum_wallet} TIDAK menerima airdrop.")
                out.write(f"{checksum_wallet} | TIDAK MENERIMA\n")
        except Exception as e:
            print(f"[!] Error cek private key {pk}: {e}")
            out.write(f"{pk} | ERROR: {str(e)}\n")
