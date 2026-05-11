<div align="center">

```
  ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
  ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
  ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
  ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
  ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
  ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
```

**Sentinel Port Scanner**

*Fast · Lightweight · No Dependencies*

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

</div>

---

## Overview

**Sentinel** is a fast, multi-threaded TCP port scanner written in pure Python using only the standard library. It is designed for network administrators, penetration testers, and security researchers who need quick, reliable port reconnaissance without installing third-party packages.

- **Zero external dependencies** — uses only Python's standard library
- **Multi-threaded** — scans hundreds of ports in parallel
- **CIDR range support** — scan entire subnets in one command
- **Banner grabbing** — identify services running on open ports
- **Clean, colored terminal output** — easy to read at a glance
- **Report export** — save results to a plain-text file

---

## Features

| Feature | Description |
|---|---|
| TCP Connect Scan | Full TCP handshake to determine open/closed state |
| Top-100 Ports | Pre-built list of the most commonly targeted ports |
| Custom Port Ranges | Flexible syntax: `80`, `1-1024`, `22,80,443,8080` |
| CIDR Scanning | Scan entire subnets: `192.168.1.0/24` |
| Banner Grabbing | Retrieve service banners from open ports |
| Progress Indicator | Live per-port counter during scan |
| Summary Report | Clean end-of-scan summary with open port list |
| File Export | Save results to `.txt` for documentation |
| Verbose Mode | Optionally display closed ports |

---

## Requirements

- Python **3.7 or higher**
- No third-party packages required

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sentinel-port-scanner.git
cd sentinel-port-scanner

# Make executable (Linux / macOS)
chmod +x sentinel.py
```

**Windows Setup:**
- Use the provided launcher files for easy execution:
  - `run.bat` - Batch file launcher
  - `run.ps1` - PowerShell script launcher  
  - `Sentinel Launcher.vbs` - VBScript launcher
- Or run directly with: `"C:\path\to\python.exe" sentinel.py [arguments]`

No `pip install` needed. Sentinel runs entirely on the Python standard library.

---

## Usage

**Linux/macOS:**
```
python sentinel.py <target> [options]
```

**Windows:**
```
run.bat <target> [options]
# or
run.ps1 <target> [options]
# or
Sentinel Launcher.vbs <target> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `target` | IP address, hostname, or CIDR range |

### Options

| Flag | Description | Default |
|---|---|---|
| `-p`, `--ports` | Ports to scan (`22`, `1-1024`, `22,80,443`) | Top 100 |
| `--top` | Scan top ~100 common ports | — |
| `-t`, `--threads` | Number of concurrent threads | `100` |
| `--timeout` | Per-port connection timeout in seconds | `1.0` |
| `--banner` | Attempt banner grabbing on open ports | off |
| `-v`, `--verbose` | Show closed ports as well | off |
| `-o`, `--output` | Save report to a file | — |
| `--no-banner` | Suppress the ASCII art banner | off |

---

## Examples

**Scan a single host using the default top-100 ports:**
```bash
# Linux/macOS
python sentinel.py 192.168.1.1

# Windows
run.bat 192.168.1.1
```

**Scan specific ports:**
```bash
# Linux/macOS
python sentinel.py example.com -p 22,80,443,8080,8443

# Windows
run.bat example.com -p 22,80,443,8080,8443
```

**Scan a port range with banner grabbing:**
```bash
python sentinel.py 10.0.0.5 -p 1-1024 --banner
```

**Scan with increased threads and a tighter timeout:**
```bash
python sentinel.py 10.0.0.1 -p 1-65535 -t 500 --timeout 0.5
```

**Scan a full subnet:**
```bash
python sentinel.py 192.168.1.0/24 --top
```

**Save results to a file:**
```bash
python sentinel.py 192.168.1.1 --top --banner -o report.txt
```

**Verbose output (show closed ports too):**
```bash
python sentinel.py 10.0.0.1 -p 1-100 -v
```

---

## Sample Output

```
  ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
  ...

  TARGET  192.168.1.1 (192.168.1.1)
  PORTS   scanning 100 ports with 100 threads [timeout=1.0s]

  PORT                SERVICE                     BANNER
  ──────────────────────────────────────────────────────────────
  OPEN    22/tcp   SSH                         SSH-2.0-OpenSSH_8.9
  OPEN    80/tcp   HTTP                        HTTP/1.1 200 OK
  OPEN   443/tcp   HTTPS                       TLS/SSL
  OPEN  3306/tcp   MySQL

  ──────────────────────────────────────────────────────────────
  SCAN SUMMARY
  ──────────────────────────────────────────────────────────────
  Target        : 192.168.1.1  (192.168.1.1)
  Ports scanned : 100
  Open ports    : 4
  Elapsed time  : 1.42s
  Scan finished : 2025-04-21 14:30:02
  ──────────────────────────────────────────────────────────────

  Open Ports:
    22/SSH
    80/HTTP
    443/HTTPS
    3306/MySQL
```

---

## Well-Known Ports Included

Sentinel's top-100 list covers the most targeted services:

| Port | Service | Port | Service |
|---|---|---|---|
| 21 | FTP | 3306 | MySQL |
| 22 | SSH | 3389 | RDP |
| 23 | Telnet | 5432 | PostgreSQL |
| 25 | SMTP | 5900 | VNC |
| 53 | DNS | 6379 | Redis |
| 80 | HTTP | 8080 | HTTP-Alt |
| 443 | HTTPS | 9200 | Elasticsearch |
| 445 | SMB | 27017 | MongoDB |

---

## Performance Tips

| Goal | Recommendation |
|---|---|
| Fastest scan | `-t 500 --timeout 0.3` (LAN only) |
| Most reliable | `-t 100 --timeout 1.0` (default) |
| Remote/WAN targets | `-t 50 --timeout 2.0` |
| Full port range | `-p 1-65535 -t 300 --timeout 0.5` |

> **Note:** Very high thread counts (`500+`) may trigger IDS/IPS alerts or cause OS-level socket exhaustion. Use responsibly.

---

## Project Structure

```
sentinel-port-scanner/
├── sentinel.py        # Main scanner — single-file, no dependencies
└── README.md          # This file
```

---

## Legal Disclaimer

> **Sentinel is intended for authorized security testing and network administration only.**
>
> Scanning networks, hosts, or systems **without explicit written permission** from the owner is illegal in most jurisdictions and may violate the Computer Fraud and Abuse Act (CFAA), the Computer Misuse Act, and similar laws worldwide.
>
> The author assumes **no liability** for misuse. Always obtain proper authorization before scanning any system you do not own.

---

## License

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

Made with Python 🐍 · Built for security professionals · Use responsibly

</div>
