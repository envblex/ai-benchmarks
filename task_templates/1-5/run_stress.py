#!/usr/bin/env python3
import subprocess
import sys

def main():
    runs = 30
    failed = 0
    print(f"[*] Running stress test ({runs} iterations)...")
    for i in range(runs):
        res = subprocess.run(["python3", "-m", "pytest", "tests/test_fanout.py"], capture_output=True, text=True)
        if res.returncode != 0:
            failed += 1
            print(f"[-] Iteration {i+1}: FAILED")
            print(res.stdout)
            break
        else:
            print(f"[+] Iteration {i+1}: passed", end="\r")

    if failed > 0:
        print(f"\n[FAIL] Flaky test reproduced! Failed on run with assertion error.")
        sys.exit(1)
    else:
        print(f"\n[SUCCESS] Deterministic pass: 0 failures across {runs} runs.")
        sys.exit(0)

if __name__ == "__main__":
    main()
