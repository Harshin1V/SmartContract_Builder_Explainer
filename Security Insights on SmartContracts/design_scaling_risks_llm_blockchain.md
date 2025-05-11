# 🧠 Smart Contract Explainability Tool

## 🧩 Design Tradeoffs

- **Model choice:** We use `gpt-4o-mini` for cost-effective reasoning. While `gpt-4` provides more accurate results, it’s slower and costlier.
- **Security vs. Speed:** LLM responses are safeguarded with guardrails in prompts to avoid code generation or security leaks. This slightly slows down output generation but improves safety.
- **ABI fallback:** When source code is unavailable, the tool explains contracts using only the ABI — trading off depth for broader applicability.

---

## 📈 Scaling the Prototype

- **Caching:** Add memoization or Redis to avoid re-processing identical contracts.
- **On-chain/off-chain separation:**
  - **On-chain:** ABI, bytecode, and metadata live on-chain (retrieved via Etherscan/Web3).
  - **Off-chain:** The LLM inference, formatting, and explainability are off-chain — ideal for maintaining cost and speed efficiency.
- **Queue/Async processing:** Add background task queues (e.g., Celery + Redis) to manage long-running LLM calls.

---

## ⚠️ Risks of LLM-Generated Code in Blockchain

- **Overtrust in summaries:** Users might falsely assume the contract is safe if the LLM doesn't detect edge-case vulnerabilities.
- **LLM hallucinations:** Fabricated functions or incorrect logic interpretation could mislead users.
- **No real auditing:** This tool is not a substitute for formal verification or human auditing.
- **Security impact:** LLMs should never suggest or generate Solidity code without context or controls — we strictly avoid code generation.

---

# 🧠 Smart Contract Explainer – Summary

A tool that takes Sepolia testnet contract addresses or Solidity code and uses `web3.py`, Etherscan, and OpenAI (GPT-4o-mini) to generate plain-English summaries explaining key functions, permissions, and security aspects.

**Design Tradeoffs:** Balanced LLM quality vs. cost/speed, fallback to ABI when source missing, security-first prompt design.

**Scaling Ideas:** Caching, async LLM calls, separate on-chain data fetch from off-chain analysis.

**LLM Risks:** Misleading summaries, hallucinations, false sense of security — no replacement for audits.

