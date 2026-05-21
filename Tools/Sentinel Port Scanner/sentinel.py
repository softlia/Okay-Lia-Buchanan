#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════╗
║              SENTINEL PORT SCANNER v1.0               ║
║         Fast, Lightweight Network Reconnaissance      ║
╚═══════════════════════════════════════════════════════╝

Author: Okay-Lia Buchanan
License: MIT
"""

import socket
import argparse
import sys
import time
import threading
import ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

# ── ANSI Colors ──────────────────────────────────────────────────────────────
class Colors:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

def c(text: str, color: str) -> str:
    """Wrap text in ANSI color codes."""
    return f"{color}{text}{Colors.RESET}"

# ── Common port/service map ───────────────────────────────────────────────────
COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    111:  "RPC",
    135:  "MSRPC",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    465:  "SMTPS",
    587:  "SMTP (Submission)",
    993:  "IMAPS",
    995:  "POP3S",
    1433: "MSSQL",
    1521: "Oracle DB",
    2181: "ZooKeeper",
    3000: "Node.js / Grafana",
    3306: "MySQL",
    3389: "RDP",
    4369: "RabbitMQ",
    5000: "Flask / UPnP",
    5432: "PostgreSQL",
    5672: "AMQP (RabbitMQ)",
    5900: "VNC",
    6379: "Redis",
    6443: "Kubernetes API",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8888: "Jupyter",
    9000: "PHP-FPM / SonarQube",
    9200: "Elasticsearch",
    9300: "Elasticsearch (Node)",
    27017:"MongoDB",
    27018:"MongoDB (Shard)",
    50000:"DB2",
}

TOP_100_PORTS = sorted(COMMON_PORTS.keys()) + [
    20, 69, 79, 88, 102, 113, 119, 123, 137, 138, 161, 162, 179,
    194, 389, 500, 512, 513, 514, 515, 520, 631, 636, 873, 902,
    1080, 1194, 1723, 1883, 2049, 2375, 2376, 4444, 5601, 5985,
    6000, 6667, 7001, 7077, 7474, 8000, 8081, 8888, 9090, 10000,
    11211, 15672, 49152,
]
TOP_100_PORTS = sorted(set(TOP_100_PORTS))[:100]

# ── Banner ────────────────────────────────────────────────────────────────────
BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
  ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
  ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
  ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
  ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
  ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
  ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
{Colors.RESET}{Colors.DIM}                Port Scanner v1.0 — Network Reconnaissance Tool{Colors.RESET}
"""

# ── Core scanning logic ───────────────────────────────────────────────────────
def resolve_host(host: str) -> Optional[str]:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None

def grab_banner(host: str, port: int, timeout: float = 2.0) -> Optional[str]:
    """Attempt a banner grab on an open port."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            try:
                # Send a generic HTTP request for web ports, else just read
                if port in (80, 8080, 8000, 8888, 8081):
                    s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                elif port in (443, 8443):
                    return "TLS/SSL"
                else:
                    s.sendall(b"\r\n")
                banner = s.recv(256).decode("utf-8", errors="replace").strip()
                return banner[:80] if banner else None
            except Exception:
                return None
    except Exception:
        return None

def scan_port(host: str, port: int, timeout: float, grab: bool) -> dict:
    """
    Try to connect to host:port.
    Returns a dict with status, service, and optional banner.
    """
    result = {
        "port":    port,
        "state":   "closed",
        "service": COMMON_PORTS.get(port, "unknown"),
        "banner":  None,
    }
    try:
        with socket.create_connection((host, port), timeout=timeout):
            result["state"] = "open"
            if grab:
                result["banner"] = grab_banner(host, port, timeout)
    except (ConnectionRefusedError, socket.timeout, OSError):
        pass
    return result

# ── Output helpers ────────────────────────────────────────────────────────────
def print_result(r: dict, verbose: bool = False) -> None:
    """Pretty-print a single port result."""
    port    = r["port"]
    state   = r["state"]
    service = r["service"]
    banner  = r["banner"]

    if state == "open":
        status_str = c("OPEN  ", Colors.GREEN + Colors.BOLD)
        port_str   = c(f"{port:>5}", Colors.WHITE + Colors.BOLD)
        svc_str    = c(f"{service:<28}", Colors.CYAN)
        line = f"  {status_str} {port_str}/tcp   {svc_str}"
        if banner:
            line += c(f"  ↳ {banner}", Colors.DIM)
        print(line)
    elif verbose:
        port_str   = c(f"{port:>5}", Colors.DIM)
        svc_str    = c(f"{service:<28}", Colors.DIM)
        print(f"  {c('CLOSED', Colors.DIM)}  {port_str}/tcp   {svc_str}")

def print_summary(host: str, ip: str, open_ports: list, elapsed: float,
                  total_scanned: int) -> None:
    """Print a scan summary block."""
    width = 62
    sep = c("─" * width, Colors.DIM)
    print(f"\n{sep}")
    print(c("  SCAN SUMMARY", Colors.BOLD + Colors.YELLOW))
    print(sep)
    print(f"  Target        : {c(host, Colors.WHITE)}  ({c(ip, Colors.DIM)})")
    print(f"  Ports scanned : {c(str(total_scanned), Colors.WHITE)}")
    print(f"  Open ports    : {c(str(len(open_ports)), Colors.GREEN + Colors.BOLD)}")
    print(f"  Elapsed time  : {c(f'{elapsed:.2f}s', Colors.WHITE)}")
    print(f"  Scan finished : {c(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Colors.DIM)}")
    print(sep)
    if open_ports:
        print(f"\n  {c('Open Ports:', Colors.BOLD + Colors.GREEN)}")
        for r in open_ports:
            b = f"  [{r['banner'][:40]}]" if r["banner"] else ""
            print(f"    {c(str(r['port']), Colors.WHITE)}/{c(r['service'], Colors.CYAN)}{c(b, Colors.DIM)}")
    print()

def save_report(host: str, ip: str, open_ports: list, elapsed: float,
                total_scanned: int, path: str) -> None:
    """Write a plain-text report to a file."""
    with open(path, "w") as f:
        f.write("SENTINEL PORT SCANNER — REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Target        : {host} ({ip})\n")
        f.write(f"Scan date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Ports scanned : {total_scanned}\n")
        f.write(f"Open ports    : {len(open_ports)}\n")
        f.write(f"Elapsed       : {elapsed:.2f}s\n\n")
        f.write(f"{'PORT':<8}{'STATE':<10}{'SERVICE'}\n")
        f.write("-" * 40 + "\n")
        for r in open_ports:
            banner = f"  | {r['banner']}" if r["banner"] else ""
            f.write(f"{r['port']:<8}{'open':<10}{r['service']}{banner}\n")
    print(c(f"  [+] Report saved → {path}", Colors.GREEN))

# ── Argument parser ───────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="Sentinel — a fast, multi-threaded Python port scanner.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python sentinel.py 192.168.1.1
  python sentinel.py example.com -p 80,443,8080
  python sentinel.py 10.0.0.1 -p 1-1024 -t 200 --banner
  python sentinel.py 10.0.0.1 --top --banner --output report.txt
  python sentinel.py 192.168.1.0/24 --top
""",
    )
    parser.add_argument("target",
        help="Target IP, hostname, or CIDR range (e.g. 192.168.1.0/24)")
    parser.add_argument("-p", "--ports",
        help="Ports to scan. Examples:\n  -p 22,80,443\n  -p 1-1024\n  -p 80",
        default=None)
    parser.add_argument("--top",
        action="store_true",
        help="Scan top ~100 common ports (default if no -p given)")
    parser.add_argument("-t", "--threads",
        type=int, default=100, metavar="N",
        help="Number of concurrent threads (default: 100)")
    parser.add_argument("--timeout",
        type=float, default=1.0, metavar="SEC",
        help="Connection timeout per port in seconds (default: 1.0)")
    parser.add_argument("--banner",
        action="store_true",
        help="Attempt banner grabbing on open ports")
    parser.add_argument("-v", "--verbose",
        action="store_true",
        help="Show closed ports as well")
    parser.add_argument("-o", "--output",
        metavar="FILE",
        help="Save results to a text file")
    parser.add_argument("--no-banner",
        action="store_true",
        help="Suppress the ASCII banner")
    return parser

# ── Port range parser ─────────────────────────────────────────────────────────
def parse_ports(port_str: str) -> list:
    """Parse port expressions like '80,443,1-1024' into a sorted list."""
    ports = set()
    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            lo, hi = int(lo.strip()), int(hi.strip())
            if lo > hi or lo < 1 or hi > 65535:
                raise ValueError(f"Invalid port range: {part}")
            ports.update(range(lo, hi + 1))
        else:
            p = int(part)
            if p < 1 or p > 65535:
                raise ValueError(f"Invalid port: {p}")
            ports.add(p)
    return sorted(ports)

# ── Host list expansion ───────────────────────────────────────────────────────
def expand_targets(target: str) -> list:
    """Return a list of host strings from a target (single host or CIDR)."""
    try:
        network = ipaddress.ip_network(target, strict=False)
        if network.num_addresses > 256:
            print(c(f"  [!] Large CIDR range ({network.num_addresses} hosts). Proceeding…", Colors.YELLOW))
        return [str(ip) for ip in network.hosts()] or [str(network.network_address)]
    except ValueError:
        return [target]

# ── Single-host scan ──────────────────────────────────────────────────────────
def scan_host(host: str, ports: list, threads: int, timeout: float,
              grab: bool, verbose: bool) -> tuple:
    """Scan all ports on a single host. Returns (ip, open_ports, elapsed)."""
    ip = resolve_host(host)
    if not ip:
        print(c(f"  [✗] Cannot resolve host: {host}", Colors.RED))
        return None, [], 0.0

    print(f"\n{c('  TARGET', Colors.BOLD + Colors.YELLOW)}  {c(host, Colors.WHITE)} "
          f"{c(f'({ip})', Colors.DIM)}")
    print(f"  {c('PORTS', Colors.BOLD)}   scanning {c(str(len(ports)), Colors.WHITE)} ports "
          f"with {c(str(threads), Colors.WHITE)} threads "
          f"[timeout={c(f'{timeout}s', Colors.WHITE)}]\n")

    open_ports  = []
    lock        = threading.Lock()
    start_time  = time.time()
    scanned     = 0

    def worker(p):
        return scan_port(ip, p, timeout, grab)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(worker, p): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            scanned += 1
            # Progress indicator on the same line
            sys.stdout.write(
                f"\r  {c('Scanning…', Colors.DIM)} "
                f"{c(str(scanned), Colors.WHITE)}/{c(str(len(ports)), Colors.DIM)} "
                f"ports"
            )
            sys.stdout.flush()
            if result["state"] == "open":
                with lock:
                    open_ports.append(result)

    sys.stdout.write("\r" + " " * 50 + "\r")  # clear progress line
    elapsed = time.time() - start_time

    # Sort open ports numerically and print
    open_ports.sort(key=lambda x: x["port"])
    if open_ports:
        print(f"  {c('PORT', Colors.BOLD + Colors.WHITE):<20}"
              f"{c('SERVICE', Colors.BOLD + Colors.CYAN):<32}"
              f"{c('BANNER', Colors.BOLD + Colors.DIM)}")
        print(c("  " + "─" * 58, Colors.DIM))
        for r in open_ports:
            print_result(r, verbose)
    elif verbose:
        print(c("  All scanned ports are closed.", Colors.DIM))

    return ip, open_ports, elapsed

# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    if not args.no_banner:
        print(BANNER)

    # Determine port list
    if args.ports:
        try:
            ports = parse_ports(args.ports)
        except ValueError as e:
            print(c(f"  [✗] {e}", Colors.RED))
            sys.exit(1)
    else:
        ports = TOP_100_PORTS  # default to top 100

    # Expand CIDR or single host
    targets = expand_targets(args.target)

    all_open = []
    total_elapsed = 0.0

    for host in targets:
        ip, open_ports, elapsed = scan_host(
            host, ports,
            threads=args.threads,
            timeout=args.timeout,
            grab=args.banner,
            verbose=args.verbose,
        )
        if ip:
            all_open.extend(open_ports)
            total_elapsed += elapsed
            print_summary(host, ip, open_ports, elapsed, len(ports))
            if args.output and len(targets) == 1:
                save_report(host, ip, open_ports, elapsed, len(ports), args.output)

    if len(targets) > 1:
        print(c(f"\n  [✓] Scan complete. "
                f"{len(all_open)} open port(s) found across {len(targets)} hosts "
                f"in {total_elapsed:.2f}s.", Colors.GREEN + Colors.BOLD))
        if args.output:
            # crude combined report
            with open(args.output, "w") as f:
                f.write(f"SENTINEL MULTI-HOST REPORT — {datetime.now()}\n\n")
                for r in all_open:
                    f.write(f"{r['port']}/tcp  open  {r['service']}\n")
            print(c(f"  [+] Report saved → {args.output}", Colors.GREEN))

if __name__ == "__main__":
    main()
