# Cybersecurity Awareness Competition Platform

Welcome to the DevSecOps Cybersecurity Awareness Competition Platform. This repository serves as a fully automated, GitHub Actions-driven arena for conducting security training and assessment.

## Platform Features

1. **Automated Event Lifecycle**: Start an event via GitHub Actions with a set duration. The platform hard-locks submissions once the timer hits the cutoff.
2. **Concurrent Participation**: Players submit PRs for code challenges and Issues for flag submissions safely.
3. **Automated Evaluation**: Code checks and flag assertions run in isolated, secure actions against player submissions.
4. **Dynamic Scoreboard**: Ranks are automatically calculated by Score vs Time-elapsed and appended to this README upon event completion.

---

## Operator Guide: How to Run an Event

### 1. Preparation
Ensure the repository settings allow GitHub Actions to modify the repository (`Settings` > `Actions` > `General` > `Workflow permissions` -> check `Read and write permissions`).

### 2. Launching the Competition
1. Navigate to the **Actions** tab in GitHub.
2. Select **Admin Start Event** on the left pane.
3. Click **Run workflow**, entering details such as:
   - Event Name (e.g., `AppSec Month Challenge`)
   - Duration in minutes (e.g., `15`)
4. The workflow will initialize the `event-state.json`, record start epochs, and sleep for the duration + 2-minute buffer.

### 3. Monitoring & Closing
- As players push Pull Requests or open Issues containing `FLAG: <flag_name>`, the **Evaluate Submission** workflow will trigger.
- The `evaluator.py` rejects any incoming submissions past the state's `cutoff_epoch`.
- After the 2-minute buffer ends, the Start Action automatically triggers **Publish Results**.
- The `scoreboard.py` generates the final tie-broken leaderboard and publishes it below automatically.

---

## Challenge Specifications (For Players)

### Level 1: Secrets in Code
Navigate to `challenges/level1/config.json`. An AWS API key was accidentally committed. Your mission is to modify the `config.json` removing the keys. Submit via a Pull Request. *(Advanced: Remove it transparently using git history rewriting).*

### Level 2: Supply Chain Security
Navigate to `challenges/level2/package.json`. A typosquatted dependency has infiltrated the app. Detect and remove the malicious package, then submit a Pull Request.

### Level 3: Incident Response (IR)
Navigate to `challenges/level3/dropper.sh`. This is an emulated malicious shell script found on a compromised web server. Extract the base64 payload to find the attacker's Command & Control (C2) server domain.
To capture the flag, open an Issue in this repository formatting your text as:
`FLAG: your_extracted_domain.com`

---

<!-- The final leaderboard will be appended below by the publish-results GitHub Action -->
