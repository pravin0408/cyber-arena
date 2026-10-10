import os
import json
import sys
import subprocess
import re

def get_event_state():
    try:
        with open('base-repo/event-state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: event-state.json not found. Did the admin start the event?")
        sys.exit(1)

def evaluate_pr(state):
    print("Evaluating Pull Request Code Changes...")
    # Level 1: Verify secret is removed
    # Assuming code path is submission-repo/challenges/level1/config.json
    try:
        with open('submission-repo/challenges/level1/config.json', 'r') as f:
            content = f.read()
            if "AKIAIOSFODNN7EXAMPLE" in content:
                print("Level 1 Check Failed: Secret still present in config.json")
                sys.exit(1)
            else:
                print("Level 1 Check Passed: Secret removed efficiently.")
    except Exception as e:
        print(f"Level 1 Check Failed: {e}")
        sys.exit(1)

    # Level 2: Typosquatted dependency removed
    try:
        with open('submission-repo/challenges/level2/package.json', 'r') as f:
            data = json.load(f)
            deps = data.get("dependencies", {})
            if "expresss" in deps:
                print("Level 2 Check Failed: Malicious dependency 'expresss' still present.")
                sys.exit(1)
            else:
                print("Level 2 Check Passed: Malicious dependency removed.")
    except Exception as e:
        print(f"Level 2 Check Failed: {e}")
        sys.exit(1)

def evaluate_issue(state):
    print("Evaluating Issue Submission (Flags)...")
    body = os.environ.get("ISSUE_BODY", "")
    
    # Level 3: Extract C2 domain flag
    match = re.search(r'FLAG:\s*([^\s]+)', body)
    if match:
        flag = match.group(1).strip()
        if flag == "evil-c2.com":
            print("Level 3 Check Passed: Correct C2 Domain identified!")
        else:
            print("Level 3 Check Failed: Incorrect flag.")
            sys.exit(1)
    else:
        print("Level 3 Check Failed: No flag found in submission body.")
        sys.exit(1)

def main():
    state = get_event_state()
    current_time = int(subprocess.check_output(['date', '+%s']).decode('utf-8').strip())
    
    if current_time > state.get('cutoff'):
        print("Submission Rejected: Competition cutoff time has passed.")
        sys.exit(1)
    
    event_type = os.environ.get("EVENT_NAME")
    if event_type == "pull_request":
        evaluate_pr(state)
    elif event_type == "issues":
        evaluate_issue(state)
    else:
        print(f"Unknown event type: {event_type}")

if __name__ == "__main__":
    main()
