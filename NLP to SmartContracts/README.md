# 🛡️ Smart Contract Builder 

A developer tool that helps you:
- 🧠 Convert natural language requirements into secure Solidity smart contracts.

---


### ✅ Task 1: Natural Language → Smart Contract Logic

**Problem:** Developers struggle to translate plain-English specs into production-ready smart contracts.

**Solution:** This Streamlit-based app uses GPT-4 to:
- Convert plain-English prompts (e.g., _“ERC-20 token with allowlist minting”_) into secure Solidity code.
- Follow best practices: input validation, gas-efficiency, OpenZeppelin use.
- Output a short **security analysis** (e.g., _“used modifier for allowlist check”_).

**Files Used:**
- `app.py` — Streamlit app for contract generation

[▶️ Watch the Demo](https://www.youtube.com/watch?v=M_5-KpZAwNk)




---

## 🚀 How to Run

```bash

python -m venv venv

pip install -r requirements.txt

streamlit run app.py

