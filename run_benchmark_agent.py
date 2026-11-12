#!/usr/bin/env python3
"""
ai-benchmarks v4 Deterministic ReAct Agent Runner (Hardened Sandbox Edition)
Evaluates LLM models by allowing interactive terminal execution in Podman sandbox.
Features:
- Physical host-level sandbox purge before every trial (zero residual files)
- Forced PYTHONDONTWRITEBYTECODE=1 to prevent .pyc cache pollution
- Automatic assertion of initial FAIL state (aborts defective templates)
- Dynamic Early Exit on test pass to save tokens and avoid turn timeouts
- Strict task scoping to implemented task templates
"""
import os
import sys
import json
import time
import shutil
import argparse
import subprocess
import urllib.request
import urllib.error
import re
from datetime import datetime

BASE_DIR = "/home/takayoshi/workspace/projects/ai-benchmarks"
RUNS_DIR = os.path.join(BASE_DIR, "benchmark_runs")
SANDBOX_HOST_DIR = "/home/takayoshi/workspace/lab/bench-sandbox"
os.makedirs(RUNS_DIR, exist_ok=True)

DEFAULT_TEMPS = [0.2, 0.3, 0.4, 0.5, 0.6]
MAX_TURNS_PER_TRIAL = 15
COMMAND_TIMEOUT_SEC = 45
MAX_OUTPUT_CHARS = 3000

SYSTEM_PROMPT = """You are an expert autonomous software engineer solving an engineering problem in an Ubuntu Linux sandbox environment (/workspace).
You can investigate the environment, read files, edit code, and run tests by executing Bash shell commands.

CRITICAL INSTRUCTIONS:
1. You have access to a single Bash shell execution environment.
2. To run commands, write them inside a single ```bash ... ``` code block, or call `<tool_call> bash<param_key>command</param_key><param_value>YOUR_BASH_COMMAND</param_value></tool_call>`.
3. To inspect files, use `cat <path>` or `head`/`tail`. To edit files, use `python3 -c ...`, `sed`, or heredocs (`cat << 'EOF' > ...`).
4. Keep commands focused and decisive (e.g. inspecting logs, reading files, patching files, running pytest).
5. When you have resolved the issue and verified your fix with tests, print "COMPLETE" on its own line to submit your solution.
"""

TASK_CONFIGS = {
    "1-1": {
        "sub_dir": "proxy_service",
        "init_cmd": "chmod +x /workspace/proxy_service/start.sh && cd /workspace/proxy_service && ./start.sh",
        "test_cmd": "cd /workspace/proxy_service && pytest -v tests/test_proxy.py 2>&1"
    },
    "1-2": {
        "sub_dir": "",
        "init_cmd": "",
        "test_cmd": "cd /workspace && PYTHONPATH=. pytest -v tests/test_security.py 2>&1"
    },
    "1-3": {
        "sub_dir": "",
        "init_cmd": "",
        "test_cmd": "cd /workspace && PYTHONPATH=. pytest -v tests/test_leak.py 2>&1"
    },
    "1-4": {
        "sub_dir": "",
        "init_cmd": "chmod +x /workspace/scripts/verify_repo.sh",
        "test_cmd": "cd /workspace && ./scripts/verify_repo.sh 2>&1"
    },
    "1-5": {
        "sub_dir": "",
        "init_cmd": "",
        "test_cmd": "cd /workspace && python3 run_stress.py 2>&1"
    }
}

def clean_sandbox_completely():
    """Physically delete all files in host sandbox and kill any leftover container processes."""
    # 1. Clean host directory
    if os.path.exists(SANDBOX_HOST_DIR):
        for item in os.listdir(SANDBOX_HOST_DIR):
            item_path = os.path.join(SANDBOX_HOST_DIR, item)
            try:
                if os.path.islink(item_path) or os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
            except Exception as e:
                print(f"[!] Clean error on host file {item_path}: {e}")
    os.makedirs(SANDBOX_HOST_DIR, exist_ok=True)
    try:
        os.chmod(SANDBOX_HOST_DIR, 0o777)
    except Exception:
        pass

    # 2. Kill leftover container daemons and wipe /tmp in container
    try:
        subprocess.run(
            ["podman", "exec", "bench-box", "bash", "-c", 
             "pkill -9 -f uvicorn 2>/dev/null || true; pkill -9 -f python3 2>/dev/null || true; rm -rf /tmp/* /tmp/.* 2>/dev/null || true"],
            timeout=10, capture_output=True, text=True, check=False
        )
    except Exception as e:
        print(f"[!] Warning cleaning container /tmp: {e}")

def exec_sandbox_command(cmd, timeout=COMMAND_TIMEOUT_SEC):
    # Enforce PYTHONDONTWRITEBYTECODE=1 to eradicate __pycache__ pollution
    full_cmd = ["podman", "exec", "-e", "PYTHONDONTWRITEBYTECODE=1", "bench-box", "bash", "-c", cmd]
    try:
        res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
        stdout = res.stdout
        stderr = res.stderr
        exit_code = res.returncode
    except subprocess.TimeoutExpired:
        stdout = ""
        stderr = f"[TIMEOUT] Command timed out after {timeout} seconds."
        exit_code = 124
    except Exception as e:
        stdout = ""
        stderr = f"[EXEC_ERROR] {str(e)}"
        exit_code = -1

    # Truncate output if too long
    if len(stdout) > MAX_OUTPUT_CHARS:
        stdout = stdout[:1000] + f"\n... [truncated {len(stdout) - 2000} chars] ...\n" + stdout[-1000:]
    if len(stderr) > MAX_OUTPUT_CHARS:
        stderr = stderr[:1000] + f"\n... [truncated {len(stderr) - 2000} chars] ...\n" + stderr[-1000:]

    return stdout, stderr, exit_code

def check_task_passed(task_id, stdout, exit_code):
    """Deterministic grading check for a task."""
    stdout_l = stdout.lower() if stdout else ""
    if task_id in ["1-1", "1-2", "1-3"]:
        return (exit_code == 0) and ("failed" not in stdout_l) and ("passed" in stdout_l)
    elif task_id in ["1-4", "1-5"]:
        return (exit_code == 0) and ("[success]" in stdout_l or "success" in stdout_l)
    else:
        return exit_code == 0

def extract_bash_commands(text):
    if not text:
        return ""
    # 0. LFM2.5 native tool call format (<|tool_call_start|>[bash(command='...')]<|tool_call_end|>)
    if "<|tool_call_start|>" in text or "bash(command=" in text:
        m_lfm = re.findall(r"bash\(command=['\"](.*?)['\"]\)", text, re.DOTALL)
        if m_lfm:
            cmds = [m.strip() for m in m_lfm if m.strip()]
            if cmds:
                return "\n".join(cmds)

    # 1. Xing4.0 native tool call format (bash / read / write tools)
    if "<param_key>" in text or ("<tool_call>" in text and "bash" in text):
        cmds = []
        # 1. bash command: <param_key>command</param_key><param_value>...</param_value>
        m_bash = re.findall(r"<param_key>(?:command|cmd)</param_key>\s*<param_value>(.*?)</param_value>", text, re.DOTALL | re.IGNORECASE)
        for b in m_bash:
            if b.strip():
                cmds.append(b.strip())
        
        # 2. read tool: <tool_call> read<param_key>filePath</param_key><param_value>...</param_value></tool_call>
        m_read = re.findall(r"<param_key>(?:filePath|file_path|path)</param_key>\s*<param_value>(.*?)</param_value>", text, re.DOTALL | re.IGNORECASE)
        for r in m_read:
            if r.strip():
                cmds.append(f"echo '===== {r.strip()} =====' && cat '{r.strip()}'")
                
        if cmds:
            return "\n".join(cmds)

    # 1. Ornith / Claude-style native tool call format (<tool_call> ... <parameter=command>...</parameter> ...)
    if "<tool_call>" in text or "<function=" in text or "<parameter=" in text:
        matches = re.findall(r"<parameter=(?:command|cmd)>(.*?)</parameter>", text, re.DOTALL | re.IGNORECASE)
        if matches:
            cmds = [m.strip() for m in matches if m.strip()]
            if cmds:
                return "\n".join(cmds)
        m_func = re.search(r"<function=(?:bash|Bash|sh|shell)>(.*?)</function>", text, re.DOTALL | re.IGNORECASE)
        if m_func and m_func.group(1).strip():
            cmd = m_func.group(1).strip()
            m_nested = re.search(r"<parameter=(?:command|cmd)>(.*?)</parameter>", cmd, re.DOTALL | re.IGNORECASE)
            if m_nested and m_nested.group(1).strip():
                return m_nested.group(1).strip()
            return cmd

    # 2. K2-Horizon IFM native tool call format
    if "<ifm|tool_call" in text or "<ifm|arg_key>command" in text or "<ifm|tool_calls>" in text:
        matches = re.findall(r"<ifm\|arg_key>command</ifm\|arg_key>\s*<ifm\|arg_value>(.*?)(?:</ifm\|arg_value>|<ifm\||$)", text, re.DOTALL)
        if matches:
            cmds = [m.strip() for m in matches if m.strip()]
            if cmds:
                return "\n".join(cmds)

    # 3. Standard markdown bash code blocks (support multiple blocks)
    matches = re.findall(r"```bash(.*?)```", text, re.DOTALL)
    if matches:
        cmds = [m.strip() for m in matches if m.strip()]
        if cmds:
            return "\n".join(cmds)

    matches_generic = re.findall(r"```(?:sh|shell)(.*?)```", text, re.DOTALL)
    if matches_generic:
        cmds = [m.strip() for m in matches_generic if m.strip()]
        if cmds:
            return "\n".join(cmds)

    # 4. Fallback: generic code block if command detected
    m_code = re.findall(r"```(.*?)```", text, re.DOTALL)
    if m_code and m_code[0].strip():
        first_line = m_code[0].strip().split("\n")[0]
        if any(c in first_line for c in ["cd ", "ls", "find ", "cat ", "grep ", "git ", "pytest", "python"]):
            return m_code[0].strip()
    return ""

def query_llm(api_url, messages, temperature=0.2, max_tokens=4096, retries=4):
    curr_messages = list(messages)
    last_err = None
    for attempt in range(retries):
        try:
            payload = {
                "messages": curr_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=120) as resp:
                res = json.loads(resp.read().decode("utf-8"))
            dur = time.time() - t0
            
            choice = res["choices"][0]
            msg = choice.get("message", {})
            content = msg.get("content", "") or ""
            reasoning = msg.get("reasoning_content", "") or ""
            
            usage = res.get("usage", {})
            p_toks = usage.get("prompt_tokens", 0)
            c_toks = usage.get("completion_tokens", 0)
            tok_s = c_toks / dur if dur > 0 else 0
            
            return {
                "content": content,
                "reasoning": reasoning,
                "duration": dur,
                "prompt_tokens": p_toks,
                "completion_tokens": c_toks,
                "tok_s": tok_s
            }
        except urllib.error.HTTPError as e:
            last_err = e
            print(f"[!] API call HTTP {e.code} retry {attempt+1}/{retries}: {e}")
            if e.code == 400 and len(curr_messages) > 3:
                print("[!] 400 Bad Request detected (likely context overflow) -> Truncating old turns...")
                # Keep system prompt (idx 0) and initial user prompt (idx 1), truncate middle
                curr_messages = [curr_messages[0], curr_messages[1]] + curr_messages[4:]
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = e
            print(f"[!] API call retry {attempt+1}/{retries} due to: {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to query LLM after {retries} retries: {last_err}")

def load_or_init_results(model_slug):
    res_path = os.path.join(RUNS_DIR, f"results_{model_slug}.json")
    if os.path.exists(res_path):
        try:
            with open(res_path, "r") as f:
                return json.load(f), res_path
        except Exception:
            pass
    init_data = {
        "model_slug": model_slug,
        "benchmark_version": "v4_hardened",
        "started_at": datetime.now().isoformat(),
        "tasks": {}
    }
    return init_data, res_path

def save_results(data, res_path):
    tmp_path = res_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, res_path)

def run_trial(api_url, task, temperature, max_turns=MAX_TURNS_PER_TRIAL):
    task_id = task["id"]
    task_title = task["title"]
    task_spec = task["content"]
    cfg = TASK_CONFIGS[task_id]
    
    print(f"\n=================================================================")
    print(f"▶ Task {task_id}: {task_title} (Temp: {temperature})")
    print(f"=================================================================")
    
    # 1. Physically clean and reset sandbox
    clean_sandbox_completely()
    
    tmpl_dir = os.path.join(BASE_DIR, "task_templates", task_id)
    if not os.path.exists(tmpl_dir):
        raise FileNotFoundError(f"Template directory {tmpl_dir} does not exist!")
        
    sub_dir = cfg.get("sub_dir", "")
    host_target = os.path.join(SANDBOX_HOST_DIR, sub_dir)
    os.makedirs(host_target, exist_ok=True)
    subprocess.run(f"cp -r '{tmpl_dir}'/* '{host_target}'/", shell=True, check=False)
    if os.path.exists(os.path.join(tmpl_dir, ".git")):
        subprocess.run(f"cp -r '{tmpl_dir}/.git' '{host_target}/'", shell=True, check=False)
        
    init_cmd = cfg.get("init_cmd", "")
    if init_cmd:
        init_out, init_err, init_code = exec_sandbox_command(init_cmd)
        if init_code != 0:
            print(f"[!] Warning: init_cmd returned {init_code}: {init_err}")
            
    # 2. Assert initial FAIL condition
    test_cmd = cfg.get("test_cmd", "cd /workspace && pytest -v 2>&1")
    pre_out, pre_err, pre_code = exec_sandbox_command(test_cmd)
    pre_passed = check_task_passed(task_id, pre_out, pre_code)
    if pre_passed:
        raise RuntimeError(f"[ABORT] Task {task_id} unexpectedly passed before any agent changes! Template is defective.")
    print(f"[✓] Verified initial FAIL condition for Task {task_id}.")

    # 3. Setup initial dialogue
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Task Specification:\n\n{task_spec}\n\nPlease begin by investigating the workspace and diagnosing the issue."}
    ]
    
    dialogue_history = []
    total_tokens = 0
    start_time = time.time()
    passed = False
    score = 0
    last_test_stdout = ""
    
    for turn in range(1, max_turns + 1):
        print(f"\n--- Turn {turn}/{max_turns} ---")
        llm_resp = query_llm(api_url, messages, temperature=temperature)
        content = llm_resp["content"]
        reasoning = llm_resp["reasoning"]
        tok_s = llm_resp["tok_s"]
        total_tokens += llm_resp["completion_tokens"]
        
        print(f"\n=======================================================")
        print(f"[LLM] Turn {turn}/{max_turns} | Speed: {tok_s:.1f} tok/s | Generated: {llm_resp['completion_tokens']} toks")
        print(f"=======================================================")
        if reasoning:
            print(f"🧠 [THINKING / REASONING]:\n{reasoning.strip()}\n")
        print(f"💬 [RAW MODEL OUTPUT]:\n{content.strip()}\n")
        
        messages.append({"role": "assistant", "content": content})
        
        bash_cmd = extract_bash_commands(content)
        if not bash_cmd:
            if "COMPLETE" in content:
                print("[✓] Model signaled COMPLETE without command.")
                # Run test to check
                t_out, t_err, t_code = exec_sandbox_command(test_cmd)
                last_test_stdout = t_out
                if check_task_passed(task_id, t_out, t_code):
                    passed = True
                    score = 20
                    print(f"[✓] Task {task_id} passed upon COMPLETE signal at Turn {turn}!")
                    dialogue_history.append({"turn": turn, "content": content, "reasoning": reasoning, "action": "SUBMIT_PASS"})
                    break
            print("[-] No bash command detected. Asking model to continue...")
            messages.append({"role": "user", "content": "Please provide a bash command in a ```bash ... ``` code block to investigate or solve the task, or print COMPLETE when finished."})
            dialogue_history.append({"turn": turn, "content": content, "reasoning": reasoning, "action": "NO_CMD"})
            continue
            
        print(f"⚡ [PODMAN EXEC]:\n{bash_cmd}\n")
        stdout, stderr, exit_code = exec_sandbox_command(bash_cmd)
        print(f"📥 [EXEC RESULT (Exit {exit_code})]:")
        if stdout:
            print(f"[STDOUT]\n{stdout.strip()[:1500]}")
        if stderr:
            print(f"[STDERR]\n{stderr.strip()[:1000]}")
        
        if "<tool_call>" in content:
            feedback = f"<tool_response>\n<function=Bash>\n<result>\n{stdout if stdout else ''}{stderr if stderr else ''}\n</result>\n<exit_code>{exit_code}</exit_code>\n</function>\n</tool_response>\n\nCommand exited with code {exit_code}.\n"
            if stdout:
                feedback += f"STDOUT:\n{stdout}\n"
            if stderr:
                feedback += f"STDERR:\n{stderr}\n"
        else:
            feedback = f"Command exited with code {exit_code}.\n"
            if stdout:
                feedback += f"STDOUT:\n{stdout}\n"
            if stderr:
                feedback += f"STDERR:\n{stderr}\n"
            
        messages.append({"role": "user", "content": feedback})
        dialogue_history.append({
            "turn": turn,
            "content": content,
            "reasoning": reasoning,
            "command": bash_cmd,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code
        })
        
        # Check Early Exit: If agent signaled COMPLETE or ran a test that passed
        if "COMPLETE" in content or any(kw in bash_cmd for kw in ["pytest", "run_stress", "verify_repo"]):
            t_out, t_err, t_code = exec_sandbox_command(test_cmd)
            last_test_stdout = t_out
            if check_task_passed(task_id, t_out, t_code):
                passed = True
                score = 20
                print(f"\n[✓✓✓] EARLY EXIT: Task {task_id} PASSED at Turn {turn}/{max_turns}!")
                break
                
    total_dur = time.time() - start_time
    
    # Final validation if not already passed
    if not passed:
        test_stdout, test_stderr, test_code = exec_sandbox_command(test_cmd)
        last_test_stdout = test_stdout
        passed = check_task_passed(task_id, test_stdout, test_code)
        score = 20 if passed else 0
    
    print(f"\n[Result] Task {task_id} Temp {temperature} -> Passed: {passed} | Score: {score}/20 | Time: {total_dur:.1f}s")
    
    return {
        "task_id": task_id,
        "task_title": task_title,
        "temperature": temperature,
        "passed": passed,
        "score": score,
        "duration_s": total_dur,
        "total_tokens": total_tokens,
        "turns": len(dialogue_history),
        "test_output": last_test_stdout,
        "dialogue_history": dialogue_history
    }

def main():
    parser = argparse.ArgumentParser(description="ai-benchmarks v4 Autonomous Agent Runner")
    parser.add_argument("--api-url", type=str, required=True, help="Colab LLM API URL")
    parser.add_argument("--model-slug", type=str, default="k2-horizon-mova-36b-a4b", help="Model slug name")
    parser.add_argument("--temps", type=float, nargs="+", default=DEFAULT_TEMPS, help="Temperatures to run")
    parser.add_argument("--task-id", type=str, help="Run specific task ID only (e.g. 1-1)")
    parser.add_argument("--reset", action="store_true", help="Reset existing results for this model")
    args = parser.parse_args()
    
    with open(os.path.join(BASE_DIR, "v4_tasks.json"), "r") as f:
        all_tasks = json.load(f)
        
    # Strictly scope to implemented task templates only
    available_task_ids = set(TASK_CONFIGS.keys())
    scoped_tasks = [t for t in all_tasks if t["id"] in available_task_ids]
    
    if args.task_id:
        tasks = [t for t in scoped_tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"[!] Task {args.task_id} not found in available task templates ({list(available_task_ids)})!")
            sys.exit(1)
    else:
        tasks = scoped_tasks
        
    if args.reset:
        res_path = os.path.join(RUNS_DIR, f"results_{args.model_slug}.json")
        if os.path.exists(res_path):
            os.remove(res_path)
            print(f"[✓] Reset existing results file: {res_path}")

    results_data, res_path = load_or_init_results(args.model_slug)
    print(f"Loaded results from: {res_path}")
    print(f"Total available tasks: {len(tasks)} ({[t['id'] for t in tasks]}) | Temperatures: {args.temps}")
    
    total_trials = len(tasks) * len(args.temps)
    completed_trials = 0
    
    for task in tasks:
        tid = task["id"]
        if tid not in results_data["tasks"]:
            results_data["tasks"][tid] = []
            
        existing_temps = [r["temperature"] for r in results_data["tasks"][tid]]
        
        for temp in args.temps:
            if temp in existing_temps:
                print(f"[Skip] Task {tid} at temp {temp} already completed.")
                completed_trials += 1
                continue
                
            try:
                trial_res = run_trial(args.api_url, task, temp)
            except Exception as e:
                print(f"\n[!] ERROR in Task {tid} Temp {temp}: {e}")
                trial_res = {
                    "task_id": tid,
                    "task_title": task["title"],
                    "temperature": temp,
                    "passed": False,
                    "score": 0,
                    "duration_s": 0,
                    "total_tokens": 0,
                    "turns": 0,
                    "test_output": f"CRASH: {str(e)}",
                    "dialogue_history": []
                }
            results_data["tasks"][tid].append(trial_res)
            save_results(results_data, res_path)
            completed_trials += 1
            print(f"[Progress] {completed_trials}/{total_trials} trials saved.")

if __name__ == "__main__":
    main()
