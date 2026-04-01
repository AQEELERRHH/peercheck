# PeerCheck: Questions & Answers

*Anticipated questions from critics, judges, and the community with honest, substantiated answers.*

---

## 1. "There is no market for academia on-chain. Why does this belong in Web3?"

This question assumes academia and crypto are separate worlds. The evidence says otherwise.

**CertiK**  the largest Web3 security firm with a $2B+ valuation was founded in 2017 by two university professors: Professor Ronghui Gu (Associate Professor of Computer Science at Columbia University) and Professor Zhong Shao (Thomas L. Kempner Professor and Chair of Computer Science at Yale University). CertiK's entire founding thesis was applying academic formal verification research to blockchain security. Their most cited work CertiKOS, the first formally verified vulnerability-free OS kernel was published in academic journals before becoming the foundation of a billion-dollar company.

**Ethereum itself** began as an academic whitepaper. Vitalik Buterin published the Ethereum whitepaper in 2013 at age 19. He was subsequently awarded a $100,000 Thiel Fellowship to finish it. The Ethereum whitepaper is one of the most cited technical documents in computer science history. Vitalik served on the editorial board of *Ledger*  a peer-reviewed scholarly journal on cryptocurrency from 2016 to 2024.

**Charles Hoskinson**, co-founder of Ethereum and founder of Cardano, has a background in mathematics and built Cardano explicitly as an academically peer-reviewed blockchain every protocol upgrade goes through formal academic review before deployment.

The relationship between academia and crypto is not a new idea. It is the foundation of the industry's most credible infrastructure.

---

## 2. "Even if there are professors in crypto, why would they use PeerCheck specifically?"

Consider the specific use case: a PhD student or early-career researcher working on a paper about zero-knowledge proofs, consensus mechanisms, or DeFi economics wants to apply for a research grant from a crypto foundation (Ethereum Foundation, Solana Foundation, Cardano's Project Catalyst, etc.).

Today that process is:
- Submit a PDF application
- Wait months for a committee decision
- Receive no standardized quality signal about their work

With PeerCheck:
- Submit the abstract for pre-screening
- Receive an on-chain credibility certificate in minutes
- Attach the verifiable certificate to the grant application
- The foundation can programmatically read the researcher's reputation score

This is not hypothetical. The Ethereum Foundation distributes millions in grants annually. Gitcoin has funded hundreds of academic and research projects. Protocol Labs (Filecoin) has an active research grants program. Every one of these programs currently relies on manual, slow, opaque review with no verifiable quality signal. PeerCheck introduces exactly that.

---

## 3. "Why does peer review need to be on-chain? You could just use a centralized database."

You could. But a centralized database introduces a trusted intermediary someone controls it, someone can edit it, someone can delete entries.

On-chain storage provides three things a database cannot:
1. **Verifiability**: anyone can confirm a certificate exists, when it was issued, and what it concluded, without trusting a third party
2. **Portability**: the certificate is tied to the researcher's wallet, not to PeerCheck's platform. If PeerCheck shuts down tomorrow, every certificate issued still exists permanently on-chain
3. **Programmability**: other smart contracts (DAOs, grant systems, hackathon platforms) can read reputation scores directly without API calls or platform agreements

The value is not that blockchain makes the AI evaluation more correct. The value is that it makes the evaluation process permanently auditable and the results permanently portable.

---

## 4. "AI can't actually evaluate research quality. It hallucinates and lacks domain expertise."

This is a fair concern with an important clarification: PeerCheck is a **pre-screening layer**, not a replacement for expert review.

PeerCheck evaluates abstracts for surface-level credibility signals, the kind of signals a reasonably informed reader can assess without deep domain expertise: Is the methodology described clearly? Are the claims proportionate to what the data can support? Does the logic flow? Are there red flags like scope overclaiming or weak citation framing?

These are the same signals a journal editor uses when making a desk-rejection decision before the paper ever reaches a domain expert. PeerCheck automates and decentralizes that first-pass check.

For deep domain validity statistical rigor, novel contribution, correctness of mathematical proofs human experts remain irreplaceable. PeerCheck does not claim otherwise.

---
## 5. "The A-F grading system is too simplistic. It reduces complex research to a single number."

Single-number scores are reductive by nature but they are widely used precisely because they provide actionable signal at scale. h-index, impact factor, journal tier, grant scores, and SAT scores all share this limitation. The question is not whether a single number is perfect. It is whether it is *useful*.

PeerCheck's certificate includes more than a grade: methodology, citations, and logic are scored separately, risk flags are identified, and a reasoning summary is provided. The grade is an entry point, not the full picture.

For the specific use case of pre-screening filtering 500 hackathon submissions, prioritizing grant applications, surfacing papers for journal editors a consistent, fast, verifiable signal is more useful than no signal at all.

---

## 6. "This could be gamed. People will optimize abstracts to score well rather than do good research."

Yes, and this is called Goodhart's Law: when a measure becomes a target, it ceases to be a good measure. Every evaluation system faces this.

The mitigation is that PeerCheck is explicitly a pre-screening layer with no gatekeeping authority. It cannot block publication, deny grants, or prevent anyone from doing anything. A researcher who games their abstract to score an A still has to submit the full paper to human reviewers. Gaming PeerCheck provides a certificate it does not bypass the actual peer review process.

Additionally, the flags system is specifically designed to catch common gaming patterns: scope overclaiming, weak citation framing, and logical inconsistency are all flagged and visible to anyone reading the certificate.

---

## 7. "There is no proven adoption or benchmarking vs human reviewers. This is vaporware."

PeerCheck was built in 2 weeks as a hackathon prototype. It is not a production system the README says this explicitly. It is a proof of concept demonstrating that decentralized AI peer review is technically feasible on GenLayer.

The relevant question for a hackathon submission is: does it demonstrate a valid use of the technology in a meaningful domain? PeerCheck uses GenLayer's Optimistic Democracy and Equivalence Principle in a way that is fundamental to the application's value not decorative. The contract is deployed on Bradbury testnet. Transactions are verifiable on the explorer. The technical implementation is real.

Benchmarking vs human reviewers, longitudinal adoption studies, and domain calibration are post-hackathon work the same kind of work that CertiK, Chainlink, and every other infrastructure project continued after their initial demos.

---

## 8. "Why GenLayer specifically? Couldn't this be done with an off-chain AI service and an on-chain record?"

You could build a system where an off-chain service calls OpenAI, gets a result, and writes a hash on-chain. Many projects do this. The problems are:

1. **Trust in the off-chain oracle**  who runs it? Who can modify the result before it is written on-chain?
2. **No validator consensus** one API call produces one result. There is no mechanism to detect if the result was manipulated or the API was compromised.
3. **No programmable non-determinism handling**  different AI models produce different scores. An off-chain system has no principled way to reconcile this. GenLayer's Equivalence Principle solves this natively.

GenLayer's value is not just LLM access on-chain. It is *decentralized consensus over non-deterministic AI outputs*. That is the specific primitive PeerCheck needs and it exists only on GenLayer.

---

## 9. "Academia is conservative. They will never adopt a blockchain-based system."

Institutional change is slow, but the market for this does not require institutional adoption first.

The immediate market is the **crypto-native research community**: researchers writing papers on cryptography, consensus mechanisms, DeFi economics, ZK proofs, and formal verification. This community already operates on-chain, already uses wallets, and already submits to crypto foundations for grants. They do not need to convince a traditional journal to accept PeerCheck they are the initial market.

As on-chain reputation becomes a standard signal in crypto grant programs and hackathons, the network effects grow. Traditional academia follows when the tooling becomes unavoidable the same pattern followed by Git (dismissed by traditional developers), arXiv (dismissed by traditional journals), and open-source licenses (dismissed by traditional IP law).

PeerCheck builds the infrastructure now for a market that is already emerging.

---

*Built by Aqeelerh. Bradbury Builders Hackathon 2026*
