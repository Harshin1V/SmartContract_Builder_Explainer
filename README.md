# 🛠️ Smart Contract Toolkit  

This project implements two tools leveraging Large Language Models (LLMs) to assist blockchain developers and users:

1. **Task 1**: Natural Language → Secure Smart Contract Logic  
2. **Task 2**: Smart Contract Explainability (via Contract Address or Raw Code)

---

## 🚀 Project Structure
```
.
├── NLP to SmartContracts/
│   ├── app.py 
│   ├── requirements.txt
│   └── design_scaling_risks_llm_blockchain.md
├── Security Insights on SmartContracts/
│   ├── smart_contract_explainer.py
│   ├── streamlit_app.py
│   ├── requirements.txt
│   └── design_scaling_risks_llm_blockchain.md
└── README.md
```


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

## 🛡️ Guardrails & Security Measures

- Prompt templates designed to minimize **hallucination**
- Output filtered for dangerous patterns (`tx.origin`, unprotected state access)
- Safety checks for unrestricted access or missing modifiers

---

### ⚙️ Setup Instructions

```bash

python -m venv venv
pip install -r requirements.txt
streamlit run app.py
