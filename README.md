# 🔬 PeerCheck
### Decentralized AI-Assisted Academic Pre-Screening on GenLayer

> *A proof-of-concept for programmable, verifiable research credibility built in 2 weeks for the Bradbury Builders Hackathon.*

---

##  Hackathon Submission

| | |
|---|---|
| **Hackathon** | Bradbury Builders Hackathon by GenLayer |
| **Track** | Future of Work |
| **Builder** | Aqeelerh |
| **Contract Address** | `0xa0643eE708b52b79FC49093eEACbeEeeFf5Fd87F` |
| **Network** | GenLayer Bradbury Testnet (Chain ID: 4221) |
| **Explorer** | [View Contract](https://explorer-bradbury.genlayer.com/address/0xa0643eE708b52b79FC49093eEACbeEeeFf5Fd87F) |

---

##  The Problem

Academic peer review faces well-documented structural challenges:

- **Speed:** Average time from submission to decision is 6–18 months across major journals
- **Opacity:** Most reviews are anonymous with limited accountability mechanisms
- **Scale:** Over 2.5 million papers are published annually, human review capacity is a genuine bottleneck
- **Verification gap:** There is no fast, decentralized, machine-readable quality signal for research output

Existing signals: citations, h-index, impact factor, journal tier are valuable but lagging indicators. They measure past reception, not prospective quality. Grant organizations, early-stage investors, and hackathon organizers making time-sensitive decisions have no neutral, real-time pre-screening layer.

**PeerCheck does not claim to replace human peer review.** It introduces a transparent, consistent pre-screening layer to surface high-signal work faster.

---

##  The Solution

PeerCheck is an Intelligent Contract on GenLayer that provides AI-assisted pre-screening of research paper abstracts using decentralized validator consensus.

**What it evaluates:**
- Methodology clarity and reproducibility signals
- Citation adequacy based on claim strength
- Logical consistency from abstract to conclusion

**What it produces:**
- A credibility score (0–100) and letter grade (A–F)
- Identified risk flags (weak citations, scope overclaim, etc.)
- A one-sentence AI reasoning summary
- A permanent on-chain certificate with a unique paper hash

**What it is not:**
- A replacement for domain expert review
- A ground-truth validator of scientific correctness

---

##  How It Works

```
1. Researcher submits abstract (min 100 chars) + paper link
2. evaluate_paper() runs inside a non-deterministic block
3. gl.exec_prompt() calls the LLM with a structured evaluation prompt
4. Output normalized: scores clamped 0-100, flags validated, score recomputed deterministically
5. gl.eq_principle_prompt_non_comparative() runs validator consensus
6. If validators agree within tolerance → certificate written on-chain
7. Researcher profile updated automatically
```

---

##  GenLayer-Specific Implementation

### Optimistic Democracy

Multiple AI validators independently execute `evaluate_paper()`. A leader proposes a result. Other validators recompute and check whether the result falls within tolerance. Majority agreement finalizes the certificate on-chain without requiring identical outputs.

### Equivalence Principle

PeerCheck uses `gl.eq_principle_prompt_non_comparative()` with:
- **Task:** Evaluate the credibility and quality of this academic research paper abstract
- **Criteria:** Score tolerance ±20 points overall, ±25 points per sub-criterion, at least one flag must overlap

This allows GPT, Claude, and LLaMA running on different validator nodes to reach meaningful consensus even when their exact scores differ, as long as they agree on the paper's general quality band.

### Why On-Chain?

The value of on-chain storage is not that AI evaluation is more correct than human review. It is:

1. **Verifiability** — anyone can confirm a review happened, when, and what it concluded
2. **Portability** — the certificate belongs to the researcher's wallet permanently
3. **Programmability** — reputation scores can be read by other contracts (DAOs, grant systems)
4. **Decentralization** — no single editor or platform controls the result

---

##  Market Context

| Segment | Scale |
|---|---|
| Academic publishing | ~$28B annually (STM Association) |
| Global research grant disbursement | $180B+ annually |
| Scientific integrity services | ~$2B annually |

PeerCheck earns 20% of all transaction fees permanently via GenLayer's Dev Fee model.

---

## Track Fit: Future of Work

| Criterion | PeerCheck |
|---|---|
| AI-verified deliverables | ✅ Abstracts evaluated by AI validators |
| Reputation tracking | ✅ On-chain profile: NOVICE → LUMINARY |
| Outcome-based validation | ✅ Grade and score issued per submission |
| Optimistic Democracy | ✅ Core to certificate issuance |
| Equivalence Principle | ✅ `eq_principle_prompt_non_comparative` with task + criteria |

---

## Reputation System

| Level | Requirement |
|---|---|
| NOVICE | Starting point |
| CONTRIBUTOR | 3+ papers, avg ≥ 50 |
| ESTABLISHED | 5+ papers, avg ≥ 65 |
| EXPERT | 10+ papers, avg ≥ 75 |
| LUMINARY | 20+ papers, avg ≥ 85 |

---

## How to Deploy

```bash
npm install -g genlayer
genlayer network set testnet-bradbury
genlayer account create --name default
genlayer account unlock
genlayer deploy --contract contracts/peercheck_contract.py --args 0
```

### Test

```bash
genlayer write CONTRACT_ADDRESS submit_paper --args "YOUR ABSTRACT (min 100 chars)" "https://arxiv.org/abs/..."
genlayer call CONTRACT_ADDRESS get_all_certificates
genlayer call CONTRACT_ADDRESS get_profile --args "0xYOUR_WALLET"
```

---

## Repository Structure

```
peercheck/
├── contracts/
│   └── peercheck_contract.py
├── frontend/
│   └── index.html
└── README.md
```

---

## Builder

Built by **Aqeelerh** for the Bradbury Builders Hackathon 2026.

Academic peer review has real structural problems. GenLayer provides infrastructure that makes new approaches technically feasible. PeerCheck is a first step not a finished solution.

---

*Built on [GenLayer](https://genlayer.com) · Bradbury Builders Hackathon 2026*
