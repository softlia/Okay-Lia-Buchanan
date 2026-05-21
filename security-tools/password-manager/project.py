"""
Password Manager — inspired by Dr. Angela Yu's 100 Days of Code
Built with tkinter GUI, random password generator, and JSON storage.
"""

import json
import random
import string
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────
DATA_FILE = Path(__file__).parent / "data.json"

LETTERS = list(string.ascii_letters)
NUMBERS = list(string.digits)
SYMBOLS = list("!#$%&()*+")

# ── Colour palette (subtle warmth, close to Dr. Angela's vanilla/white style) ──
BG        = "#F5F0E8"
ENTRY_BG  = "#FFFDF7"
BTN_GREEN = "#4A7C59"
BTN_BLUE  = "#2E6B9E"
BTN_RED   = "#C0392B"
FG        = "#2C2C2C"
LABEL_FG  = "#4A4A4A"
FONT      = ("Courier", 12)
FONT_BOLD = ("Courier", 12, "bold")
TITLE_FONT= ("Courier", 16, "bold")


# ── Password Generator ─────────────────────────────────────────────────────────
def generate_password() -> str:
    """Generate a secure random password (same recipe as Dr. Angela)."""
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pwd_list = (
        random.choices(LETTERS, k=nr_letters)
        + random.choices(SYMBOLS, k=nr_symbols)
        + random.choices(NUMBERS, k=nr_numbers)
    )
    random.shuffle(pwd_list)
    return "".join(pwd_list)


# ── Data helpers ───────────────────────────────────────────────────────────────
def load_data() -> dict:
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_entry(website: str, email: str, password: str) -> None:
    data = load_data()
    data[website] = {"email": email, "password": password}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def find_entry(website: str):
    data = load_data()
    return data.get(website)


def delete_entry(website: str) -> bool:
    data = load_data()
    if website in data:
        del data[website]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    return False


# ── GUI ────────────────────────────────────────────────────────────────────────
class PasswordManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Password Manager")
        self.config(bg=BG, padx=40, pady=40)
        self.resizable(False, False)
        self._build_ui()
        self._center_window()

    # ── Layout ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title
        tk.Label(self, text="🔐 Password Manager",
                 font=TITLE_FONT, bg=BG, fg=BTN_GREEN).grid(
                 row=0, column=0, columnspan=3, pady=(0, 20))

        # ── Labels ──
        for row, text in enumerate(("Website:", "Email / Username:", "Password:"), start=1):
            tk.Label(self, text=text, font=FONT_BOLD,
                     bg=BG, fg=LABEL_FG, anchor="e", width=18).grid(
                     row=row, column=0, pady=6, sticky="e")

        # ── Website row ──
        self.website_entry = self._entry(row=1, col=1, colspan=1)
        self._btn("Search 🔍", self._search, BTN_BLUE, row=1, col=2)

        # ── Email row ──
        self.email_entry = self._entry(row=2, col=1, colspan=2)
        self.email_entry.insert(0, "your@email.com")   # default prefill

        # ── Password row ──
        self.password_entry = self._entry(row=3, col=1, colspan=1, show="•")
        self._btn("Generate 🎲", self._fill_password, BTN_GREEN, row=3, col=2)

        # ── Show / Hide toggle ──
        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Show password", variable=self.show_var,
                       command=self._toggle_show, bg=BG, fg=LABEL_FG,
                       font=("Courier", 10), activebackground=BG,
                       selectcolor=BG).grid(row=4, column=1, sticky="w", pady=2)

        # ── Action buttons ──
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=(18, 0))

        self._btn("Add ✅",    self._save,   BTN_GREEN, frame=btn_frame, side="left",  padx=6)
        self._btn("Delete 🗑", self._delete, BTN_RED,   frame=btn_frame, side="left",  padx=6)
        self._btn("Clear 🧹",  self._clear,  "#888888", frame=btn_frame, side="left",  padx=6)

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self, textvariable=self.status_var, font=("Courier", 10),
                 bg=BG, fg="#888888").grid(row=6, column=0, columnspan=3,
                 pady=(14, 0))

    def _entry(self, row, col, colspan=1, show=""):
        e = tk.Entry(self, font=FONT, bg=ENTRY_BG, fg=FG,
                     relief="flat", bd=0, highlightthickness=1,
                     highlightbackground="#CCCCCC",
                     highlightcolor=BTN_BLUE,
                     show=show, width=28)
        e.grid(row=row, column=col, columnspan=colspan,
               padx=6, pady=6, ipady=6, sticky="ew")
        return e

    def _btn(self, text, cmd, colour, row=None, col=None,
             frame=None, side=None, padx=0):
        b = tk.Button(
            frame if frame else self,
            text=text, command=cmd,
            font=FONT_BOLD, bg=colour, fg="white",
            activebackground=colour, activeforeground="white",
            relief="flat", bd=0, padx=10, pady=6,
            cursor="hand2",
        )
        if frame:
            b.pack(side=side, padx=padx)
        else:
            b.grid(row=row, column=col, padx=6, pady=6, sticky="ew")
        # Hover effect
        b.bind("<Enter>", lambda e, btn=b, c=colour: btn.config(bg=self._darken(c)))
        b.bind("<Leave>", lambda e, btn=b, c=colour: btn.config(bg=c))
        return b

    # ── Helpers ──────────────────────────────────────────────────────────────
    @staticmethod
    def _darken(hex_color: str) -> str:
        """Return a slightly darker shade of the given hex colour."""
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        factor = 0.82
        return "#{:02x}{:02x}{:02x}".format(
            int(r * factor), int(g * factor), int(b * factor))

    def _center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    def _set_status(self, msg: str, colour: str = "#888888"):
        self.status_var.set(msg)
        self.nametowidget(".").option_add("*Label.foreground", colour)

    def _toggle_show(self):
        char = "" if self.show_var.get() else "•"
        self.password_entry.config(show=char)

    # ── Actions ──────────────────────────────────────────────────────────────
    def _fill_password(self):
        pwd = generate_password()
        self.password_entry.config(show="")
        self.show_var.set(True)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, pwd)
        self.clipboard_clear()
        self.clipboard_append(pwd)
        self.status_var.set("✅ Password generated & copied to clipboard!")

    def _save(self):
        website  = self.website_entry.get().strip().lower()
        email    = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not email or not password:
            messagebox.showwarning("Oops", "Please fill in all fields before saving.")
            return

        ok = messagebox.askokcancel(
            "Confirm",
            f"Save entry?\n\nWebsite : {website}\nEmail   : {email}\nPassword: {password}"
        )
        if ok:
            save_entry(website, email, password)
            self._clear()
            self.status_var.set(f"✅ Entry saved for '{website}'.")

    def _search(self):
        website = self.website_entry.get().strip().lower()
        if not website:
            messagebox.showwarning("Oops", "Please enter a website to search.")
            return
        entry = find_entry(website)
        if entry:
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, entry["email"])
            self.password_entry.config(show="")
            self.show_var.set(True)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, entry["password"])
            self.clipboard_clear()
            self.clipboard_append(entry["password"])
            self.status_var.set(f"🔍 Found '{website}' — password copied to clipboard!")
        else:
            messagebox.showinfo("Not Found", f"No entry found for '{website}'.")
            self.status_var.set(f"❌ No entry for '{website}'.")

    def _delete(self):
        website = self.website_entry.get().strip().lower()
        if not website:
            messagebox.showwarning("Oops", "Please enter a website to delete.")
            return
        ok = messagebox.askyesno("Confirm Delete",
                                 f"Delete the entry for '{website}'?")
        if ok:
            if delete_entry(website):
                self._clear()
                self.status_var.set(f"🗑 Entry for '{website}' deleted.")
            else:
                messagebox.showinfo("Not Found",
                                    f"No entry for '{website}' exists.")

    def _clear(self):
        for entry in (self.website_entry, self.email_entry, self.password_entry):
            entry.delete(0, tk.END)
        self.password_entry.config(show="•")
        self.show_var.set(False)
        self.email_entry.insert(0, "your@email.com")
        self.status_var.set("Ready.")


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()
