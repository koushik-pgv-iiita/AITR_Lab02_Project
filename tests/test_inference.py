import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.inference import LocalInferenceEngine

def run_inference_sanity_test():
    print("=" * 60)
    print("      UNIT TEST: LOCAL INFERENCE ENGINE MODULE")
    print("=" * 60)
    
    engine = LocalInferenceEngine(model_id="Qwen/Qwen2.5-0.5B-Instruct", device="cpu")
    
    sample_context = "User ID u_1001 registered under email test@example.org with score 95.0."
    sample_schema = {
        "title": "UserProfile",
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "email": {"type": "string"},
            "score": {"type": "number"}
        },
        "required": ["user_id", "email", "score"]
    }
    
    # 1. Check prompt formatting logic
    formatted_user_prompt = engine.format_user_prompt(sample_context, sample_schema)
    print("[+] Formatted Prompt Test:")
    print("    " + formatted_user_prompt.replace("\n", "\n    "))
    
    assert "Context:" in formatted_user_prompt
    assert "Required JSON Schema:" in formatted_user_prompt
    assert "user_id" in formatted_user_prompt
    
    # 2. Test Model Loading & Generation (Downloads ~1GB lightweight model on first run)
    print("\n[+] Testing live model loading and generation...")
    try:
        engine.load_model()
        completion = engine.generate_completion(sample_context, sample_schema, max_new_tokens=128)
        print("\n[+] Live Generation Output:")
        print(f"    {completion}")
        assert len(completion) > 0, "Completion returned empty string!"
        
        print("\n=" * 60)
        print("UNIT TEST RESULT: PASSED (Inference engine verified)")
        print("=" * 60)
    except Exception as e:
        print(f"\n[-] Model load/inference error: {e}")
        print("[-] Note: Ensure internet access is available to download 'Qwen/Qwen2.5-0.5B-Instruct'.")
        sys.exit(1)

if __name__ == "__main__":
    run_inference_sanity_test()