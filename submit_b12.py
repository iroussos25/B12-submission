import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

def submit():
    # Note: Replace hardcoded strings with your actual info or env vars
    name = "Giannis Roussos"
    email = "grcodes@outlook.com"
    resume_link = "https://www.giannisroussos.com" # Or your LinkedIn
    repo_link = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}"
    
    # This dynamic link points to the specific run that triggers the script
    run_id = os.getenv('GITHUB_RUN_ID')
    action_run_link = f"{repo_link}/actions/runs/{run_id}"

    payload = {
        "action_run_link": action_run_link,
        "email": email,
        "name": name,
        "repository_link": repo_link,
        "resume_link": resume_link,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
    }

    # 2. Canonicalize JSON (Compact, Sorted Keys, No extra whitespace)
    # Using sort_keys=True and separators=(',', ':') to match B12 requirements
    raw_body = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')

    # 3. Create HMAC-SHA256 Signature
    secret = b"hello-there-from-b12"
    signature = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}"
    }

    # 4. POST to B12
    url = "https://b12.io/apply/submission"
    response = requests.post(url, data=raw_body, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(f"Submission Successful!")
        print(f"Receipt: {result.get('receipt')}")
    else:
        print(f"Error {response.status_code}: {response.text}")
        exit(1)

if __name__ == "__main__":
    submit()