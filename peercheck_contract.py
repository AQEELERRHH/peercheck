# {"Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0"}

from genlayer import *

import json
import hashlib
import typing


class PeerCheck(gl.Contract):
    certificates: TreeMap[str, str]
    profiles: TreeMap[str, str]
    submission_count: u256
    submission_fee: u256
    treasury: u256

    def __init__(self, submission_fee: u256):
        self.submission_count = u256(0)
        self.submission_fee = submission_fee
        self.treasury = u256(0)

    @gl.public.write
    def submit_paper(self, abstract: str, link: str) -> typing.Any:
        if len(abstract.strip()) < 100:
            raise Exception("Abstract too short.")
        if not (link.startswith("http://") or link.startswith("https://")):
            raise Exception("Invalid link.")

        submitter = str(gl.message.sender_address)
        canonical = f"{abstract.strip()}|{link.strip()}"
        paper_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

        if self.certificates.get(paper_hash, None) is not None:
            return paper_hash

        def evaluate_paper() -> str:
            task = (
                'Evaluate this research paper abstract as an academic peer reviewer.\n\n'
                f'ABSTRACT: {abstract[:500]}\n\n'
                'Return ONLY a JSON object with these exact keys:\n'
                '{"methodology": 75, "citations": 70, "logic": 72, "score": 72, '
                '"flags": "no_issues", "reasoning": "Brief one sentence evaluation."}\n\n'
                'Rules:\n'
                '- All scores must be integers between 0 and 100\n'
                '- score = int(methodology*0.4 + citations*0.3 + logic*0.3)\n'
                '- flags must be one or more of: weak_citations, flawed_methodology, '
                'logical_inconsistency, reproducibility_concern, scope_overclaim, no_issues\n'
                '- reasoning must be a single short sentence under 80 characters\n'
                '- Return ONLY the JSON object, no markdown, no explanation'
            )

            raw = gl.exec_prompt(task)

            # Aggressive cleaning
            clean = raw.strip()
            # Remove markdown fences
            if '```' in clean:
                parts = clean.split('```')
                for part in parts:
                    p = part.strip()
                    if p.startswith('json'):
                        p = p[4:].strip()
                    if p.startswith('{'):
                        clean = p
                        break

            # Find the JSON object
            start = clean.find('{')
            end = clean.rfind('}')
            if start != -1 and end != -1:
                clean = clean[start:end+1]

            try:
                parsed = json.loads(clean)
            except Exception:
                # Return safe default if parsing fails
                return json.dumps({
                    "methodology": 65,
                    "citations": 60,
                    "logic": 65,
                    "score": 63,
                    "flags": "no_issues",
                    "reasoning": "Evaluation completed with default scoring."
                }, sort_keys=True)

            # Safely extract and clamp all values
            m = max(0, min(100, int(float(str(parsed.get("methodology", 65))))))
            c = max(0, min(100, int(float(str(parsed.get("citations", 60))))))
            l = max(0, min(100, int(float(str(parsed.get("logic", 65))))))
            s = int(m * 0.4 + c * 0.3 + l * 0.3)

            # Normalize flags
            valid = {
                "weak_citations", "flawed_methodology", "logical_inconsistency",
                "reproducibility_concern", "scope_overclaim", "no_issues"
            }
            raw_flags = str(parsed.get("flags", "no_issues"))
            flags_list = sorted([
                f.strip() for f in raw_flags.replace("|", ",").split(",")
                if f.strip() in valid
            ])
            if not flags_list:
                flags_list = ["no_issues"]

            reasoning = str(parsed.get("reasoning", "Paper evaluated successfully."))[:80]

            return json.dumps({
                "methodology": m,
                "citations": c,
                "logic": l,
                "score": s,
                "flags": ",".join(flags_list),
                "reasoning": reasoning
            }, sort_keys=True)

        raw_result = gl.eq_principle_prompt_non_comparative(
            evaluate_paper,
            task="Evaluate the credibility and quality of this academic research paper abstract.",
            criteria=(
                "Two evaluations are equivalent if the overall score values differ by no more than 20 points, "
                "and methodology, citations, and logic scores each differ by no more than 25 points. "
                "The flags should overlap by at least one value. "
                "The reasoning text may differ freely between validators."
            )
        )

        result = json.loads(raw_result)
        score = max(0, min(100, int(result.get("score", 50))))

        if score >= 85:   grade = "A"
        elif score >= 70: grade = "B"
        elif score >= 55: grade = "C"
        elif score >= 40: grade = "D"
        else:             grade = "F"

        cert = {
            "paper_hash": paper_hash,
            "abstract": abstract[:200],
            "link": link,
            "score": score,
            "grade": grade,
            "flags": result.get("flags", "no_issues"),
            "methodology": result.get("methodology", 50),
            "citations": result.get("citations", 50),
            "logic": result.get("logic", 50),
            "reasoning": result.get("reasoning", ""),
            "submitter": submitter,
        }

        self.certificates[paper_hash] = json.dumps(cert)
        self.submission_count = u256(int(self.submission_count) + 1)
        self.treasury = u256(int(self.treasury) + int(self.submission_fee))
        self._update_profile(submitter, paper_hash, score, grade)

        return cert

    def _update_profile(self, address: str, paper_hash: str, score: int, grade: str) -> None:
        existing_raw = self.profiles.get(address, None)
        if existing_raw is None:
            profile = {
                "address": address, "total_submissions": 1,
                "average_score": score, "highest_score": score,
                "lowest_score": score, "total_score_sum": score,
                "grade_a": 1 if grade=="A" else 0,
                "grade_b": 1 if grade=="B" else 0,
                "grade_c": 1 if grade=="C" else 0,
                "grade_d": 1 if grade=="D" else 0,
                "grade_f": 1 if grade=="F" else 0,
                "reputation_level": "NOVICE",
                "paper_hashes": paper_hash,
            }
        else:
            p = json.loads(existing_raw)
            new_total = p["total_submissions"] + 1
            new_sum   = p["total_score_sum"] + score
            profile = {
                "address": address,
                "total_submissions": new_total,
                "average_score": new_sum // new_total,
                "highest_score": max(p["highest_score"], score),
                "lowest_score": min(p["lowest_score"], score),
                "total_score_sum": new_sum,
                "grade_a": p["grade_a"] + (1 if grade=="A" else 0),
                "grade_b": p["grade_b"] + (1 if grade=="B" else 0),
                "grade_c": p["grade_c"] + (1 if grade=="C" else 0),
                "grade_d": p["grade_d"] + (1 if grade=="D" else 0),
                "grade_f": p["grade_f"] + (1 if grade=="F" else 0),
                "reputation_level": self._compute_reputation(new_sum // new_total, new_total),
                "paper_hashes": p["paper_hashes"] + "," + paper_hash,
            }
        self.profiles[address] = json.dumps(profile)

    def _compute_reputation(self, avg: int, total: int) -> str:
        if total >= 20 and avg >= 85:   return "LUMINARY"
        elif total >= 10 and avg >= 75: return "EXPERT"
        elif total >= 5 and avg >= 65:  return "ESTABLISHED"
        elif total >= 3 and avg >= 50:  return "CONTRIBUTOR"
        else:                            return "NOVICE"

    @gl.public.view
    def get_certificate(self, paper_hash: str) -> dict[str, typing.Any]:
        raw = self.certificates.get(paper_hash, None)
        if raw is None:
            return {"error": f"No certificate found for '{paper_hash}'"}
        return json.loads(raw)

    @gl.public.view
    def get_all_certificates(self) -> list[typing.Any]:
        items = []
        for key in self.certificates:
            cert = json.loads(self.certificates[key])
            items.append({
                "paper_hash": cert.get("paper_hash",""),
                "link": cert.get("link",""),
                "score": cert.get("score",0),
                "grade": cert.get("grade",""),
                "flags": cert.get("flags",""),
                "submitter": cert.get("submitter",""),
            })
        return items

    @gl.public.view
    def get_profile(self, address: str) -> dict[str, typing.Any]:
        raw = self.profiles.get(address, None)
        if raw is None:
            return {"error": f"No profile found for '{address}'"}
        p = json.loads(raw)
        return {
            "address": p["address"],
            "total_submissions": p["total_submissions"],
            "average_score": p["average_score"],
            "highest_score": p["highest_score"],
            "lowest_score": p["lowest_score"],
            "reputation_level": p["reputation_level"],
            "grade_breakdown": {
                "A": p["grade_a"], "B": p["grade_b"],
                "C": p["grade_c"], "D": p["grade_d"], "F": p["grade_f"]
            },
            "paper_hashes": p["paper_hashes"].split(",") if p["paper_hashes"] else [],
        }

    @gl.public.view
    def get_reputation_level(self, address: str) -> str:
        raw = self.profiles.get(address, None)
        if raw is None:
            return "NOVICE"
        return json.loads(raw).get("reputation_level", "NOVICE")

    @gl.public.view
    def get_submission_count(self) -> u256:
        return self.submission_count

    @gl.public.view
    def get_fee(self) -> u256:
        return self.submission_fee