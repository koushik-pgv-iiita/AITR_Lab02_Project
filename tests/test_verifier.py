import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.verifier import DualPassSchemaVerifier

def run_verifier_sanity_tests():
    print("=" * 60)
    print("      UNIT TEST: DUAL-PASS SCHEMA VERIFIER MODULE")
    print("=" * 60)
    
    verifier = DualPassSchemaVerifier()
    
    sample_schema = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["user_id", "age"]
    }
    
    # Case 1: Direct Clean Pass
    raw_clean = '{"user_id": "u_101", "age": 25}'
    res1 = verifier.verify_completion(raw_clean, sample_schema)
    print(f"[+] Case 1 (Direct Pass): Mode={res1['pass_mode']}, Strict={res1['strict_raw_pass']}")
    assert res1["strict_raw_pass"] is True
    assert res1["pass_mode"] == "DIRECT_PASS"
    
    # Case 2: Markdown Fence Violation (Scrubbed Pass)
    raw_markdown = '```json\n{"user_id": "u_102", "age": 30}\n```'
    res2 = verifier.verify_completion(raw_markdown, sample_schema)
    print(f"[+] Case 2 (Markdown Pass): Mode={res2['pass_mode']}, Strict={res2['strict_raw_pass']}, Category={res2['error_category']}")
    assert res2["strict_raw_pass"] is False
    assert res2["scrubbed_pass"] is True
    assert res2["pass_mode"] == "SCRUBBED_PASS"
    assert res2["error_category"] == "MARKDOWN_FENCE_VIOLATION"
    
    # Case 3: Syntax Error (Invalid JSON)
    raw_invalid = '{"user_id": "u_103", "age": 25,'
    res3 = verifier.verify_completion(raw_invalid, sample_schema)
    print(f"[+] Case 3 (Syntax Fail): Mode={res3['pass_mode']}, Category={res3['error_category']}")
    assert res3["scrubbed_pass"] is False
    assert res3["error_category"] == "SYNTAX_ERROR"
    
    # Case 4: Schema Type Mismatch
    raw_type_err = '{"user_id": "u_104", "age": "twenty-five"}'
    res4 = verifier.verify_completion(raw_type_err, sample_schema)
    print(f"[+] Case 4 (Type Mismatch): Mode={res4['pass_mode']}, Category={res4['error_category']}")
    assert res4["scrubbed_pass"] is False
    assert res4["error_category"] == "SCHEMA_TYPE_MISMATCH"

    print("=" * 60)
    print("UNIT TEST RESULT: PASSED (All 4 verification cases verified)")
    print("=" * 60)

if __name__ == "__main__":
    run_verifier_sanity_tests()