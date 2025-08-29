#!/usr/bin/env python3
import requests, json, random, time, sys

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "curl/7.68.0",
    "Wget/1.21.2"
]

# ---------- Animations ----------
def type_out(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(duration=3):
    spin_chars = "|/-\\"
    end_time = time.time() + duration
    while time.time() < end_time:
        for c in spin_chars:
            sys.stdout.write(f"\rScanning... {c}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\rScanning... Done! ")

# ---------- Networking ----------
def fetch(url, stealth=True):
    headers = {}
    headers["User-Agent"] = random.choice(USER_AGENTS) if stealth else "Mozilla/5.0 (compatible; Googlebot/2.1;)"
    if stealth:
        time.sleep(random.uniform(1, 3))
    try:
        return requests.get(url, headers=headers, timeout=6, allow_redirects=True)
    except:
        return None

def detect_cms(url, signatures, stealth=True):
    if not url.startswith("http"):
        url = "http://" + url

    resp = fetch(url, stealth)
    if not resp:
        return "Not sure (site unreachable or blocked)"

    content = resp.text.lower()
    headers = {k.lower(): v.lower() for k, v in resp.headers.items()}
    cookies = [c.name.lower() for c in resp.cookies]

    for cms, sigs in signatures.items():
        if any(s.lower() in content for s in sigs.get("html", [])):
            return f"{cms} detected"
        if any(h.split(":")[0] in headers and h.split(":")[1] in headers[h.split(':')[0]] for h in sigs.get("headers", [])):
            return f"{cms} detected"
        if any(c in cookies for c in sigs.get("cookies", [])):
            return f"{cms} detected"

    # If request succeeded but no match
    return "Not a CMS or Unknown CMS"

# ---------- Main ----------
if __name__ == "__main__":
    # Cool ASCII logo
    logo = r"""
   ____ ___  __  __ ____    ____  _ __ ___
  / ___/ _ \|  \/  |  _ \  / ___|| '__/ _ \
 | |  | | | | |\/| | | | | \___ \| | |  __/
 | |__| |_| | |  | | |_| |  ___) | |  \___|
  \____\___/|_|  |_|____/  |____/|_|
    """
    print(logo)
    print('still in dev')
    type_out(">>> Welcome to GhostCMS Scanner <<<\n", 0.03)

    # Load signatures
    with open("cms_signatures.json") as f:
        signatures = json.load(f)

    url = input("Enter URL to scan: ").strip()
    mode = input("Select mode (stealth/aggressive): ").strip().lower()
    stealth = (mode != "aggressive")

    type_out(f"\n[*] Starting scan on {url} in {mode} mode...", 0.03)
    spinner(duration=4)  # simple loading animation

    result = detect_cms(url, signatures, stealth)
    type_out(f"[+] Result: {result}", 0.05)
