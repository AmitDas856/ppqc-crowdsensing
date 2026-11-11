# PPQC: Blockchain-Based Privacy-Preserving Quality Control for Crowdsensing

A desktop simulation of a mobile crowdsensing network in which participants report their location with privacy protection, the publisher checks the quality of each report, and the result is recorded on a blockchain.

Undergraduate (B.Tech) project, 2023-2025. Team project; this repo holds the code from my working copy.

## What it does
- **Crowdsensing network (Tkinter):** generates a publisher and 19 participant nodes, routes a report through a relay node and animates the transfer.
- **Privacy layer (`Homomorphic.py`):** encrypts each location coordinate with a small lattice-based (BFV-style) homomorphic encryption scheme implemented with NumPy polynomial arithmetic.
- **Quality control (`PPQC.py`):** compares the decrypted value to the ground truth, computes a noise value, and rewards or penalises the participant.
- **Smart contract (`CrowdSensing.sol`, Solidity 0.8.11):** stores each participant's quality record on a local Ethereum chain, accessed through `web3.py`.
- **Timing graph:** plots the running time of the proposed mechanism against a baseline.

## Run it
```bash
pip install -r requirements.txt
python PPQC.py
```
Click **Generate Mobile Crowd Sourcing Network**, pick a participant and click **Submit Data**.

Without a blockchain, quality records are written to `ledger.txt` and the app says so. To store them on a local Ethereum chain instead:
1. Start a chain (for example Ganache or `truffle develop`) and deploy `CrowdSensing.sol`.
2. Set `PPQC_CHAIN_URL` (default `http://127.0.0.1:9545`) and `PPQC_CONTRACT_ADDRESS` to your deployed address.
3. Run `python PPQC.py`.

## Tests
`python -m pytest` checks, offline: encryption then decryption returns each location, the quality check rewards and penalises correctly, and records fall back to the local ledger when no chain is running. They run on GitHub Actions on every push.

## Limitations (please read)
- The encryption is a **teaching-scale demo**: tiny parameters (n=32), and the keys and noise are fixed in the code rather than random. It is not secure and must not be used to protect real data.
- The default contract address belongs to a local test chain from my machine; set `PPQC_CONTRACT_ADDRESS` to your own.
- Written as a university project. The blockchain calls were updated to the current web3.py API (the original pinned web3 4.7 from 2018, which no longer installs on current Python).
