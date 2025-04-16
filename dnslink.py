import requests
import random
import dns.resolver
import sys
import re
import time
import os

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
NC = '\033[0m'  # No Color

def print_banner():
    print(f"{CYAN}#############################################")
    print(f"{GREEN}   Link Extractor and DNS Checker Script")
    print(f"{CYAN}#############################################")
    print(f"{WHITE}                Version 1.0")
    print(f"{CYAN}#############################################")

def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Ubuntu; X11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    return random.choice(user_agents)

def extract_links_and_dns(input_url):
    # Validate URL
    if not re.match(r'^https?://', input_url):
        print(f"{RED}Invalid URL. Please provide a valid HTTP or HTTPS URL.{NC}")
        sys.exit(1)

    try:
        headers = {'User-Agent': random_user_agent()}
        print(f"Extracting links from {input_url}...")
        response = requests.get(input_url, headers=headers)
        response.raise_for_status()

        # Extract links
        links = re.findall(r'href="(https?://[^"]+|/[^"]+)', response.text)
        links = sorted(set(links))  # Unique sorted links

        total_links = len(links)
        print("\nExtracted Links:\n")
        print(f"{'Link':<50} {'DNS Info':<20} {'HTTP Response':<30}")
        print(f"{'----':<50} {'--------':<20} {'--------------':<30}")

        for count, link in enumerate(links, start=1):
            if not link.startswith("http"):
                link = requests.compat.urljoin(input_url, link)

            print(f"Checking link: {link}")
            
            # Get DNS info
            try:
                host = link.split("/")[2]
                dns_info = dns.resolver.resolve(host, 'A')
                dns_info_str = ', '.join([str(ip) for ip in dns_info])
            except Exception:
                dns_info_str = "No DNS info"

            # Get HTTP response information
            try:
                response = requests.get(link, headers=headers)
                curl_output = f"{response.status_code} {response.url}"
            except requests.RequestException as e:
                curl_output = f"Error: {e}"

            # Print the link, DNS info, and HTTP response in table format
            print(f"{link:<50} {dns_info_str:<20} {curl_output:<30}")
            print(f"Processing link {count} of {total_links}...")

        print("Finished processing links.")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{NC}")

def main():
    print_banner()
    time.sleep(3)

    if len(sys.argv) != 2:
        print(f"{YELLOW}Usage: {sys.argv[0]} <URL>{NC}")
        sys.exit(1)

    input_url = sys.argv[1]

    # Ask for user confirmation to start
    confirm = input("Do you want to start the link extraction and DNS checking process? (y/n): ")
    if confirm.lower() == 'y':
        os.system('clear')
        extract_links_and_dns(input_url)
    else:
        print("Operation canceled by the user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
