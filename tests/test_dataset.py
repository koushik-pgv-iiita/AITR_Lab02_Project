import os
import sys

# Ensure src module is visible in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dataset import BenchmarkDatasetLoader

def run_dataset_sanity_test():
    print("=" * 60)
    print("      UNIT TEST: DATA LOADING & VALIDATION MODULE")
    print("=" * 60)
    
    loader = BenchmarkDatasetLoader("data/json_schema_eval_100.jsonl")
    
    try:
        data = loader.load_and_validate()
        print(f"[+] Load Success: Loaded {len(data)} items.")
        
        # Test Sample Record #1
        sample = data[0]
        print(f"[+] Sample Record [0] ID: {sample['id']}")
        print(f"[+] Sample Record [0] Tier: {sample['schema_tier']}")
        print(f"[+] Sample Record [0] Schema Keys: {list(sample['pydantic_schema']['properties'].keys())}")
        
        # Test Tier Partitioning
        tier1_items = loader.get_partition_by_tier("Tier 1: Primitive Flat")
        tier2_items = loader.get_partition_by_tier("Tier 2: Nested Object")
        tier3_items = loader.get_partition_by_tier("Tier 3: Typed Array")
        
        print(f"[+] Partition Check -> Tier 1: {len(tier1_items)}, Tier 2: {len(tier2_items)}, Tier 3: {len(tier3_items)}")
        
        assert len(data) == 100, "Total count failed!"
        assert len(tier1_items) == 35, "Tier 1 count failed!"
        assert len(tier2_items) == 35, "Tier 2 count failed!"
        assert len(tier3_items) == 30, "Tier 3 count failed!"
        
        print("=" * 60)
        print("UNIT TEST RESULT: PASSED (All assertions verified)")
        print("=" * 60)
        
    except Exception as e:
        print(f"[-] UNIT TEST FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_dataset_sanity_test()