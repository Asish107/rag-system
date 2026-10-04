# Retrieval Evaluation Questions

## 1. NVIDIA R&D

Question:
How much did NVIDIA spend on research and development?

Expected:
$12.914 billion in fiscal 2025.

Expected source:
raw/nvidia-10k-2025.pdf, page 52

Result:
PASS

---

## 2. Apple China risks

Question:
What are Apple's main risk factors related to China?

Expected:
China-related manufacturing/supply-chain concentration,
trade restrictions/geopolitical risks, and Greater China
business exposure.

Expected source:
raw/apple-10k-2024.pdf

Result:
FAIL — top results did not retrieve China-specific passages.

---

## 3. Out-of-domain question

Question:
What's your name?

Expected:
No relevant document context.

Result:
PASS/REQUIRES THRESHOLD — nearest distance was ~0.899,
but LIMIT 5 still returned five chunks.