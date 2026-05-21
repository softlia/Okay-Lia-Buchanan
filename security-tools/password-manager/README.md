# 🔐 Password Manager

A clean desktop **Password Manager** built with Python & Tkinter — inspired by [Dr. Angela Yu's](https://www.udemy.com/user/4b4368a3-b5c8-4529-aa65-2056ec31f37e/) **100 Days of Code** curriculum (Day 29–30).

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎲 Password Generator | Random secure passwords (letters + symbols + numbers) |
| 💾 Save Passwords | Stored locally in `data.json` |
| 🔍 Search | Instantly look up any saved website |
| 🗑 Delete | Remove entries you no longer need |
| 📋 Auto-copy | Generated/found passwords are copied to clipboard |
| 👁 Show/Hide | Toggle password visibility |
| 🧹 Clear | Reset all fields with one click |

---

## 📁 Project Structure

```
password_manager/
├── main.py          # Full application (GUI + logic)
├── data.json        # Auto-created on first save (gitignored)
├── requirements.txt # No third-party deps needed
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `tkinter` (bundled with standard Python on Windows & macOS)

> **Linux users:** `sudo apt-get install python3-tk`

### Run

```bash
git clone https://github.com/YOUR_USERNAME/password-manager.git
cd password-manager
python main.py
```

No `pip install` needed — only the Python standard library is used.

---

## 🖥 Screenshot

> Add a screenshot of the running app here.

---

## 🔒 Security Notice

Passwords are stored in **plain-text JSON** on your local machine. This project is built for **educational purposes** following Dr. Angela Yu's curriculum. For production use, consider encrypting `data.json` with a library like [`cryptography`](https://cryptography.io/).

---

## 📚 Based On

- [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu
- Day 29: Building a Password Manager GUI App
- Day 30: Errors, Exceptions & JSON Data — Improving the Password Manager

---

## 📄 License

MIT — free to use and modify.
