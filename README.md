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
1. Start a local Ethereum chain on `http://127.0.0.1:9545` (for example Truffle develop or Ganache) and deploy `CrowdSensing.sol`.
2. Put the deployed contract address into `PPQC.py` (`deployed_contract_address`, in `readDetails` and `saveDataBlockChain`).
3. `pip install -r requirements.txt` (Python 3.7 was used)
4. `python PPQC.py`

## Limitations (please read)
- The encryption is a **teaching-scale demo**: tiny parameters (n=32), and the keys and noise are fixed in the code rather than random. It is not secure and must not be used to protect real data.
- The contract address in the code belongs to a local test chain from my machine and will not work elsewhere.
- Written as a university project; the code has not been refactored or tested beyond running the simulation.
