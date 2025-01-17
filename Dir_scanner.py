import subprocess
import os
import re

def run_gobuster(target, wordlist, base_path="/"):
    """
    Run a gobuster scan on the specified target and base path.
    """
    gobuster_command = [
        "gobuster",
        "dir",                  # Mode: directory enumeration
        "-u", f"{target}{base_path}",  # Target with base path
        "-w", wordlist,         # Wordlist file
        "-q",                   # Suppress banner
        "-t", "10"              # Threads (adjust for speed/performance)
    ]

    print(f"Scanning: {target}{base_path}...")
    result = subprocess.run(gobuster_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(f"Error occurred during gobuster scan: {result.stderr}")
        return []
    
    # Parse directories from Gobuster output
    directories = []
    for line in result.stdout.splitlines():
        # Assuming gobuster output format: `http://target/path (Status: 200)`
        match = re.search(r'(/\S+)\s+\(Status:', line)
        if match:
            directories.append(match.group(1))

    # Save the output for this scan
    sanitized_path = base_path.strip("/").replace("/", "_") or "root"
    output_file = os.path.join(os.getcwd(), f"{target.replace('://', '_')}_{sanitized_path}_gobuster.txt")
    with open(output_file, "w") as file:
        file.write(result.stdout)

    print(f"Scan complete for {target}{base_path}. Results saved to {output_file}")
    return directories


def main():
    print("Gobuster Directory Enumerator")
    print("=============================")

    # Get the IP address or FQDN and wordlist location from the user
    target = input("Enter the IP address or FQDN of the target (e.g., http://example.com): ").strip()
    if not target:
        print("Invalid input. Please provide a valid IP address or FQDN.")
        return

    wordlist = input("Enter the full path to the wordlist: ").strip()
    if not os.path.isfile(wordlist):
        print("Invalid wordlist path. File does not exist.")
        return

    # Start scanning recursively
    scanned_directories = set()  # Keep track of already scanned directories
    directories_to_scan = ["/"]  # Initial scan starts at the root

    while directories_to_scan:
        base_path = directories_to_scan.pop(0)
        if base_path in scanned_directories:
            continue
        
        # Perform Gobuster scan
        found_directories = run_gobuster(target, wordlist, base_path)
        scanned_directories.add(base_path)

        # Add new directories for scanning
        for directory in found_directories:
            if directory not in scanned_directories and directory not in directories_to_scan:
                directories_to_scan.append(directory)

    print("All directory scans completed.")


if __name__ == "__main__":
    main()
