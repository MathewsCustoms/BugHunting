#!/bin/bash

read -p "Enter an IPv4 address or FQDN: " input

# Check if input is an FQDN by looking for non-numeric characters
if [[ "$input" =~ [a-zA-Z] ]]; then
    echo "Resolving FQDN to IP..."
    dig_output=$(dig +short "$input")
    ip=$(echo "$dig_output" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1)

    if [[ -z "$ip" ]]; then
        echo "Failed to resolve domain to an IP address." | tee -a error.log
        exit 1
    fi
else
    ip=$input
    dig_output="No FQDN provided, using direct IP: $ip"
fi

# Define log file
logfile="${ip}.txt"

# Save dig output
{
    echo "===== DIG OUTPUT ====="
    echo "$dig_output"
    echo
    echo "===== NMAP OUTPUT ====="
    nmap -sV -sS -p- -T2 "$ip"
} | tee "$logfile"

echo "Scan results saved to $logfile"
