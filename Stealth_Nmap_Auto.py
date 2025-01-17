import subprocess
import os
import re

def main():
    print("Nmap Stealth Scanner")
    print("=====================")
    # Get the IP address or FQDN from the user
    target = input("Enter the IP address or FQDN of the target: ").strip()
    
    if not target:
        print("Invalid input. Please provide a valid IP address or FQDN.")
        return

    # Define the nmap command with stealthy options
    nmap_command = [
        "nmap",
        "-sS",  # TCP SYN scan (stealthy)
        "-T2",  # Slow scan for reduced detectability
        "-p-",  # Scan all ports
        "-A",  # OS detection, version detection, script scanning
        target
    ]

    try:
        # Run the nmap command
        print(f"Running nmap scan on {target}...")
        result = subprocess.run(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check for errors
        if result.returncode != 0:
            print(f"Error occurred during nmap scan: {result.stderr}")
            return

        # Save the output to a file
        sanitized_name = re.sub(r'[^\w\-_\.]', '_', target)  # Sanitize filename
        output_file = os.path.join(os.getcwd(), f"{sanitized_name}_scan.txt")
        with open(output_file, "w") as file:
            file.write(result.stdout)

        print(f"Scan complete. Results saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
