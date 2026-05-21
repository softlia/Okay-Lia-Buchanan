SENTINEL PORT SCANNER v1.0
Fast, Lightweight Network Reconnaissance
Author: Okay-Lia Buchanan
License: MIT
===========================================================

DESCRIPTION
-----------
Sentinel is a multi-threaded Python port scanner for fast network
reconnaissance. It supports single hosts, hostnames, and CIDR ranges,
with optional banner grabbing, colored terminal output, and report saving.


REQUIREMENTS
------------
Python 3.7 or higher (uses only the standard library — no pip installs needed)


USAGE
-----
  python sentinel.py <target> [options]

Arguments:
  target          IP address, hostname, or CIDR range (e.g. 192.168.1.0/24)

Options:
  -p, --ports     Ports to scan. Accepts comma-separated values or ranges.
                    Examples: -p 22,80,443  |  -p 1-1024  |  -p 80
  --top           Scan the top ~100 common ports (default when -p is omitted)
  -t, --threads   Number of concurrent threads (default: 100)
  --timeout       Connection timeout per port in seconds (default: 1.0)
  --banner        Attempt banner grabbing on open ports
  -v, --verbose   Show closed ports as well as open ones
  -o, --output    Save results to a text file
  --no-banner     Suppress the ASCII art banner at startup
  -h, --help      Show help message and exit


EXAMPLES
--------
Scan top 100 ports on a host:
  python sentinel.py 192.168.1.1

Scan specific ports on a hostname:
  python sentinel.py example.com -p 80,443,8080

Scan a port range with banner grabbing:
  python sentinel.py 10.0.0.1 -p 1-1024 -t 200 --banner

Scan top ports and save a report:
  python sentinel.py 10.0.0.1 --top --banner --output report.txt

Scan an entire subnet:
  python sentinel.py 192.168.1.0/24 --top


OUTPUT
------
Results are printed to the terminal with ANSI color coding:
  - OPEN ports shown in green with service name and optional banner
  - Closed ports shown dimmed (only with --verbose)
  - A scan summary is printed after each host

When --output is used, a plain-text report is saved to the specified file.


NOTES
-----
- Sentinel uses TCP connect scanning (no raw sockets; no root required).
- Default thread count is 100; raise with -t for faster scans on larger ranges.
- Banner grabbing makes the scan slower; omit --banner for speed.
- Large CIDR ranges (>256 hosts) will display a warning before proceeding.
- TLS/SSL ports (443, 8443) return "TLS/SSL" as the banner without connecting
  over plaintext.


LEGAL NOTICE
------------
Only scan hosts and networks you own or have explicit permission to test.
Unauthorized port scanning may be illegal in your jurisdiction.
