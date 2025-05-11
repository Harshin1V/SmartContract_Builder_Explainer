# 🛡️ Smart Contract Explainer

A developer tool that helps you:
- 📖 Explain and audit existing smart contracts from an address or source code.

---

### ✅ Task 2: Smart Contract Explainability

**Problem:** Users need clear explanations of existing smart contracts.

**Solution:** This tool:
- Accepts a **contract address on Sepolia**, Solidity code, or a file.
- Uses Web3 + Etherscan + gpt-4o-mini to generate a plain-English summary, including:
  - Key functions and permissions
  - Events and state variables
  - Security patterns and best practices

**Files Used:**
- `smart_contract_explainer.py` — Backend logic
- `streamlit_app.py` — Streamlit UI for explainability


[▶️ Watch the Demo](https://www.youtube.com/watch?v=olu_j5pCcTI)



---

## 🚀 How to Run

```bash

python -m venv venv

pip install -r requirements.txt

streamlit run app.py

