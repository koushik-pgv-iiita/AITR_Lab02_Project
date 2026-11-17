import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.drift_engine import FormattingDriftEngine

def run_drift_engine_sanity_test():
    print("=" * 60)
    print("      UNIT TEST: STATISTICAL DRIFT ENGINE MODULE")
    print("=" * 60)
    
    engine = FormattingDriftEngine(sample_size=100)
    
    p_base = 0.95
    p_quant = 0.75
    
    metrics = engine.calculate_drift_and_significance(p_base, p_quant)
    
    print(f"[+] Baseline Pass Rate (P_base): {metrics['p_base'] * 100}%")
    print(f"[+] Quantized Pass Rate (P_quant): {metrics['p_quant'] * 100}%")
    print(f"[+] Relative Drift (D_formatting): {metrics['d_formatting_percent']}%")
    print(f"[+] Z-Statistic: {metrics['z_statistic']}")
    print(f"[+] p-value: {metrics['p_value']}")
    print(f"[+] Statistically Significant (p < 0.05): {metrics['is_significant_p005']}")
    
    # Assertions
    assert metrics["d_formatting_percent"] == -21.05, f"Expected -21.05%, got {metrics['d_formatting_percent']}"
    assert metrics["is_significant_p005"] is True, "Expected significance to be True"
    assert type(metrics["is_significant_p005"]) is bool, "Expected native Python bool"
    assert metrics["z_statistic"] < -3.0, "Expected significant negative Z score"

    print("=" * 60)
    print("UNIT TEST RESULT: PASSED (Drift engine math verified)")
    print("=" * 60)

if __name__ == "__main__":
    run_drift_engine_sanity_test()