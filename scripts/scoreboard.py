import sys
import json
import os
import glob
import argparse

def get_start_epoch():
    try:
        with open('base-repo/event-state.json', 'r') as st:
            state = json.load(st)
            return state.get("start", 0)
    except Exception:
        # Fallback if base-repo is not the current context
        try:
            with open('event-state.json', 'r') as st:
                state = json.load(st)
                return state.get("start", 0)
        except Exception:
            return 0

def log_submission(player, end_time):
    start_time = get_start_epoch()
    elapsed_time = int(end_time) - int(start_time)

    # Instead of an sqlite/json DB which race-conditions in GitHub Actions,
    # we emit a discrete JSON file that the action uploads as an artifact.
    record = {
        "player": player,
        "score": 1,
        "elapsed": elapsed_time
    }
    
    with open('player_score.json', 'w') as f:
        json.dump(record, f)
    
    print(f"Logged submission for {player} with elapsed time {elapsed_time}s.")

def generate_leaderboard():
    db = {}
    
    # Read all aggregated artifacts downloaded to ./scores/ (if any exist)
    score_files = glob.glob('scores/*.json') + glob.glob('player_score*.json')
    
    for sf in score_files:
        with open(sf, 'r') as f:
            try:
                record = json.load(f)
                player = record["player"]
                if player not in db:
                    db[player] = {
                        "score": 1,
                        "elapsed": record["elapsed"]
                    }
                else:
                    db[player]["score"] += 1
                    # Keep latest/highest elapsed time over multiple submissions
                    db[player]["elapsed"] = max(db[player]["elapsed"], record["elapsed"])
            except Exception as e:
                print(f"Failed parsing {sf}: {e}")

    # Sort primarily by score (desc), secondarily by elapsed time (asc)
    ranked = sorted(db.items(), key=lambda item: (-item[1]["score"], item[1]["elapsed"]))

    content = "## Final Competition Leaderboard\n\n"
    if not ranked:
        content += "> No valid submissions recorded.\n"
    else:
        content += "| Rank | Player | Score (Flags/Fixes) | Elapsed Time |\n"
        content += "|------|--------|----------------------|--------------|\n"
        
        rank = 1
        for player, stats in ranked:
            minutes, seconds = divmod(stats["elapsed"], 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            content += f"| {rank} | @{player} | {stats['score']} | {time_str} |\n"
            rank += 1
            
    with open('final_leaderboard.md', 'w') as out:
        out.write(content)
    
    print("Leaderboard generated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['log', 'generate'])
    parser.add_argument('--player', type=str, help='Player username')
    parser.add_argument('--time', type=int, help='Submission epoch time')
    
    args = parser.parse_args()
    
    if args.action == 'log':
        if not args.player or not args.time:
            print("Error: Player and time required for logging.")
            sys.exit(1)
        log_submission(args.player, args.time)
    elif args.action == 'generate':
        generate_leaderboard()