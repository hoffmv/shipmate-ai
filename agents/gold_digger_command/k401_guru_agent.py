
# k401_guru_agent.py

from typing import List, Dict
from utils.financial_memory import FinancialMemory


class K401GuruAgent:
    def __init__(self):
        self.memory = FinancialMemory()
        self.funds = self._load_funds()

    def _load_funds(self) -> List[Dict]:
        return self.memory.list_records("401k_funds")

    def recommend_allocations(self, risk_profile: str, enforce_multiples: bool = True) -> List[Dict]:
        funds = self._load_funds()

        def risk_match_score(fund_risk, user_risk):
            if fund_risk == user_risk:
                return 2
            if user_risk == "moderate" and fund_risk in ("low", "high"):
                return 1
            if fund_risk == "moderate" and user_risk in ("low", "high"):
                return 1
            return 0

        for fund in funds:
            fund['risk_match'] = risk_match_score(fund['risk_level'], risk_profile)

        sorted_funds = sorted(
            funds,
            key=lambda f: (f['risk_match'], f['performance_score']),
            reverse=True
        )

        n_funds = len(sorted_funds)
        allocations = [0] * n_funds
        maxes = [min(100, int(f['max_allowed_allocation'])) for f in sorted_funds]

        def next_step(val):
            if enforce_multiples:
                return max(5, (val // 5) * 5)
            return max(1, int(val))

        total_weight = 0
        weights = []
        for fund in sorted_funds:
            risk_weight = 2 if fund['risk_match'] == 2 else (1 if fund['risk_match'] == 1 else 0.5)
            perf_weight = fund['performance_score'] / 100.0
            weight = risk_weight * (1 + perf_weight)
            weights.append(weight)
            total_weight += weight

        raw_allocs = []
        for i, fund in enumerate(sorted_funds):
            alloc = (weights[i] / total_weight) * 100
            alloc = min(alloc, maxes[i])
            raw_allocs.append(alloc)

        rounded_allocs = []
        for i, alloc in enumerate(raw_allocs):
            rounded = int(round(alloc / 5.0) * 5) if enforce_multiples else int(round(alloc))
            rounded = min(rounded, maxes[i])
            rounded_allocs.append(rounded)

        total = sum(rounded_allocs)
        diff = 100 - total

        def adjust_allocations(allocs, diff, maxes, enforce_multiples):
            step = 5 if enforce_multiples else 1
            direction = 1 if diff > 0 else -1
            diff = abs(diff)
            while diff > 0:
                changed = False
                for i in range(len(allocs)):
                    if direction > 0:
                        if allocs[i] + step <= maxes[i]:
                            allocs[i] += step
                            diff -= step
                            changed = True
                    else:
                        if allocs[i] - step >= 0:
                            allocs[i] -= step
                            diff -= step
                            changed = True
                    if diff <= 0:
                        break
                if not changed:
                    break
            return allocs

        if total != 100:
            rounded_allocs = adjust_allocations(rounded_allocs, diff, maxes, enforce_multiples)
            total = sum(rounded_allocs)
            if total != 100:
                step = 5 if enforce_multiples else 1
                for i in range(len(rounded_allocs)):
                    if total < 100 and rounded_allocs[i] + step <= maxes[i]:
                        rounded_allocs[i] += step
                        total += step
                    elif total > 100 and rounded_allocs[i] - step >= 0:
                        rounded_allocs[i] -= step
                        total -= step
                    if total == 100:
                        break

        recommendations = []
        for i, fund in enumerate(sorted_funds):
            reason_parts = []
            if fund['risk_match'] == 2:
                reason_parts.append("Matches risk profile")
            elif fund['risk_match'] == 1:
                reason_parts.append("Partial risk profile match")
            else:
                reason_parts.append("Lower risk match")
            if fund['performance_score'] >= 90:
                reason_parts.append("Top performer")
            elif fund['performance_score'] >= 75:
                reason_parts.append("Strong performer")
            elif fund['performance_score'] >= 60:
                reason_parts.append("Solid performer")
            else:
                reason_parts.append("Lower recent performance")
            recommendations.append({
                "fund": fund['name'],
                "suggested_allocation": rounded_allocs[i],
                "reason": " and ".join(reason_parts)
            })

        return recommendations
