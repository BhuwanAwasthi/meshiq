"""
score_eval.py
Scores MeshIQ pipeline output against the ground-truth answer key.

Inputs:
  - ground_truth.csv : the answer key (file, expected_type, expected_target, expected_outcome)
  - results.csv      : exported from Dataverse (file, recording_type, detected_target,
                       routing_decision, overall_score, recommendation)

It matches rows by the transcript file name and reports:
  - Routing accuracy (type correct)
  - Target identification accuracy (correct client/job)
  - Outcome accuracy (pass/fail or hire/no-hire matches expectation)

Usage: python score_eval.py ground_truth.csv results.csv
"""

import csv
import sys
from collections import defaultdict


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm(s):
    return (s or "").strip().lower()


def outcome_matches(expected, recommendation, score):
    """Flexible outcome check across interview + qa shapes."""
    e = norm(expected)
    rec = norm(recommendation)
    # interview outcomes
    if "hire" in e:
        if "no" in e or "no_hire" in e.replace(" ", "_"):
            return "no_hire" in rec or "strong_no" in rec
        return rec in ("hire", "strong_hire")
    # qa outcomes
    if "pass" in e:
        return rec == "pass" or (score is not None and score >= 80)
    if "fail" in e:
        return rec == "fail" or (score is not None and score < 80)
    return None  # unknown shape, skip


def main():
    gt_path = sys.argv[1] if len(sys.argv) > 1 else "ground_truth.csv"
    res_path = sys.argv[2] if len(sys.argv) > 2 else "results.csv"

    gt = {norm(r["file"]): r for r in load(gt_path)}
    res = {norm(r["file"]): r for r in load(res_path)}

    totals = defaultdict(int)
    rows = []

    for fname, g in gt.items():
        r = res.get(fname)
        if not r:
            rows.append((fname, "MISSING", "-", "-", "-"))
            totals["missing"] += 1
            continue

        totals["n"] += 1

        type_ok = norm(g["expected_type"]) == norm(r.get("recording_type"))
        target_ok = norm(g["expected_target"]) == norm(r.get("detected_target"))

        try:
            score = float(r.get("overall_score") or "nan")
        except ValueError:
            score = None
        out_ok = outcome_matches(g["expected_outcome"], r.get("recommendation"), score)

        totals["type_ok"] += int(type_ok)
        totals["target_ok"] += int(target_ok)
        if out_ok is not None:
            totals["outcome_n"] += 1
            totals["outcome_ok"] += int(out_ok)

        rows.append((
            fname,
            "OK" if type_ok else "WRONG",
            "OK" if target_ok else "WRONG",
            ("OK" if out_ok else "WRONG") if out_ok is not None else "n/a",
            r.get("overall_score", "-"),
        ))

    def pct(a, b):
        return f"{(100.0 * a / b):.0f}%" if b else "n/a"

    print("\n=== MeshIQ Evaluation Results ===\n")
    print(f"{'transcript':<32} {'type':<6} {'target':<7} {'outcome':<8} {'score'}")
    print("-" * 64)
    for row in rows:
        print(f"{row[0]:<32} {row[1]:<6} {row[2]:<7} {row[3]:<8} {row[4]}")

    n = totals["n"]
    print("\n--- Summary ---")
    print(f"Transcripts scored:        {n}")
    print(f"Routing (type) accuracy:   {pct(totals['type_ok'], n)}  ({totals['type_ok']}/{n})")
    print(f"Target ID accuracy:        {pct(totals['target_ok'], n)}  ({totals['target_ok']}/{n})")
    print(f"Outcome accuracy:          {pct(totals['outcome_ok'], totals['outcome_n'])}  ({totals['outcome_ok']}/{totals['outcome_n']})")
    if totals["missing"]:
        print(f"Missing from results:      {totals['missing']}")
    print()


if __name__ == "__main__":
    main()
