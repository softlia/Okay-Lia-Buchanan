# Sentinel Port Scanner v1.0

> Fast, Lightweight Network Reconnaissance

**Author:** Okay-Lia Buchanan  
**License:** MIT

---

## Description

Sentinel is a multi-threaded Python port scanner for fast network reconnaissance. It supports single hosts, hostnames, and CIDR ranges, with optional banner grabbing, color-coded terminal output, and plain-text report saving.

## Requirements

- Python 3.7+
- No third-party dependencies — uses the standard library only

## Usage

```
python sentinel.py <target> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `target` | IP address, hostname, or CIDR range (e.g. `192.168.1.0/24`) |

### Options

| Flag | Description |
|---|---|
| `-p`, `--ports` | Ports to scan. Accepts comma-separated values or ranges (e.g. `22,80,443` or `1-1024`) |
| `--top` | Scan the top ~100 common ports (default when `-p` is omitted) |
| `-t`, `--threads` | Number of concurrent threads (default: `100`) |
| `--timeout` | Connection timeout per port in seconds (default: `1.0`) |
| `--banner` | Attempt banner grabbing on open ports |
| `-v`, `--verbose` | Show closed ports as well as open ones |
| `-o`, `--output` | Save results to a text file |
| `--no-banner` | Suppress the ASCII art banner at startup |

## Examples

```bash
# Scan top 100 ports on a host
python sentinel.py 192.168.1.1

# Scan specific ports on a hostname
python sentinel.py example.com -p 80,443,8080

# Scan a port range with banner grabbing
python sentinel.py 10.0.0.1 -p 1-1024 -t 200 --banner

# Scan top ports and save a report
python sentinel.py 10.0.0.1 --top --banner --output report.txt

# Scan an entire subnet
python sentinel.py 192.168.1.0/24 --top
```

## Output

Results are printed to the terminal with ANSI color coding:

- **Open** ports are shown in green with the service name and optional banner
- Closed ports are shown dimmed (only with `--verbose`)
- A scan summary is printed after each host

When `--output` is used, a plain-text report is saved to the specified file.

## Notes

- Sentinel uses **TCP connect scanning** — no raw sockets and no root/admin privileges required.
- Default thread count is 100; increase with `-t` for faster scans over large ranges.
- Banner grabbing adds latency; omit `--banner` when speed is the priority.
- Large CIDR ranges (>256 hosts) will display a warning before proceeding.
- TLS/SSL ports (443, 8443) return `TLS/SSL` as the banner without connecting over plaintext.

## Legal Notice

> Only scan hosts and networks you own or have explicit permission to test.  
> Unauthorized port scanning may be illegal in your jurisdiction.
