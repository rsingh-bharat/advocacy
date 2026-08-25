# ════════════════════════════════════════════════════════════════════════════════
# ║        ADVOCACY — Legal Practice Management Suite  v7.0                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
# Run:  python ADVOCACY_v7.py
# Deps: pip install customtkinter reportlab mysql-connector-python bcrypt

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 0 — IMPORTS & DEPENDENCY CHECK
# ══════════════════════════════════════════════════════════════════════════════
import sys
import datetime
import calendar
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkFont
import customtkinter as ctk

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    import bcrypt
except ImportError as _e:
    import tkinter as _tk
    import tkinter.messagebox as _mb
    _root = _tk.Tk()
    _root.withdraw()
    _mb.showerror(
        "Missing Dependency",
        f"Required package not installed:\n{_e}\n\n"
        "Run:\n  pip install mysql-connector-python bcrypt",
    )
    _root.destroy()
    sys.exit(1)

try:
    from reportlab.pdfgen import canvas as _pdf_canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — THEME
# ══════════════════════════════════════════════════════════════════════════════
COLORS = {
    "bg_primary":        "#FFFFFF",
    "bg_secondary":      "#F4F4F4",
    "bg_card":           "#FAFAFA",
    "bg_hover_cell":     "#EFEFEF",
    "navbar_bg":         "#0A0A0A",
    "navbar_text":       "#FFFFFF",
    "navbar_hover":      "#1F1F1F",
    "navbar_active":     "#2D2D2D",
    "navbar_border":     "#3A3A3A",
    "text_primary":      "#0A0A0A",
    "text_secondary":    "#4A4A4A",
    "text_muted":        "#8A8A8A",
    "text_on_dark":      "#FFFFFF",
    "accent":            "#111111",
    "accent_hover":      "#333333",
    "link":              "#1A1A1A",
    "link_hover":        "#555555",
    "border":            "#CCCCCC",
    "border_strong":     "#888888",
    "border_cell":       "#DDDDDD",
    "cal_today_bg":      "#0A0A0A",
    "cal_today_text":    "#FFFFFF",
    "cal_weekend_bg":    "#F9F9F9",
    "cal_header_bg":     "#0A0A0A",
    "cal_header_text":   "#FFFFFF",
    "cal_selected_bg":   "#2D2D2D",
    "cal_selected_text": "#FFFFFF",
    "status_active_bg":  "#0A0A0A",
    "status_active_txt": "#FFFFFF",
    "status_closed_bg":  "#E0E0E0",
    "status_closed_txt": "#555555",
    "scrollbar":         "#CCCCCC",
    "scrollbar_hover":   "#999999",
    "entry_bg":          "#FFFFFF",
    "entry_border":      "#AAAAAA",
    "chk_on":            "#0A0A0A",
    "chk_off":           "#AAAAAA",
    "sunday_border":     "#CC0000",
    "sunday_text":       "#CC0000",
    "toggle_adv_bg":     "#0A0A0A",
    "toggle_cli_bg":     "#2D5FA6",
    "toggle_off":        "#555555",
}

FONTS = {
    "brand":             ("Bauhaus 93",    42, "bold"),
    "brand_sub":         ("Bahnschrift",   13, "bold", "italic"),
    "navbar_brand":      ("Bauhaus 93",    22, "bold"),
    "navbar_brand_icon": ("Georgia",       28, "normal"),
    "navbar_brand_sub":  ("Georgia",        9, "italic"),
    "heading_1":         ("Helvetica Neue", 18, "bold"),
    "heading_2":         ("Helvetica Neue", 14, "bold"),
    "body":              ("Helvetica Neue", 12, "normal"),
    "body_bold":         ("Helvetica Neue", 12, "bold"),
    "caption":           ("Helvetica Neue", 10, "normal"),
    "caption_bold":      ("Helvetica Neue", 10, "bold"),
    "navbar":            ("Helvetica Neue", 12, "bold"),
    "navbar_item":       ("Helvetica Neue", 11, "normal"),
    "clock":             ("Helvetica Neue", 30, "bold"),
    "date_big":          ("Helvetica Neue", 15, "bold"),
    "receipt_title":     ("Georgia",        16, "bold"),
    "receipt_body":      ("Helvetica Neue", 11, "normal"),
    "receipt_bold":      ("Helvetica Neue", 11, "bold"),
}

DIMS = {
    "navbar_height": 68,
    "cal_cell_w":    110,
    "cal_cell_h":    80,
    "corner_radius": 6,
    "btn_corner":    4,
    "dropdown_w":    210,
}

def _check_font_available(font_name: str) -> bool:
    """Return True if *font_name* is available in the Tk font catalogue."""
    try:
        return font_name.lower() in [f.lower() for f in tkFont.families()]
    except Exception:
        return False

_HAS_BAUHAUS    = _check_font_available("Bauhaus 93")
_HAS_BLACKADDER = _check_font_available("Blackadder ITC")

# Title font for the panel header
BNS_FONT_TITLE = (
    "Blackadder ITC" if _HAS_BLACKADDER else
    "Bauhaus 93"     if _HAS_BAUHAUS    else
    "Georgia"
), 18, "bold"

# Section number badge
BNS_FONT_SECTION_NO = (
    "Bauhaus 93" if _HAS_BAUHAUS else "Georgia"
), 14, "bold"

# Section title / heading inside panel
BNS_FONT_SECTION_TITLE = (
    "Bauhaus 93" if _HAS_BAUHAUS else "Helvetica Neue"
), 11, "bold"

# Body text — summary
BNS_FONT_BODY   = ("Helvetica Neue", 10, "normal")
BNS_FONT_BADGE  = ("Helvetica Neue",  9, "bold")
BNS_FONT_BUTTON = ("Helvetica Neue", 10, "bold")

# BNS panel colour palette
BNS_COLORS = {
    "panel_bg":       "#0a0a0a",   # deep navy
    "panel_border":   "#FFFFFF",   # slightly lighter navy for border
    "header_bg":      "#0a0a0a",   # darker navy strip
    "title_fg":       "#FFFFFF",   # golden yellow
    "section_no_fg":  "#FFFFFF",   # white
    "section_title_fg": "#FFFFFF", # light blue
    "body_fg":        "#FFFFFF",   # light grey-blue
    "ipc_fg":         "#FFFFFF",   # muted blue-grey for IPC equivalent tag
    "cat_bg":         "#FFFFFF",   # category badge background
    "cat_fg":         "#0a0a0a",   # category badge text
    "punishment_fg":  "#CC0000",   # light orange for punishment line
    "btn_bg":         "#525558",   # next button background
    "btn_fg":         "#FFFFFF",   # next button text
    "btn_hover":      "#0a0a0a",   # next button hover
    "divider":        "#FFFFFF",
    "timer_fg":       "#525558",   # muted for auto-refresh countdown
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — DATABASE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
DB_CONFIG = {
    "host":               "localhost",
    "port":               3306,
    "user":               "root",
    "password":           "root",  
    "database":           "advocacy_db_v7_1",
    "charset":            "utf8mb4",
    "autocommit":         False,
    "connection_timeout": 10,
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — DB CLASS
# ══════════════════════════════════════════════════════════════════════════════

class DB:
    """Single-connection database layer for ADVOCACY."""

    def __init__(self):
        self._conn = None
        self._connect()

    # ── Connection ───────────────────────────────────────────────────────────

    def _connect(self):
        try:
            self._conn = mysql.connector.connect(**DB_CONFIG)
        except MySQLError as e:
            messagebox.showerror(
                "Database Connection Error",
                f"Cannot connect to MySQL database 'advocacy_db'.\n\n"
                f"Please check:\n"
                f"  \u2022 MySQL 8.0 server is running\n"
                f"  \u2022 DB_CONFIG credentials are correct\n"
                f"  \u2022 The advocacy_db database has been created\n\n"
                f"Error: {e}",
            )
            sys.exit(1)

    def _execute(self, sql, params=(), fetch="none"):
        try:
            if self._conn is None or not self._conn.is_connected():
                self._connect()
            cur = self._conn.cursor(dictionary=True)
            cur.execute(sql, params)
            if fetch == "one":
                result = cur.fetchone()
                cur.close()
                return result
            elif fetch == "all":
                result = cur.fetchall()
                cur.close()
                return result if result is not None else []
            else:
                self._conn.commit()
                lid = cur.lastrowid
                cur.close()
                return lid if lid else True
        except MySQLError as e:
            print(f"[ADVOCACY DB Error]: {e}")
            try:
                self._conn.rollback()
            except Exception:
                pass
            return None if fetch in ("one", "all") else False

    # ── Authentication ───────────────────────────────────────────────────────
    def authenticate_advocate(self, username: str, password: str):
        row = self._execute(
            "SELECT * FROM advocates WHERE username = %s AND is_active = 1",
            (username,), "one"
        )
        if not row:
            self.log_session("advocate", username, False)
            return None
        stored = row["password_hash"]
        ok = False
        try:
            ok = bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
        except Exception:
            ok = (stored == password)
        self.log_session("advocate", username, ok)
        return row if ok else None

    def authenticate_client(self, client_id: str, password: str):
        row = self._execute(
            "SELECT * FROM clients WHERE client_id = %s AND is_active = 1",
            (client_id,), "one"
        )
        if not row:
            self.log_session("client", client_id, False)
            return None
        stored = row["password_hash"]
        ok = False
        try:
            ok = bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
        except Exception:
            ok = (stored == password)
        self.log_session("client", client_id, ok)
        return row if ok else None

    def log_session(self, user_type: str, user_ref: str, success: bool) -> None:
        self._execute(
            "INSERT INTO login_sessions (user_type, user_ref, login_time, is_success) "
            "VALUES (%s, %s, NOW(), %s)",
            (user_type, user_ref, 1 if success else 0), "none"
        )

    # ── Advocate Profile ─────────────────────────────────────────────────────

    def get_advocate_profile(self, advocate_id: int):
        return self._execute(
            "SELECT advocate_id, username, full_name, bar_number, primary_court, "
            "chambers, phone, email FROM advocates WHERE advocate_id = %s",
            (advocate_id,), "one"
        )

    def update_advocate_profile(self, advocate_id: int, full_name: str,
                                bar_number: str, primary_court: str,
                                chambers: str, phone: str, email: str) -> bool:
        result = self._execute(
            "UPDATE advocates SET full_name=%s, bar_number=%s, primary_court=%s, "
            "chambers=%s, phone=%s, email=%s, updated_at=NOW() WHERE advocate_id=%s",
            (full_name, bar_number, primary_court, chambers, phone, email, advocate_id),
            "none"
        )
        return bool(result)

    def change_advocate_password(self, advocate_id: int,
                                  old_password: str, new_password: str):
        """Verify old password, then update to new bcrypt-hashed password.
        Returns True on success, None if old password wrong, False on error."""
        row = self._execute(
            "SELECT password_hash FROM advocates WHERE advocate_id = %s",
            (advocate_id,), "one"
        )
        if not row:
            return False
        stored = row["password_hash"]
        ok = False
        try:
            ok = bcrypt.checkpw(old_password.encode("utf-8"), stored.encode("utf-8"))
        except Exception:
            ok = (stored == old_password)  # fallback plain text
        if not ok:
            return None  # old password mismatch
        try:
            new_hash = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        except Exception:
            new_hash = new_password  # fallback
        result = self._execute(
            "UPDATE advocates SET password_hash=%s, updated_at=NOW() WHERE advocate_id=%s",
            (new_hash, advocate_id), "none"
        )
        return bool(result)

    def get_all_advocates(self) -> list:
        """Returns all active NON-ADMIN advocates (for selectors).
        Falls back gracefully if is_admin column does not yet exist."""
        try:
            rows = self._execute(
                "SELECT advocate_id, username, full_name, bar_number, primary_court "
                "FROM advocates WHERE is_active = 1 AND is_admin = 0 ORDER BY full_name ASC",
                fetch="all"
            )
        except Exception:
            # Column not yet added — fall back and exclude by username
            rows = self._execute(
                "SELECT advocate_id, username, full_name, bar_number, primary_court "
                "FROM advocates WHERE is_active = 1 AND username != 'admin' ORDER BY full_name ASC",
                fetch="all"
            )
        return rows or []

    def get_all_clients(self):
        return self._execute(
            "SELECT client_id, full_name, phone, email, address "
            "FROM clients WHERE is_active = 1 ORDER BY full_name ASC",
            fetch="all"
        )

    def get_cases_for_all_advocates(self, date_obj=None) -> list:
        """Returns cases for ALL advocates — used by admin only."""
        if date_obj is not None:
            return self._execute(
                "SELECT c.*, cl.full_name AS client_name, a.full_name AS advocate_name "
                "FROM cases c "
                "LEFT JOIN clients cl ON c.client_id = cl.client_id "
                "LEFT JOIN advocates a ON c.advocate_id = a.advocate_id "
                "WHERE c.upcoming_date = %s OR c.last_date = %s",
                (date_obj, date_obj), "all"
            ) or []
        else:
            return self._execute(
                "SELECT c.*, cl.full_name AS client_name, a.full_name AS advocate_name "
                "FROM cases c "
                "LEFT JOIN clients cl ON c.client_id = cl.client_id "
                "LEFT JOIN advocates a ON c.advocate_id = a.advocate_id "
                "ORDER BY c.upcoming_date DESC",
                fetch="all"
            ) or []

    def create_advocate(self, username: str, password_plain: str, full_name: str,
                        bar_number: str, primary_court: str, chambers: str,
                        phone: str, email: str) -> bool:
        """Creates a new advocate account. Returns True on success."""
        try:
            password_hash = bcrypt.hashpw(
                password_plain.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        except Exception:
            password_hash = password_plain
        result = self._execute(
            "INSERT INTO advocates (username, password_hash, full_name, bar_number, "
            "primary_court, chambers, phone, email, is_active, created_at, updated_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,NOW(),NOW())",
            (username, password_hash, full_name, bar_number,
             primary_court, chambers, phone, email),
            "none"
        )
        return bool(result)

    # ── Clients ──────────────────────────────────────────────────────────────

    def get_client(self, client_id: str):
        return self._execute(
            "SELECT * FROM clients WHERE client_id = %s",
            (client_id,), "one"
        )

    def update_client_profile(self, client_id: str, full_name: str,
                               phone: str, email: str, address: str) -> bool:
        result = self._execute(
            "UPDATE clients SET full_name=%s, phone=%s, email=%s, "
            "address=%s, updated_at=NOW() WHERE client_id=%s",
            (full_name, phone, email, address, client_id), "none"
        )
        return bool(result)

    def change_client_password(self, client_id: str,
                                old_password: str, new_password: str):
        """Verify old password, then update to new bcrypt-hashed password.
        Returns True on success, None if old password wrong, False on error."""
        row = self._execute(
            "SELECT password_hash FROM clients WHERE client_id = %s",
            (client_id,), "one"
        )
        if not row:
            return False
        stored = row["password_hash"]
        ok = False
        try:
            ok = bcrypt.checkpw(old_password.encode("utf-8"), stored.encode("utf-8"))
        except Exception:
            ok = (stored == old_password)
        if not ok:
            return None  # old password mismatch
        try:
            new_hash = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        except Exception:
            new_hash = new_password
        result = self._execute(
            "UPDATE clients SET password_hash=%s, updated_at=NOW() WHERE client_id=%s",
            (new_hash, client_id), "none"
        )
        return bool(result)

    def create_client(self, client_id: str, full_name: str, phone: str,
                      email: str, address: str, password_plain: str) -> bool:
        try:
            password_hash = bcrypt.hashpw(
                password_plain.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        except Exception:
            password_hash = password_plain
        result = self._execute(
            "INSERT INTO clients (client_id, full_name, phone, email, address, "
            "password_hash, is_active, created_at, updated_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,1,NOW(),NOW())",
            (client_id, full_name, phone, email, address, password_hash),
            "none"
        )
        return bool(result)

    def get_next_client_id(self) -> str:
        row = self._execute(
            "SELECT client_id FROM clients ORDER BY client_id DESC LIMIT 1",
            fetch="one"
        )
        if not row:
            return "C001"
        last_id = row["client_id"]
        try:
            num = int(last_id[1:]) + 1
            return f"C{num:03d}"
        except (ValueError, IndexError):
            return "C001"

    # ── Cases ─────────────────────────────────────────────────────────────────

    def get_case(self, case_no: str):
        return self._execute(
            "SELECT c.*, cl.full_name AS client_name "
            "FROM cases c LEFT JOIN clients cl ON c.client_id = cl.client_id "
            "WHERE c.case_no = %s",
            (case_no,), "one"
        )

    def validate_case_owner(self, case_no: str, advocate_id: int) -> bool:
        """Returns True only if this case belongs to this advocate."""
        row = self._execute(
            "SELECT 1 FROM cases WHERE case_no = %s AND advocate_id = %s",
            (case_no, advocate_id), "one"
        )
        return bool(row)

    def client_has_advocate_cases(self, client_id: str, advocate_id: int) -> bool:
        """Returns True if the client has at least one case under this advocate."""
        row = self._execute(
            "SELECT 1 FROM cases WHERE client_id = %s AND advocate_id = %s LIMIT 1",
            (client_id, advocate_id), "one"
        )
        return bool(row)

    def get_cases_for_client(self, client_id: str, advocate_id: int = None):
        """Returns cases for a client. If advocate_id given, only that advocate's cases."""
        if advocate_id is not None:
            return self._execute(
                "SELECT * FROM cases WHERE client_id = %s AND advocate_id = %s "
                "ORDER BY filing_date DESC",
                (client_id, advocate_id), "all"
            )
        return self._execute(
            "SELECT * FROM cases WHERE client_id = %s ORDER BY filing_date DESC",
            (client_id,), "all"
        )

    def get_cases_for_date(self, date_obj: datetime.date, advocate_id: int = None):
        """Returns cases for a specific date, filtered by advocate_id.
        If advocate_id is None, returns ALL (for admin use only)."""
        if advocate_id is not None:
            return self._execute(
                "SELECT c.*, cl.full_name AS client_name "
                "FROM cases c LEFT JOIN clients cl ON c.client_id = cl.client_id "
                "WHERE (c.upcoming_date = %s OR c.last_date = %s) "
                "AND c.advocate_id = %s",
                (date_obj, date_obj, advocate_id), "all"
            ) or []
        else:
            return self._execute(
                "SELECT c.*, cl.full_name AS client_name "
                "FROM cases c LEFT JOIN clients cl ON c.client_id = cl.client_id "
                "WHERE c.upcoming_date = %s OR c.last_date = %s",
                (date_obj, date_obj), "all"
            ) or []

    def get_cases_for_client_on_date(self, client_id: str, date_obj: datetime.date):
        return self._execute(
            "SELECT * FROM cases WHERE client_id = %s AND upcoming_date = %s",
            (client_id, date_obj), "all"
        )

    def save_new_case(self, case_no, case_name, client_id, advocate_id,
                      court, judge, case_type, filing_date_str, status, next_step) -> bool:
        fd = None
        for fmt in ("%d %b %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                fd = datetime.datetime.strptime(filing_date_str.strip(), fmt).date()
                break
            except ValueError:
                continue
        if fd is None:
            fd = datetime.date.today()
        result = self._execute(
            "INSERT INTO cases (case_no, case_name, client_id, advocate_id, court, "
            "judge, case_type, filing_date, status, next_step, created_at, updated_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())",
            (case_no, case_name, client_id, advocate_id, court,
             judge if judge else None, case_type, fd, status,
             next_step if next_step else None),
            "none"
        )
        return bool(result)

    def update_case_details(self, case_no, case_name, court, judge,
                             upcoming_date_str, next_step) -> bool:
        ud = None
        for fmt in ("%d %b %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                ud = datetime.datetime.strptime(upcoming_date_str.strip(), fmt).date()
                break
            except ValueError:
                continue
        result = self._execute(
            "UPDATE cases SET case_name=%s, court=%s, judge=%s, "
            "upcoming_date=%s, next_step=%s, updated_at=NOW() WHERE case_no=%s",
            (case_name, court, judge if judge else None,
             ud, next_step if next_step else None, case_no),
            "none"
        )
        return bool(result)

    # ── Timeline ──────────────────────────────────────────────────────────────

    def get_timeline(self, case_no: str, client_visible_only: bool = False):
        if client_visible_only:
            sql = ("SELECT * FROM case_timeline "
                   "WHERE case_no = %s AND client_visible = 1 ORDER BY event_date ASC")
        else:
            sql = "SELECT * FROM case_timeline WHERE case_no = %s ORDER BY event_date ASC"
        return self._execute(sql, (case_no,), "all")

    def add_timeline_entry(self, case_no, event_title, event_note,
                           client_visible, created_by) -> bool:
        result = self._execute(
            "INSERT INTO case_timeline "
            "(case_no, event_date, event_title, event_note, client_visible, "
            "created_by, created_at, updated_at) "
            "VALUES (%s, CURDATE(), %s, %s, %s, %s, NOW(), NOW())",
            (case_no, event_title, event_note, client_visible, created_by), "none"
        )
        if result:
            self._execute("UPDATE cases SET updated_at=NOW() WHERE case_no=%s", (case_no,), "none")
            return True
        return False

    def add_timeline_entry_on_date(self, case_no: str, event_date: datetime.date,
                                   event_title: str, event_note: str,
                                   client_visible: int, created_by: int) -> bool:
        result = self._execute(
            "INSERT INTO case_timeline (case_no, event_date, event_title, event_note, "
            "client_visible, created_by, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())",
            (case_no, event_date, event_title, event_note, client_visible, created_by),
            "none"
        )
        if result:
            self._execute("UPDATE cases SET updated_at=NOW() WHERE case_no=%s", (case_no,), "none")
            return True
        return False

    def set_timeline_visibility(self, timeline_id: int, client_visible: int) -> bool:
        result = self._execute(
            "UPDATE case_timeline SET client_visible = %s, updated_at = NOW() "
            "WHERE timeline_id = %s",
            (client_visible, timeline_id), "none"
        )
        return bool(result)

    # ── Payments ──────────────────────────────────────────────────────────────

    def get_payments_all(self, advocate_id: int = None):
        """Returns payments. If advocate_id given, shows only that advocate's records."""
        if advocate_id is not None:
            return self._execute(
                "SELECT p.*, cl.full_name AS client_name, c.case_name, c.upcoming_date "
                "FROM payments p "
                "LEFT JOIN clients cl ON p.client_id = cl.client_id "
                "LEFT JOIN cases c ON p.case_no = c.case_no "
                "WHERE p.advocate_id = %s "
                "ORDER BY p.created_at DESC",
                (advocate_id,), "all"
            )
        return self._execute(
            "SELECT p.*, cl.full_name AS client_name, c.case_name, c.upcoming_date "
            "FROM payments p "
            "LEFT JOIN clients cl ON p.client_id = cl.client_id "
            "LEFT JOIN cases c ON p.case_no = c.case_no "
            "ORDER BY p.created_at DESC",
            fetch="all"
        )

    def get_payments_for_client(self, client_id: str):
        return self._execute(
            "SELECT p.*, cl.full_name AS client_name, c.case_name "
            "FROM payments p "
            "LEFT JOIN clients cl ON p.client_id = cl.client_id "
            "LEFT JOIN cases c ON p.case_no = c.case_no "
            "WHERE p.client_id = %s "
            "ORDER BY p.created_at DESC",
            (client_id,), "all"
        )

    def get_payment_totals_today(self, advocate_id: int = None) -> dict:
        if advocate_id is not None:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS today_total "
                "FROM payments WHERE payment_date = CURDATE() AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS today_total "
                "FROM payments WHERE payment_date = CURDATE()",
                fetch="one"
            )
        return {"today_total": float(row["today_total"]) if row else 0.0}

    def get_payment_totals_month(self, advocate_id: int = None) -> dict:
        if advocate_id is not None:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS month_total FROM payments "
                "WHERE MONTH(payment_date) = MONTH(CURDATE()) "
                "AND YEAR(payment_date) = YEAR(CURDATE()) AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS month_total FROM payments "
                "WHERE MONTH(payment_date) = MONTH(CURDATE()) "
                "AND YEAR(payment_date) = YEAR(CURDATE())",
                fetch="one"
            )
        return {"month_total": float(row["month_total"]) if row else 0.0}

    
    def get_payment_total_for_period(self, period: str, advocate_id: int = None) -> float:
        """Returns total payments for the selected period, filtered by advocate_id."""
        period_sql = {
            "Today":        "payment_date = CURDATE()",
            "Yesterday":    "payment_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)",
            "Last 1 Week":  "payment_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)",
            "Last 1 Month": "payment_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)",
            "Last 1 Year":  "payment_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)",
            "All Time":     "1=1",
        }
        where = period_sql.get(period, "1=1")
        if advocate_id is not None:
            row = self._execute(
                f"SELECT COALESCE(SUM(amount), 0) AS total FROM payments "
                f"WHERE {where} AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                f"SELECT COALESCE(SUM(amount), 0) AS total FROM payments WHERE {where}",
                fetch="one"
            )
        return float(row["total"]) if row else 0.0

    def get_expense_total_for_period(self, period: str, advocate_id: int = None) -> float:
        """Returns total expenses for the selected period, filtered by advocate_id."""
        period_sql = {
            "Today":        "expense_date = CURDATE()",
            "Yesterday":    "expense_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)",
            "Last 1 Week":  "expense_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)",
            "Last 1 Month": "expense_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)",
            "Last 1 Year":  "expense_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)",
            "All Time":     "1=1",
        }
        where = period_sql.get(period, "1=1")
        if advocate_id is not None:
            row = self._execute(
                f"SELECT COALESCE(SUM(amount), 0) AS total FROM expenses "
                f"WHERE {where} AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                f"SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE {where}",
                fetch="one"
            )
        return float(row["total"]) if row else 0.0

    def record_payment(self, client_id, case_no, advocate_id, amount, note):
        receipt_no = (
            f"RCP/{datetime.date.today().strftime('%Y%m%d')}/{random.randint(1000,9999)}"
        )
        new_pid = self._execute(
            "INSERT INTO payments (client_id, case_no, advocate_id, "
            "payment_date, amount, note, receipt_no, created_at, updated_at) "
            "VALUES (%s,%s,%s,CURDATE(),%s,%s,%s,NOW(),NOW())",
            (client_id, case_no, advocate_id, amount, note, receipt_no), "none"
        )
        return int(new_pid) if new_pid else None

    def save_receipt_record(self, payment_id, receipt_no, generated_by="advocate",
                            file_path=None) -> bool:
        if payment_id is None:
            return False
        result = self._execute(
            "INSERT INTO receipts (receipt_no, payment_id, generated_at, "
            "generated_by, file_path, created_at, updated_at) "
            "VALUES (%s,%s,NOW(),%s,%s,NOW(),NOW())",
            (receipt_no, payment_id, generated_by, file_path), "none"
        )
        return bool(result)

    def apply_partial_payment_to_dues(self, client_id: str, case_no: str,
                                       payment_amount: float) -> bool:
        due = self._execute(
            "SELECT due_id, amount_due FROM pending_dues "
            "WHERE client_id=%s AND case_no=%s AND is_paid=0 "
            "ORDER BY due_id ASC LIMIT 1",
            (client_id, case_no), "one"
        )
        if not due:
            return True
        remaining = float(due["amount_due"]) - payment_amount
        if remaining <= 0:
            result = self._execute(
                "UPDATE pending_dues SET is_paid=1, paid_on=CURDATE(), updated_at=NOW() "
                "WHERE due_id=%s",
                (due["due_id"],), "none"
            )
        else:
            result = self._execute(
                "UPDATE pending_dues SET amount_due=%s, updated_at=NOW() WHERE due_id=%s",
                (remaining, due["due_id"]), "none"
            )
        return bool(result)

    # ── Pending Dues ──────────────────────────────────────────────────────────

    def get_pending_dues_all(self, advocate_id: int = None):
        """Returns pending dues. If advocate_id given, shows only that advocate's dues."""
        if advocate_id is not None:
            return self._execute(
                "SELECT pd.*, cl.full_name AS client_name, c.case_name, c.upcoming_date "
                "FROM pending_dues pd "
                "LEFT JOIN clients cl ON pd.client_id = cl.client_id "
                "LEFT JOIN cases c ON pd.case_no = c.case_no "
                "WHERE pd.is_paid = 0 AND pd.advocate_id = %s ORDER BY pd.due_date ASC",
                (advocate_id,), "all"
            )
        return self._execute(
            "SELECT pd.*, cl.full_name AS client_name, c.case_name, c.upcoming_date "
            "FROM pending_dues pd "
            "LEFT JOIN clients cl ON pd.client_id = cl.client_id "
            "LEFT JOIN cases c ON pd.case_no = c.case_no "
            "WHERE pd.is_paid = 0 ORDER BY pd.due_date ASC",
            fetch="all"
        )

    def get_pending_dues_for_client(self, client_id: str):
        return self._execute(
            "SELECT pd.*, cl.full_name AS client_name, c.case_name "
            "FROM pending_dues pd "
            "LEFT JOIN clients cl ON pd.client_id = cl.client_id "
            "LEFT JOIN cases c ON pd.case_no = c.case_no "
            "WHERE pd.is_paid = 0 AND pd.client_id = %s "
            "ORDER BY pd.due_date ASC",
            (client_id,), "all"
        )

    def get_pending_dues_total(self, advocate_id: int = None) -> float:
        if advocate_id is not None:
            row = self._execute(
                "SELECT COALESCE(SUM(amount_due), 0) AS total "
                "FROM pending_dues WHERE is_paid=0 AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                "SELECT COALESCE(SUM(amount_due), 0) AS total FROM pending_dues WHERE is_paid=0",
                fetch="one"
            )
        return float(row["total"]) if row else 0.0

    def add_pending_due(self, client_id: str, case_no: str, advocate_id: int,
                        amount_due: float, due_date: datetime.date,
                        description: str) -> bool:
        result = self._execute(
            "INSERT INTO pending_dues (client_id, case_no, advocate_id, amount_due, "
            "due_date, description, is_paid, created_at, updated_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,0,NOW(),NOW())",
            (client_id, case_no, advocate_id, amount_due, due_date, description),
            "none"
        )
        return bool(result)

    # ── Expenses ──────────────────────────────────────────────────────────────

    def get_expenses_all(self, advocate_id: int = None):
        """Returns expenses. If advocate_id given, shows only that advocate's records."""
        if advocate_id is not None:
            return self._execute(
                "SELECT e.*, cl.full_name AS client_name, c.upcoming_date "
                "FROM expenses e "
                "LEFT JOIN clients cl ON e.client_id = cl.client_id "
                "LEFT JOIN cases c ON e.case_no = c.case_no "
                "WHERE e.advocate_id = %s "
                "ORDER BY e.expense_date DESC",
                (advocate_id,), "all"
            )
        return self._execute(
            "SELECT e.*, cl.full_name AS client_name, c.upcoming_date "
            "FROM expenses e "
            "LEFT JOIN clients cl ON e.client_id = cl.client_id "
            "LEFT JOIN cases c ON e.case_no = c.case_no "
            "ORDER BY e.expense_date DESC",
            fetch="all"
        )

    def get_expense_totals_today(self, advocate_id: int = None) -> float:
        if advocate_id is not None:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS today_total "
                "FROM expenses WHERE expense_date = CURDATE() AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS today_total "
                "FROM expenses WHERE expense_date = CURDATE()",
                fetch="one"
            )
        return float(row["today_total"]) if row else 0.0

    def get_expense_totals_month(self, advocate_id: int = None) -> float:
        if advocate_id is not None:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS month_total FROM expenses "
                "WHERE MONTH(expense_date)=MONTH(CURDATE()) AND YEAR(expense_date)=YEAR(CURDATE()) "
                "AND advocate_id = %s",
                (advocate_id,), "one"
            )
        else:
            row = self._execute(
                "SELECT COALESCE(SUM(amount), 0) AS month_total FROM expenses "
                "WHERE MONTH(expense_date)=MONTH(CURDATE()) AND YEAR(expense_date)=YEAR(CURDATE())",
                fetch="one"
            )
        return float(row["month_total"]) if row else 0.0

    def add_expense(self, client_id, case_no, advocate_id, amount, title,
                    description="") -> bool:
        result = self._execute(
            "INSERT INTO expenses (client_id, case_no, advocate_id, "
            "expense_date, amount, title, description, created_at, updated_at) "
            "VALUES (%s,%s,%s,CURDATE(),%s,%s,%s,NOW(),NOW())",
            (client_id, case_no, advocate_id, amount, title, description or ""), "none"
        )
        return bool(result)

    # ── v5: Bhartiya Nyaya Samhita DB methods ───────────────────────────────────

    def get_random_bns_section(self) -> dict | None:
        """Returns one random active BNS section.
        Returns None gracefully if the table does not yet exist."""
        try:
            return self._execute(
                "SELECT section_id, bns_number, section_title, ipc_equivalent, "
                "category, summary, punishment_summary "
                "FROM bns_sections WHERE is_active = 1 "
                "ORDER BY RAND() LIMIT 1",
                fetch="one",
            )
        except Exception:
            return None

    def get_random_bns_section_excluding(self, exclude_id: int) -> dict | None:
        """Returns one random active BNS section excluding *exclude_id*.
        Falls back to get_random_bns_section if only one row exists."""
        try:
            row = self._execute(
                "SELECT section_id, bns_number, section_title, ipc_equivalent, "
                "category, summary, punishment_summary "
                "FROM bns_sections WHERE is_active = 1 AND section_id != %s "
                "ORDER BY RAND() LIMIT 1",
                (exclude_id,),
                fetch="one",
            )
            return row if row else self.get_random_bns_section()
        except Exception:
            return self.get_random_bns_section()

    # ── v6: Smart Search — autocomplete data ─────────────────────────────────
    def get_all_case_nos_for_advocate(self, advocate_id):
        rows = self._execute(
            "SELECT DISTINCT case_no FROM cases WHERE advocate_id=%s ORDER BY case_no",
            (advocate_id,), "all") or []
        return [r["case_no"] for r in rows if r.get("case_no")]

    def get_all_client_names_for_advocate(self, advocate_id):
        rows = self._execute(
            "SELECT DISTINCT cl.full_name FROM cases c "
            "JOIN clients cl ON c.client_id=cl.client_id "
            "WHERE c.advocate_id=%s ORDER BY cl.full_name",
            (advocate_id,), "all") or []
        return [r["full_name"] for r in rows if r.get("full_name")]

    def get_all_client_ids_for_advocate(self, advocate_id):
        rows = self._execute(
            "SELECT DISTINCT c.client_id FROM cases c WHERE c.advocate_id=%s ORDER BY c.client_id",
            (advocate_id,), "all") or []
        return [str(r["client_id"]) for r in rows if r.get("client_id")]

    def get_all_hearing_dates_for_advocate(self, advocate_id):
        rows = self._execute(
            "SELECT DISTINCT upcoming_date FROM cases "
            "WHERE advocate_id=%s AND upcoming_date IS NOT NULL ORDER BY upcoming_date DESC",
            (advocate_id,), "all") or []
        return [str(r["upcoming_date"]) for r in rows if r.get("upcoming_date")]

    def get_cases_by_client_name(self, name_query, advocate_id):
        return self._execute(
            "SELECT c.case_no, c.case_name, cl.full_name AS client_name, c.client_id, c.upcoming_date "
            "FROM cases c JOIN clients cl ON c.client_id=cl.client_id "
            "WHERE c.advocate_id=%s AND cl.full_name LIKE %s ORDER BY cl.full_name",
            (advocate_id, f"%{name_query}%"), "all") or []

    def get_cases_by_client_id(self, cid_query, advocate_id):
        return self._execute(
            "SELECT c.case_no, c.case_name, cl.full_name AS client_name, c.client_id, c.upcoming_date "
            "FROM cases c JOIN clients cl ON c.client_id=cl.client_id "
            "WHERE c.advocate_id=%s AND CAST(c.client_id AS CHAR) LIKE %s ORDER BY c.client_id",
            (advocate_id, f"%{cid_query}%"), "all") or []

    def get_cases_by_hearing_date(self, date_query, advocate_id):
        return self._execute(
            "SELECT c.case_no, c.case_name, cl.full_name AS client_name, c.client_id, c.upcoming_date "
            "FROM cases c JOIN clients cl ON c.client_id=cl.client_id "
            "WHERE c.advocate_id=%s AND CAST(c.upcoming_date AS CHAR) LIKE %s ORDER BY c.upcoming_date",
            (advocate_id, f"%{date_query}%"), "all") or []

    def get_cases_by_case_no(self, case_no_query, advocate_id):
        return self._execute(
            "SELECT c.case_no, c.case_name, cl.full_name AS client_name, c.client_id, c.upcoming_date "
            "FROM cases c JOIN clients cl ON c.client_id=cl.client_id "
            "WHERE c.advocate_id=%s AND c.case_no LIKE %s ORDER BY c.case_no",
            (advocate_id, f"%{case_no_query}%"), "all") or []

    # ── v6: Dual Validation ───────────────────────────────────────────────────

    def validate_case_client_match(self, case_no, client_id, advocate_id):
        try:
            row = self._execute(
                "SELECT 1 FROM cases WHERE case_no=%s AND client_id=%s AND advocate_id=%s",
                (case_no, client_id, advocate_id), "one")
            return bool(row)
        except Exception:
            return False

    # ── v6: Assistant System ──────────────────────────────────────────────────

    def is_username_taken(self, username):
        r1 = self._execute("SELECT 1 FROM advocates WHERE username=%s", (username,), "one")
        if r1: return True
        try:
            r3 = self._execute("SELECT 1 FROM advocate_assistants WHERE username=%s", (username,), "one")
            if r3: return True
        except Exception:
            pass
        return False

    def create_assistant(self, linked_advocate_id, username, password_plain, full_name, phone="", email=""):
        try:
            import bcrypt as _bcrypt
            pw_hash = _bcrypt.hashpw(password_plain.encode(), _bcrypt.gensalt()).decode()
        except Exception:
            pw_hash = password_plain
        ok = self._execute(
            "INSERT INTO advocate_assistants "
            "(username,password_hash,full_name,phone,email,linked_advocate_id,is_active,created_at,updated_at) "
            "VALUES(%s,%s,%s,%s,%s,%s,1,NOW(),NOW())",
            (username, pw_hash, full_name, phone or None, email or None, linked_advocate_id), "none")
        if not ok:
            return False
        row = self._execute("SELECT assistant_id FROM advocate_assistants WHERE username=%s",
                            (username,), "one")
        if not row:
            return False
        aid = row["assistant_id"]
        for fk in ["case_info","case_addition","case_updation","client_cases",
                   "fees_tracking","expenses","money_incoming"]:
            self._execute(
                "INSERT IGNORE INTO assistant_permissions(assistant_id,feature_key,has_access) VALUES(%s,%s,0)",
                (aid, fk), "none")
        return True

    def get_assistants_for_advocate(self, advocate_id):
        return self._execute(
            "SELECT assistant_id,username,full_name,phone,email,is_active "
            "FROM advocate_assistants WHERE linked_advocate_id=%s ORDER BY full_name",
            (advocate_id,), "all") or []

    def get_assistant_by_id(self, assistant_id):
        return self._execute(
            "SELECT * FROM advocate_assistants WHERE assistant_id=%s", (assistant_id,), "one") or {}

    def get_assistant_by_username_for_advocate(self, username, advocate_id):
        return self._execute(
            "SELECT * FROM advocate_assistants WHERE username=%s AND linked_advocate_id=%s",
            (username, advocate_id), "one") or {}

    def delete_assistant(self, assistant_id):
        result = self._execute(
            "DELETE FROM advocate_assistants WHERE assistant_id=%s", (assistant_id,), "none")
        return bool(result)

    def authenticate_assistant(self, username, password):
        row = self._execute(
            "SELECT aa.*, a.full_name AS advocate_name, a.advocate_id AS linked_advocate_id "
            "FROM advocate_assistants aa "
            "JOIN advocates a ON aa.linked_advocate_id=a.advocate_id "
            "WHERE aa.username=%s AND aa.is_active=1",
            (username,), "one")
        if not row: return None
        try:
            import bcrypt as _bcrypt
            ok = _bcrypt.checkpw(password.encode(), row["password_hash"].encode())
        except Exception:
            ok = (row.get("password_hash") == password)
        return row if ok else None

    def get_assistant_permissions(self, assistant_id):
        rows = self._execute(
            "SELECT feature_key,has_access FROM assistant_permissions WHERE assistant_id=%s",
            (assistant_id,), "all") or []
        return {r["feature_key"]: bool(r["has_access"]) for r in rows}

    def set_assistant_permissions(self, assistant_id, permissions):
        for fk, val in permissions.items():
            self._execute(
                "INSERT INTO assistant_permissions(assistant_id,feature_key,has_access) "
                "VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE has_access=%s",
                (assistant_id, fk, 1 if val else 0, 1 if val else 0), "none")
        return True

    def get_all_assistants_admin(self):
        return self._execute(
            "SELECT aa.assistant_id,aa.username,aa.full_name,aa.phone,aa.email,"
            "aa.is_active,a.full_name AS advocate_name "
            "FROM advocate_assistants aa "
            "JOIN advocates a ON aa.linked_advocate_id=a.advocate_id "
            "ORDER BY a.full_name,aa.full_name",
            fetch="all") or []

    def update_assistant_profile(self, assistant_id, full_name, phone, email):
        result = self._execute(
            "UPDATE advocate_assistants SET full_name=%s,phone=%s,email=%s,updated_at=NOW() "
            "WHERE assistant_id=%s",
            (full_name, phone, email, assistant_id), "none")
        return bool(result)

    def change_assistant_password(self, assistant_id, old_password, new_password):
        """Returns True on success, None if old password wrong, False on DB error."""
        row = self._execute(
            "SELECT password_hash FROM advocate_assistants WHERE assistant_id=%s",
            (assistant_id,), "one")
        if not row:
            return False
        try:
            import bcrypt as _bcrypt
            ok = _bcrypt.checkpw(old_password.encode(), row["password_hash"].encode())
        except Exception:
            ok = (row.get("password_hash") == old_password)
        if not ok:
            return None  # wrong old password
        try:
            import bcrypt as _bcrypt
            new_hash = _bcrypt.hashpw(new_password.encode(), _bcrypt.gensalt()).decode()
        except Exception:
            new_hash = new_password
        result = self._execute(
            "UPDATE advocate_assistants SET password_hash=%s,updated_at=NOW() WHERE assistant_id=%s",
            (new_hash, assistant_id), "none")
        return bool(result)

    def set_assistant_active(self, assistant_id, is_active):
        result = self._execute(
            "UPDATE advocate_assistants SET is_active=%s,updated_at=NOW() WHERE assistant_id=%s",
            (is_active, assistant_id), "none")
        return bool(result)

    def close(self):
        if self._conn and self._conn.is_connected():
            self._conn.close()


# ── Global DB instance ────────────────────────────────────────────────────────
db = DB()


# ── v7: Application-Wide Zoom Control ─────────────────────────────────────────
_ZOOM_LEVELS = [0.75, 1.0, 1.25]
_ZOOM_LEVEL  = 1.0

# Store the base (unscaled) font sizes for recalculation on zoom
_BASE_FONTS = {k: v for k, v in FONTS.items()}

def _apply_zoom(level, on_zoom_cb=None):
    """Scale all fonts and CTk widgets to the given zoom level, then rebuild."""
    global _ZOOM_LEVEL, FONTS
    _ZOOM_LEVEL = level
    # Recalculate every font tuple with the scaled size
    new_fonts = {}
    for key, base in _BASE_FONTS.items():
        # base is e.g. ("Helvetica Neue", 12, "bold") or ("Georgia", 9, "italic")
        family = base[0]
        base_size = base[1]
        rest = base[2:]  # ("bold",) or ("bold", "italic") etc.
        new_size = max(7, int(round(base_size * level)))  # minimum size 7
        new_fonts[key] = (family, new_size, *rest)
    FONTS = new_fonts
    # Also scale CTk widgets (buttons, entries, scrollable frames etc.)
    try:
        import customtkinter as _ctk
        _ctk.set_widget_scaling(level)
    except Exception:
        pass
    # Trigger UI rebuild if callback provided
    if on_zoom_cb:
        on_zoom_cb()

def _build_zoom_controls(parent, on_zoom_cb=None):
    """Build A- / A / A+ buttons. on_zoom_cb is called after zoom to rebuild UI."""
    host = tk.Frame(parent, bg=COLORS["bg_secondary"])
    btns = []
    for label, level in [("A−", 0.75), ("A", 1.0), ("A+", 1.25)]:
        is_active = (abs(_ZOOM_LEVEL - level) < 0.01)
        bg = "#999999" if is_active else "#CCCCCC"
        btn = tk.Label(
            host, text=label, font=FONTS["caption_bold"],
            fg=COLORS["text_primary"], bg=bg,
            padx=6, pady=1, cursor="hand2",
        )
        btn.pack(side="left", padx=2, pady=3)
        btn.bind("<Button-1>", lambda e, lv=level: _apply_zoom(lv, on_zoom_cb))
        btn.bind("<Enter>",    lambda e, b=btn: b.config(bg="#AAAAAA"))
        btn.bind("<Leave>",    lambda e, b=btn, lv=level: b.config(
            bg="#999999" if abs(_ZOOM_LEVEL - lv) < 0.01 else "#CCCCCC"))
        btns.append(btn)
    return host






# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — SHARED UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _recursive_bg(widget, color):
    try:
        widget.config(bg=color)
    except Exception:
        pass
    for child in widget.winfo_children():
        _recursive_bg(child, color)


def _win(parent, title, w=820, h=580):
    """Still used only by open_print_receipt."""
    top = ctk.CTkToplevel(parent)
    top.title(f"ADVOCACY — {title}")
    top.geometry(f"{w}x{h}+{parent.winfo_rootx()+60}+{parent.winfo_rooty()+60}")
    top.configure(fg_color=COLORS["bg_primary"])
    top.grab_set()
    top.lift()
    _win_header(top, title)
    return top


def _win_header(parent, title):
    bar = tk.Frame(parent, bg=COLORS["navbar_bg"], height=44)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    tk.Label(bar, text=f"  ADVOCACY  ·  {title}",
             bg=COLORS["navbar_bg"], fg=COLORS["navbar_text"],
             font=FONTS["navbar"]).pack(side="left", padx=12, pady=10)


def _scrollable(parent, h=400):
    frame = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
        height=h,
    )
    frame.pack(fill="both", expand=True, padx=16, pady=10)
    return frame


def _divider(parent):
    tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x", padx=16, pady=4)


def _black_btn(parent, text, command, width=160):
    return ctk.CTkButton(
        parent, text=text, command=command, width=width,
        fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_on_dark"], font=FONTS["body_bold"],
        corner_radius=DIMS["btn_corner"],
    )


def _ghost_btn(parent, text, command, width=140):
    return ctk.CTkButton(
        parent, text=text, command=command, width=width,
        fg_color=COLORS["bg_secondary"], hover_color=COLORS["border"],
        text_color=COLORS["text_primary"], border_color=COLORS["border"],
        border_width=1, font=FONTS["body"], corner_radius=DIMS["btn_corner"],
    )


def _entry_row(parent, label_text, width=340, show=""):
    row = tk.Frame(parent, bg=COLORS["bg_primary"])
    row.pack(fill="x", padx=20, pady=4)
    tk.Label(row, text=label_text, font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
             width=22, anchor="w").pack(side="left")
    ent = ctk.CTkEntry(row, width=width, show=show,
                        fg_color=COLORS["entry_bg"],
                        text_color=COLORS["text_primary"],
                        border_color=COLORS["entry_border"],
                        placeholder_text_color=COLORS["text_muted"],
                        corner_radius=DIMS["btn_corner"])
    ent.pack(side="left", padx=6)
    return ent


def _case_link(parent, case_no, router, bg=None):
    bg = bg or COLORS["bg_card"]
    lbl = tk.Label(parent, text=case_no, font=FONTS["body_bold"],
                   fg=COLORS["link"], bg=bg, cursor="hand2", anchor="w")
    lbl.bind("<Enter>", lambda e: lbl.config(fg=COLORS["link_hover"]))
    lbl.bind("<Leave>", lambda e: lbl.config(fg=COLORS["link"]))
    lbl.bind("<Button-1>", lambda e, c=case_no: router("case_info", c))
    return lbl


def _status_pill(parent, status):
    bg = COLORS["status_active_bg"] if status == "Ongoing" else COLORS["status_closed_bg"]
    fg = COLORS["status_active_txt"] if status == "Ongoing" else COLORS["status_closed_txt"]
    tk.Label(parent, text=f"  {status}  ", bg=bg, fg=fg,
             font=FONTS["caption_bold"], padx=4, pady=2).pack(side="right", padx=8)


def _confirm_popup(dashboard, title, message):
    """Modal yes/no confirmation. Returns True if user clicked Yes."""
    result = [False]
    pop = tk.Toplevel(dashboard)
    pop.title(title)
    pop.resizable(False, False)
    pop.configure(bg=COLORS["bg_primary"])
    pop.grab_set()
    pop.update_idletasks()
    w, h = 420, 190
    x = dashboard.winfo_x() + (dashboard.winfo_width()  - w) // 2
    y = dashboard.winfo_y() + (dashboard.winfo_height() - h) // 2
    pop.geometry(f"{w}x{h}+{x}+{y}")
    tk.Label(pop, text=title, font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(pady=(18, 6))
    tk.Label(pop, text=message, font=FONTS["body"], fg=COLORS["text_secondary"],
             bg=COLORS["bg_primary"], wraplength=380, justify="center").pack(padx=16)
    btn_row = tk.Frame(pop, bg=COLORS["bg_primary"])
    btn_row.pack(pady=18)
    def yes():
        result[0] = True
        pop.destroy()
    def no():
        pop.destroy()
    _black_btn(btn_row, "Yes, Proceed", yes, 140).pack(side="left", padx=8)
    cancel = tk.Label(btn_row, text="  Cancel  ", font=FONTS["body_bold"],
                      fg=COLORS["text_primary"], bg=COLORS["bg_secondary"],
                      cursor="hand2", padx=6, pady=6)
    cancel.pack(side="left", padx=8)
    cancel.bind("<Button-1>", lambda e: no())
    pop.bind("<Escape>", lambda e: no())
    pop.wait_window()
    return result[0]


def _info_popup(parent, title, message):
    pop = ctk.CTkToplevel(parent)
    pop.title(f"ADVOCACY — {title}")
    pop.geometry("420x200")
    pop.configure(fg_color=COLORS["bg_primary"])
    pop.grab_set()
    pop.lift()
    bar = tk.Frame(pop, bg=COLORS["navbar_bg"], height=40)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    tk.Label(bar, text=f"  {title}", bg=COLORS["navbar_bg"],
             fg=COLORS["navbar_text"], font=FONTS["body_bold"]).pack(side="left", padx=12)
    tk.Label(pop, text=message, font=FONTS["body"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"],
             wraplength=360, justify="center").pack(pady=22)
    _black_btn(pop, "OK", pop.destroy, 120).pack()


def _fmt_date(d):
    if d is None:
        return "—"
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.strftime("%d %b %Y")
    return str(d)


def _fmt_amount(a):
    try:
        return f"Rs.{int(float(a)):,}"
    except (TypeError, ValueError):
        return "Rs.0"


def _make_table_header(parent, col_defs):
    """col_defs = [(label, min_width_px), ...]
    Returns the header frame (already packed) and the grid frame."""
    hdr = tk.Frame(parent, bg=COLORS["navbar_bg"])
    hdr.pack(fill="x", padx=16, pady=(0, 2))
    for i, (lbl, w) in enumerate(col_defs):
        hdr.columnconfigure(i, minsize=w, weight=1, uniform="col")
        tk.Label(hdr, text=lbl, font=FONTS["caption_bold"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"],
                 anchor="w").grid(row=0, column=i, sticky="ew", padx=6, pady=5)
    return hdr


def _make_table_row(parent, values_and_widths, bg=None):
    """values_and_widths = [(value_or_widget_factory, min_width_px), ...]
    Returns the row frame."""
    bg = bg or COLORS["bg_card"]
    row = tk.Frame(parent, bg=bg,
                   highlightbackground=COLORS["border_cell"], highlightthickness=1)
    row.pack(fill="x", pady=2, padx=2)
    for i, (val, w) in enumerate(values_and_widths):
        row.columnconfigure(i, minsize=w, weight=1, uniform="col")
        if callable(val):
            widget = val(row)
            widget.grid(row=0, column=i, sticky="ew", padx=6, pady=5)
        else:
            tk.Label(row, text=str(val) if val is not None else "—",
                     font=FONTS["body"], fg=COLORS["text_primary"],
                     bg=bg, anchor="w").grid(row=0, column=i, sticky="ew", padx=6, pady=5)
    return row


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — PDF RECEIPT GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def _make_receipt_no():
    return f"RCP/{datetime.date.today().strftime('%Y%m%d')}/{random.randint(1000,9999)}"


def _generate_pdf(filepath, data):
    c = _pdf_canvas.Canvas(filepath, pagesize=A4)
    W, H = A4
    c.setFillColorRGB(0.04, 0.04, 0.04)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(28*mm, H - 42, "ADVOCACY")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(28*mm, H - 56, "Legal Practice Management Suite")
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(W - 28*mm, H - 42, "PAYMENT RECEIPT")
    c.setFont("Helvetica", 9)
    c.drawRightString(W - 28*mm, H - 56, data["receipt_no"])
    c.setFillColorRGB(0, 0, 0)
    y = H - 115

    def row(label, value, bold_val=True):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawString(28*mm, y, label)
        c.setFont("Helvetica-Bold" if bold_val else "Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(85*mm, y, str(value))
        y -= 18

    row("Receipt No.", data["receipt_no"])
    row("Date", data["date"])
    y -= 5
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.line(28*mm, y, W - 28*mm, y)
    y -= 12
    row("Client Name", data["client"])
    row("Client ID",   data["client_id"])
    row("Case Number", data["case_no"])
    row("Case Title",  data["case_name"][:55], bold_val=False)
    y -= 5
    c.line(28*mm, y, W - 28*mm, y)
    y -= 14
    c.setFillColorRGB(0.04, 0.04, 0.04)
    c.rect(28*mm, y - 14, W - 56*mm, 32, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(34*mm, y - 4, "Amount Paid:")
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(W - 34*mm, y - 4, f"Rs. {data['amount']:,}")
    y -= 42
    row("Remarks",  data.get("note", "—"), bold_val=False)
    row("Advocate", "Prakash Singh  —  BAR/MH/2008/04521", bold_val=False)
    row("Court",    "Bombay High Court", bold_val=False)
    y -= 14
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.line(28*mm, y, W - 28*mm, y)
    y -= 18
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(28*mm, y, "This is a computer-generated receipt. No signature required.")
    c.drawString(28*mm, y - 12,
                 "ADVOCACY Legal Practice Management Suite  |  prakash.singh@advocacylaw.in")
    c.save()


def open_print_receipt(parent, pmt, generated_by="advocate"):
    """Receipt preview popup (stays as a popup)."""
    receipt_no = _make_receipt_no()
    client_row = db.get_client(pmt.get("client_id", "")) or {}
    case_row   = db.get_case(pmt.get("case_no", ""))   or {}
    data = {
        "receipt_no": receipt_no,
        "date":       pmt.get("date", datetime.date.today().strftime("%d %b %Y")),
        "client":     client_row.get("full_name", "—"),
        "client_id":  pmt.get("client_id", "—"),
        "case_no":    pmt.get("case_no", "—"),
        "case_name":  case_row.get("case_name", "—"),
        "amount":     int(float(pmt.get("amount", 0))),
        "note":       pmt.get("note", "—"),
    }
    top = ctk.CTkToplevel(parent)
    top.title("ADVOCACY — Transaction Receipt")
    top.geometry("540x560")
    top.configure(fg_color=COLORS["bg_primary"])
    top.grab_set()
    top.lift()
    hdr = tk.Frame(top, bg=COLORS["navbar_bg"], height=56)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Label(hdr, text="  ADVOCACY  ·  Transaction Receipt",
             bg=COLORS["navbar_bg"], fg=COLORS["navbar_text"],
             font=FONTS["navbar"]).pack(side="left", padx=12, pady=16)
    tk.Label(hdr, text=f"  {receipt_no}  ",
             bg=COLORS["navbar_hover"], fg=COLORS["navbar_text"],
             font=FONTS["caption_bold"]).pack(side="right", padx=12)
    card = tk.Frame(top, bg=COLORS["bg_card"],
                    highlightbackground=COLORS["border"], highlightthickness=1)
    card.pack(fill="both", expand=True, padx=20, pady=14)
    title_bar = tk.Frame(card, bg=COLORS["bg_secondary"])
    title_bar.pack(fill="x")
    tk.Label(title_bar, text="OFFICIAL PAYMENT RECEIPT", font=FONTS["receipt_title"],
             fg=COLORS["text_primary"], bg=COLORS["bg_secondary"], pady=12).pack()

    def rrow(label, val, bold=True):
        r = tk.Frame(card, bg=COLORS["bg_card"])
        r.pack(fill="x", padx=20, pady=3)
        tk.Label(r, text=label, font=FONTS["caption_bold"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"],
                 width=18, anchor="w").pack(side="left")
        tk.Label(r, text=val,
                 font=FONTS["receipt_bold"] if bold else FONTS["receipt_body"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"],
                 anchor="w", wraplength=310).pack(side="left")

    rrow("Receipt No.", data["receipt_no"])
    rrow("Date",         data["date"])
    tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", padx=20, pady=6)
    rrow("Client Name",  data["client"])
    rrow("Client ID",    data["client_id"])
    rrow("Case Number",  data["case_no"])
    rrow("Case Title",   data["case_name"], bold=False)
    tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", padx=20, pady=6)
    amt_box = tk.Frame(card, bg=COLORS["navbar_bg"])
    amt_box.pack(fill="x", padx=20, pady=6)
    tk.Label(amt_box, text="  Amount Paid", font=FONTS["body_bold"],
             fg=COLORS["text_muted"], bg=COLORS["navbar_bg"]).pack(side="left", pady=10)
    tk.Label(amt_box, text=f"Rs. {data['amount']:,}  ",
             font=FONTS["heading_1"],
             fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(side="right", pady=10)
    rrow("Remarks",  data["note"], bold=False)
    adv_name = data.get("advocate_name", "Advocate")
    adv_bar  = data.get("advocate_bar", "")
    rrow("Advocate", f"{adv_name}  {('|  ' + adv_bar) if adv_bar else ''}", bold=False)
    tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", padx=20, pady=6)
    tk.Label(card, text="Computer-generated receipt. Valid without signature.",
             font=FONTS["caption"], fg=COLORS["text_muted"],
             bg=COLORS["bg_card"]).pack(pady=(0, 10))

    def download():
        if not REPORTLAB_OK:
            messagebox.showwarning(
                "reportlab Not Found",
                "PDF library not installed.\nRun:  pip install reportlab",
                parent=top,
            )
            return
        fp = filedialog.asksaveasfilename(
            parent=top, defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Receipt_{receipt_no.replace('/', '_')}.pdf",
        )
        if not fp:
            return
        try:
            _generate_pdf(fp, data)
            db.save_receipt_record(pmt.get("payment_id"), receipt_no,
                                   generated_by, fp)
            _info_popup(top, "Downloaded", f"Receipt saved to:\n{fp}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=top)

    btn_bar = tk.Frame(top, bg=COLORS["bg_primary"])
    btn_bar.pack(pady=(0, 14))
    _black_btn(btn_bar, "\u2b07  Download PDF", download, 200).pack(side="left", padx=8)
    _ghost_btn(btn_bar, "Close", top.destroy, 120).pack(side="left", padx=8)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — FEATURE VIEW BUILDERS  (all in-window)
# ══════════════════════════════════════════════════════════════════════════════

def _render_case_detail(parent, row, router, is_client_view=False):
    case_no = row["case_no"]
    hdr = tk.Frame(parent, bg=COLORS["bg_secondary"])
    hdr.pack(fill="x", padx=16, pady=(6, 0))
    tk.Label(hdr, text=case_no, font=FONTS["heading_2"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=10, pady=6)
    _status_pill(hdr, row.get("status", "Ongoing"))
    tk.Label(parent, text=row.get("case_name", "—"), font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"],
             wraplength=820, justify="left").pack(anchor="w", padx=16, pady=(6, 2))
    meta = tk.Frame(parent, bg=COLORS["bg_primary"])
    meta.pack(fill="x", padx=16)
    for label, val in [
        ("Court",     row.get("court", "—")),
        ("Judge",     row.get("judge", "—")),
        ("Type",      row.get("case_type", "—")),
        ("Client",    row.get("client_name", "—")),
        ("Filed",     _fmt_date(row.get("filing_date"))),
        ("Next Date", _fmt_date(row.get("upcoming_date"))),
        ("Next Step", row.get("next_step", "—")),
    ]:
        r = tk.Frame(meta, bg=COLORS["bg_primary"])
        r.pack(fill="x", pady=1)
        tk.Label(r, text=f"{label}:", font=FONTS["body_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
                 width=14, anchor="w").pack(side="left")
        tk.Label(r, text=val or "—", font=FONTS["body"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"],
                 anchor="w").pack(side="left")
    _divider(parent)
    header_label = ("Case Progress (Shared Updates)" if is_client_view
                    else "Legal History Timeline  (Full — Advocate View)")
    tk.Label(parent, text=header_label, font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=16, pady=(4, 2))
    timeline = db.get_timeline(case_no, client_visible_only=is_client_view) or []
    scroll = _scrollable(parent, h=260)
    if not timeline:
        tk.Label(scroll, text="No updates for this case yet.",
                 font=FONTS["body"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(pady=20)
        return
    for i, evt in enumerate(reversed(timeline)):
        trow = tk.Frame(scroll, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border_cell"], highlightthickness=1)
        trow.pack(fill="x", pady=3, padx=2)
        tk.Label(trow, text=_fmt_date(evt.get("event_date")),
                 font=FONTS["caption_bold"],
                 fg=COLORS["text_on_dark"], bg=COLORS["cal_today_bg"],
                 padx=8, pady=4).pack(side="left")
        right = tk.Frame(trow, bg=COLORS["bg_card"])
        right.pack(side="left", fill="x", expand=True, padx=10, pady=4)
        tk.Label(right, text=evt.get("event_title", "—"), font=FONTS["body_bold"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
        tk.Label(right, text=evt.get("event_note", "—"), font=FONTS["caption"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                 anchor="w", wraplength=580, justify="left").pack(anchor="w")
        if i == 0:
            tk.Label(trow, text=" LATEST ", font=FONTS["caption_bold"],
                     fg=COLORS["text_on_dark"], bg=COLORS["navbar_hover"],
                     padx=4).pack(side="right", padx=6)


# ── 1.1 Case Info ─────────────────────────────────────────────────────────────
def build_case_info_view(parent, router, dashboard, prefill_case_no=None,
                         is_client_view=False, advocate_id=None):
    """advocate_id=None means admin/unrestricted view. Otherwise enforces ownership."""
    dashboard._back_bar(parent, "1.1 — Case Info")

    search_results_frame = [None]  # mutable ref

    def _clear_search_results():
        if search_results_frame[0]:
            for w in search_results_frame[0].winfo_children():
                w.destroy()
            search_results_frame[0].pack_forget()


    if advocate_id:
        def _do_search_ci(cat, q):
            if not q:
                _clear_search_results()
                return
            res = []
            if cat == "Case No.":
                res = db.get_cases_by_case_no(q, advocate_id) or []
            elif cat == "Client Name":
                res = db.get_cases_by_client_name(q, advocate_id) or []
            elif cat == "Client ID":
                res = db.get_cases_by_client_id(q, advocate_id) or []
            elif cat == "Last Hearing Date":
                res = db.get_cases_by_hearing_date(q, advocate_id) or []

            _clear_search_results()

            if not res:
                _info_popup(dashboard, "No Results", "No matching cases found.")
                return

            # Show sr_host (pre-created inside scroll, above og_search_bar)
            sr_host.pack(fill="x", padx=16, pady=(4, 0), before=og_search_bar)
            search_results_frame[0] = sr_host

            for w in sr_host.winfo_children():
                w.destroy()

            tk.Label(sr_host, text=f"Search Results ({len(res)} found)",
                     font=FONTS["caption_bold"], fg=COLORS["text_secondary"],
                     bg=COLORS["bg_primary"]).pack(anchor="w", pady=(2, 2))

            COL_DEFS_SR = [
                ("Case No.",          180),
                ("Client Name",       200),
                ("Client ID",         100),
                ("Last Hearing Date", 140),
            ]
            _make_table_header(sr_host, COL_DEFS_SR)

            for case_row in res:
                c_no = case_row.get("case_no", "\u2014")

                def _make_click_link(sr_case_no=c_no):
                    def make(row_frame):
                        lbl = tk.Label(row_frame, text=sr_case_no,
                                       font=FONTS["body_bold"],
                                       fg=COLORS["link"], bg=COLORS["bg_card"],
                                       cursor="hand2", anchor="w")
                        lbl.bind("<Enter>", lambda e: lbl.config(fg=COLORS["link_hover"]))
                        lbl.bind("<Leave>", lambda e: lbl.config(fg=COLORS["link"]))
                        def _on_click(e, cn=sr_case_no):
                            cn_var.set(cn)
                            _clear_search_results()
                            load(cn)
                        lbl.bind("<Button-1>", _on_click)
                        return lbl
                    return make

                _make_table_row(sr_host, [
                    (_make_click_link(c_no),                         COL_DEFS_SR[0][1]),
                    (case_row.get("client_name", "\u2014"),               COL_DEFS_SR[1][1]),
                    (str(case_row.get("client_id", "\u2014")),           COL_DEFS_SR[2][1]),
                    (_fmt_date(case_row.get("upcoming_date")),      COL_DEFS_SR[3][1]),
                ])

        def _get_sug_ci(cat):
            if cat == "Case No.":        return db.get_all_case_nos_for_advocate(advocate_id)
            if cat == "Client Name":     return db.get_all_client_names_for_advocate(advocate_id)
            if cat == "Client ID":       return db.get_all_client_ids_for_advocate(advocate_id)
            return db.get_all_hearing_dates_for_advocate(advocate_id)
        build_smart_search_bar(parent,
            ["Case No.", "Client Name", "Client ID", "Last Hearing Date"],
            _do_search_ci, _get_sug_ci)
    # ── Main scroll area ────────────────────────────────────────────────────────
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    # Pre-created search-results host (hidden until search fires)
    sr_host = tk.Frame(scroll, bg=COLORS["bg_primary"])
    # Not packed yet — _do_search_ci packs it with before=og_search_bar

    og_search_bar = tk.Frame(scroll, bg=COLORS["bg_secondary"])
    og_search_bar.pack(fill="x", padx=16, pady=(10, 0))
    tk.Label(og_search_bar, text="Case Number:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=(8, 4), pady=8)
    cn_var = tk.StringVar(value=prefill_case_no or "")
    ent = ctk.CTkEntry(og_search_bar, width=280, textvariable=cn_var,
                        fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                        border_color=COLORS["entry_border"],
                        placeholder_text="e.g. HC/MH/2024/001",
                        corner_radius=DIMS["btn_corner"])
    ent.pack(side="left", padx=6, pady=8)

    result_frame = tk.Frame(scroll, bg=COLORS["bg_primary"])
    result_frame.pack(fill="both", expand=True)

    def load(case_no=None):
        cn = (case_no or cn_var.get()).strip()
        for w in result_frame.winfo_children():
            w.destroy()
        row = db.get_case(cn)
        if not row:
            tk.Label(result_frame, text=f'Case "{cn}" not found.',
                     font=FONTS["body"], fg="#CC0000",
                     bg=COLORS["bg_primary"]).pack(pady=30)
            return
        # ─ v7: Ownership guard — advocates can only see their own cases ─
        if advocate_id is not None and not is_client_view:
            if not db.validate_case_owner(cn, advocate_id):
                tk.Label(result_frame,
                         text=f'⛔  Access Denied\nCase "{cn}" does not belong to your account.',
                         font=FONTS["body"], fg="#CC0000",
                         bg=COLORS["bg_primary"], justify="center").pack(pady=30)
                return
        _render_case_detail(result_frame, row, router, is_client_view=is_client_view)

    _black_btn(og_search_bar, "Load Case", load, 120).pack(side="left", padx=6, pady=8)
    ent.bind("<Return>", lambda e: load())
    if prefill_case_no:
        load(prefill_case_no)


# ── 1.2 New Case ──────────────────────────────────────────────────────────────
def build_new_case_view(parent, router, dashboard, advocate_id=1):
    dashboard._back_bar(parent, "1.2 — New Case Addition")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Initialize New Case", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))
    fields = {}
    for lbl in ["Case Number", "Case Name / Title", "Client ID", "Court",
                 "Judge", "Case Type", "Filing Date"]:
        fields[lbl] = _entry_row(scroll, lbl, width=360)

    row_f = tk.Frame(scroll, bg=COLORS["bg_primary"])
    row_f.pack(fill="x", padx=20, pady=4)
    tk.Label(row_f, text="Status", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
             width=22, anchor="w").pack(side="left")
    sv = tk.StringVar(value="Ongoing")
    ctk.CTkOptionMenu(row_f, values=["Ongoing", "Disposed", "Adjourned", "Stayed", "Settled"],
                      variable=sv, fg_color=COLORS["accent"],
                      button_color=COLORS["navbar_hover"],
                      button_hover_color=COLORS["accent_hover"],
                      text_color=COLORS["text_on_dark"],
                      dropdown_fg_color=COLORS["bg_primary"],
                      dropdown_text_color=COLORS["text_primary"],
                      width=200).pack(side="left", padx=0)

    def save():
        cn        = fields["Case Number"].get().strip()
        case_name = fields["Case Name / Title"].get().strip()
        client_id = fields["Client ID"].get().strip()
        court     = fields["Court"].get().strip()
        judge     = fields["Judge"].get().strip()
        case_type = fields["Case Type"].get().strip()
        filing_s  = fields["Filing Date"].get().strip()
        status    = sv.get()
        if not cn or not case_name or not client_id:
            _info_popup(dashboard, "Missing Fields",
                        "Case Number, Case Name, and Client ID are required.")
            return
        success = db.save_new_case(
            cn, case_name, client_id, advocate_id,
            court, judge, case_type,
            filing_s or datetime.date.today().strftime("%d %b %Y"),
            status, ""
        )
        if success:
            _info_popup(dashboard, "Case Saved", f"Case '{cn}' initialized successfully.")
            for e in fields.values():
                e.delete(0, "end")
        else:
            _info_popup(dashboard, "Error",
                        "Failed to save case.\nCheck: case number not duplicate, client ID exists.")

    br = tk.Frame(scroll, bg=COLORS["bg_primary"])
    br.pack(anchor="w", padx=59, pady=16)
    _black_btn(br, "Save Case", save, 180).pack(side="left", padx=8)
    _ghost_btn(br, "Clear Form",
               lambda: [e.delete(0, "end") for e in fields.values()], 140).pack(side="left", padx=8)


# ── 1.3 Case Updation ─────────────────────────────────────────────────────────
def build_case_update_view(parent, router, dashboard, advocate_id=1):
    dashboard._back_bar(parent, "1.3 — Case Updation")

    # v7: Search results area (pre-created sr_host, shown on search)
    search_results_frame = [None]  # mutable ref

    def _clear_search_results():
        if search_results_frame[0]:
            for w in search_results_frame[0].winfo_children():
                w.destroy()
            search_results_frame[0].pack_forget()
            search_results_frame[0] = None

    # v7: Smart Search bar ────────────────────────────────────────────────────
    def _do_search_upd(cat, q):
        if not q:
            _clear_search_results()
            return
        res = []
        if cat == "Case No.":
            res = db.get_cases_by_case_no(q, advocate_id) or []
        elif cat == "Client Name":
            res = db.get_cases_by_client_name(q, advocate_id) or []
        elif cat == "Client ID":
            res = db.get_cases_by_client_id(q, advocate_id) or []
        elif cat == "Last Hearing Date":
            res = db.get_cases_by_hearing_date(q, advocate_id) or []

        _clear_search_results()

        if not res:
            _info_popup(dashboard, "No Results", "No matching cases found.")
            return

        # Show sr_host above og_search_bar
        sr_host.pack(fill="x", padx=16, pady=(4, 0), before=og_search_bar)
        search_results_frame[0] = sr_host

        for w in sr_host.winfo_children():
            w.destroy()

        tk.Label(sr_host, text=f"Search Results ({len(res)} found)",
                 font=FONTS["caption_bold"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", pady=(2, 2))

        COL_DEFS_SR = [
            ("Case No.",          180),
            ("Client Name",       200),
            ("Client ID",         100),
            ("Last Hearing Date", 140),
        ]
        _make_table_header(sr_host, COL_DEFS_SR)

        for case_row in res:
            c_no = case_row.get("case_no", "—")

            def _make_click_link(sr_case_no=c_no):
                def make(row_frame):
                    lbl = tk.Label(row_frame, text=sr_case_no,
                                   font=FONTS["body_bold"],
                                   fg=COLORS["link"], bg=COLORS["bg_card"],
                                   cursor="hand2", anchor="w")
                    lbl.bind("<Enter>", lambda e: lbl.config(fg=COLORS["link_hover"]))
                    lbl.bind("<Leave>", lambda e: lbl.config(fg=COLORS["link"]))
                    def _on_click(e, cn=sr_case_no):
                        cn_var.set(cn)
                        _clear_search_results()
                        load()
                    lbl.bind("<Button-1>", _on_click)
                    return lbl
                return make

            _make_table_row(sr_host, [
                (_make_click_link(c_no),                         COL_DEFS_SR[0][1]),
                (case_row.get("client_name", "—"),               COL_DEFS_SR[1][1]),
                (str(case_row.get("client_id", "—")),           COL_DEFS_SR[2][1]),
                (_fmt_date(case_row.get("upcoming_date")),      COL_DEFS_SR[3][1]),
            ])

    def _get_sug_upd(cat):
        if cat == "Case No.":    return db.get_all_case_nos_for_advocate(advocate_id)
        if cat == "Client Name": return db.get_all_client_names_for_advocate(advocate_id)
        if cat == "Client ID":   return db.get_all_client_ids_for_advocate(advocate_id)
        return db.get_all_hearing_dates_for_advocate(advocate_id)
    build_smart_search_bar(parent,
        ["Case No.", "Client Name", "Client ID", "Last Hearing Date"],
        _do_search_upd, _get_sug_upd)
    # ── Main frame ──────────────────────────────────────────────────────────────
    top_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
    top_frame.pack(fill="both", expand=True)

    # Pre-created search results host (hidden until search fires)
    sr_host = tk.Frame(top_frame, bg=COLORS["bg_primary"])
    # Not packed yet — _do_search_upd packs it with before=og_search_bar


    # OG search bar (original case number entry bar)
    og_search_bar = tk.Frame(top_frame, bg=COLORS["bg_secondary"])
    og_search_bar.pack(fill="x", padx=16, pady=10)
    cn_var = tk.StringVar()
    tk.Label(og_search_bar, text="Case Number:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=(8, 4), pady=8)
    ctk.CTkEntry(og_search_bar, width=260, textvariable=cn_var,
                 fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                 border_color=COLORS["entry_border"],
                 placeholder_text="Enter Case No.", corner_radius=DIMS["btn_corner"]
                 ).pack(side="left", padx=6, pady=8)

    form_host = tk.Frame(top_frame, bg=COLORS["bg_primary"])
    form_host.pack(fill="both", expand=True)

    def load():
        cn = cn_var.get().strip()
        for w in form_host.winfo_children():
            w.destroy()
        # ─ v7: Ownership guard ─
        if not db.validate_case_owner(cn, advocate_id):
            tk.Label(form_host,
                     text=f'⛔  Access Denied\nCase "{cn}" does not belong to your account.',
                     font=FONTS["body"], fg="#CC0000",
                     bg=COLORS["bg_primary"], justify="center").pack(pady=20)
            return
        case_row = db.get_case(cn)
        if not case_row:
            tk.Label(form_host, text="Case not found.", font=FONTS["body"],
                     fg="#CC0000", bg=COLORS["bg_primary"]).pack(pady=20)
            return

        scroll = ctk.CTkScrollableFrame(
            form_host, fg_color=COLORS["bg_primary"],
            scrollbar_button_color=COLORS["scrollbar"],
            scrollbar_button_hover_color=COLORS["scrollbar_hover"],
        )
        scroll.pack(fill="both", expand=True)

        tk.Label(scroll, text="Edit Case Details", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(8, 6))
        fields = {}
        for label, val in [
            ("Case Name",         case_row.get("case_name", "")),
            ("Court",             case_row.get("court", "")),
            ("Judge",             case_row.get("judge", "") or ""),
            ("Next Hearing Date", _fmt_date(case_row.get("upcoming_date"))),
            ("Next Step",         case_row.get("next_step", "") or ""),
        ]:
            fields[label] = _entry_row(scroll, label, width=400)
            fields[label].insert(0, val if val != "—" else "")

        _divider(scroll)

        hdr_row = tk.Frame(scroll, bg=COLORS["navbar_bg"])
        hdr_row.pack(fill="x", padx=2, pady=(6, 4))
        tk.Label(hdr_row, text="  Existing Timeline Entries",
                 font=FONTS["caption_bold"], fg=COLORS["navbar_text"],
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=8, pady=5)
        tk.Label(hdr_row, text="Show to Client  ",
                 font=FONTS["caption_bold"], fg=COLORS["navbar_text"],
                 bg=COLORS["navbar_bg"]).pack(side="right", padx=8, pady=5)

        timeline = db.get_timeline(cn) or []
        for evt in timeline:
            er = tk.Frame(scroll, bg=COLORS["bg_card"],
                          highlightbackground=COLORS["border_cell"], highlightthickness=1)
            er.pack(fill="x", pady=2, padx=2)
            tk.Label(er, text=_fmt_date(evt.get("event_date")),
                     font=FONTS["caption_bold"],
                     fg=COLORS["text_on_dark"], bg=COLORS["cal_today_bg"],
                     padx=6, pady=3).pack(side="left")
            txt = tk.Frame(er, bg=COLORS["bg_card"])
            txt.pack(side="left", fill="x", expand=True, padx=8, pady=4)
            tk.Label(txt, text=evt.get("event_title", "—"), font=FONTS["body_bold"],
                     fg=COLORS["text_primary"], bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
            tk.Label(txt, text=evt.get("event_note", "—"), font=FONTS["caption"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                     anchor="w", wraplength=450).pack(anchor="w")
            var = tk.BooleanVar(value=bool(evt.get("client_visible", 1)))

            def _on_toggle(tid=evt["timeline_id"], v=var):
                db.set_timeline_visibility(tid, 1 if v.get() else 0)

            ctk.CTkCheckBox(
                er, text="", variable=var, command=_on_toggle,
                fg_color=COLORS["chk_on"], hover_color=COLORS["accent_hover"],
                border_color=COLORS["chk_off"], checkmark_color=COLORS["text_on_dark"],
                width=24, height=24,
            ).pack(side="right", padx=14, pady=6)

        _divider(scroll)

        tk.Label(scroll, text="Add New Timeline Update", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(8, 4))

        today_str = datetime.date.today().strftime("%d %b %Y")
        date_entry = _entry_row(scroll, "Date of Update", width=200)
        date_entry.insert(0, today_str)
        tk.Label(scroll, text="  Format: DD Mon YYYY  (e.g. 15 Jan 2026)",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 4))

        new_event_ent = _entry_row(scroll, "Event / Hearing Title", width=380)
        tk.Label(scroll, text="Details / Notes:", font=FONTS["body_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(6, 2))
        note_box = ctk.CTkTextbox(scroll, width=580, height=70,
                                   fg_color=COLORS["entry_bg"],
                                   text_color=COLORS["text_primary"],
                                   border_color=COLORS["entry_border"], border_width=1)
        note_box.pack(anchor="w", padx=20)

        new_vis_row = tk.Frame(scroll, bg=COLORS["bg_primary"])
        new_vis_row.pack(anchor="w", padx=20, pady=(8, 0))
        new_vis_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            new_vis_row, text="  Show this update to client",
            variable=new_vis_var, fg_color=COLORS["chk_on"],
            hover_color=COLORS["accent_hover"], border_color=COLORS["chk_off"],
            checkmark_color=COLORS["text_on_dark"], text_color=COLORS["text_secondary"],
            font=FONTS["body"],
        ).pack(side="left")

        def save():
            db.update_case_details(
                cn,
                fields["Case Name"].get().strip(),
                fields["Court"].get().strip(),
                fields["Judge"].get().strip(),
                fields["Next Hearing Date"].get().strip(),
                fields["Next Step"].get().strip(),
            )
            ev      = new_event_ent.get().strip()
            nt      = note_box.get("0.0", "end").strip()
            date_s  = date_entry.get().strip()
            if ev:
                event_date = None
                for fmt in ("%d %b %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                    try:
                        event_date = datetime.datetime.strptime(date_s, fmt).date()
                        break
                    except ValueError:
                        continue
                if event_date is None:
                    _info_popup(dashboard, "Invalid Date",
                                f'Date "{date_s}" is not recognised.\n'
                                f'Use format: DD Mon YYYY (e.g. 15 Jan 2026)')
                    return
                db.add_timeline_entry_on_date(
                    cn, event_date, ev, nt or "—",
                    1 if new_vis_var.get() else 0,
                    advocate_id
                )
            _info_popup(dashboard, "Updated", f"Case {cn} updated successfully.")

        br2 = tk.Frame(scroll, bg=COLORS["bg_primary"])
        br2.pack(pady=14)
        _black_btn(br2, "Save All Updates", save, 200).pack()

    _black_btn(og_search_bar, "Load", load, 100).pack(side="left", padx=6, pady=8)


# ── 2.1 Cases Ongoing  ─────────────────────────────────────────
def build_cases_ongoing_view(parent, router, dashboard, advocate_id=None):
    """advocate_id=None → admin unrestricted view."""
    dashboard._back_bar(parent, "2.1 — Cases Ongoing")

    # v7: Search results area
    search_results_frame = [None]

    def _clear_search_results():
        if search_results_frame[0]:
            for w in search_results_frame[0].winfo_children():
                w.destroy()
            search_results_frame[0].pack_forget()
            search_results_frame[0] = None

    COL_DEFS_SR = [
        ("Case No.",          180),
        ("Client Name",       200),
        ("Client ID",         100),
        ("Last Hearing Date", 140),
    ]

    if advocate_id:
        def _do_search_ong(cat, q):
            if not q:
                _clear_search_results()
                return
            res = []
            if cat == "Client ID":
                res = db.get_cases_by_client_id(q, advocate_id) or []
            elif cat == "Case No.":
                res = db.get_cases_by_case_no(q, advocate_id) or []
            elif cat == "Client Name":
                res = db.get_cases_by_client_name(q, advocate_id) or []
            elif cat == "Last Hearing Date":
                res = db.get_cases_by_hearing_date(q, advocate_id) or []

            _clear_search_results()

            if not res:
                _info_popup(dashboard, "No Results", "No matching cases found.")
                return

            # Show sr_host at top of results_host
            sr_host.pack(fill="x", padx=16, pady=(4, 4))
            search_results_frame[0] = sr_host

            for w in sr_host.winfo_children():
                w.destroy()

            tk.Label(sr_host, text=f"Search Results ({len(res)} found)",
                     font=FONTS["caption_bold"], fg=COLORS["text_secondary"],
                     bg=COLORS["bg_primary"]).pack(anchor="w", pady=(2, 2))
            _make_table_header(sr_host, COL_DEFS_SR)

            for case_row in res:
                c_no = case_row.get("case_no", "—")

                def _make_click_link(sr_case_no=c_no):
                    def make(row_frame):
                        lbl = tk.Label(row_frame, text=sr_case_no,
                                       font=FONTS["body_bold"],
                                       fg=COLORS["link"], bg=COLORS["bg_card"],
                                       cursor="hand2", anchor="w")
                        lbl.bind("<Enter>", lambda e: lbl.config(fg=COLORS["link_hover"]))
                        lbl.bind("<Leave>", lambda e: lbl.config(fg=COLORS["link"]))
                        def _on_click(e, cn=sr_case_no):
                            _clear_search_results()
                            router("case_info", cn)
                        lbl.bind("<Button-1>", _on_click)
                        return lbl
                    return make

                _make_table_row(sr_host, [
                    (_make_click_link(c_no),                          COL_DEFS_SR[0][1]),
                    (case_row.get("client_name", "—"),                COL_DEFS_SR[1][1]),
                    (str(case_row.get("client_id", "—")),            COL_DEFS_SR[2][1]),
                    (_fmt_date(case_row.get("upcoming_date")),       COL_DEFS_SR[3][1]),
                ])

        def _get_sug_ong(cat):
            if cat == "Client ID":   return db.get_all_client_ids_for_advocate(advocate_id)
            if cat == "Case No.":    return db.get_all_case_nos_for_advocate(advocate_id)
            if cat == "Client Name": return db.get_all_client_names_for_advocate(advocate_id)
            return db.get_all_hearing_dates_for_advocate(advocate_id)
        build_smart_search_bar(parent,
            ["Client ID", "Case No.", "Client Name", "Last Hearing Date"],
            _do_search_ong, _get_sug_ong)

    # Host for search results (sr_host lives here as first child)
    results_host = tk.Frame(parent, bg=COLORS["bg_primary"])
    results_host.pack(fill="both", expand=True)

    # Pre-created search results host (hidden until search fires)
    sr_host = tk.Frame(results_host, bg=COLORS["bg_primary"])
    # Not packed yet — _do_search_ong packs it when results arrive


# ── 2.2 Fees Tracking ────────────────────────────────
def build_fees_tracking_view(parent, router, dashboard, advocate_id=1):
    dashboard._back_bar(parent, "2.2 — Fees Tracking")

    # v7: Smart Search bar — placed FIRST, right after back bar ───────────────
    def _do_search_fees(cat, q):
        if not q:
            # Clear = show all
            fresh = db.get_pending_dues_all(advocate_id=advocate_id) or []
            _render_dues_table(fresh)
            t = db.get_pending_dues_total(advocate_id=advocate_id)
            total_label.config(text=f"Total Outstanding:  Rs.{int(t):,}")
            return
        # Get all dues, then filter by search criteria
        all_d = db.get_pending_dues_all(advocate_id=advocate_id) or []
        q_lower = q.strip().lower()
        filtered = []
        if cat == "Case No.":
            filtered = [d for d in all_d if q_lower in str(d.get("case_no", "")).lower()]
        elif cat == "Client ID":
            filtered = [d for d in all_d if q_lower in str(d.get("client_id", "")).lower()]
        elif cat == "Client Name":
            filtered = [d for d in all_d if q_lower in str(d.get("client_name", "")).lower()]
        elif cat == "Last Hearing Date":
            filtered = [d for d in all_d if q_lower in str(_fmt_date(d.get("upcoming_date", ""))).lower()]

        if not filtered:
            for w in table_host.winfo_children():
                w.destroy()
            tk.Label(table_host,
                     text="This case has no due fees.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_primary"]).pack(pady=20)
            total_label.config(text="Total Outstanding:  Rs.0")
            return
        _render_dues_table(filtered)

    def _get_sug_fees(cat):
        if cat == "Case No.":    return db.get_all_case_nos_for_advocate(advocate_id)
        if cat == "Client ID":   return db.get_all_client_ids_for_advocate(advocate_id)
        if cat == "Client Name": return db.get_all_client_names_for_advocate(advocate_id)
        return db.get_all_hearing_dates_for_advocate(advocate_id)
    build_smart_search_bar(parent,
        ["Case No.", "Client ID", "Client Name", "Last Hearing Date"],
        _do_search_fees, _get_sug_fees)

    bottom_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
    bottom_frame.pack(side="bottom", fill="x")

    _divider(bottom_frame)
    tk.Label(bottom_frame, text="Add Pending Due", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(4, 2))
    due_frame = tk.Frame(bottom_frame, bg=COLORS["bg_secondary"])
    due_frame.pack(fill="x", padx=16, pady=4)
    tk.Label(due_frame, text="Add Pending Due:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=8, pady=8)
    due_cid = ctk.CTkEntry(due_frame, width=90, placeholder_text="Client ID",
                             fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                             border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    due_cid.pack(side="left", padx=3)
    due_cn = ctk.CTkEntry(due_frame, width=140, placeholder_text="Case No.",
                           fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                           border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    due_cn.pack(side="left", padx=3)
    due_amt = ctk.CTkEntry(due_frame, width=100, placeholder_text="Amount",
                            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    due_amt.pack(side="left", padx=3)
    due_date_ent = ctk.CTkEntry(due_frame, width=120, placeholder_text="DD Mon YYYY",
                                 fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                                 border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    due_date_ent.pack(side="left", padx=3)
    default_due = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d %b %Y")
    due_date_ent.insert(0, default_due)
    due_desc = ctk.CTkEntry(due_frame, width=160, placeholder_text="Description",
                             fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                             border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    due_desc.pack(side="left", padx=3)

    def send_due():
        cid    = due_cid.get().strip()
        cn     = due_cn.get().strip()
        amt_s  = due_amt.get().strip()
        date_s = due_date_ent.get().strip()
        desc   = due_desc.get().strip()
        if not cid or not cn or not amt_s or not desc:
            _info_popup(dashboard, "Missing Fields",
                        "Client ID, Case No., Amount, and Description are all required.")
            return
        if not db.validate_case_client_match(cn, cid, advocate_id):
            _info_popup(dashboard, "⛔ Access Denied",
                        f'Case "{cn}" does not belong to Client "{cid}" under your account.\n'
                        'Ensure the Client ID and Case No. match and belong to you.')
            return
        try:
            amt = float(amt_s)
            if amt <= 0:
                raise ValueError
        except ValueError:
            _info_popup(dashboard, "Invalid Amount", "Enter a valid positive number.")
            return
        due_date_obj = None
        for fmt in ("%d %b %Y", "%Y-%m-%d"):
            try:
                due_date_obj = datetime.datetime.strptime(date_s, fmt).date()
                break
            except ValueError:
                continue
        if due_date_obj is None:
            _info_popup(dashboard, "Invalid Date",
                        f'Date "{date_s}" not recognised.\nUse: DD Mon YYYY (e.g. 29 May 2026)')
            return
        success = db.add_pending_due(cid, cn, advocate_id, amt, due_date_obj, desc)
        if success:
            _info_popup(dashboard, "Due Sent",
                        f"Pending due of Rs.{int(amt):,} added to {cid}'s account.\n"
                        f"Due date: {due_date_obj.strftime('%d %b %Y')}")
            for e in [due_cid, due_cn, due_amt, due_desc]:
                e.delete(0, "end")
            due_date_ent.delete(0, "end")
            due_date_ent.insert(0, default_due)
        else:
            _info_popup(dashboard, "Error",
                        "Failed to add due. Check Client ID and Case No. are valid.")

    _black_btn(due_frame, "Send Due Request", send_due, 160).pack(side="left", padx=8)

    # ── Log Payment strip — v7: Date field + Description + triple validation ──
    lf = tk.Frame(bottom_frame, bg=COLORS["bg_secondary"])
    lf.pack(fill="x", padx=16, pady=(2, 6))
    tk.Label(lf, text="Log Payment:        ", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=8, pady=8)
    pid = ctk.CTkEntry(lf, width=90, placeholder_text="Client ID",
                        fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                        border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    pid.pack(side="left", padx=3)
    pcn = ctk.CTkEntry(lf, width=140, placeholder_text="Case No.",
                        fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                        border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    pcn.pack(side="left", padx=3)
    pamt = ctk.CTkEntry(lf, width=100, placeholder_text="Amount Rs.",
                         fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                         border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    pamt.pack(side="left", padx=3)
    p_date_ent = ctk.CTkEntry(lf, width=120, placeholder_text="DD Mon YYYY",
                               fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                               border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    p_date_ent.pack(side="left", padx=3)
    default_pay_date = datetime.date.today().strftime("%d %b %Y")
    p_date_ent.insert(0, default_pay_date)
    p_desc = ctk.CTkEntry(lf, width=160, placeholder_text="Description",
                           fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                           border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    p_desc.pack(side="left", padx=3)

    def _do_record():
        cid   = pid.get().strip()
        cn_p  = pcn.get().strip()
        amt_s = pamt.get().strip()
        date_s = p_date_ent.get().strip()
        desc  = p_desc.get().strip() or "Manual entry"
        if not cid or not amt_s:
            _info_popup(dashboard, "Missing", "Enter Client ID and Amount.")
            return
        if not cn_p:
            _info_popup(dashboard, "Missing", "Case No. is required for payment logging.")
            return
        # ─ v7: Validate triple: case must belong to this client AND this advocate ─
        if not db.validate_case_client_match(cn_p, cid, advocate_id):
            _info_popup(dashboard, "⛔ Access Denied",
                        f'Case "{cn_p}" does not belong to Client "{cid}" under your account.\n'
                        'Ensure the Client ID and Case No. match and belong to you.')
            return
        try:
            amt = float(amt_s)
        except ValueError:
            _info_popup(dashboard, "Invalid Amount", "Please enter a valid number.")
            return
        # Parse date
        pay_date_obj = None
        for fmt in ("%d %b %Y", "%Y-%m-%d"):
            try:
                pay_date_obj = datetime.datetime.strptime(date_s, fmt).date()
                break
            except ValueError:
                continue
        if pay_date_obj is None:
            _info_popup(dashboard, "Invalid Date",
                        f'Date "{date_s}" not recognised.\nUse: DD Mon YYYY (e.g. 29 May 2026)')
            return
        new_pid = db.record_payment(cid, cn_p, advocate_id, amt, desc)
        if new_pid:
            _info_popup(dashboard, "Logged",
                        f"Payment of Rs.{int(amt):,} recorded for {cid}.\n"
                        f"Date: {pay_date_obj.strftime('%d %b %Y')}\nPayment ID: {new_pid}")
        else:
            _info_popup(dashboard, "Error",
                        "Failed to record payment.\nCheck Client ID and Case No. are valid.")

    _black_btn(lf, "Record Payment", _do_record, 160).pack(side="left", padx=8)

    # ── Scrollable middle area: dues table ───────────────────────────────────
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    tk.Label(scroll, text="Pending Client Dues", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(10, 4))
    _divider(scroll)

    COL_DEFS = [
        ("Client",      140),
        ("Case No.",    180),
        ("Amount Due",  110),
        ("Due Date",    120),
        ("Description", 200),
        ("Hearing Date", 120),
    ]

    # Dues table host — gets rebuilt on search/clear
    table_host = tk.Frame(scroll, bg=COLORS["bg_primary"])
    table_host.pack(fill="x")

    total_label = tk.Label(scroll, text="", font=FONTS["heading_2"],
                           fg=COLORS["text_primary"], bg=COLORS["bg_primary"])
    total_label.pack(anchor="e", padx=20, pady=6)

    def _render_dues_table(dues_list):
        """Render the dues into the table_host. Clears previous content."""
        for w in table_host.winfo_children():
            w.destroy()
        if not dues_list:
            tk.Label(table_host, text="No pending dues found for this search.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_primary"]).pack(pady=20)
            total_label.config(text="Total Outstanding:  Rs.0")
            return

        _make_table_header(table_host, COL_DEFS)
        t = 0
        for due in dues_list:
            t += float(due.get("amount_due", 0))
            def link_factory(due=due):
                def make(row_frame):
                    return _case_link(row_frame, due["case_no"], router, bg=COLORS["bg_card"])
                return make
            _make_table_row(table_host, [
                (due.get("client_name", "—"),           COL_DEFS[0][1]),
                (link_factory(due),                      COL_DEFS[1][1]),
                (_fmt_amount(due.get("amount_due", 0)),  COL_DEFS[2][1]),
                (_fmt_date(due.get("due_date")),         COL_DEFS[3][1]),
                (due.get("description", "—"),            COL_DEFS[4][1]),
                (_fmt_date(due.get("upcoming_date")),    COL_DEFS[5][1]),
            ])
        total_label.config(text=f"Total Outstanding:  Rs.{int(t):,}")

    # Initial load — show all dues
    all_dues = db.get_pending_dues_all(advocate_id=advocate_id) or []
    total = db.get_pending_dues_total(advocate_id=advocate_id)
    _render_dues_table(all_dues)
    total_label.config(text=f"Total Outstanding:  Rs.{int(total):,}")


# ── 3.1 Expenses ────────────────────────────
def build_expenses_view(parent, router, dashboard, advocate_id=1):
    dashboard._back_bar(parent, "3.1 — Expenses")

    # v7: Smart Search bar — placed FIRST, right after back bar ───────────────
    def _do_search_exp(cat, q):
        if not q:
            fresh = db.get_expenses_all(advocate_id=advocate_id) or []
            _render_expenses_table(fresh)
            return
        all_e = db.get_expenses_all(advocate_id=advocate_id) or []
        q_lower = q.strip().lower()
        filtered = []
        if cat == "Case No.":
            filtered = [e for e in all_e if q_lower in str(e.get("case_no", "")).lower()]
        elif cat == "Client ID":
            filtered = [e for e in all_e if q_lower in str(e.get("client_id", "")).lower()]
        elif cat == "Client Name":
            filtered = [e for e in all_e if q_lower in str(e.get("client_name", "")).lower()]
        elif cat == "Last Hearing Date":
            filtered = [e for e in all_e if q_lower in str(_fmt_date(e.get("upcoming_date", ""))).lower()]

        if not filtered:
            for w in table_host.winfo_children():
                w.destroy()
            tk.Label(table_host,
                     text="No expenses found for this search.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_primary"]).pack(pady=20)
            return
        _render_expenses_table(filtered)

    def _get_sug_exp(cat):
        if cat == "Case No.":    return db.get_all_case_nos_for_advocate(advocate_id)
        if cat == "Client ID":   return db.get_all_client_ids_for_advocate(advocate_id)
        if cat == "Client Name": return db.get_all_client_names_for_advocate(advocate_id)
        return db.get_all_hearing_dates_for_advocate(advocate_id)
    build_smart_search_bar(parent,
        ["Case No.", "Client ID", "Client Name", "Last Hearing Date"],
        _do_search_exp, _get_sug_exp)

    # ── Fixed bottom frame: Add Expense (won't shift) ────────────────────────
    bottom_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
    bottom_frame.pack(side="bottom", fill="x")

    _divider(bottom_frame)
    tk.Label(bottom_frame, text="Add New Expense", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(4, 2))
    ef = tk.Frame(bottom_frame, bg=COLORS["bg_secondary"])
    ef.pack(fill="x", padx=16, pady=(2, 6))
    tk.Label(ef, text="Add Expense:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=8, pady=8)
    e_cid   = ctk.CTkEntry(ef, width=90, placeholder_text="Client ID",
                             fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                             border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    e_cid.pack(side="left", padx=3)
    e_cn    = ctk.CTkEntry(ef, width=140, placeholder_text="Case No.",
                            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    e_cn.pack(side="left", padx=3)
    e_amt   = ctk.CTkEntry(ef, width=100, placeholder_text="Amount Rs.",
                            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    e_amt.pack(side="left", padx=3)
    e_title = ctk.CTkEntry(ef, width=140, placeholder_text="Title",
                            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    e_title.pack(side="left", padx=3)

    def save_expense():
        cid_e = e_cid.get().strip()
        cn_e  = e_cn.get().strip()
        if not cid_e or not cn_e:
            _info_popup(dashboard, "Missing Fields",
                        "Both Client ID and Case No. are required.")
            return
        # ─ v7: Validate triple: case must belong to this client AND this advocate ─
        if not db.validate_case_client_match(cn_e, cid_e, advocate_id):
            _info_popup(dashboard, "⛔ Access Denied",
                        f'Case "{cn_e}" does not belong to Client "{cid_e}" under your account.\n'
                        'Ensure the Client ID and Case No. match and belong to you.')
            return
        try:
            amt = float(e_amt.get().strip())
        except ValueError:
            _info_popup(dashboard, "Invalid", "Enter a valid amount.")
            return
        success = db.add_expense(
            cid_e, cn_e,
            advocate_id, amt, e_title.get().strip()
        )
        if success:
            _info_popup(dashboard, "Saved", "Expense recorded successfully.")
        else:
            _info_popup(dashboard, "Error",
                        "Failed to record expense.\nCheck Client ID and Case No.")

    _black_btn(ef, "Save Expense", save_expense, 140).pack(side="left", padx=8)

    # ── Scrollable middle area ───────────────────────────────────────────────
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    t_tot = db.get_expense_totals_today(advocate_id=advocate_id)
    m_tot = db.get_expense_totals_month(advocate_id=advocate_id)

    # FIX 4: 3-box stats strip
    strip = tk.Frame(scroll, bg=COLORS["bg_secondary"])
    strip.pack(fill="x", padx=16, pady=8)
    strip.columnconfigure(0, weight=1)
    strip.columnconfigure(1, weight=1)
    strip.columnconfigure(2, weight=1)

    for col, (label, val) in enumerate([
        ("Total Expended Today",      f"Rs.{int(t_tot):,}"),
        ("Total Expended This Month", f"Rs.{int(m_tot):,}"),
    ]):
        box = tk.Frame(strip, bg=COLORS["navbar_bg"], padx=20, pady=10)
        box.grid(row=0, column=col, sticky="nsew", padx=6)
        tk.Label(box, text=label, font=FONTS["caption_bold"],
                 fg=COLORS["text_muted"], bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Label(box, text=val, font=FONTS["heading_1"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(anchor="w")

    # FIX 4: 3rd box — period selector
    period_box = tk.Frame(strip, bg=COLORS["navbar_bg"], padx=20, pady=10)
    period_box.grid(row=0, column=2, sticky="nsew", padx=6)
    tk.Label(period_box, text="Selected Period", font=FONTS["caption_bold"],
             fg=COLORS["text_muted"], bg=COLORS["navbar_bg"]).pack(anchor="w")
    period_val_lbl = tk.Label(period_box, text="Rs.0", font=FONTS["heading_1"],
                               fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"])
    period_val_lbl.pack(anchor="w")

    PERIOD_OPTIONS = ["Today", "Yesterday", "Last 1 Week", "Last 1 Month", "Last 1 Year", "All Time"]
    period_var = tk.StringVar(value="All Time")

    def update_period_total(*_):
        total = db.get_expense_total_for_period(period_var.get(), advocate_id=advocate_id)
        period_val_lbl.config(text=f"Rs.{int(total):,}")

    period_var.trace_add("write", update_period_total)
    update_period_total()

    ctk.CTkOptionMenu(
        period_box, values=PERIOD_OPTIONS, variable=period_var,
        fg_color=COLORS["navbar_hover"], button_color=COLORS["navbar_active"],
        button_hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_on_dark"],
        dropdown_fg_color=COLORS["bg_primary"],
        dropdown_text_color=COLORS["text_primary"],
        width=160,
    ).pack(anchor="w", pady=(4, 0))

    _divider(scroll)

    # v7: table with Last Hearing Date column
    COL_DEFS = [
        ("Date",              120),
        ("Amount",            110),
        ("Title",             140),
        ("Client",            130),
        ("Case No.",          170),
        ("Last Hearing Date", 120),
    ]

    # Table host — gets rebuilt on search/clear
    table_host = tk.Frame(scroll, bg=COLORS["bg_primary"])
    table_host.pack(fill="x")

    def _render_expenses_table(exp_list):
        """Render expenses into table_host. Clears previous content."""
        for w in table_host.winfo_children():
            w.destroy()
        if not exp_list:
            tk.Label(table_host, text="No expenses found.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_primary"]).pack(pady=20)
            return
        _make_table_header(table_host, COL_DEFS)
        for exp in exp_list:
            def link_factory(exp=exp):
                def make(row_frame):
                    return _case_link(row_frame, exp.get("case_no", "—"), router, bg=COLORS["bg_card"])
                return make
            _make_table_row(table_host, [
                (_fmt_date(exp.get("expense_date")),    COL_DEFS[0][1]),
                (_fmt_amount(exp.get("amount", 0)),     COL_DEFS[1][1]),
                (exp.get("title", "—"),                 COL_DEFS[2][1]),
                (exp.get("client_name", "—"),           COL_DEFS[3][1]),
                (link_factory(exp),                     COL_DEFS[4][1]),
                (_fmt_date(exp.get("upcoming_date")),   COL_DEFS[5][1]),
            ])

    # Initial load
    expenses = db.get_expenses_all(advocate_id=advocate_id) or []
    _render_expenses_table(expenses)


# ── 3.2 Money Incoming ─────────────────────────
def build_money_incoming_view(parent, router, dashboard, advocate_id=1):
    dashboard._back_bar(parent, "3.2 — Money Incoming")

    # v7: Smart Search bar — placed FIRST, right after back bar ───────────────
    def _do_search_inc(cat, q):
        if not q:
            fresh = db.get_payments_all(advocate_id=advocate_id) or []
            _render_payments_table(fresh)
            return
        all_p = db.get_payments_all(advocate_id=advocate_id) or []
        q_lower = q.strip().lower()
        filtered = []
        if cat == "Case No.":
            filtered = [p for p in all_p if q_lower in str(p.get("case_no", "")).lower()]
        elif cat == "Client ID":
            filtered = [p for p in all_p if q_lower in str(p.get("client_id", "")).lower()]
        elif cat == "Client Name":
            filtered = [p for p in all_p if q_lower in str(p.get("client_name", "")).lower()]
        elif cat == "Last Hearing Date":
            filtered = [p for p in all_p if q_lower in str(_fmt_date(p.get("upcoming_date", ""))).lower()]

        if not filtered:
            for w in table_host.winfo_children():
                w.destroy()
            tk.Label(table_host,
                     text="No payments found for this search.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_primary"]).pack(pady=20)
            return
        _render_payments_table(filtered)

    def _get_sug_inc(cat):
        if cat == "Case No.":    return db.get_all_case_nos_for_advocate(advocate_id)
        if cat == "Client ID":   return db.get_all_client_ids_for_advocate(advocate_id)
        if cat == "Client Name": return db.get_all_client_names_for_advocate(advocate_id)
        return db.get_all_hearing_dates_for_advocate(advocate_id)
    build_smart_search_bar(parent,
        ["Case No.", "Client ID", "Client Name", "Last Hearing Date"],
        _do_search_inc, _get_sug_inc)

    bottom_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
    bottom_frame.pack(side="bottom", fill="x")

    _divider(bottom_frame)
    tk.Label(bottom_frame, text="Send Due / Log Payment", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(4, 2))

    # ── Send Due Request bar ─────────────────────────────────────────────────
    due_frame = tk.Frame(bottom_frame, bg=COLORS["bg_secondary"])
    due_frame.pack(fill="x", padx=16, pady=2)
    tk.Label(due_frame, text="Send Due:      ", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=8, pady=8)
    inc_due_cid = ctk.CTkEntry(due_frame, width=90, placeholder_text="Client ID",
                                fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                                border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_due_cid.pack(side="left", padx=3)
    inc_due_cn = ctk.CTkEntry(due_frame, width=140, placeholder_text="Case No.",
                               fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                               border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_due_cn.pack(side="left", padx=3)
    inc_due_amt = ctk.CTkEntry(due_frame, width=100, placeholder_text="Amount",
                                fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                                border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_due_amt.pack(side="left", padx=3)
    inc_due_date = ctk.CTkEntry(due_frame, width=120, placeholder_text="DD Mon YYYY",
                                 fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                                 border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_due_date.pack(side="left", padx=3)
    default_due_inc = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d %b %Y")
    inc_due_date.insert(0, default_due_inc)
    inc_due_desc = ctk.CTkEntry(due_frame, width=160, placeholder_text="Description",
                                 fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                                 border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_due_desc.pack(side="left", padx=3)

    def send_due_inc():
        cid    = inc_due_cid.get().strip()
        cn     = inc_due_cn.get().strip()
        amt_s  = inc_due_amt.get().strip()
        date_s = inc_due_date.get().strip()
        desc   = inc_due_desc.get().strip()
        if not cid or not cn or not amt_s or not desc:
            _info_popup(dashboard, "Missing Fields",
                        "Client ID, Case No., Amount, and Description are all required.")
            return
        if not db.validate_case_client_match(cn, cid, advocate_id):
            _info_popup(dashboard, "⛔ Access Denied",
                        f'Case "{cn}" does not belong to Client "{cid}" under your account.\n'
                        'Ensure the Client ID and Case No. match and belong to you.')
            return
        try:
            amt = float(amt_s)
            if amt <= 0:
                raise ValueError
        except ValueError:
            _info_popup(dashboard, "Invalid Amount", "Enter a valid positive number.")
            return
        due_date_obj = None
        for fmt in ("%d %b %Y", "%Y-%m-%d"):
            try:
                due_date_obj = datetime.datetime.strptime(date_s, fmt).date()
                break
            except ValueError:
                continue
        if due_date_obj is None:
            _info_popup(dashboard, "Invalid Date",
                        f'Date "{date_s}" not recognised.\nUse: DD Mon YYYY (e.g. 29 May 2026)')
            return
        success = db.add_pending_due(cid, cn, advocate_id, amt, due_date_obj, desc)
        if success:
            _info_popup(dashboard, "Due Sent",
                        f"Pending due of Rs.{int(amt):,} added to {cid}'s account.\n"
                        f"Due date: {due_date_obj.strftime('%d %b %Y')}")
            for e in [inc_due_cid, inc_due_cn, inc_due_amt, inc_due_desc]:
                e.delete(0, "end")
            inc_due_date.delete(0, "end")
            inc_due_date.insert(0, default_due_inc)
        else:
            _info_popup(dashboard, "Error",
                        "Failed to add due. Check Client ID and Case No. are valid.")

    _black_btn(due_frame, "Send Due Request", send_due_inc, 160).pack(side="left", padx=8)

    # ── Log Payment bar ──────────────────────────────────────────────────────
    lf = tk.Frame(bottom_frame, bg=COLORS["bg_secondary"])
    lf.pack(fill="x", padx=16, pady=(2, 6))
    tk.Label(lf, text="Log Payment:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=8, pady=8)
    inc_pid = ctk.CTkEntry(lf, width=90, placeholder_text="Client ID",
                            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_pid.pack(side="left", padx=3)
    inc_pcn = ctk.CTkEntry(lf, width=140, placeholder_text="Case No.",
                            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_pcn.pack(side="left", padx=3)
    inc_pamt = ctk.CTkEntry(lf, width=100, placeholder_text="Amount Rs.",
                             fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                             border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_pamt.pack(side="left", padx=3)
    inc_p_date = ctk.CTkEntry(lf, width=120, placeholder_text="DD Mon YYYY",
                               fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                               border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_p_date.pack(side="left", padx=3)
    default_pay_date_inc = datetime.date.today().strftime("%d %b %Y")
    inc_p_date.insert(0, default_pay_date_inc)
    inc_p_desc = ctk.CTkEntry(lf, width=160, placeholder_text="Description",
                               fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                               border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"])
    inc_p_desc.pack(side="left", padx=3)

    def _do_record_inc():
        cid   = inc_pid.get().strip()
        cn_p  = inc_pcn.get().strip()
        amt_s = inc_pamt.get().strip()
        date_s = inc_p_date.get().strip()
        desc  = inc_p_desc.get().strip() or "Manual entry"
        if not cid or not amt_s:
            _info_popup(dashboard, "Missing", "Enter Client ID and Amount.")
            return
        if not cn_p:
            _info_popup(dashboard, "Missing", "Case No. is required for payment logging.")
            return
        if not db.validate_case_client_match(cn_p, cid, advocate_id):
            _info_popup(dashboard, "⛔ Access Denied",
                        f'Case "{cn_p}" does not belong to Client "{cid}" under your account.\n'
                        'Ensure the Client ID and Case No. match and belong to you.')
            return
        try:
            amt = float(amt_s)
        except ValueError:
            _info_popup(dashboard, "Invalid Amount", "Please enter a valid number.")
            return
        pay_date_obj = None
        for fmt in ("%d %b %Y", "%Y-%m-%d"):
            try:
                pay_date_obj = datetime.datetime.strptime(date_s, fmt).date()
                break
            except ValueError:
                continue
        if pay_date_obj is None:
            _info_popup(dashboard, "Invalid Date",
                        f'Date "{date_s}" not recognised.\nUse: DD Mon YYYY (e.g. 29 May 2026)')
            return
        new_pid = db.record_payment(cid, cn_p, advocate_id, amt, desc)
        if new_pid:
            _info_popup(dashboard, "Logged",
                        f"Payment of Rs.{int(amt):,} recorded for {cid}.\n"
                        f"Date: {pay_date_obj.strftime('%d %b %Y')}\nPayment ID: {new_pid}")
        else:
            _info_popup(dashboard, "Error",
                        "Failed to record payment.\nCheck Client ID and Case No. are valid.")

    _black_btn(lf, "Record Payment", _do_record_inc, 160).pack(side="left", padx=8)

    # ── Scrollable middle area: stats + payments table ───────────────────────
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    t_tot = db.get_payment_totals_today(advocate_id=advocate_id).get("today_total", 0.0)
    m_tot = db.get_payment_totals_month(advocate_id=advocate_id).get("month_total", 0.0)

    strip = tk.Frame(scroll, bg=COLORS["bg_secondary"])
    strip.pack(fill="x", padx=16, pady=8)
    strip.columnconfigure(0, weight=1)
    strip.columnconfigure(1, weight=1)
    strip.columnconfigure(2, weight=1)

    for col, (label, val) in enumerate([
        ("Total Received Today",      f"Rs.{int(t_tot):,}"),
        ("Total Received This Month", f"Rs.{int(m_tot):,}"),
    ]):
        box = tk.Frame(strip, bg=COLORS["navbar_bg"], padx=20, pady=10)
        box.grid(row=0, column=col, sticky="nsew", padx=6)
        tk.Label(box, text=label, font=FONTS["caption_bold"],
                 fg=COLORS["text_muted"], bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Label(box, text=val, font=FONTS["heading_1"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(anchor="w")

    period_box = tk.Frame(strip, bg=COLORS["navbar_bg"], padx=20, pady=10)
    period_box.grid(row=0, column=2, sticky="nsew", padx=6)
    tk.Label(period_box, text="Selected Period", font=FONTS["caption_bold"],
             fg=COLORS["text_muted"], bg=COLORS["navbar_bg"]).pack(anchor="w")
    period_val_lbl = tk.Label(period_box, text="Rs.0", font=FONTS["heading_1"],
                               fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"])
    period_val_lbl.pack(anchor="w")

    PERIOD_OPTIONS = ["Today", "Yesterday", "Last 1 Week", "Last 1 Month", "Last 1 Year", "All Time"]
    period_var = tk.StringVar(value="All Time")

    def update_period_total(*_):
        total = db.get_payment_total_for_period(period_var.get(), advocate_id=advocate_id)
        period_val_lbl.config(text=f"Rs.{int(total):,}")

    period_var.trace_add("write", update_period_total)
    update_period_total()

    ctk.CTkOptionMenu(
        period_box, values=PERIOD_OPTIONS, variable=period_var,
        fg_color=COLORS["navbar_hover"], button_color=COLORS["navbar_active"],
        button_hover_color=COLORS["accent_hover"],
        text_color=COLORS["text_on_dark"],
        dropdown_fg_color=COLORS["bg_primary"],
        dropdown_text_color=COLORS["text_primary"],
        width=160,
    ).pack(anchor="w", pady=(4, 0))

    _divider(scroll)

    # v7: table with Last Hearing Date column
    COL_DEFS = [
        ("Logged At",         155),
        ("Amount",            100),
        ("Client",            120),
        ("Case No.",          160),
        ("Note",              140),
        ("Last Hearing Date", 110),
        ("",                   70),
    ]

    # Table host — gets rebuilt on search/clear
    table_host = tk.Frame(scroll, bg=COLORS["bg_primary"])
    table_host.pack(fill="x")

    def _render_payments_table(pmt_list):
        """Render payments into table_host. Clears previous content."""
        for w in table_host.winfo_children():
            w.destroy()
        if not pmt_list:
            tk.Label(table_host, text="No payments found.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_primary"]).pack(pady=20)
            return
        _make_table_header(table_host, COL_DEFS)
        for pmt in pmt_list:
            ca = pmt.get("created_at")
            if ca and isinstance(ca, datetime.datetime):
                ts_str = ca.strftime("%d %b %Y  %H:%M")
            elif ca:
                ts_str = str(ca)[:16]
            else:
                ts_str = _fmt_date(pmt.get("payment_date"))

            p_data = {
                "date":       ts_str,
                "amount":     int(float(pmt.get("amount", 0))),
                "client_id":  pmt.get("client_id", ""),
                "case_no":    pmt.get("case_no", ""),
                "note":       pmt.get("note", "—"),
                "payment_id": pmt.get("payment_id"),
                "advocate_id": pmt.get("advocate_id")
            }

            def print_factory(p=p_data):
                def make(row_frame):
                    btn = ctk.CTkButton(
                        row_frame, text="Print", width=60, height=26,
                        fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                        text_color=COLORS["text_on_dark"], font=FONTS["caption_bold"],
                        corner_radius=DIMS["btn_corner"],
                        command=lambda pm=p: open_print_receipt(dashboard, pm, "advocate"),
                    )
                    return btn
                return make

            def case_link_factory(pmt=pmt):
                def make(row_frame):
                    return _case_link(row_frame, pmt.get("case_no", "—"), router, bg=COLORS["bg_card"])
                return make

            _make_table_row(table_host, [
                (ts_str,                                  COL_DEFS[0][1]),
                (_fmt_amount(pmt.get("amount", 0)),       COL_DEFS[1][1]),
                (pmt.get("client_name", "—"),             COL_DEFS[2][1]),
                (case_link_factory(pmt),                  COL_DEFS[3][1]),
                (pmt.get("note", ""),                     COL_DEFS[4][1]),
                (_fmt_date(pmt.get("upcoming_date")),     COL_DEFS[5][1]),
                (print_factory(p_data),                   COL_DEFS[6][1]),
            ])

    # Initial load
    payments = db.get_payments_all(advocate_id=advocate_id) or []
    _render_payments_table(payments)


# ── Account Settings ──────────────────────────────────────────────────────────
def build_account_settings_view(parent, profile, dashboard):
    dashboard._back_bar(parent, "Account Settings")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Account Settings", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))

    field_map = [
        ("name",     "Full Name"),
        ("bar_no",   "Bar Number"),
        ("court",    "Primary Court"),
        ("chambers", "Chambers"),
        ("phone",    "Phone"),
        ("email",    "Email"),
    ]
    fields = {}
    for key, label in field_map:
        ent = _entry_row(scroll, label, width=300)
        ent.insert(0, str(profile.get(key, "")))
        fields[key] = ent

    def save():
        advocate_id = profile.get("advocate_id")
        if not advocate_id:
            _info_popup(dashboard, "Read Only",
                        "Client profile editing is not available in this version.")
            return
        success = db.update_advocate_profile(
            advocate_id,
            fields["name"].get().strip(),
            fields["bar_no"].get().strip(),
            fields["court"].get().strip(),
            fields["chambers"].get().strip(),
            fields["phone"].get().strip(),
            fields["email"].get().strip(),
        )
        if success:
            _info_popup(dashboard, "Saved", "Profile updated successfully.")
        else:
            _info_popup(dashboard, "Error", "Failed to save profile.")

    # Bug 15 fix: left-aligned save button
    _black_btn(scroll, "Save Settings", save, 180).pack(anchor="w", padx=20, pady=14)

    # ── v7: Update Password section ──────────────────────────────────────────
    advocate_id = profile.get("advocate_id")
    if advocate_id:
        _divider(scroll)
        tk.Label(scroll, text="Update Password", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(8, 4))
        tk.Label(scroll, text="Change your login password. Enter your current password to verify your identity.",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 8))

        pw_old     = _entry_row(scroll, "Old Password",     width=260, show="\u2022")
        pw_new     = _entry_row(scroll, "New Password",     width=260, show="\u2022")
        pw_confirm = _entry_row(scroll, "Confirm Password", width=260, show="\u2022")

        def change_password():
            old_pw = pw_old.get().strip()
            new_pw = pw_new.get().strip()
            cfm_pw = pw_confirm.get().strip()
            if not old_pw or not new_pw or not cfm_pw:
                _info_popup(dashboard, "Missing Fields",
                            "All three password fields are required.")
                return
            if new_pw != cfm_pw:
                _info_popup(dashboard, "Mismatch",
                            "New Password and Confirm Password do not match.\n"
                            "Please re-enter them.")
                return
            if len(new_pw) < 4:
                _info_popup(dashboard, "Too Short",
                            "New password must be at least 4 characters.")
                return
            result = db.change_advocate_password(advocate_id, old_pw, new_pw)
            if result is None:
                _info_popup(dashboard, "⛔ Wrong Password",
                            "The old password you entered is incorrect.\n"
                            "Please try again.")
            elif result:
                _info_popup(dashboard, "✓ Password Updated",
                            "Your password has been changed successfully.\n"
                            "Use the new password on your next login.")
                pw_old.delete(0, "end")
                pw_new.delete(0, "end")
                pw_confirm.delete(0, "end")
            else:
                _info_popup(dashboard, "Error",
                            "Failed to update password. Please try again.")

        _black_btn(scroll, "Update Password", change_password, 180).pack(anchor="w", padx=20, pady=14)


# ── Admin Profile View ───────────
def build_admin_profile_view(parent, profile, dashboard):
    """Profile view for the admin account — shows only name/phone/email + password."""
    dashboard._back_bar(parent, "Admin Profile Settings")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Admin Account Settings", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))

    # Read-only admin badge
    badge_row = tk.Frame(scroll, bg=COLORS["bg_secondary"], padx=16, pady=8)
    badge_row.pack(fill="x", padx=20, pady=(0, 12))
    tk.Label(badge_row, text="\U0001f6e1  System Administrator", font=FONTS["body_bold"],
             fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]).pack(side="left")

    field_map = [
        ("name",  "Full Name"),
        ("phone", "Phone"),
        ("email", "Email"),
    ]
    fields = {}
    for key, label in field_map:
        ent = _entry_row(scroll, label, width=300)
        ent.insert(0, str(profile.get(key, "")))
        fields[key] = ent

    advocate_id = profile.get("advocate_id")

    def save():
        if not advocate_id:
            _info_popup(dashboard, "Error", "Admin ID not found.")
            return
        existing = db.get_advocate_profile(advocate_id) or {}
        success = db.update_advocate_profile(
            advocate_id,
            fields["name"].get().strip(),
            existing.get("bar_number", ""),
            existing.get("primary_court", ""),
            existing.get("chambers", ""),
            fields["phone"].get().strip(),
            fields["email"].get().strip(),
        )
        if success:
            _info_popup(dashboard, "Saved", "Admin profile updated successfully.")
        else:
            _info_popup(dashboard, "Error", "Failed to save profile.")

    _black_btn(scroll, "Save Settings", save, 180).pack(anchor="w", padx=20, pady=14)

    # ── Update Password section ──────────────────────────────────────────────
    _divider(scroll)
    tk.Label(scroll, text="Update Password", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(8, 4))
    tk.Label(scroll, text="Change the admin login password. Enter your current password to verify.",
             font=FONTS["caption"], fg=COLORS["text_muted"],
             bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 8))

    pw_old     = _entry_row(scroll, "Old Password",     width=260, show="\u2022")
    pw_new     = _entry_row(scroll, "New Password",     width=260, show="\u2022")
    pw_confirm = _entry_row(scroll, "Confirm Password", width=260, show="\u2022")

    def change_password():
        old_pw = pw_old.get().strip()
        new_pw = pw_new.get().strip()
        cfm_pw = pw_confirm.get().strip()
        if not old_pw or not new_pw or not cfm_pw:
            _info_popup(dashboard, "Missing Fields", "All three password fields are required.")
            return
        if new_pw != cfm_pw:
            _info_popup(dashboard, "Mismatch",
                        "New Password and Confirm Password do not match.")
            return
        if len(new_pw) < 4:
            _info_popup(dashboard, "Too Short", "New password must be at least 4 characters.")
            return
        result = db.change_advocate_password(advocate_id, old_pw, new_pw)
        if result is None:
            _info_popup(dashboard, "\u26d4 Wrong Password",
                        "The old password you entered is incorrect. Please try again.")
        elif result:
            _info_popup(dashboard, "\u2713 Password Updated",
                        "Admin password changed successfully.\nUse the new password on next login.")
            pw_old.delete(0, "end")
            pw_new.delete(0, "end")
            pw_confirm.delete(0, "end")
        else:
            _info_popup(dashboard, "Error", "Failed to update password. Please try again.")

    _black_btn(scroll, "Update Password", change_password, 180).pack(anchor="w", padx=20, pady=14)


# ── Assistant Profile View ────────────────────────────────
def build_assistant_profile_view(parent, asst_data, dashboard):
    """Profile view for an assistant — name/phone/email editable + password change."""
    dashboard._back_bar(parent, "Assistant Profile")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Assistant Account Settings", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))

    # Read-only info strip
    info_row = tk.Frame(scroll, bg=COLORS["bg_secondary"], padx=16, pady=8)
    info_row.pack(fill="x", padx=20, pady=(0, 12))
    asst_id = asst_data.get("assistant_id") or asst_data.get("id")
    username = asst_data.get("username", "")
    adv_name = asst_data.get("advocate_name", asst_data.get("linked_advocate_name", ""))
    tk.Label(info_row,
             text=f"\U0001f464  {username}   ·   Linked to: {adv_name}",
             font=FONTS["body_bold"],
             fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]).pack(side="left")

    # Editable fields
    field_map = [
        ("full_name", "Full Name"),
        ("phone",     "Phone"),
        ("email",     "Email"),
    ]
    fields = {}
    for key, label in field_map:
        ent = _entry_row(scroll, label, width=300)
        ent.insert(0, str(asst_data.get(key, "") or ""))
        fields[key] = ent

    def save():
        if not asst_id:
            _info_popup(dashboard, "Error", "Assistant ID not found.")
            return
        success = db.update_assistant_profile(
            asst_id,
            fields["full_name"].get().strip(),
            fields["phone"].get().strip(),
            fields["email"].get().strip(),
        )
        if success:
            _info_popup(dashboard, "Saved", "Profile updated successfully.")
        else:
            _info_popup(dashboard, "Error", "Failed to save profile.")

    _black_btn(scroll, "Save Settings", save, 180).pack(anchor="w", padx=20, pady=14)

    # ── Update Password section  ─────────────────────────────────────
    _divider(scroll)
    tk.Label(scroll, text="Update Password", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(8, 4))
    tk.Label(scroll,
             text="Change your login password. Enter your current password to verify your identity.",
             font=FONTS["caption"], fg=COLORS["text_muted"],
             bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 8))

    pw_old     = _entry_row(scroll, "Old Password",     width=260, show="\u2022")
    pw_new     = _entry_row(scroll, "New Password",     width=260, show="\u2022")
    pw_confirm = _entry_row(scroll, "Confirm Password", width=260, show="\u2022")

    def change_password():
        old_pw = pw_old.get().strip()
        new_pw = pw_new.get().strip()
        cfm_pw = pw_confirm.get().strip()
        if not old_pw or not new_pw or not cfm_pw:
            _info_popup(dashboard, "Missing Fields", "All three password fields are required.")
            return
        if new_pw != cfm_pw:
            _info_popup(dashboard, "Mismatch",
                        "New Password and Confirm Password do not match.\nPlease re-enter them.")
            return
        if len(new_pw) < 4:
            _info_popup(dashboard, "Too Short", "New password must be at least 4 characters.")
            return
        result = db.change_assistant_password(asst_id, old_pw, new_pw)
        if result is None:
            _info_popup(dashboard, "\u26d4 Wrong Password",
                        "The old password you entered is incorrect.\nPlease try again.")
        elif result:
            _info_popup(dashboard, "\u2713 Password Updated",
                        "Your password has been changed successfully.\nUse the new password on your next login.")
            pw_old.delete(0, "end")
            pw_new.delete(0, "end")
            pw_confirm.delete(0, "end")
        else:
            _info_popup(dashboard, "Error", "Failed to update password. Please try again.")

    _black_btn(scroll, "Update Password", change_password, 180).pack(anchor="w", padx=20, pady=14)


# ── Client Account Settings ──────────────────────────────────────────────────
def build_client_settings_view(parent, client_data, dashboard):
    """Client-specific settings view — shows only client-relevant fields."""
    dashboard._back_bar(parent, "Account Settings")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Account Settings", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))

    client_id = client_data.get("client_id", "")
    # Show Client ID as read-only label
    id_row = tk.Frame(scroll, bg=COLORS["bg_primary"])
    id_row.pack(fill="x", padx=20, pady=4)
    tk.Label(id_row, text="Client ID", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
             width=22, anchor="w").pack(side="left")
    tk.Label(id_row, text=client_id, font=FONTS["body"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(side="left", padx=6)

    field_map = [
        ("full_name", "Full Name"),
        ("phone",     "Phone"),
        ("email",     "Email"),
        ("address",   "Address"),
    ]
    fields = {}
    for key, label in field_map:
        ent = _entry_row(scroll, label, width=300)
        ent.insert(0, str(client_data.get(key, "") or ""))
        fields[key] = ent

    def save():
        success = db.update_client_profile(
            client_id,
            fields["full_name"].get().strip(),
            fields["phone"].get().strip(),
            fields["email"].get().strip(),
            fields["address"].get().strip(),
        )
        if success:
            _info_popup(dashboard, "Saved", "Profile updated successfully.")
        else:
            _info_popup(dashboard, "Error", "Failed to save profile.")

    _black_btn(scroll, "Save Settings", save, 180).pack(anchor="w", padx=20, pady=14)

    # ── Update Password section ──────────────────────────────────────────
    _divider(scroll)
    tk.Label(scroll, text="Update Password", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(8, 4))
    tk.Label(scroll, text="Change your login password. Enter your current password to verify your identity.",
             font=FONTS["caption"], fg=COLORS["text_muted"],
             bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 8))

    pw_old     = _entry_row(scroll, "Old Password",     width=260, show="\u2022")
    pw_new     = _entry_row(scroll, "New Password",     width=260, show="\u2022")
    pw_confirm = _entry_row(scroll, "Confirm Password", width=260, show="\u2022")

    def change_password():
        old_pw = pw_old.get().strip()
        new_pw = pw_new.get().strip()
        cfm_pw = pw_confirm.get().strip()
        if not old_pw or not new_pw or not cfm_pw:
            _info_popup(dashboard, "Missing Fields",
                        "All three password fields are required.")
            return
        if new_pw != cfm_pw:
            _info_popup(dashboard, "Mismatch",
                        "New Password and Confirm Password do not match.\n"
                        "Please re-enter them.")
            return
        if len(new_pw) < 4:
            _info_popup(dashboard, "Too Short",
                        "New password must be at least 4 characters.")
            return
        result = db.change_client_password(client_id, old_pw, new_pw)
        if result is None:
            _info_popup(dashboard, "\u26d4 Wrong Password",
                        "The old password you entered is incorrect.\n"
                        "Please try again.")
        elif result:
            _info_popup(dashboard, "\u2713 Password Updated",
                        "Your password has been changed successfully.\n"
                        "Use the new password on your next login.")
            pw_old.delete(0, "end")
            pw_new.delete(0, "end")
            pw_confirm.delete(0, "end")
        else:
            _info_popup(dashboard, "Error",
                        "Failed to update password. Please try again.")

    _black_btn(scroll, "Update Password", change_password, 180).pack(anchor="w", padx=20, pady=14)


# ── 2.3 Create New Client ─────────────────────────────────────────────────────
def build_create_client_view(parent, router, dashboard, advocate_id=1):
    dashboard._back_bar(parent, "2.3 — Create New Client")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Create New Client Account", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))

    next_id = db.get_next_client_id()
    f_id    = _entry_row(scroll, "Client ID (auto-suggested)", width=340)
    f_id.insert(0, next_id)

    f_name  = _entry_row(scroll, "Full Name", width=340)
    f_phone = _entry_row(scroll, "Phone Number", width=340)
    f_email = _entry_row(scroll, "Email Address", width=340)

    addr_row = tk.Frame(scroll, bg=COLORS["bg_primary"])
    addr_row.pack(fill="x", padx=20, pady=4)
    tk.Label(addr_row, text="Residential Address", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
             width=22, anchor="w").pack(side="left")
    addr_box = ctk.CTkTextbox(addr_row, width=340, height=56,
                               fg_color=COLORS["entry_bg"],
                               text_color=COLORS["text_primary"],
                               border_color=COLORS["entry_border"], border_width=1)
    addr_box.pack(side="left", padx=6)

    f_pw  = _entry_row(scroll, "Login Password", width=340, show="\u2022")
    f_pw2 = _entry_row(scroll, "Confirm Password", width=340, show="\u2022")

    def create_client():
        cid   = f_id.get().strip()
        name  = f_name.get().strip()
        phone = f_phone.get().strip()
        email = f_email.get().strip()
        addr  = addr_box.get("0.0", "end").strip()
        pw    = f_pw.get().strip()
        pw2   = f_pw2.get().strip()
        if not cid or not name or not pw:
            _info_popup(dashboard, "Missing Fields",
                        "Client ID, Full Name, and Password are required.")
            return
        if pw != pw2:
            _info_popup(dashboard, "Password Mismatch",
                        "Password and Confirm Password do not match.")
            return
        success = db.create_client(cid, name, phone, email, addr, pw)
        if success:
            _info_popup(dashboard, "Client Created",
                        f"Client account created!\nThey can log in with ID: {cid}")
            for e in [f_id, f_name, f_phone, f_email, f_pw, f_pw2]:
                e.delete(0, "end")
            addr_box.delete("0.0", "end")
            f_id.insert(0, db.get_next_client_id())
        else:
            _info_popup(dashboard, "Error",
                        f"Client ID '{cid}' may already exist.\n"
                        "Choose a different ID or use the auto-suggested one.")

    def clear_form():
        for e in [f_id, f_name, f_phone, f_email, f_pw, f_pw2]:
            e.delete(0, "end")
        addr_box.delete("0.0", "end")
        f_id.insert(0, db.get_next_client_id())

    br = tk.Frame(scroll, bg=COLORS["bg_primary"])
    br.pack(anchor="w", padx=59, pady=16)
    _black_btn(br, "Create Client", create_client, 180).pack(side="left", padx=8)
    _ghost_btn(br, "Clear Form", clear_form, 140).pack(side="left", padx=8)


# ── 4.1 Create New Advocate (Admin only) ─────────────────────────────────────
def build_create_advocate_view(parent, router, dashboard):
    dashboard._back_bar(parent, "4.1 — Create New Advocate Account")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text="Create New Advocate Account", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", pady=(8, 12))

    f_user    = _entry_row(scroll, "Username", width=340)
    f_name    = _entry_row(scroll, "Full Name", width=340)
    f_bar     = _entry_row(scroll, "Bar Number", width=340)
    f_court   = _entry_row(scroll, "Primary Court", width=340)
    f_chamber = _entry_row(scroll, "Chambers Address", width=340)
    f_phone   = _entry_row(scroll, "Phone", width=340)
    f_email   = _entry_row(scroll, "Email", width=340)
    f_pw      = _entry_row(scroll, "Password", width=340, show="\u2022")
    f_pw2     = _entry_row(scroll, "Confirm Password", width=340, show="\u2022")

    def create_adv():
        username  = f_user.get().strip()
        full_name = f_name.get().strip()
        bar_no    = f_bar.get().strip()
        court     = f_court.get().strip()
        chambers  = f_chamber.get().strip()
        phone     = f_phone.get().strip()
        email     = f_email.get().strip()
        pw        = f_pw.get().strip()
        pw2       = f_pw2.get().strip()
        if not username or not full_name or not bar_no or not court or not pw:
            _info_popup(dashboard, "Missing Fields",
                        "Username, Full Name, Bar Number, Primary Court and Password are required.")
            return
        if pw != pw2:
            _info_popup(dashboard, "Password Mismatch",
                        "Password and Confirm Password do not match.")
            return
        success = db.create_advocate(username, pw, full_name, bar_no,
                                     court, chambers, phone, email)
        if success:
            _info_popup(dashboard, "Advocate Created",
                        f"Advocate account for '{full_name}' created.\n"
                        f"They can now log in with username: {username}")
            for e in [f_user, f_name, f_bar, f_court, f_chamber,
                      f_phone, f_email, f_pw, f_pw2]:
                e.delete(0, "end")
        else:
            _info_popup(dashboard, "Error",
                        f"Username '{username}' already exists.\nChoose a different username.")

    def clear_form():
        for e in [f_user, f_name, f_bar, f_court, f_chamber,
                  f_phone, f_email, f_pw, f_pw2]:
            e.delete(0, "end")

    br = tk.Frame(scroll, bg=COLORS["bg_primary"])
    br.pack(anchor="w", padx=19, pady=16)
    _black_btn(br, "Create Advocate Account", create_adv, 220).pack(side="left", padx=8)
    _ghost_btn(br, "Clear Form", clear_form, 140).pack(side="left", padx=8)


# ── Client: My Cases ──────────────────────────────────────────────────────────
def build_client_case_view(parent, router, dashboard, client_id):
    dashboard._back_bar(parent, "My Cases")
    cases = db.get_cases_for_client(client_id) or []
    if not cases:
        tk.Label(parent, text="No cases found.", font=FONTS["body"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_primary"]).pack(pady=40)
        return
    cn_list = [c["case_no"] for c in cases]
    cn_var  = tk.StringVar(value=cn_list[0])

    sb = tk.Frame(parent, bg=COLORS["bg_secondary"])
    sb.pack(fill="x", padx=16, pady=10)
    tk.Label(sb, text="Select Case:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=(8, 4), pady=8)
    ctk.CTkOptionMenu(sb, values=cn_list, variable=cn_var,
                      fg_color=COLORS["accent"], button_color=COLORS["navbar_hover"],
                      button_hover_color=COLORS["accent_hover"],
                      text_color=COLORS["text_on_dark"],
                      dropdown_fg_color=COLORS["bg_primary"],
                      dropdown_text_color=COLORS["text_primary"],
                      width=280).pack(side="left", padx=6)

    rf = tk.Frame(parent, bg=COLORS["bg_primary"])
    rf.pack(fill="both", expand=True)

    def load(*_):
        for w in rf.winfo_children():
            w.destroy()
        row = db.get_case(cn_var.get())
        if row:
            _render_case_detail(rf, row, router, is_client_view=True)
        else:
            tk.Label(rf, text="Case not found.", font=FONTS["body"],
                     fg="#CC0000", bg=COLORS["bg_primary"]).pack(pady=20)

    _black_btn(sb, "View", load, 100).pack(side="left", padx=6, pady=8)
    load()


# ── Client: Payment Portal ────────────────────────────────────────────────────
def build_payment_portal_view(parent, router, dashboard, client_id):
    """v6: Per-case payment input - each due row has its own amount box and PAY button."""
    dashboard._back_bar(parent, "Payment Portal")
    client_row = db.get_client(client_id) or {}
    dues       = db.get_pending_dues_for_client(client_id) or []
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)
    tk.Label(scroll, text=f"Outstanding Dues - {client_row.get('full_name', '')}",
             font=FONTS["heading_1"], fg=COLORS["text_primary"],
             bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=10)
    _divider(scroll)
    if not dues:
        tk.Label(scroll, text="No outstanding dues. You are all clear!",
                 font=FONTS["body"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(pady=30)
        return
    total = sum(int(float(d.get("amount_due", 0))) for d in dues)
    for due in dues:
        case_no    = due.get("case_no", "---")
        amount_due = int(float(due.get("amount_due", 0)))
        desc       = due.get("description", "")
        due_date   = _fmt_date(due.get("due_date"))
        row = tk.Frame(scroll, bg=COLORS["bg_card"],
                       highlightbackground=COLORS["border_cell"], highlightthickness=1)
        row.pack(fill="x", pady=4, padx=2)
        info = tk.Frame(row, bg=COLORS["bg_card"])
        info.pack(side="left", fill="x", expand=True, padx=8, pady=6)
        tk.Label(info, text=f"Case No: {case_no}", font=FONTS["body_bold"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
        tk.Label(info, text=f"Amount Due: {_fmt_amount(amount_due)}   |   Due: {due_date}",
                 font=FONTS["caption"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
        if desc:
            tk.Label(info, text=desc, font=FONTS["caption"],
                     fg=COLORS["text_muted"], bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
        pay_frame = tk.Frame(row, bg=COLORS["bg_card"])
        pay_frame.pack(side="right", padx=10)
        amt_entry = ctk.CTkEntry(
            pay_frame, width=120, placeholder_text="Enter amount",
            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"],
        )
        amt_entry.pack(side="left", padx=(0, 6))
        def make_pay(entry=amt_entry, cn=case_no, max_amt=amount_due):
            def _pay():
                val_str = entry.get().strip()
                try:
                    val = float(val_str)
                    if val <= 0: raise ValueError
                except ValueError:
                    _info_popup(dashboard, "Invalid Amount",
                                "Please enter a valid positive number.")
                    return
                if val > max_amt:
                    _info_popup(dashboard, "Exceeds Due",
                                f"Amount cannot exceed {_fmt_amount(max_amt)}.")
                    return
                db.apply_partial_payment_to_dues(client_id, cn, val)
                db.record_payment(client_id, cn, 1, val, "Client portal payment")
                _info_popup(dashboard, "Payment Recorded",
                            f"Payment of Rs.{int(val):,} for Case No. {cn} submitted successfully.")
                for w in parent.winfo_children(): w.destroy()
                build_payment_portal_view(parent, router, dashboard, client_id)
            return _pay
        _black_btn(pay_frame, "PAY", make_pay(), 70).pack(side="left")
    tk.Label(scroll, text=f"Total Outstanding:  Rs.{total:,}", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="e", padx=20, pady=10)


def build_payment_history_view(parent, router, dashboard, client_id):
    dashboard._back_bar(parent, "Payment History")
    client_row = db.get_client(client_id) or {}
    pmts       = db.get_payments_for_client(client_id) or []

    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    tk.Label(scroll, text=f"Payment History — {client_row.get('full_name', '')}",
             font=FONTS["heading_1"], fg=COLORS["text_primary"],
             bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=10)
    _divider(scroll)

    COL_DEFS = [
        ("Date",      120),
        ("Amount",    110),
        ("Case No.",  180),
        ("Remarks",   180),
        ("",           70),
    ]
    _make_table_header(scroll, COL_DEFS)

    if not pmts:
        tk.Label(scroll, text="No payment records found.", font=FONTS["body"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_primary"]).pack(pady=20)
    for pmt in pmts:
        p_data = {
            "date":       _fmt_date(pmt.get("payment_date")),
            "amount":     int(float(pmt.get("amount", 0))),
            "client_id":  pmt.get("client_id", ""),
            "case_no":    pmt.get("case_no", ""),
            "note":       pmt.get("note", "—"),
            "payment_id": pmt.get("payment_id"),
            "advocate_id": pmt.get("advocate_id")
        }

        def print_factory(p=p_data):
            def make(row_frame):
                return ctk.CTkButton(
                    row_frame, text="Print", width=60, height=26,
                    fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                    text_color=COLORS["text_on_dark"], font=FONTS["caption_bold"],
                    corner_radius=DIMS["btn_corner"],
                    command=lambda pm=p: open_print_receipt(dashboard, pm, "client"),
                )
            return make

        _make_table_row(scroll, [
            (_fmt_date(pmt.get("payment_date")),   COL_DEFS[0][1]),
            (_fmt_amount(pmt.get("amount", 0)),    COL_DEFS[1][1]),
            (pmt.get("case_no", "—"),              COL_DEFS[2][1]),
            (pmt.get("note", ""),                  COL_DEFS[3][1]),
            (print_factory(p_data),                COL_DEFS[4][1]),
        ])


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — NAVBAR DROPDOWN ENGINE
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION v6-A — SMART SEARCH BAR HELPER
# ══════════════════════════════════════════════════════════════════════════════

def build_smart_search_bar(parent, categories, on_search, get_suggestions=None):
    bar = tk.Frame(parent, bg=COLORS["bg_secondary"])
    bar.pack(fill="x", padx=0, pady=0)
    cat_var = tk.StringVar(value=categories[0] if categories else "")
    cat_menu = ctk.CTkOptionMenu(
        bar, values=categories, variable=cat_var, width=160,
        fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
        button_color=COLORS["navbar_hover"], button_hover_color=COLORS["accent_hover"],
        dropdown_fg_color=COLORS["bg_primary"], dropdown_text_color=COLORS["text_primary"],
        corner_radius=4, font=FONTS["caption_bold"],
    )
    cat_menu.pack(side="left", padx=(10, 4), pady=5)
    entry_var = tk.StringVar()
    entry = ctk.CTkEntry(
        bar, textvariable=entry_var, width=260, placeholder_text="Search...",
        fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
        border_color=COLORS["entry_border"], corner_radius=4,
        placeholder_text_color=COLORS["text_muted"],
    )
    entry.pack(side="left", padx=(0, 4), pady=5)
    _ac_top = [None]

    def _close_ac():
        if _ac_top[0]:
            try: _ac_top[0].destroy()
            except Exception: pass
            _ac_top[0] = None

    def _show_ac(items):
        _close_ac()
        if not items: return
        x = entry.winfo_rootx()
        y = entry.winfo_rooty() + entry.winfo_height()
        top = tk.Toplevel(parent)
        top.wm_overrideredirect(True)
        top.geometry(f"260x{min(len(items)*22+4, 180)}+{x}+{y}")
        top.configure(bg=COLORS["bg_secondary"])
        top.lift()
        _ac_top[0] = top
        lb = tk.Listbox(top, font=FONTS["caption"], bg=COLORS["bg_card"],
                        fg=COLORS["text_primary"], selectbackground=COLORS["accent"],
                        activestyle="none", bd=0, relief="flat", highlightthickness=0)
        lb.pack(fill="both", expand=True)
        for item in items:
            lb.insert("end", str(item))
        def _pick(e):
            sel = lb.curselection()
            if sel:
                entry_var.set(lb.get(sel[0]))
            _close_ac()
        lb.bind("<ButtonRelease-1>", _pick)

    def _on_key(e):
        if get_suggestions:
            q = entry_var.get().strip().lower()
            items = get_suggestions(cat_var.get())
            if q:
                items = [i for i in items if q in str(i).lower()]
            _show_ac(items[:20])

    def _on_click(e):
        if get_suggestions:
            items = get_suggestions(cat_var.get())
            q = entry_var.get().strip().lower()
            if q:
                items = [i for i in items if q in str(i).lower()]
            _show_ac(items)

    entry.bind("<FocusIn>",   _on_click)
    entry.bind("<KeyRelease>", _on_key)
    entry.bind("<Return>", lambda e: (_close_ac(), on_search(cat_var.get(), entry_var.get().strip())))

    _black_btn(bar, "Search",
               lambda: (_close_ac(), on_search(cat_var.get(), entry_var.get().strip())),
               88).pack(side="left", padx=4, pady=5)
    clr = tk.Label(bar, text="X Clear", font=FONTS["caption"], fg=COLORS["text_muted"],
                   bg=COLORS["bg_secondary"], cursor="hand2", padx=4)
    clr.pack(side="left", pady=5)
    def _clear():
        entry_var.set("")
        _close_ac()
        on_search("", "")
    clr.bind("<Button-1>", lambda e: _clear())
    clr.bind("<Enter>",    lambda e: clr.config(fg=COLORS["text_primary"]))
    clr.bind("<Leave>",    lambda e: clr.config(fg=COLORS["text_muted"]))
    return bar


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION v6-B — ASSISTANT MANAGEMENT VIEWS
# ══════════════════════════════════════════════════════════════════════════════

_FEATURE_LABELS = [
    ("case_info",      "1.1  Case Info"),
    ("case_addition",  "1.2  Case Addition"),
    ("case_updation",  "1.3  Case Updation"),
    ("client_cases",   "2.1  Client Cases Ongoing"),
    ("fees_tracking",  "2.2  Fees Tracking"),
    ("expenses",       "3.1  Expenses"),
    ("money_incoming", "3.2  Money Incoming"),
]


def build_manage_assistant_view(parent, router, dashboard, advocate_id):
    dashboard._back_bar(parent, "Manage Assistants")
    body = tk.Frame(parent, bg=COLORS["bg_primary"])
    body.pack(fill="both", expand=True)
    body.grid_columnconfigure(0, weight=2, minsize=220)
    body.grid_columnconfigure(1, weight=0)
    body.grid_columnconfigure(2, weight=5)
    body.grid_rowconfigure(0, weight=1)

    left = tk.Frame(body, bg=COLORS["bg_card"])
    left.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
    tk.Label(left, text="Assistants", font=FONTS["heading_2"],
             fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(anchor="w", padx=12, pady=(10, 4))
    _divider(left)
    scroll_left = ctk.CTkScrollableFrame(left, fg_color=COLORS["bg_card"])
    scroll_left.pack(fill="both", expand=True)
    tk.Frame(body, bg=COLORS["border"], width=1).grid(row=0, column=1, sticky="ns", pady=12)

    right = tk.Frame(body, bg=COLORS["bg_primary"])
    right.grid(row=0, column=2, sticky="nsew", padx=12, pady=12)
    detail_host = [right]

    def show_placeholder():
        for w in detail_host[0].winfo_children(): w.destroy()
        tk.Label(detail_host[0], text="<- Select an assistant",
                 font=FONTS["body"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(pady=40)

    def show_assistant(asst):
        for w in detail_host[0].winfo_children(): w.destroy()
        aid = asst["assistant_id"]
        card = tk.Frame(detail_host[0], bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", padx=4, pady=8)
        for lbl, val in [
            ("Full Name", asst.get("full_name", "")),
            ("Username",  asst.get("username", "")),
            ("Phone",     asst.get("phone", "---")),
            ("Email",     asst.get("email", "---")),
            ("Status",    "Active" if asst.get("is_active") else "Inactive"),
        ]:
            row = tk.Frame(card, bg=COLORS["bg_card"])
            row.pack(fill="x", padx=14, pady=3)
            tk.Label(row, text=f"{lbl}:", font=FONTS["body_bold"], width=12, anchor="w",
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(side="left")
            tk.Label(row, text=val, font=FONTS["body"], anchor="w",
                     fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(side="left")

        tk.Label(detail_host[0], text="Feature Access Permissions",
                 font=FONTS["heading_2"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=6, pady=(14, 4))
        _divider(detail_host[0])
        perms = db.get_assistant_permissions(aid)
        check_vars = {}
        for fk, label in _FEATURE_LABELS:
            var = tk.BooleanVar(value=perms.get(fk, False))
            check_vars[fk] = var
            row = tk.Frame(detail_host[0], bg=COLORS["bg_primary"])
            row.pack(fill="x", padx=8, pady=2)
            ctk.CTkCheckBox(
                row, text=label, variable=var,
                font=FONTS["body"],
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_hover"],
                border_color=COLORS["border_strong"],
                checkmark_color=COLORS["text_on_dark"],
            ).pack(anchor="w")

        def save_perms():
            db.set_assistant_permissions(aid, {fk: v.get() for fk, v in check_vars.items()})
            _info_popup(dashboard, "Saved", "Assistant permissions updated successfully.")

        _black_btn(detail_host[0], "Save Changes", save_perms, 200).pack(pady=14)

    def load_list():
        for w in scroll_left.winfo_children(): w.destroy()
        assistants = db.get_assistants_for_advocate(advocate_id)
        if not assistants:
            tk.Label(scroll_left, text="No assistants yet.", font=FONTS["caption"],
                     fg=COLORS["text_muted"], bg=COLORS["bg_card"]).pack(pady=20)
        for a in assistants:
            row = tk.Frame(scroll_left, bg=COLORS["bg_secondary"],
                           highlightbackground=COLORS["border_cell"], highlightthickness=1,
                           cursor="hand2")
            row.pack(fill="x", pady=2, padx=4)
            tk.Label(row, text=a["full_name"], font=FONTS["body_bold"],
                     fg=COLORS["text_primary"], bg=COLORS["bg_secondary"], anchor="w").pack(
                side="left", padx=8, pady=6)
            tk.Label(row, text=f"@{a['username']}", font=FONTS["caption"],
                     fg=COLORS["text_muted"], bg=COLORS["bg_secondary"]).pack(side="left")
            row.bind("<Button-1>", lambda e, asst=a: show_assistant(asst))
            for ch in row.winfo_children():
                ch.bind("<Button-1>", lambda e, asst=a: show_assistant(asst))

    load_list()
    show_placeholder()


def build_create_delete_assistant_view(parent, router, dashboard, advocate_id):
    dashboard._back_bar(parent, "Create / Delete Assistant")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    tk.Label(scroll, text="Create New Assistant", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(14, 4))
    _divider(scroll)
    form = tk.Frame(scroll, bg=COLORS["bg_primary"])
    form.pack(fill="x", padx=30, pady=6)
    fields = {}
    field_defs = [
        ("username",  "Username / Login ID *", ""),
        ("full_name", "Full Name *",            ""),
        ("password",  "Password *",             "*"),
        ("confirm",   "Confirm Password *",     "*"),
        ("phone",     "Phone (optional)",       ""),
        ("email",     "Email (optional)",       ""),
    ]
    for key, label, show in field_defs:
        tk.Label(form, text=label, font=FONTS["body_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
                 anchor="w").pack(anchor="w", pady=(8, 2))
        ent = ctk.CTkEntry(
            form, width=320, show=show,
            fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
            border_color=COLORS["entry_border"], corner_radius=DIMS["btn_corner"],
            placeholder_text_color=COLORS["text_muted"],
        )
        ent.pack(anchor="w")
        fields[key] = ent
    err_lbl = tk.Label(form, text="", font=FONTS["caption"], fg="#CC2222",
                       bg=COLORS["bg_primary"])
    err_lbl.pack(anchor="w", pady=(6, 0))

    def do_create():
        username  = fields["username"].get().strip()
        full_name = fields["full_name"].get().strip()
        password  = fields["password"].get()
        confirm   = fields["confirm"].get()
        phone     = fields["phone"].get().strip()
        email     = fields["email"].get().strip()
        if not username or not full_name or not password:
            err_lbl.config(text="X  Username, Full Name, and Password are required.")
            return
        if password != confirm:
            err_lbl.config(text="X  Passwords do not match.")
            return
        if db.is_username_taken(username):
            _info_popup(dashboard, "Username Taken",
                        "This username is already in use. Please choose another.")
            return
        ok = db.create_assistant(advocate_id, username, password, full_name, phone, email)
        if ok:
            for ent in fields.values(): ent.delete(0, "end")
            err_lbl.config(text="")
            _info_popup(dashboard, "Assistant Created",
                        "Assistant account created successfully!\n"
                        "Go to 'Manage Assistants' to set their permissions.")
        else:
            err_lbl.config(text="X  Failed to create assistant. Username may be duplicate.")

    _black_btn(form, "Create Assistant", do_create, 200).pack(pady=12)

    tk.Frame(scroll, bg=COLORS["border"], height=1).pack(fill="x", padx=20, pady=(20, 6))
    tk.Label(scroll, text="Delete Assistant", font=FONTS["heading_1"],
             fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(6, 4))
    _divider(scroll)
    del_frame = tk.Frame(scroll, bg=COLORS["bg_primary"])
    del_frame.pack(fill="x", padx=30, pady=6)
    tk.Label(del_frame, text="Enter Assistant Username or ID:", font=FONTS["body_bold"],
             fg=COLORS["text_secondary"], bg=COLORS["bg_primary"], anchor="w").pack(anchor="w", pady=(6, 2))
    del_row = tk.Frame(del_frame, bg=COLORS["bg_primary"])
    del_row.pack(anchor="w")
    del_entry = ctk.CTkEntry(
        del_row, width=240, fg_color=COLORS["entry_bg"],
        text_color=COLORS["text_primary"], border_color=COLORS["entry_border"],
        corner_radius=DIMS["btn_corner"], placeholder_text="username or assistant ID",
    )
    del_entry.pack(side="left", padx=(0, 8))
    result_host = tk.Frame(del_frame, bg=COLORS["bg_primary"])
    result_host.pack(fill="x", pady=6)

    def do_search():
        for w in result_host.winfo_children(): w.destroy()
        query = del_entry.get().strip()
        if not query: return
        asst = None
        if query.isdigit():
            a = db.get_assistant_by_id(int(query))
            if a and a.get("linked_advocate_id") == advocate_id:
                asst = a
        if asst is None:
            a = db.get_assistant_by_username_for_advocate(query, advocate_id)
            if a: asst = a
        if not asst:
            tk.Label(result_host, text="X  No assistant found under your account.",
                     font=FONTS["caption"], fg="#CC2222", bg=COLORS["bg_primary"]).pack(anchor="w")
            return
        card = tk.Frame(result_host, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", pady=4)
        tk.Label(card, text=f"{asst['full_name']}  (@{asst['username']})",
                 font=FONTS["body_bold"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_card"]).pack(side="left", padx=12, pady=8)
        def confirm_delete():
            resp = _confirm_popup(
                dashboard, "Confirm Deletion",
                f"Delete assistant {asst['full_name']} (@{asst['username']})?\n"
                "This cannot be undone.")
            if resp:
                db.delete_assistant(asst["assistant_id"])
                del_entry.delete(0, "end")
                for w in result_host.winfo_children(): w.destroy()
                _info_popup(dashboard, "Deleted", "Assistant account deleted successfully.")
        del_btn = tk.Label(card, text="  DELETE  ", font=FONTS["caption_bold"],
                           fg="white", bg="#CC2222", cursor="hand2", padx=6, pady=4)
        del_btn.pack(side="right", padx=8, pady=6)
        del_btn.bind("<Button-1>", lambda e: confirm_delete())
        del_btn.bind("<Enter>",    lambda e: del_btn.config(bg="#AA0000"))
        del_btn.bind("<Leave>",    lambda e: del_btn.config(bg="#CC2222"))

    _black_btn(del_row, "Search", do_search, 90).pack(side="left")


def build_admin_assistants_view(parent, router, dashboard):
    dashboard._back_bar(parent, "All Assistants - System Wide")
    scroll = ctk.CTkScrollableFrame(
        parent, fg_color=COLORS["bg_primary"],
        scrollbar_button_color=COLORS["scrollbar"],
        scrollbar_button_hover_color=COLORS["scrollbar_hover"],
    )
    scroll.pack(fill="both", expand=True)

    def load():
        for w in scroll.winfo_children(): w.destroy()
        assistants = db.get_all_assistants_admin()
        tk.Label(scroll, text=f"Total Assistants: {len(assistants)}",
                 font=FONTS["heading_2"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=18, pady=(10, 4))
        _divider(scroll)
        if not assistants:
            tk.Label(scroll, text="No assistants found.", font=FONTS["body"],
                     fg=COLORS["text_muted"], bg=COLORS["bg_primary"]).pack(pady=30)
            return
        hdr = tk.Frame(scroll, bg=COLORS["bg_secondary"])
        hdr.pack(fill="x", padx=2, pady=(4, 0))
        for col in ["Full Name", "Username", "Advocate", "Status", "Actions"]:
            tk.Label(hdr, text=col, font=FONTS["caption_bold"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"],
                     anchor="w", width=16).pack(side="left", padx=6, pady=4)
        for a in assistants:
            row = tk.Frame(scroll, bg=COLORS["bg_card"],
                           highlightbackground=COLORS["border_cell"], highlightthickness=1)
            row.pack(fill="x", pady=2, padx=2)
            for val in [a.get("full_name",""), f"@{a.get('username','')}",
                        a.get("advocate_name","")]:
                tk.Label(row, text=val, font=FONTS["caption"], width=16, anchor="w",
                         fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(side="left", padx=6, pady=5)
            status = "Active" if a.get("is_active") else "Inactive"
            scol   = COLORS["accent"] if a.get("is_active") else "#CC2222"
            tk.Label(row, text=status, font=FONTS["caption_bold"], fg=scol,
                     bg=COLORS["bg_card"], width=10, anchor="w").pack(side="left", padx=4)
            act = tk.Frame(row, bg=COLORS["bg_card"])
            act.pack(side="left", padx=4)
            ttxt = "Deactivate" if a.get("is_active") else "Activate"
            tcol = "#444444"    if a.get("is_active") else COLORS["accent"]
            def make_toggle(asst_id, cur):
                def _t():
                    db.set_assistant_active(asst_id, 0 if cur else 1)
                    load()
                return _t
            def make_del(asst_id, nm, un):
                def _d():
                    if _confirm_popup(dashboard, "Confirm Delete",
                                      f"Delete {nm} (@{un})?"):
                        db.delete_assistant(asst_id)
                        load()
                return _d
            tgl = tk.Label(act, text=ttxt, font=FONTS["caption_bold"],
                           fg="white", bg=tcol, cursor="hand2", padx=5, pady=2)
            tgl.pack(side="left", padx=2)
            tgl.bind("<Button-1>", lambda e, fn=make_toggle(a["assistant_id"], a.get("is_active")): fn())
            dl = tk.Label(act, text="Delete", font=FONTS["caption_bold"],
                          fg="white", bg="#CC2222", cursor="hand2", padx=5, pady=2)
            dl.pack(side="left", padx=2)
            dl.bind("<Button-1>", lambda e, fn=make_del(
                a["assistant_id"], a.get("full_name",""), a.get("username","")): fn())

    load()


class NavDropdown:


    def __init__(self, navbar, label_text, items, router):
        self._router     = router
        self._menu_frame = None
        self._after_id   = None
        self._items      = items
        self.btn = tk.Label(
            navbar, text=f"  {label_text}  \u25be",
            font=FONTS["navbar"], fg=COLORS["navbar_text"],
            bg=COLORS["navbar_bg"], cursor="hand2", padx=6, pady=0,
        )
        self.btn.pack(side="left")
        self.btn.bind("<Enter>",    self._show)
        self.btn.bind("<Leave>",    self._schedule_hide)
        self.btn.bind("<Button-1>", self._show)

    def _show(self, event=None):
        if self._after_id:
            self.btn.after_cancel(self._after_id)
            self._after_id = None
        self._destroy_menu()
        root = self.btn.winfo_toplevel()
        x    = self.btn.winfo_rootx()
        y    = self.btn.winfo_rooty() + self.btn.winfo_height()
        self._menu_frame = tk.Toplevel(root)
        self._menu_frame.wm_overrideredirect(True)
        self._menu_frame.wm_geometry(f"+{x}+{y}")
        self._menu_frame.configure(bg=COLORS["navbar_bg"],
                                    highlightbackground=COLORS["navbar_border"],
                                    highlightthickness=1)
        self._menu_frame.lift()
        for label, route_key in self._items:
            row = tk.Label(
                self._menu_frame, text=f"  {label}  ",
                font=FONTS["navbar_item"], fg=COLORS["navbar_text"],
                bg=COLORS["navbar_bg"], cursor="hand2",
                anchor="w", width=DIMS["dropdown_w"] // 8, padx=4, pady=8,
            )
            row.pack(fill="x")
            row.bind("<Enter>",    lambda e, r=row: r.config(bg=COLORS["navbar_active"]))
            row.bind("<Leave>",    lambda e, r=row: r.config(bg=COLORS["navbar_bg"]))
            row.bind("<Button-1>", lambda e, k=route_key: (self._destroy_menu(), self._router(k)))
        self._menu_frame.bind("<Leave>",  self._schedule_hide)
        self._menu_frame.bind("<Enter>",  self._cancel_hide)

    def _schedule_hide(self, event=None):
        self._after_id = self.btn.after(300, self._destroy_menu)

    def _cancel_hide(self, event=None):
        if self._after_id:
            self.btn.after_cancel(self._after_id)
            self._after_id = None

    def _destroy_menu(self):
        if self._menu_frame:
            try:
                self._menu_frame.destroy()
            except Exception:
                pass
            self._menu_frame = None


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 8 — TODAY'S LIVE SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

class TodaySidebar(tk.Frame):
    def __init__(self, parent, router, client_id=None, is_admin=False,
                 advocate_id=None, **kw):
        super().__init__(parent, bg=COLORS["bg_secondary"], **kw)
        self._router     = router
        self._client_id  = client_id
        self._is_admin   = is_admin
        self._advocate_id = advocate_id
        self._current_dt = datetime.date.today()
        self._day_lbl    = None
        self._date_lbl   = None
        self._sect_lbl   = None
        self._cases_host = None
        self._clock_lbl  = None
        self._build()

    def _build(self):
        today = datetime.date.today()
        date_block = tk.Frame(self, bg=COLORS["navbar_bg"])
        date_block.pack(fill="x")
        self._day_lbl = tk.Label(
            date_block, text=today.strftime("%A").upper(),
            font=FONTS["caption_bold"], fg=COLORS["text_muted"],
            bg=COLORS["navbar_bg"],
        )
        self._day_lbl.pack(pady=(14, 0))
        self._date_lbl = tk.Label(
            date_block, text=today.strftime("%d %B %Y"),
            font=FONTS["date_big"], fg=COLORS["navbar_text"],
            bg=COLORS["navbar_bg"],
        )
        self._date_lbl.pack(pady=(0, 4))
        self._clock_lbl = tk.Label(
            date_block, text="", font=FONTS["clock"],
            fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"],
        )
        self._clock_lbl.pack(pady=(0, 14))
        self._tick()

        sub = tk.Frame(self, bg=COLORS["bg_secondary"])
        sub.pack(fill="x")
        self._sect_lbl = tk.Label(
            sub, text="TODAY'S CASES", font=FONTS["caption_bold"],
            fg=COLORS["text_muted"], bg=COLORS["bg_secondary"], pady=8,
        )
        self._sect_lbl.pack(anchor="w", padx=12)
        tk.Frame(sub, bg=COLORS["border"], height=1).pack(fill="x")

        self._cases_host = tk.Frame(self, bg=COLORS["bg_secondary"])
        self._cases_host.pack(fill="both", expand=True)
        self._populate_cases(today)

    def _populate_cases(self, date_obj):
        for w in self._cases_host.winfo_children():
            w.destroy()
        scroll = ctk.CTkScrollableFrame(
            self._cases_host, fg_color=COLORS["bg_secondary"],
            scrollbar_button_color=COLORS["scrollbar"],
            scrollbar_button_hover_color=COLORS["scrollbar_hover"],
        )
        scroll.pack(fill="both", expand=True)

        if self._is_admin:
            cases = db.get_cases_for_all_advocates(date_obj) or []
        elif self._client_id:
            cases = db.get_cases_for_client_on_date(self._client_id, date_obj) or []
        else:
            cases = db.get_cases_for_date(date_obj, self._advocate_id) or []

        if not cases:
            tk.Label(scroll, text="No cases scheduled for this date.",
                     font=FONTS["caption"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_secondary"], pady=20).pack()
        else:
            for case in cases:
                self._case_row(scroll, case["case_no"], case)

    def show_date(self, date_obj):
        today = datetime.date.today()
        self._current_dt = date_obj
        self._day_lbl.config(text=date_obj.strftime("%A").upper())
        self._date_lbl.config(text=date_obj.strftime("%d %B %Y"))
        if date_obj == today:
            self._sect_lbl.config(text="TODAY'S CASES")
        else:
            self._sect_lbl.config(text=f"CASES — {date_obj.strftime('%d %b').upper()}")
        self._populate_cases(date_obj)

    def _case_row(self, parent, cn, case):
        name = case.get("case_name", case.get("name", "—"))
        card = tk.Frame(parent, bg=COLORS["bg_card"],
                         highlightbackground=COLORS["border_cell"], highlightthickness=1)
        card.pack(fill="x", pady=3, padx=6)
        hdr = tk.Frame(card, bg=COLORS["navbar_bg"])
        hdr.pack(fill="x")
        lbl = tk.Label(hdr, text=f"  {cn}  ", font=FONTS["caption_bold"],
                       fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"],
                       cursor="hand2", pady=4)
        lbl.pack(side="left")
        lbl.bind("<Button-1>", lambda e, c=cn: self._router("case_info", c))
        lbl.bind("<Enter>",    lambda e: lbl.config(bg=COLORS["navbar_hover"]))
        lbl.bind("<Leave>",    lambda e: lbl.config(bg=COLORS["navbar_bg"]))
        if self._is_admin and case.get("advocate_name"):
            tk.Label(hdr, text=f"  {case['advocate_name']}  ",
                     font=FONTS["caption"], fg=COLORS["text_muted"],
                     bg=COLORS["navbar_bg"]).pack(side="right", padx=4)
        tk.Label(card, text=name, font=FONTS["caption"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                 wraplength=240, justify="left", anchor="w", pady=4).pack(anchor="w", padx=8)
        tk.Label(card, text=f"  {case.get('next_step', '—')}", font=FONTS["caption"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"],
                 anchor="w").pack(anchor="w", padx=8, pady=(0, 6))

    def _tick(self):
        if self._clock_lbl.winfo_exists():
            self._clock_lbl.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
            self._clock_lbl.after(1000, self._tick)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 9 — MONTH CALENDAR
# ══════════════════════════════════════════════════════════════════════════════

class MonthCalendar(tk.Frame):
    def __init__(self, parent, router, year=None, month=None,
                 client_id=None, on_date_click=None, is_admin=False,
                 advocate_id=None, **kw):
        super().__init__(parent, bg=COLORS["bg_primary"], **kw)
        today               = datetime.date.today()
        self._year          = year or today.year
        self._month         = month or today.month
        self._router        = router
        self._client_id     = client_id
        self._is_admin      = is_admin
        self._advocate_id   = advocate_id
        self._today         = today
        self._tooltip       = None
        self._on_date_click = on_date_click
        self._selected_date = None
        self._build()

    def _build(self):
        for w in self.winfo_children():
            w.destroy()
        nav = tk.Frame(self, bg=COLORS["navbar_bg"])
        nav.pack(fill="x")
        pb = tk.Label(nav, text="  \u25c0  ", font=FONTS["body_bold"],
                       fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"], cursor="hand2")
        pb.pack(side="left", padx=4, pady=8)
        pb.bind("<Button-1>", self._prev_month)
        pb.bind("<Enter>",    lambda e: pb.config(bg=COLORS["navbar_hover"]))
        pb.bind("<Leave>",    lambda e: pb.config(bg=COLORS["navbar_bg"]))
        tk.Label(nav,
                 text=datetime.date(self._year, self._month, 1).strftime("%B  %Y").upper(),
                 font=FONTS["heading_2"], fg=COLORS["navbar_text"],
                 bg=COLORS["navbar_bg"]).pack(side="left", expand=True)
        nb = tk.Label(nav, text="  \u25b6  ", font=FONTS["body_bold"],
                       fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"], cursor="hand2")
        nb.pack(side="right", padx=4, pady=8)
        nb.bind("<Button-1>", self._next_month)
        nb.bind("<Enter>",    lambda e: nb.config(bg=COLORS["navbar_hover"]))
        nb.bind("<Leave>",    lambda e: nb.config(bg=COLORS["navbar_bg"]))
        hdr = tk.Frame(self, bg=COLORS["cal_header_bg"])
        hdr.pack(fill="x")
        for day in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]:
            tk.Label(hdr, text=day, font=FONTS["caption_bold"],
                     fg=COLORS["cal_header_text"], bg=COLORS["cal_header_bg"],
                     width=DIMS["cal_cell_w"] // 8, pady=6).pack(side="left", expand=True, fill="x")
        grid = tk.Frame(self, bg=COLORS["bg_primary"])
        grid.pack(fill="both", expand=True)
        for week in calendar.monthcalendar(self._year, self._month):
            row_f = tk.Frame(grid, bg=COLORS["border_cell"])
            row_f.pack(fill="x", pady=1)
            for day in week:
                if day == 0:
                    tk.Frame(row_f, bg=COLORS["bg_secondary"],
                             width=DIMS["cal_cell_w"], height=DIMS["cal_cell_h"],
                             highlightbackground=COLORS["border_cell"],
                             highlightthickness=1).pack(side="left", expand=True, fill="both")
                else:
                    self._make_cell(row_f, day)

    def _make_cell(self, parent, day):
        date_obj    = datetime.date(self._year, self._month, day)
        is_today    = (date_obj == self._today)
        is_selected = (date_obj == self._selected_date and not is_today)
        is_weekend  = date_obj.weekday() >= 5
        is_sunday   = (date_obj.weekday() == 6)

        if is_today:
            cell_bg, day_col, name_col = (COLORS["cal_today_bg"],
                                          COLORS["cal_today_text"], COLORS["text_muted"])
        elif is_selected:
            cell_bg, day_col, name_col = (COLORS["cal_selected_bg"],
                                          COLORS["cal_selected_text"], COLORS["text_muted"])
        elif is_weekend:
            cell_bg, day_col, name_col = (COLORS["cal_weekend_bg"],
                                          COLORS["text_secondary"], COLORS["text_muted"])
        else:
            cell_bg, day_col, name_col = (COLORS["bg_primary"],
                                          COLORS["text_primary"], COLORS["text_secondary"])

        if is_sunday and not is_today and not is_selected:
            day_col = COLORS["sunday_text"]

        if self._is_admin:
            cases = db.get_cases_for_all_advocates(date_obj) or []
        elif self._client_id:
            cases = db.get_cases_for_client_on_date(self._client_id, date_obj) or []
        else:
            cases = db.get_cases_for_date(date_obj, self._advocate_id) or []

        border_col = COLORS["border_cell"]
        border_th  = 1
        if is_sunday and not is_today and not is_selected:
            border_col = COLORS["sunday_border"]
            border_th  = 2

        cell = tk.Frame(parent, bg=cell_bg,
                         width=DIMS["cal_cell_w"], height=DIMS["cal_cell_h"],
                         highlightbackground=border_col, highlightthickness=border_th,
                         cursor="hand2")
        cell.pack(side="left", expand=True, fill="both")
        cell.pack_propagate(False)

        tk.Label(cell, text=str(day), font=FONTS["body_bold"],
                 fg=day_col, bg=cell_bg, anchor="nw").pack(anchor="nw", padx=6, pady=(4, 0))
        tk.Label(cell, text=date_obj.strftime("%a"), font=FONTS["caption"],
                 fg=name_col, bg=cell_bg, anchor="nw").pack(anchor="nw", padx=6)

        if cases:
            badge_bg = COLORS["navbar_text"] if (is_today or is_selected) else COLORS["navbar_bg"]
            badge_fg = COLORS["navbar_bg"]   if (is_today or is_selected) else COLORS["navbar_text"]
            n        = len(cases)
            MAX_ICONS = 3
            badge_frame = tk.Frame(cell, bg=badge_bg)
            badge_frame.pack(anchor="se", padx=4, pady=4)
            if n <= MAX_ICONS:
                icons_text = ("\u2696 " * n).strip()
                tk.Label(badge_frame, text=icons_text,
                         font=("Georgia", 8, "normal"),
                         fg=badge_fg, bg=badge_bg, padx=3, pady=1).pack()
            else:
                tk.Label(badge_frame, text=f"\u2696  x{n}",
                         font=("Georgia", 8, "bold"),
                         fg=badge_fg, bg=badge_bg, padx=3, pady=1).pack()

        def on_click(e, d=date_obj):
            self._selected_date = d
            self._build()
            if self._on_date_click:
                self._on_date_click(d)

        def on_enter(e, bg=cell_bg, c_list=cases, container=cell):
            if not is_today and not is_selected:
                container.config(bg=COLORS["bg_hover_cell"])
                for ch in container.winfo_children():
                    try:
                        ch.config(bg=COLORS["bg_hover_cell"])
                    except Exception:
                        pass
            if c_list:
                self._show_tooltip(date_obj, c_list, e.x_root, e.y_root)

        def on_leave(e, bg=cell_bg, container=cell):
            if not is_today and not is_selected:
                container.config(bg=bg)
                for ch in container.winfo_children():
                    try:
                        ch.config(bg=bg)
                    except Exception:
                        pass
            self._hide_tooltip()

        all_widgets = [cell] + list(cell.winfo_children())
        for wgt in all_widgets:
            wgt.bind("<Button-1>", on_click)
            wgt.bind("<Enter>",    on_enter)
            wgt.bind("<Leave>",    on_leave)

    def _show_tooltip(self, date_obj, cases, rx, ry):
        self._hide_tooltip()
        tip = tk.Toplevel(self)
        tip.wm_overrideredirect(True)
        tip.wm_geometry(f"+{rx+10}+{ry+10}")
        tip.configure(bg=COLORS["navbar_bg"],
                      highlightbackground=COLORS["navbar_border"], highlightthickness=1)
        self._tooltip = tip
        tk.Label(tip, text=date_obj.strftime("  %d %B — Cases  "),
                 font=FONTS["caption_bold"], fg=COLORS["navbar_text"],
                 bg=COLORS["navbar_bg"], pady=6).pack(fill="x")
        for case in cases:
            cn        = case.get("case_no", "—")
            case_name = case.get("case_name", case.get("name", "—"))
            extra     = f"  [{case.get('advocate_name', '')}]" if self._is_admin and case.get("advocate_name") else ""
            row = tk.Label(tip,
                           text=f"  {cn}\n  {case_name[:35]}{extra}",
                           font=FONTS["caption"], fg=COLORS["navbar_text"],
                           bg=COLORS["navbar_bg"], justify="left",
                           cursor="hand2", pady=4, padx=8, anchor="w")
            row.pack(fill="x")
            row.bind("<Enter>",    lambda e, r=row: r.config(bg=COLORS["navbar_active"]))
            row.bind("<Leave>",    lambda e, r=row: r.config(bg=COLORS["navbar_bg"]))
            row.bind("<Button-1>", lambda e, c=cn: (self._hide_tooltip(), self._router("case_info", c)))

    def _hide_tooltip(self):
        if self._tooltip:
            try:
                self._tooltip.destroy()
            except Exception:
                pass
            self._tooltip = None

    def _prev_month(self, *_):
        if self._month == 1:
            self._month, self._year = 12, self._year - 1
        else:
            self._month -= 1
        self._build()

    def _next_month(self, *_):
        if self._month == 12:
            self._month, self._year = 1, self._year + 1
        else:
            self._month += 1
        self._build()


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 10 — ADVOCATE DASHBOARD  
# ══════════════════════════════════════════════════════════════════════════════

class AdvocateDashboard(ctk.CTk):
    def __init__(self, profile):
        super().__init__()
        self._profile           = profile
        self._sidebar           = None
        self._content_area      = None
        # v5: BNS state
        self._bns_section       = None
        self._bns_section_id    = None
        self._bns_refresh_job   = None
        self._bns_panel_frame   = None
        self._bns_panel_dismissed = False  # v6: session flag
        self._current_route = None  # v7: zoom stay-on-page
        self.title("ADVOCACY — Advocate Dashboard")
        self.geometry("1300x820")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_primary"])
        self._build_navbar()
        self._build_content_area()
        self._show_home()

    # ── Back bar helper ───────────────────────────────────────────────────────
    def _back_bar(self, parent, title):
        bar = tk.Frame(parent, bg=COLORS["bg_secondary"], height=40)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        back_btn = tk.Label(
            bar, text="  \u2190  Back to Home  ",
            font=FONTS["body_bold"], fg=COLORS["text_primary"],
            bg=COLORS["bg_secondary"], cursor="hand2", padx=8,
        )
        back_btn.pack(side="left", pady=8)
        back_btn.bind("<Enter>",    lambda e: back_btn.config(bg=COLORS["border"]))
        back_btn.bind("<Leave>",    lambda e: back_btn.config(bg=COLORS["bg_secondary"]))
        back_btn.bind("<Button-1>", lambda e: self._show_home())
        tk.Frame(bar, bg=COLORS["border_strong"], width=1).pack(side="left", fill="y", pady=6)
        tk.Label(bar, text=f"  {title}", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=12, pady=8)

    # ── View management ───────────────────────────────────────────────────────
    def _show_home(self):
        self._current_route = None  # v7
        for w in self._content_area.winfo_children():
            w.destroy()
        self._build_home_content(self._content_area)

    def _zoom_refresh(self):
        """v7: Full teardown + rebuild so ALL widgets (navbar, subbar, content) get new fonts."""
        route = self._current_route  # save before destroy
        for w in self.winfo_children():
            w.destroy()
        self._sidebar = None
        self._bns_panel_frame = None
        self._bns_refresh_job = None
        self._build_navbar()
        self._build_content_area()
        if route:
            self._current_route = route
            self._route(*route)
        else:
            self._show_home()

    def _build_content_area(self):
        self._content_area = tk.Frame(self, bg=COLORS["bg_primary"])
        self._content_area.pack(fill="both", expand=True)

    def _build_home_content(self, parent):
        """v5: Two-row layout — row 0: Calendar + Sidebar  |  row 1: BNS panel."""
        aid = self._profile.get("advocate_id")

        # Cancel any existing auto-refresh job
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
            self._bns_refresh_job = None

        body = tk.Frame(parent, bg=COLORS["bg_primary"])
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=6)
        body.grid_columnconfigure(1, weight=0)
        body.grid_columnconfigure(2, weight=4)
        body.grid_rowconfigure(0, weight=1)   # top row: cal + sidebar
        body.grid_rowconfigure(1, weight=0)   # bottom row: BNS panel (fixed height)

        # ── Row 0: Calendar ─────────────────────────────────────────────────────────────
        cal_host = tk.Frame(body, bg=COLORS["bg_primary"])
        cal_host.grid(row=0, column=0, sticky="nsew", padx=(12, 4), pady=12)
        cal = MonthCalendar(
            cal_host, self._route, advocate_id=aid,
            on_date_click=lambda d: self._sidebar.show_date(d) if self._sidebar else None,
        )
        cal.pack(fill="both", expand=True)

        tk.Frame(body, bg=COLORS["border"], width=1
                 ).grid(row=0, column=1, sticky="ns", pady=12)

        self._sidebar = TodaySidebar(body, self._route, advocate_id=aid)
        self._sidebar.grid(row=0, column=2, sticky="nsew", padx=(4, 12), pady=12)

        # v6: Row 1 BNS Panel (dismissable for session)
        if not self._bns_panel_dismissed:
            bns_host = tk.Frame(body, bg=BNS_COLORS["panel_bg"])
            bns_host.grid(row=1, column=0, columnspan=3, sticky="ew")
            self._bns_panel_frame = bns_host
            self._build_bns_panel(bns_host)
            self._start_bns_refresh()

    # ────────────────────────────────────────────────────────────────────────────
    # BNS Panel helpers
    # ────────────────────────────────────────────────────────────────────────────
    def _dismiss_bns_panel(self):
        """v6: Dismiss BNS panel for this login session."""
        self._bns_panel_dismissed = True
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
            self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._bns_panel_frame.grid_remove()

    def _build_bns_panel(self, parent):
        """Build (or rebuild) the BNS knowledge panel inside *parent*."""
        # Destroy previous content
        for w in parent.winfo_children():
            w.destroy()
        self._bns_panel_frame = parent

        # Fetch a section if we don't have one yet (first draw)
        if self._bns_section is None:
            self._bns_section = db.get_random_bns_section()
        sec = self._bns_section

        if not sec:
            # Table not yet populated — show placeholder row
            tk.Label(
                parent,
                text="  ⚖⚖  Bhartiya Nyaya Samhita  —  "
                     "Add BNS section data to the bns_sections table to enable this panel.  ⚖⚖",
                font=BNS_FONT_BODY, fg=BNS_COLORS["title_fg"],
                bg=BNS_COLORS["panel_bg"], pady=10,
            ).pack(fill="x", padx=16)
            return

        self._bns_section_id = sec.get("section_id")

        # ── Header strip ───────────────────────────────────────────────────────
        hdr = tk.Frame(parent, bg=BNS_COLORS["header_bg"])
        hdr.pack(fill="x")

        tk.Label(
            hdr, text="⚖  Bhartiya Nyaya Samhita  ⚖",
            font=BNS_FONT_TITLE, fg=BNS_COLORS["title_fg"],
            bg=BNS_COLORS["header_bg"], padx=16, pady=6,
        ).pack(side="left")

        # Auto-refresh timer label (shows countdown)
        self._bns_timer_label = tk.Label(
            hdr, text="", font=BNS_FONT_BADGE,
            fg=BNS_COLORS["timer_fg"], bg=BNS_COLORS["header_bg"], padx=8,
        )
        self._bns_timer_label.pack(side="right", padx=(0, 8))

        # “Next Section” button
        next_btn = tk.Label(
            hdr, text="  Next Section ⯈  ",
            font=BNS_FONT_BUTTON, fg=BNS_COLORS["btn_fg"],
            bg=BNS_COLORS["btn_bg"], cursor="hand2", padx=8, pady=4,
        )
        next_btn.pack(side="right", padx=(0, 4), pady=4)
        next_btn.bind("<Button-1>", lambda e: self._rotate_bns_section())
        next_btn.bind("<Enter>", lambda e: next_btn.config(bg=BNS_COLORS["btn_hover"]))
        next_btn.bind("<Leave>", lambda e: next_btn.config(bg=BNS_COLORS["btn_bg"]))

        # v6: Close (X) button
        close_btn = tk.Label(
            hdr, text="  X  ", font=BNS_FONT_BADGE,
            fg=BNS_COLORS["title_fg"], bg=BNS_COLORS["btn_bg"],
            cursor="hand2", padx=6, pady=4,
        )
        close_btn.pack(side="right", padx=(0, 2), pady=4)
        close_btn.bind("<Button-1>", lambda e: self._dismiss_bns_panel())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#333333"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=BNS_COLORS["btn_bg"]))

        # Bhartiya Nyaya Samhita label
        tk.Label(
            hdr, text="Bhartiya Nyaya Samhita, 2023",
            font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
            bg=BNS_COLORS["header_bg"], padx=8,
        ).pack(side="right")

        # Thin divider below header
        tk.Frame(parent, bg=BNS_COLORS["divider"], height=1).pack(fill="x")

        # ── Content row ──────────────────────────────────────────────────────────
        content = tk.Frame(parent, bg=BNS_COLORS["panel_bg"])
        content.pack(fill="x", padx=16, pady=(6, 8))

        # Left column: section number badge + IPC equivalent + category
        left_col = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        left_col.pack(side="left", anchor="n", padx=(0, 20))

        tk.Label(
            left_col,
            text=f"Section\n{sec.get('bns_number', '---')}",
            font=BNS_FONT_SECTION_NO, fg=BNS_COLORS["section_no_fg"],
            bg=BNS_COLORS["panel_bg"], justify="center",
        ).pack()

        ipc = sec.get("ipc_equivalent")
        if ipc:
            tk.Label(
                left_col, text=f"IPC: {ipc}",
                font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
                bg=BNS_COLORS["panel_bg"],
            ).pack(pady=(4, 0))

        cat_badge = tk.Label(
            left_col, text=f" {sec.get('category', '')} ",
            font=BNS_FONT_BADGE, fg=BNS_COLORS["cat_fg"],
            bg=BNS_COLORS["cat_bg"], padx=4, pady=2,
        )
        cat_badge.pack(pady=(6, 0))

        # Right column: section title + summary + punishment
        right_col = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        right_col.pack(side="left", fill="x", expand=True, anchor="n")

        tk.Label(
            right_col,
            text=sec.get("section_title", ""),
            font=BNS_FONT_SECTION_TITLE, fg=BNS_COLORS["section_title_fg"],
            bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
        ).pack(anchor="w")

        summary = sec.get("summary", "")
        if summary:
            # Wrap to ~120 chars per line for display
            tk.Label(
                right_col,
                text=summary,
                font=BNS_FONT_BODY, fg=BNS_COLORS["body_fg"],
                bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                wraplength=1050,
            ).pack(anchor="w", pady=(4, 0))

        punishment = sec.get("punishment_summary")
        if punishment:
            tk.Label(
                right_col,
                text=f"⚖ Punishment:  {punishment}",
                font=BNS_FONT_BADGE, fg=BNS_COLORS["punishment_fg"],
                bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                wraplength=1050,
            ).pack(anchor="w", pady=(4, 0))

    def _rotate_bns_section(self):
        """Fetch the next BNS section and refresh the panel (manual or auto)."""
        # Cancel any pending auto-refresh first
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
            self._bns_refresh_job = None

        # Fetch the next section excluding the current one
        if self._bns_section_id is not None:
            self._bns_section = db.get_random_bns_section_excluding(self._bns_section_id)
        else:
            self._bns_section = db.get_random_bns_section()

        # Rebuild the panel in-place if the frame still exists
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._build_bns_panel(self._bns_panel_frame)

        # Restart the auto-refresh timer
        self._start_bns_refresh()

    def _start_bns_refresh(self):
        """Schedule the next auto-refresh in 120 seconds."""
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
        self._bns_refresh_job = self.after(120_000, self._auto_refresh_bns)

    def _auto_refresh_bns(self):
        """Called by the 120-second after() timer; rotates to the next section."""
        self._bns_refresh_job = None
        # Only rotate if still on home screen (BNS panel frame still exists)
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._rotate_bns_section()


    # ── Router ────────────────────────────────────────────────────────────────
    def _route(self, key, case_no=None):
        self._current_route = (key, case_no)  # v7: zoom stay-on-page
        # v6: assistant management routes
        if key == "manage_assistant":
            aid_v6 = self._profile.get("advocate_id", 1)
            for w in self._content_area.winfo_children(): w.destroy()
            build_manage_assistant_view(self._content_area, self._route, self, aid_v6)
            return
        if key == "create_assistant":
            aid_v6 = self._profile.get("advocate_id", 1)
            for w in self._content_area.winfo_children(): w.destroy()
            build_create_delete_assistant_view(self._content_area, self._route, self, aid_v6)
            return
        aid = self._profile.get("advocate_id", 1)

        def show(builder_fn):
            for w in self._content_area.winfo_children():
                w.destroy()
            builder_fn(self._content_area)

        actions = {
            "case_info":   lambda: show(lambda p: build_case_info_view(p, self._route, self, case_no, advocate_id=aid)),
            "new_case":    lambda: show(lambda p: build_new_case_view(p, self._route, self, aid)),
            "case_update": lambda: show(lambda p: build_case_update_view(p, self._route, self, aid)),
            "ongoing":     lambda: show(lambda p: build_cases_ongoing_view(p, self._route, self, advocate_id=aid)),
            "fees":        lambda: show(lambda p: build_fees_tracking_view(p, self._route, self, aid)),
            "expenses":    lambda: show(lambda p: build_expenses_view(p, self._route, self, aid)),
            "incoming":    lambda: show(lambda p: build_money_incoming_view(p, self._route, self, aid)),
            "settings":    lambda: show(lambda p: build_account_settings_view(p, self._profile, self)),
            "new_client":  lambda: show(lambda p: build_create_client_view(p, self._route, self, aid)),
        }
        if key in actions:
            actions[key]()

    # ── Navbar ────────────────────────────────────────────────────────────────
    def _build_navbar(self):
        bar = tk.Frame(self, bg=COLORS["navbar_bg"], height=DIMS["navbar_height"])
        bar.pack(fill="x")
        bar.pack_propagate(False)

        brand = tk.Frame(bar, bg=COLORS["navbar_bg"])
        brand.pack(side="left", padx=(14, 6))
        tk.Label(brand, text="\u2696", font=FONTS["navbar_brand_icon"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(side="left", padx=(0, 8))
        txt_stack = tk.Frame(brand, bg=COLORS["navbar_bg"])
        txt_stack.pack(side="left")
        tk.Label(txt_stack, text="ADVOCACY", font=FONTS["navbar_brand"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Label(txt_stack, text="Legal Practice Management Suite",
                 font=FONTS["navbar_brand_sub"], fg=COLORS["text_muted"],
                 bg=COLORS["navbar_bg"]).pack(anchor="w")

        tk.Frame(bar, bg=COLORS["navbar_border"], width=1, height=38
                 ).pack(side="left", padx=14, pady=14)

        NavDropdown(bar, "CASE MANAGEMENT", [
            ("1.1  Case Info",     "case_info"),
            ("1.2  New Case",      "new_case"),
            ("1.3  Case Updation", "case_update"),
        ], self._route)
        NavDropdown(bar, "CLIENTS", [
            ("2.1  Cases Ongoing",    "ongoing"),
            ("2.2  Fees Tracking",    "fees"),
            ("2.3  Create New Client","new_client"),
        ], self._route)
        NavDropdown(bar, "EXPENSES / GAIN", [
            ("3.1  Expenses",       "expenses"),
            ("3.2  Money Incoming", "incoming"),
        ], self._route)
        # v6: Assistant management dropdown
        NavDropdown(bar, "ASSISTANT", [
            ("Manage Assistants",         "manage_assistant"),
            ("Create / Delete Assistant", "create_assistant"),
        ], self._route)

        pf = tk.Frame(bar, bg=COLORS["navbar_bg"], cursor="hand2")
        pf.pack(side="right", padx=14)
        name = self._profile.get("name", "Advocate")
        initials = "".join(p[0] for p in name.split()[:2]).upper() or "AV"
        av = tk.Label(pf, text=f" {initials} ", font=FONTS["caption_bold"],
                      fg=COLORS["navbar_bg"], bg=COLORS["navbar_text"], padx=2, pady=2)
        av.pack(side="left", padx=(0, 6))
        nm = tk.Label(pf, text=name,
                      font=FONTS["navbar"], fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"])
        nm.pack(side="left")
        for w in [pf, av, nm]:
            w.bind("<Button-1>", lambda e: self._route("settings"))
            w.bind("<Enter>",    lambda e: pf.config(bg=COLORS["navbar_hover"]))
            w.bind("<Leave>",    lambda e: pf.config(bg=COLORS["navbar_bg"]))

        sub = tk.Frame(self, bg=COLORS["bg_secondary"], height=26)
        sub.pack(fill="x")
        sub.pack_propagate(False)
        tk.Label(sub,
                 text=f"  Advocate  \u00b7  {self._profile.get('bar_no', '')}  "
                      f"\u00b7  {self._profile.get('court', '')}",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_secondary"]).pack(side="left", padx=10)
        tk.Label(sub, text=datetime.date.today().strftime("  %d %B %Y  "),
                 font=FONTS["caption_bold"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_secondary"]).pack(side="right", padx=10)
        _build_zoom_controls(sub, self._zoom_refresh).pack(side="right", padx=6)  # v7 zoom


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 11 — ADMIN DASHBOARD  
# ══════════════════════════════════════════════════════════════════════════════

class AdminDashboard(ctk.CTk):
    def __init__(self, profile):
        super().__init__()
        self._profile           = profile
        self._sidebar           = None
        self._content_area      = None
        self._view_mode         = "advocate"   
        # v5: BNS state
        self._bns_section       = None
        self._bns_section_id    = None
        self._bns_refresh_job   = None
        self._bns_panel_frame   = None
        self._bns_panel_dismissed = False  # v6: session flag
        self._current_route = None  # v7: zoom stay-on-page
        self.title("ADVOCACY — Admin Dashboard")
        self.geometry("1300x820")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_primary"])
        self._build_navbar()
        self._build_content_area()
        self._show_home()

    # ── Back bar helper ───────────────────────────────────────────────────────
    def _back_bar(self, parent, title):
        bar = tk.Frame(parent, bg=COLORS["bg_secondary"], height=40)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        back_btn = tk.Label(
            bar, text="  \u2190  Back to Home  ",
            font=FONTS["body_bold"], fg=COLORS["text_primary"],
            bg=COLORS["bg_secondary"], cursor="hand2", padx=8,
        )
        back_btn.pack(side="left", pady=8)
        back_btn.bind("<Enter>",    lambda e: back_btn.config(bg=COLORS["border"]))
        back_btn.bind("<Leave>",    lambda e: back_btn.config(bg=COLORS["bg_secondary"]))
        back_btn.bind("<Button-1>", lambda e: self._show_home())
        tk.Frame(bar, bg=COLORS["border_strong"], width=1).pack(side="left", fill="y", pady=6)
        tk.Label(bar, text=f"  {title}", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=12, pady=8)

    # ── View management ───────────────────────────────────────────────────────
    def _show_home(self):
        self._current_route = None  # v7
        for w in self._content_area.winfo_children():
            w.destroy()
        self._build_home_content(self._content_area)

    def _zoom_refresh(self):
        """v7: Full teardown + rebuild so ALL widgets (navbar, subbar, content) get new fonts."""
        route = self._current_route  # save before destroy
        for w in self.winfo_children():
            w.destroy()
        self._sidebar = None
        self._bns_panel_frame = None
        self._bns_refresh_job = None
        self._navbar_bar = None
        self._subbar_frame = None
        self._build_navbar()
        self._build_content_area()
        if route:
            self._current_route = route
            self._route(*route)
        else:
            self._show_home()

    def _build_content_area(self):
        self._content_area = tk.Frame(self, bg=COLORS["bg_primary"])
        self._content_area.pack(fill="both", expand=True)

    def _build_home_content(self, parent):
        """v5: Two-row layout — row 0: Calendar + Sidebar  |  row 1: BNS panel."""
        # Cancel any existing auto-refresh job
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
            self._bns_refresh_job = None

        body = tk.Frame(parent, bg=COLORS["bg_primary"])
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=6)
        body.grid_columnconfigure(1, weight=0)
        body.grid_columnconfigure(2, weight=4)
        body.grid_rowconfigure(0, weight=1)   # top row: cal + sidebar
        body.grid_rowconfigure(1, weight=0)   # bottom row: BNS panel (fixed height)

        # ── Row 0: Calendar ────────────────────────────────────────────────────────────
        cal_host = tk.Frame(body, bg=COLORS["bg_primary"])
        cal_host.grid(row=0, column=0, sticky="nsew", padx=(12, 4), pady=12)
        cal = MonthCalendar(
            cal_host, self._route, is_admin=True,
            on_date_click=lambda d: self._sidebar.show_date(d) if self._sidebar else None,
        )
        cal.pack(fill="both", expand=True)

        tk.Frame(body, bg=COLORS["border"], width=1
                 ).grid(row=0, column=1, sticky="ns", pady=12)

        self._sidebar = TodaySidebar(body, self._route, is_admin=True)
        self._sidebar.grid(row=0, column=2, sticky="nsew", padx=(4, 12), pady=12)

        # v6: Row 1 BNS Panel (dismissable for session)
        if not self._bns_panel_dismissed:
            bns_host = tk.Frame(body, bg=BNS_COLORS["panel_bg"])
            bns_host.grid(row=1, column=0, columnspan=3, sticky="ew")
            self._bns_panel_frame = bns_host
            self._build_bns_panel(bns_host)
            self._start_bns_refresh()

    # ────────────────────────────────────────────────────────────────────────────
    # BNS Panel helpers (v5 + v6 close button)
    # ────────────────────────────────────────────────────────────────────────────
    def _dismiss_bns_panel(self):
        """v6: Dismiss BNS panel for this login session."""
        self._bns_panel_dismissed = True
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
            self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._bns_panel_frame.grid_remove()

    def _build_bns_panel(self, parent):
        """Build (or rebuild) the BNS knowledge panel inside *parent*."""
        for w in parent.winfo_children():
            w.destroy()
        self._bns_panel_frame = parent

        if self._bns_section is None:
            self._bns_section = db.get_random_bns_section()
        sec = self._bns_section

        if not sec:
            tk.Label(
                parent,
                text="  ⚖⚖  Bhartiya Nyaya Samhita  —  "
                     "Add BNS section data to the bns_sections table to enable this panel.  ⚖⚖",
                font=BNS_FONT_BODY, fg=BNS_COLORS["title_fg"],
                bg=BNS_COLORS["panel_bg"], pady=10,
            ).pack(fill="x", padx=16)
            return

        self._bns_section_id = sec.get("section_id")

        hdr = tk.Frame(parent, bg=BNS_COLORS["header_bg"])
        hdr.pack(fill="x")

        tk.Label(
            hdr, text="⚖  Bhartiya Nyaya Samhita  ⚖",
            font=BNS_FONT_TITLE, fg=BNS_COLORS["title_fg"],
            bg=BNS_COLORS["header_bg"], padx=16, pady=6,
        ).pack(side="left")

        self._bns_timer_label = tk.Label(
            hdr, text="", font=BNS_FONT_BADGE,
            fg=BNS_COLORS["timer_fg"], bg=BNS_COLORS["header_bg"], padx=8,
        )
        self._bns_timer_label.pack(side="right", padx=(0, 8))

        next_btn = tk.Label(
            hdr, text="  Next Section ⯈  ",
            font=BNS_FONT_BUTTON, fg=BNS_COLORS["btn_fg"],
            bg=BNS_COLORS["btn_bg"], cursor="hand2", padx=8, pady=4,
        )
        next_btn.pack(side="right", padx=(0, 4), pady=4)
        next_btn.bind("<Button-1>", lambda e: self._rotate_bns_section())
        next_btn.bind("<Enter>", lambda e: next_btn.config(bg=BNS_COLORS["btn_hover"]))
        next_btn.bind("<Leave>", lambda e: next_btn.config(bg=BNS_COLORS["btn_bg"]))

        # v7: Close (X) button — dismisses BNS panel for this session
        close_btn = tk.Label(
            hdr, text="  ✕  ", font=BNS_FONT_BADGE,
            fg=BNS_COLORS["title_fg"], bg=BNS_COLORS["btn_bg"],
            cursor="hand2", padx=6, pady=4,
        )
        close_btn.pack(side="right", padx=(0, 2), pady=4)
        close_btn.bind("<Button-1>", lambda e: self._dismiss_bns_panel())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#333333"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=BNS_COLORS["btn_bg"]))

        tk.Label(
            hdr, text="Bhartiya Nyaya Samhita, 2023",
            font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
            bg=BNS_COLORS["header_bg"], padx=8,
        ).pack(side="right")

        tk.Frame(parent, bg=BNS_COLORS["divider"], height=1).pack(fill="x")

        content = tk.Frame(parent, bg=BNS_COLORS["panel_bg"])
        content.pack(fill="x", padx=16, pady=(6, 8))

        left_col = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        left_col.pack(side="left", anchor="n", padx=(0, 20))

        tk.Label(
            left_col,
            text=f"Section\n{sec.get('bns_number', '---')}",
            font=BNS_FONT_SECTION_NO, fg=BNS_COLORS["section_no_fg"],
            bg=BNS_COLORS["panel_bg"], justify="center",
        ).pack()

        ipc = sec.get("ipc_equivalent")
        if ipc:
            tk.Label(
                left_col, text=f"IPC: {ipc}",
                font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
                bg=BNS_COLORS["panel_bg"],
            ).pack(pady=(4, 0))

        cat_badge = tk.Label(
            left_col, text=f" {sec.get('category', '')} ",
            font=BNS_FONT_BADGE, fg=BNS_COLORS["cat_fg"],
            bg=BNS_COLORS["cat_bg"], padx=4, pady=2,
        )
        cat_badge.pack(pady=(6, 0))

        right_col = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        right_col.pack(side="left", fill="x", expand=True, anchor="n")

        tk.Label(
            right_col,
            text=sec.get("section_title", ""),
            font=BNS_FONT_SECTION_TITLE, fg=BNS_COLORS["section_title_fg"],
            bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
        ).pack(anchor="w")

        summary = sec.get("summary", "")
        if summary:
            tk.Label(
                right_col,
                text=summary,
                font=BNS_FONT_BODY, fg=BNS_COLORS["body_fg"],
                bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                wraplength=1050,
            ).pack(anchor="w", pady=(4, 0))

        punishment = sec.get("punishment_summary")
        if punishment:
            tk.Label(
                right_col,
                text=f"⚖ Punishment:  {punishment}",
                font=BNS_FONT_BADGE, fg=BNS_COLORS["punishment_fg"],
                bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                wraplength=1050,
            ).pack(anchor="w", pady=(4, 0))

    def _rotate_bns_section(self):
        """Fetch the next BNS section and refresh the panel."""
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
            self._bns_refresh_job = None
        if self._bns_section_id is not None:
            self._bns_section = db.get_random_bns_section_excluding(self._bns_section_id)
        else:
            self._bns_section = db.get_random_bns_section()
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._build_bns_panel(self._bns_panel_frame)
        self._start_bns_refresh()

    def _start_bns_refresh(self):
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
        self._bns_refresh_job = self.after(120_000, self._auto_refresh_bns)

    def _auto_refresh_bns(self):
        self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._rotate_bns_section()


    # ── FIX 2: Toggle view mode ───────────────────────────────────────────────
    def _toggle_view_mode(self, mode):
        self._view_mode = mode
        self._rebuild_subbar()
        self._rebuild_navbar_menus()
        self._show_home()

    def _rebuild_subbar(self):
        """Rebuilds the subbar frame with updated toggle state."""
        # Destroy existing subbar by stored reference (avoids fragile height-search)
        if hasattr(self, '_subbar_frame') and self._subbar_frame and self._subbar_frame.winfo_exists():
            self._subbar_frame.destroy()
            self._subbar_frame = None
        self._build_subbar()

    # ── Admin Router  ─────────────────────────────────────────────────
    def _route(self, key, case_no=None):
        self._current_route = (key, case_no)  # v7: zoom stay-on-page
        # v6: Admin assistants view
        if key == "admin_assistants":
            for w in self._content_area.winfo_children(): w.destroy()
            build_admin_assistants_view(self._content_area, self._route, self)
            return
        # v7: Profile viewing — works in both modes
        if key == "profile":
            self._show_profile_selector()
            return
        if self._view_mode == "advocate":
            direct_routes = {
                "create_advocate": lambda: self._show_feature(
                    lambda p: build_create_advocate_view(p, self._route, self)
                ),
            }
            if key in direct_routes:
                direct_routes[key]()
                return
            self._show_advocate_selector(key, case_no)
        else:
            # client view mode
            direct_routes = {
                "new_client": lambda: self._show_feature(
                    lambda p: build_create_client_view(p, self._route, self)
                ),
            }
            if key in direct_routes:
                direct_routes[key]()
                return
            self._show_client_selector(key)

    # ── Profile Selector (v7) ─────────────────────────────────────────────────
    def _show_profile_selector(self):
        """Show a selector so admin can view/edit any advocate, admin, or client profile."""
        for w in self._content_area.winfo_children():
            w.destroy()
        self._back_bar(self._content_area, "Profile — Select Account")

        scroll = ctk.CTkScrollableFrame(
            self._content_area, fg_color=COLORS["bg_primary"],
            scrollbar_button_color=COLORS["scrollbar"],
            scrollbar_button_hover_color=COLORS["scrollbar_hover"],
        )
        scroll.pack(fill="both", expand=True)

        tk.Label(scroll, text="View / Edit Profile", font=FONTS["heading_1"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(12, 4))
        tk.Label(scroll, text="Select an account to view and edit its profile and password.",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 16))

        # ── Advocate / Admin profiles ──────────────────────────────────────
        adv_section = tk.Frame(scroll, bg=COLORS["bg_secondary"])
        adv_section.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(adv_section, text="Advocates & Admin", font=FONTS["body_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(anchor="w", padx=12, pady=(8, 4))

        # Include admin itself (is_admin=1 row) in the list
        all_advocates = db.get_all_advocates() or []  # excludes admin
        admin_row = db.get_advocate_profile(self._profile.get("advocate_id")) or {}
        # Build list: admin first, then advocates
        admin_id = self._profile.get("advocate_id")
        entries = [(admin_id, f"[ADMIN] {admin_row.get('full_name', 'Administrator')}", True)]
        for a in all_advocates:
            entries.append((a["advocate_id"], f"{a['advocate_id']}  —  {a['full_name']} ({a.get('username','')})", False))

        for aid, label, is_adm in entries:
            row = tk.Frame(adv_section, bg=COLORS["bg_secondary"], cursor="hand2")
            row.pack(fill="x", padx=8, pady=2)
            icon = "🛡" if is_adm else "⚖"
            lbl = tk.Label(row, text=f"  {icon}  {label}",
                           font=FONTS["body"], fg=COLORS["text_primary"],
                           bg=COLORS["bg_secondary"], anchor="w", padx=6, pady=6)
            lbl.pack(fill="x")
            def open_adv_profile(aid=aid, is_adm=is_adm, row=row):
                profile_data = db.get_advocate_profile(aid) or {}
                profile_dict = {
                    "name":        profile_data.get("full_name", ""),
                    "bar_no":      profile_data.get("bar_number", ""),
                    "court":       profile_data.get("primary_court", ""),
                    "chambers":    profile_data.get("chambers", ""),
                    "phone":       profile_data.get("phone", ""),
                    "email":       profile_data.get("email", ""),
                    "advocate_id": aid,
                    "is_admin":    is_adm,
                }
                for w in self._content_area.winfo_children(): w.destroy()
                if is_adm:
                    build_admin_profile_view(self._content_area, profile_dict, self)
                else:
                    build_account_settings_view(self._content_area, profile_dict, self)
            for w in [row, lbl]:
                w.bind("<Button-1>", lambda e, fn=open_adv_profile: fn())
                w.bind("<Enter>", lambda e, r=row: r.config(bg=COLORS["border"]))
                w.bind("<Leave>", lambda e, r=row: r.config(bg=COLORS["bg_secondary"]))

        # ── Assistant profiles ────────────────────────────────────────────────
        _divider(scroll)
        asst_section = tk.Frame(scroll, bg=COLORS["bg_secondary"])
        asst_section.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(asst_section, text="Assistants", font=FONTS["body_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(anchor="w", padx=12, pady=(8, 4))
        all_assistants = db.get_all_assistants_admin() or []
        if not all_assistants:
            tk.Label(asst_section, text="No assistants found.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_secondary"]).pack(anchor="w", padx=12, pady=6)
        for asst in all_assistants:
            asst_id  = asst.get("assistant_id")
            asst_name = asst.get("full_name", "")
            adv_name = asst.get("advocate_name", "")
            a_row = tk.Frame(asst_section, bg=COLORS["bg_secondary"], cursor="hand2")
            a_row.pack(fill="x", padx=8, pady=2)
            a_lbl = tk.Label(a_row,
                             text=f"  \U0001f464  {asst_name}  \u2014  of {adv_name}",
                             font=FONTS["body"], fg=COLORS["text_primary"],
                             bg=COLORS["bg_secondary"], anchor="w", padx=6, pady=6)
            a_lbl.pack(fill="x")
            def open_asst_profile(asst=asst, row=a_row):
                for w in self._content_area.winfo_children(): w.destroy()
                build_assistant_profile_view(self._content_area, asst, self)
            for w in [a_row, a_lbl]:
                w.bind("<Button-1>", lambda e, fn=open_asst_profile: fn())
                w.bind("<Enter>", lambda e, r=a_row: r.config(bg=COLORS["border"]))
                w.bind("<Leave>", lambda e, r=a_row: r.config(bg=COLORS["bg_secondary"]))

        # ── Client profiles ────────────────────────────────────────────────
        _divider(scroll)
        cli_section = tk.Frame(scroll, bg=COLORS["bg_secondary"])
        cli_section.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(cli_section, text="Clients", font=FONTS["body_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]).pack(anchor="w", padx=12, pady=(8, 4))

        clients = db.get_all_clients() or []
        if not clients:
            tk.Label(cli_section, text="No clients found.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_secondary"]).pack(anchor="w", padx=12, pady=6)
        for cli in clients:
            cid  = cli.get("client_id", "")
            cname = cli.get("full_name", "")
            row = tk.Frame(cli_section, bg=COLORS["bg_secondary"], cursor="hand2")
            row.pack(fill="x", padx=8, pady=2)
            lbl = tk.Label(row, text=f"  👤  {cid}  —  {cname}",
                           font=FONTS["body"], fg=COLORS["text_primary"],
                           bg=COLORS["bg_secondary"], anchor="w", padx=6, pady=6)
            lbl.pack(fill="x")
            def open_cli_profile(cli=cli, row=row):
                for w in self._content_area.winfo_children(): w.destroy()
                build_client_settings_view(self._content_area, cli, self)
            for w in [row, lbl]:
                w.bind("<Button-1>", lambda e, fn=open_cli_profile: fn())
                w.bind("<Enter>", lambda e, r=row: r.config(bg=COLORS["border"]))
                w.bind("<Leave>", lambda e, r=row: r.config(bg=COLORS["bg_secondary"]))


    def _show_feature(self, builder_fn):
        for w in self._content_area.winfo_children():
            w.destroy()
        builder_fn(self._content_area)

    # ── Advocate Selector ─────────────────────────────────────────────────────
    def _show_advocate_selector(self, route_key, case_no=None):
        for w in self._content_area.winfo_children():
            w.destroy()
        self._back_bar(self._content_area,
                       f"Select Advocate — {route_key.replace('_', ' ').title()}")

        advocates   = db.get_all_advocates()   # FIX 2: excludes admin
        adv_options = [f"{a['advocate_id']}  —  {a['full_name']}  ({a['username']})"
                       for a in advocates]
        adv_ids     = [a["advocate_id"] for a in advocates]

        sel_frame = tk.Frame(self._content_area, bg=COLORS["bg_primary"])
        sel_frame.pack(pady=40)

        tk.Label(sel_frame, text="Select the Advocate to act as:",
                 font=FONTS["heading_2"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 10))

        chosen_var = tk.StringVar(value=adv_options[0] if adv_options else "")
        ctk.CTkOptionMenu(sel_frame, values=adv_options if adv_options else ["(no advocates)"],
                          variable=chosen_var,
                          fg_color=COLORS["accent"], button_color=COLORS["navbar_hover"],
                          button_hover_color=COLORS["accent_hover"],
                          text_color=COLORS["text_on_dark"],
                          dropdown_fg_color=COLORS["bg_primary"],
                          dropdown_text_color=COLORS["text_primary"],
                          width=440).pack(padx=20, pady=6)

        info_lbl = tk.Label(sel_frame, text="", font=FONTS["caption"],
                            fg=COLORS["text_muted"], bg=COLORS["bg_primary"])
        info_lbl.pack(anchor="w", padx=20, pady=(4, 0))

        def on_change(*_):
            if not adv_options or chosen_var.get() not in adv_options:
                return
            idx = adv_options.index(chosen_var.get())
            a   = advocates[idx]
            info_lbl.config(text=f"Court: {a.get('primary_court', '—')}  |  Bar: {a.get('bar_number', '—')}")

        chosen_var.trace_add("write", lambda *_: on_change())
        on_change()

        def confirm():
            if not adv_options or chosen_var.get() not in adv_options:
                return
            idx = adv_options.index(chosen_var.get())
            selected_advocate_id = adv_ids[idx]
            adv_profile = db.get_advocate_profile(selected_advocate_id) or {}
            profile_for_feature = {
                "name":        adv_profile.get("full_name", ""),
                "bar_no":      adv_profile.get("bar_number", ""),
                "court":       adv_profile.get("primary_court", ""),
                "chambers":    adv_profile.get("chambers", ""),
                "phone":       adv_profile.get("phone", ""),
                "email":       adv_profile.get("email", ""),
                "advocate_id": selected_advocate_id,
            }
            self._open_feature_as_advocate(route_key, profile_for_feature, case_no)

        _black_btn(sel_frame, "Confirm & Open Feature", confirm, 240).pack(padx=20, pady=16)

    def _open_feature_as_advocate(self, route_key, adv_profile, case_no=None):
        aid = adv_profile["advocate_id"]

        def show(builder_fn):
            for w in self._content_area.winfo_children():
                w.destroy()
            builder_fn(self._content_area)

        # ── Bound advocate router ──────────────────────────────────────────────
        # Routes directly to advocate features WITHOUT re-asking advocate selection.
        # This prevents the double-selector bug when any view calls router("case_info", cn).
        def _adv_router(key, cn=None):
            _adv_actions = {
                "case_info":   lambda: show(lambda p: build_case_info_view(p, _adv_router, self, cn, advocate_id=aid)),
                "new_case":    lambda: show(lambda p: build_new_case_view(p, _adv_router, self, aid)),
                "case_update": lambda: show(lambda p: build_case_update_view(p, _adv_router, self, aid)),
                "ongoing":     lambda: show(lambda p: build_cases_ongoing_view(p, _adv_router, self, aid)),
                "fees":        lambda: show(lambda p: build_fees_tracking_view(p, _adv_router, self, aid)),
                "expenses":    lambda: show(lambda p: build_expenses_view(p, _adv_router, self, aid)),
                "incoming":    lambda: show(lambda p: build_money_incoming_view(p, _adv_router, self, aid)),
                "settings":    lambda: show(lambda p: build_account_settings_view(p, adv_profile, self)),
                "new_client":  lambda: show(lambda p: build_create_client_view(p, _adv_router, self, aid)),
            }
            if key in _adv_actions:
                _adv_actions[key]()
            else:
                # Fall back to admin top-level routing for non-advocate routes
                self._route(key, cn)

        actions = {
            "case_info":   lambda: show(lambda p: build_case_info_view(p, _adv_router, self, case_no, advocate_id=aid)),
            "new_case":    lambda: show(lambda p: build_new_case_view(p, _adv_router, self, aid)),
            "case_update": lambda: show(lambda p: build_case_update_view(p, _adv_router, self, aid)),
            "ongoing":     lambda: show(lambda p: build_cases_ongoing_view(p, _adv_router, self, aid)),
            "fees":        lambda: show(lambda p: build_fees_tracking_view(p, _adv_router, self, aid)),
            "expenses":    lambda: show(lambda p: build_expenses_view(p, _adv_router, self, aid)),
            "incoming":    lambda: show(lambda p: build_money_incoming_view(p, _adv_router, self, aid)),
            "settings":    lambda: show(lambda p: build_account_settings_view(p, adv_profile, self)),
            "new_client":  lambda: show(lambda p: build_create_client_view(p, _adv_router, self, aid)),
        }
        if route_key in actions:
            actions[route_key]()

    # ── FIX 2: Client Selector ────────────────────────────────────────────────
    def _show_client_selector(self, route_key):
        for w in self._content_area.winfo_children():
            w.destroy()
        self._back_bar(self._content_area,
                       f"Select Client — {route_key.replace('_', ' ').title()}")

        clients     = db.get_all_clients() or []
        cli_options = [f"{c['client_id']}  —  {c['full_name']}" for c in clients]
        cli_ids     = [c["client_id"] for c in clients]

        sel_frame = tk.Frame(self._content_area, bg=COLORS["bg_primary"])
        sel_frame.pack(pady=40)

        tk.Label(sel_frame, text="Select the Client to act as:",
                 font=FONTS["heading_2"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_primary"]).pack(anchor="w", padx=20, pady=(0, 10))

        chosen_var = tk.StringVar(value=cli_options[0] if cli_options else "")
        ctk.CTkOptionMenu(sel_frame, values=cli_options if cli_options else ["(no clients)"],
                          variable=chosen_var,
                          fg_color=COLORS["toggle_cli_bg"], button_color=COLORS["navbar_hover"],
                          button_hover_color=COLORS["accent_hover"],
                          text_color=COLORS["text_on_dark"],
                          dropdown_fg_color=COLORS["bg_primary"],
                          dropdown_text_color=COLORS["text_primary"],
                          width=380).pack(padx=20, pady=6)

        info_lbl = tk.Label(sel_frame, text="", font=FONTS["caption"],
                            fg=COLORS["text_muted"], bg=COLORS["bg_primary"])
        info_lbl.pack(anchor="w", padx=20, pady=(4, 0))

        def on_change(*_):
            if not cli_options or chosen_var.get() not in cli_options:
                return
            idx = cli_options.index(chosen_var.get())
            c   = clients[idx]
            info_lbl.config(text=f"Phone: {c.get('phone', '—')}  |  Email: {c.get('email', '—')}")

        chosen_var.trace_add("write", lambda *_: on_change())
        on_change()

        def confirm():
            if not cli_options or chosen_var.get() not in cli_options:
                return
            idx = cli_options.index(chosen_var.get())
            selected_client_id = cli_ids[idx]
            self._open_feature_as_client(route_key, selected_client_id)

        _black_btn(sel_frame, "Confirm & Open Feature", confirm, 240).pack(padx=20, pady=16)

    def _open_feature_as_client(self, route_key, client_id):
        def show(builder_fn):
            for w in self._content_area.winfo_children():
                w.destroy()
            builder_fn(self._content_area)

        actions = {
            "case_info":   lambda: show(lambda p: build_client_case_view(p, self._route, self, client_id)),
            "pay_portal":  lambda: show(lambda p: build_payment_portal_view(p, self._route, self, client_id)),
            "pay_history": lambda: show(lambda p: build_payment_history_view(p, self._route, self, client_id)),
        }
        if route_key in actions:
            actions[route_key]()
        else:
            self._show_client_selector(route_key)

    # ── Admin Navbar (FIX 2: menus change based on _view_mode) ───────────────
    def _build_navbar(self):
        bar = tk.Frame(self, bg=COLORS["navbar_bg"], height=DIMS["navbar_height"])
        bar.pack(fill="x")
        bar.pack_propagate(False)
        self._navbar_bar = bar

        brand = tk.Frame(bar, bg=COLORS["navbar_bg"])
        brand.pack(side="left", padx=(14, 6))
        tk.Label(brand, text="\u2696", font=FONTS["navbar_brand_icon"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(side="left", padx=(0, 8))
        txt_stack = tk.Frame(brand, bg=COLORS["navbar_bg"])
        txt_stack.pack(side="left")
        tk.Label(txt_stack, text="ADVOCACY", font=FONTS["navbar_brand"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Label(txt_stack, text="Legal Practice Management Suite",
                 font=FONTS["navbar_brand_sub"], fg=COLORS["text_muted"],
                 bg=COLORS["navbar_bg"]).pack(anchor="w")

        tk.Frame(bar, bg=COLORS["navbar_border"], width=1, height=38
                 ).pack(side="left", padx=14, pady=14)

        self._nav_menu_host = tk.Frame(bar, bg=COLORS["navbar_bg"])
        self._nav_menu_host.pack(side="left")

        pf = tk.Frame(bar, bg=COLORS["navbar_bg"], cursor="hand2")
        pf.pack(side="right", padx=14)
        av = tk.Label(pf, text=" AD ", font=FONTS["caption_bold"],
                      fg=COLORS["navbar_bg"], bg=COLORS["navbar_text"], padx=2, pady=2)
        av.pack(side="left", padx=(0, 6))
        nm = tk.Label(pf, text="System Administrator",
                      font=FONTS["navbar"], fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"])
        nm.pack(side="left")
        for w in [pf, av, nm]:
            w.bind("<Button-1>", lambda e: self._route("profile"))  # v7: profile viewer
            w.bind("<Enter>", lambda e: pf.config(bg=COLORS["navbar_hover"]))
            w.bind("<Leave>", lambda e: pf.config(bg=COLORS["navbar_bg"]))

        self._build_subbar()
        self._rebuild_navbar_menus()

    def _rebuild_navbar_menus(self):
        for w in self._nav_menu_host.winfo_children():
            w.destroy()
        if self._view_mode == "advocate":
            NavDropdown(self._nav_menu_host, "CASE MANAGEMENT", [
                ("1.1  Case Info",     "case_info"),
                ("1.2  New Case",      "new_case"),
                ("1.3  Case Updation", "case_update"),
            ], self._route)
            NavDropdown(self._nav_menu_host, "CLIENTS", [
                ("2.1  Cases Ongoing",     "ongoing"),
                ("2.2  Fees Tracking",     "fees"),
                ("2.3  Create New Client", "new_client"),
            ], self._route)
            NavDropdown(self._nav_menu_host, "EXPENSES / GAIN", [
                ("3.1  Expenses",       "expenses"),
                ("3.2  Money Incoming", "incoming"),
            ], self._route)
            NavDropdown(self._nav_menu_host, "ADMIN TOOLS", [
                ("4.1  Create New Advocate", "create_advocate"),
                ("4.2  All Assistants",       "admin_assistants"),
            ], self._route)
        else:
            # client view menus
            NavDropdown(self._nav_menu_host, "CASES", [
                ("Client Cases", "case_info"),
            ], self._route)
            NavDropdown(self._nav_menu_host, "PAYMENT", [
                ("Payment Portal",  "pay_portal"),
                ("Payment History", "pay_history"),
            ], self._route)
            NavDropdown(self._nav_menu_host, "ADMIN TOOLS", [
                ("4.2  Create New Client", "new_client"),
            ], self._route)

    def _build_subbar(self):
        sub = tk.Frame(self, bg=COLORS["bg_secondary"], height=36)
        # Always pack right after the main navbar bar
        sub.pack(fill="x", after=self._navbar_bar)
        sub.pack_propagate(False)
        self._subbar_frame = sub  # store ref for reliable destroy in _rebuild_subbar

        tk.Label(sub, text="  Admin  \u00b7  Full System Access",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_secondary"]).pack(side="left", padx=10)

        # FIX 2: Toggle pill in subbar
        toggle_host = tk.Frame(sub, bg=COLORS["bg_secondary"])
        toggle_host.pack(side="left", padx=20)

        adv_active = (self._view_mode == "advocate")
        cli_active = (self._view_mode == "client")

        adv_bg  = COLORS["toggle_adv_bg"] if adv_active else COLORS["toggle_off"]
        cli_bg  = COLORS["toggle_cli_bg"] if cli_active else COLORS["toggle_off"]

        adv_pill = tk.Label(toggle_host, text="  \u2696  ADVOCATE VIEW  ",
                            font=FONTS["caption_bold"], fg="#FFFFFF",
                            bg=adv_bg, cursor="hand2", padx=4, pady=3)
        adv_pill.pack(side="left", ipadx=2)
        adv_pill.bind("<Button-1>", lambda e: self._toggle_view_mode("advocate"))
        adv_pill.bind("<Enter>", lambda e: adv_pill.config(bg=COLORS["navbar_hover"]) if not adv_active else None)
        adv_pill.bind("<Leave>", lambda e: adv_pill.config(bg=adv_bg))

        cli_pill = tk.Label(toggle_host, text="  \U0001f464  CLIENT VIEW  ",
                            font=FONTS["caption_bold"], fg="#FFFFFF",
                            bg=cli_bg, cursor="hand2", padx=4, pady=3)
        cli_pill.pack(side="left", ipadx=2, padx=(2, 0))
        cli_pill.bind("<Button-1>", lambda e: self._toggle_view_mode("client"))
        cli_pill.bind("<Enter>", lambda e: cli_pill.config(bg=COLORS["navbar_hover"]) if not cli_active else None)
        cli_pill.bind("<Leave>", lambda e: cli_pill.config(bg=cli_bg))

        tk.Label(sub, text=datetime.date.today().strftime("  %d %B %Y  "),
                 font=FONTS["caption_bold"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_secondary"]).pack(side="right", padx=10)
        _build_zoom_controls(sub, self._zoom_refresh).pack(side="right", padx=6)  # v7 zoom


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 12 — CLIENT DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

class ClientDashboard(ctk.CTk):
    def __init__(self, client_id):
        super().__init__()
        self._client_id         = client_id
        self._client            = db.get_client(client_id) or {"full_name": "Client"}
        self._sidebar           = None
        self._content_area      = None
        # v5: BNS state
        self._bns_section       = None
        self._bns_section_id    = None
        self._bns_refresh_job   = None
        self._bns_panel_frame   = None
        self._bns_panel_dismissed = False  # v6: session flag
        self._current_route = None  # v7: zoom stay-on-page
        name = self._client.get("full_name", "Client")
        self.title(f"ADVOCACY — Client Portal ({name})")
        self.geometry("1300x820")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_primary"])
        self._build_navbar()
        self._build_content_area()
        self._show_home()

    # ── Back bar helper ───────────────────────────────────────────────────────
    def _back_bar(self, parent, title):
        bar = tk.Frame(parent, bg=COLORS["bg_secondary"], height=40)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        back_btn = tk.Label(
            bar, text="  \u2190  Back to Home  ",
            font=FONTS["body_bold"], fg=COLORS["text_primary"],
            bg=COLORS["bg_secondary"], cursor="hand2", padx=8,
        )
        back_btn.pack(side="left", pady=8)
        back_btn.bind("<Enter>",    lambda e: back_btn.config(bg=COLORS["border"]))
        back_btn.bind("<Leave>",    lambda e: back_btn.config(bg=COLORS["bg_secondary"]))
        back_btn.bind("<Button-1>", lambda e: self._show_home())
        tk.Frame(bar, bg=COLORS["border_strong"], width=1).pack(side="left", fill="y", pady=6)
        tk.Label(bar, text=f"  {title}", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=12, pady=8)

    # ── View management ───────────────────────────────────────────────────────
    def _show_home(self):
        self._current_route = None  # v7
        for w in self._content_area.winfo_children():
            w.destroy()
        self._build_home_content(self._content_area)

    def _zoom_refresh(self):
        """v7: Full teardown + rebuild so ALL widgets (navbar, subbar, content) get new fonts."""
        route = self._current_route  # save before destroy
        for w in self.winfo_children():
            w.destroy()
        self._sidebar = None
        self._bns_panel_frame = None
        self._bns_refresh_job = None
        self._build_navbar()
        self._build_content_area()
        if route:
            self._current_route = route
            self._route(*route)
        else:
            self._show_home()

    def _build_content_area(self):
        self._content_area = tk.Frame(self, bg=COLORS["bg_primary"])
        self._content_area.pack(fill="both", expand=True)

    def _build_home_content(self, parent):
        """v5: Two-row layout — row 0: Calendar + Sidebar  |  row 1: BNS panel."""
        # Cancel any existing auto-refresh job
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
            self._bns_refresh_job = None

        body = tk.Frame(parent, bg=COLORS["bg_primary"])
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=6)
        body.grid_columnconfigure(1, weight=0)
        body.grid_columnconfigure(2, weight=4)
        body.grid_rowconfigure(0, weight=1)   # top row: cal + sidebar
        body.grid_rowconfigure(1, weight=0)   # bottom row: BNS panel (fixed height)

        # ── Row 0: Calendar ────────────────────────────────────────────────────────────
        cal_host = tk.Frame(body, bg=COLORS["bg_primary"])
        cal_host.grid(row=0, column=0, sticky="nsew", padx=(12, 4), pady=12)
        cal = MonthCalendar(
            cal_host, self._route, client_id=self._client_id,
            on_date_click=lambda d: self._sidebar.show_date(d) if self._sidebar else None,
        )
        cal.pack(fill="both", expand=True)

        tk.Frame(body, bg=COLORS["border"], width=1
                 ).grid(row=0, column=1, sticky="ns", pady=12)

        self._sidebar = TodaySidebar(body, self._route, client_id=self._client_id)
        self._sidebar.grid(row=0, column=2, sticky="nsew", padx=(4, 12), pady=12)

        # v6: Row 1 BNS Panel (dismissable for session)
        if not self._bns_panel_dismissed:
            bns_host = tk.Frame(body, bg=BNS_COLORS["panel_bg"])
            bns_host.grid(row=1, column=0, columnspan=3, sticky="ew")
            self._bns_panel_frame = bns_host
            self._build_bns_panel(bns_host)
            self._start_bns_refresh()

    # ────────────────────────────────────────────────────────────────────────────
    # BNS Panel helpers 
    # ────────────────────────────────────────────────────────────────────────────
    def _dismiss_bns_panel(self):
        """v6: Dismiss BNS panel for this login session."""
        self._bns_panel_dismissed = True
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
            self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._bns_panel_frame.grid_remove()

    def _build_bns_panel(self, parent):
        """Build (or rebuild) the BNS knowledge panel inside *parent*."""
        for w in parent.winfo_children():
            w.destroy()
        self._bns_panel_frame = parent

        if self._bns_section is None:
            self._bns_section = db.get_random_bns_section()
        sec = self._bns_section

        if not sec:
            tk.Label(
                parent,
                text="  ⚖⚖  Bhartiya Nyaya Samhita  —  "
                     "Add BNS section data to the bns_sections table to enable this panel.  ⚖⚖",
                font=BNS_FONT_BODY, fg=BNS_COLORS["title_fg"],
                bg=BNS_COLORS["panel_bg"], pady=10,
            ).pack(fill="x", padx=16)
            return

        self._bns_section_id = sec.get("section_id")

        hdr = tk.Frame(parent, bg=BNS_COLORS["header_bg"])
        hdr.pack(fill="x")

        tk.Label(
            hdr, text="⚖  Bhartiya Nyaya Samhita  ⚖",
            font=BNS_FONT_TITLE, fg=BNS_COLORS["title_fg"],
            bg=BNS_COLORS["header_bg"], padx=16, pady=6,
        ).pack(side="left")

        self._bns_timer_label = tk.Label(
            hdr, text="", font=BNS_FONT_BADGE,
            fg=BNS_COLORS["timer_fg"], bg=BNS_COLORS["header_bg"], padx=8,
        )
        self._bns_timer_label.pack(side="right", padx=(0, 8))

        next_btn = tk.Label(
            hdr, text="  Next Section ⯈  ",
            font=BNS_FONT_BUTTON, fg=BNS_COLORS["btn_fg"],
            bg=BNS_COLORS["btn_bg"], cursor="hand2", padx=8, pady=4,
        )
        next_btn.pack(side="right", padx=(0, 4), pady=4)
        next_btn.bind("<Button-1>", lambda e: self._rotate_bns_section())
        next_btn.bind("<Enter>", lambda e: next_btn.config(bg=BNS_COLORS["btn_hover"]))
        next_btn.bind("<Leave>", lambda e: next_btn.config(bg=BNS_COLORS["btn_bg"]))

        # v7: Close (X) button
        close_btn = tk.Label(
            hdr, text="  X  ", font=BNS_FONT_BADGE,
            fg=BNS_COLORS["title_fg"], bg=BNS_COLORS["btn_bg"],
            cursor="hand2", padx=6, pady=4,
        )
        close_btn.pack(side="right", padx=(0, 2), pady=4)
        close_btn.bind("<Button-1>", lambda e: self._dismiss_bns_panel())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#333333"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=BNS_COLORS["btn_bg"]))

        tk.Label(
            hdr, text="Bhartiya Nyaya Samhita, 2023",
            font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
            bg=BNS_COLORS["header_bg"], padx=8,
        ).pack(side="right")

        tk.Frame(parent, bg=BNS_COLORS["divider"], height=1).pack(fill="x")

        content = tk.Frame(parent, bg=BNS_COLORS["panel_bg"])
        content.pack(fill="x", padx=16, pady=(6, 8))

        left_col = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        left_col.pack(side="left", anchor="n", padx=(0, 20))

        tk.Label(
            left_col,
            text=f"Section\n{sec.get('bns_number', '---')}",
            font=BNS_FONT_SECTION_NO, fg=BNS_COLORS["section_no_fg"],
            bg=BNS_COLORS["panel_bg"], justify="center",
        ).pack()

        ipc = sec.get("ipc_equivalent")
        if ipc:
            tk.Label(
                left_col, text=f"IPC: {ipc}",
                font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
                bg=BNS_COLORS["panel_bg"],
            ).pack(pady=(4, 0))

        cat_badge = tk.Label(
            left_col, text=f" {sec.get('category', '')} ",
            font=BNS_FONT_BADGE, fg=BNS_COLORS["cat_fg"],
            bg=BNS_COLORS["cat_bg"], padx=4, pady=2,
        )
        cat_badge.pack(pady=(6, 0))

        right_col = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        right_col.pack(side="left", fill="x", expand=True, anchor="n")

        tk.Label(
            right_col,
            text=sec.get("section_title", ""),
            font=BNS_FONT_SECTION_TITLE, fg=BNS_COLORS["section_title_fg"],
            bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
        ).pack(anchor="w")

        summary = sec.get("summary", "")
        if summary:
            tk.Label(
                right_col,
                text=summary,
                font=BNS_FONT_BODY, fg=BNS_COLORS["body_fg"],
                bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                wraplength=1050,
            ).pack(anchor="w", pady=(4, 0))

        punishment = sec.get("punishment_summary")
        if punishment:
            tk.Label(
                right_col,
                text=f"⚖ Punishment:  {punishment}",
                font=BNS_FONT_BADGE, fg=BNS_COLORS["punishment_fg"],
                bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                wraplength=1050,
            ).pack(anchor="w", pady=(4, 0))

    def _rotate_bns_section(self):
        """Fetch the next BNS section and refresh the panel."""
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
            self._bns_refresh_job = None
        if self._bns_section_id is not None:
            self._bns_section = db.get_random_bns_section_excluding(self._bns_section_id)
        else:
            self._bns_section = db.get_random_bns_section()
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._build_bns_panel(self._bns_panel_frame)
        self._start_bns_refresh()

    def _start_bns_refresh(self):
        if self._bns_refresh_job:
            try:
                self.after_cancel(self._bns_refresh_job)
            except Exception:
                pass
        self._bns_refresh_job = self.after(120_000, self._auto_refresh_bns)

    def _auto_refresh_bns(self):
        self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._rotate_bns_section()


    # ── Router ────────────────────────────────────────────────────────────────
    def _route(self, key, case_no=None):
        self._current_route = (key, case_no)  # v7: zoom stay-on-page
        def show(builder_fn):
            for w in self._content_area.winfo_children():
                w.destroy()
            builder_fn(self._content_area)

        actions = {
            "case_info":   lambda: show(lambda p: build_client_case_view(
                                p, self._route, self, self._client_id)),
            "pay_portal":  lambda: show(lambda p: build_payment_portal_view(
                                p, self._route, self, self._client_id)),
            "pay_history": lambda: show(lambda p: build_payment_history_view(
                                p, self._route, self, self._client_id)),
            "settings":    lambda: show(lambda p: build_client_settings_view(
                                p, self._client, self)),
        }
        if key in actions:
            actions[key]()

    # ── Navbar ────────────────────────────────────────────────────────────────
    def _build_navbar(self):
        bar = tk.Frame(self, bg=COLORS["navbar_bg"], height=DIMS["navbar_height"])
        bar.pack(fill="x")
        bar.pack_propagate(False)

        brand = tk.Frame(bar, bg=COLORS["navbar_bg"])
        brand.pack(side="left", padx=(14, 6))
        tk.Label(brand, text="\u2696", font=FONTS["navbar_brand_icon"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(side="left", padx=(0, 8))
        txt_stack = tk.Frame(brand, bg=COLORS["navbar_bg"])
        txt_stack.pack(side="left")
        tk.Label(txt_stack, text="ADVOCACY", font=FONTS["navbar_brand"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Label(txt_stack, text="Legal Practice Management Suite",
                 font=FONTS["navbar_brand_sub"], fg=COLORS["text_muted"],
                 bg=COLORS["navbar_bg"]).pack(anchor="w")

        tk.Frame(bar, bg=COLORS["navbar_border"], width=1, height=38
                 ).pack(side="left", padx=14, pady=14)

        NavDropdown(bar, "CASES",   [("My Cases", "case_info")], self._route)
        NavDropdown(bar, "PAYMENT", [
            ("Payment Portal",  "pay_portal"),
            ("Payment History", "pay_history"),
        ], self._route)

        name     = self._client.get("full_name", "Client")
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        pf = tk.Frame(bar, bg=COLORS["navbar_bg"], cursor="hand2")
        pf.pack(side="right", padx=14)
        av = tk.Label(pf, text=f" {initials} ", font=FONTS["caption_bold"],
                      fg=COLORS["navbar_bg"], bg=COLORS["navbar_text"], padx=2, pady=2)
        av.pack(side="left", padx=(0, 6))
        nm = tk.Label(pf, text=name, font=FONTS["navbar"],
                      fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"])
        nm.pack(side="left")
        for w in [pf, av, nm]:
            w.bind("<Button-1>", lambda e: self._route("settings"))
            w.bind("<Enter>",    lambda e: pf.config(bg=COLORS["navbar_hover"]))
            w.bind("<Leave>",    lambda e: pf.config(bg=COLORS["navbar_bg"]))

        sub = tk.Frame(self, bg=COLORS["bg_secondary"], height=26)
        sub.pack(fill="x")
        sub.pack_propagate(False)
        tk.Label(sub, text=f"  Client Portal  \u00b7  ID: {self._client_id}",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_secondary"]).pack(side="left", padx=10)
        _build_zoom_controls(sub, self._zoom_refresh).pack(side="right", padx=6)  # v7 zoom



# ==============================================================================
#  SECTION v6-D — ASSISTANT DASHBOARD
# ==============================================================================

class AssistantDashboard(ctk.CTk):
    """Advocate assistant login - RBAC enforced."""
    _PERM_KEY = {
        "case_info":    "case_info",
        "new_case":     "case_addition",
        "case_update":  "case_updation",
        "ongoing":      "client_cases",
        "fees":         "fees_tracking",
        "expenses":     "expenses",
        "incoming":     "money_incoming",
    }

    def __init__(self, assistant_data):
        super().__init__()
        self._asst          = assistant_data
        self._advocate_id   = assistant_data.get("linked_advocate_id")
        self._advocate_name = assistant_data.get("advocate_name", "")
        self._permissions   = db.get_assistant_permissions(assistant_data["assistant_id"])
        self._bns_section       = None
        self._bns_section_id    = None
        self._bns_refresh_job   = None
        self._bns_panel_frame   = None
        self._bns_panel_dismissed = False
        self._current_route = None  # v7: zoom stay-on-page
        self._content_area  = None
        self._sidebar       = None
        name = assistant_data.get("full_name", "Assistant")
        self.title(f"ADVOCACY \u2014 Assistant Portal ({name})")
        self.geometry("1300x820")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_primary"])
        self._build_navbar()
        self._build_content_area()
        self._show_home()

    def _has_perm(self, fk):
        return self._permissions.get(fk, False)

    def _back_bar(self, parent, title):
        bar = tk.Frame(parent, bg=COLORS["bg_secondary"], height=40)
        bar.pack(fill="x"); bar.pack_propagate(False)
        back = tk.Label(bar, text="  \u2190  Back  ", font=FONTS["body_bold"],
                        fg=COLORS["text_primary"], bg=COLORS["bg_secondary"],
                        cursor="hand2", padx=8)
        back.pack(side="left", pady=8)
        back.bind("<Enter>",    lambda e: back.config(bg=COLORS["border"]))
        back.bind("<Leave>",    lambda e: back.config(bg=COLORS["bg_secondary"]))
        back.bind("<Button-1>", lambda e: self._show_home())
        tk.Frame(bar, bg=COLORS["border_strong"], width=1).pack(side="left", fill="y", pady=6)
        tk.Label(bar, text=f"  {title}", font=FONTS["heading_2"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]).pack(side="left", padx=12, pady=8)

    def _no_access_view(self, parent):
        for w in parent.winfo_children(): w.destroy()
        tk.Label(parent, text="\U0001f512  Access Not Granted",
                 font=FONTS["heading_1"], fg="#CC2222",
                 bg=COLORS["bg_primary"]).pack(pady=(60, 10))
        tk.Label(parent,
                 text="You do not have permission to access this feature.\n"
                      "Contact your advocate to request access.",
                 font=FONTS["body"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_primary"], justify="center").pack(pady=6)
        _black_btn(parent, "\u2190 Go Back", self._show_home, 160).pack(pady=20)

    def _build_content_area(self):
        self._content_area = tk.Frame(self, bg=COLORS["bg_primary"])
        self._content_area.pack(fill="both", expand=True)

    def _show_home(self):
        self._current_route = None  # v7
        for w in self._content_area.winfo_children(): w.destroy()
        self._build_home_content(self._content_area)

    def _zoom_refresh(self):
        """v7: Full teardown + rebuild so ALL widgets (navbar, subbar, content) get new fonts."""
        route = self._current_route  # save before destroy
        for w in self.winfo_children():
            w.destroy()
        self._sidebar = None
        self._bns_panel_frame = None
        self._bns_refresh_job = None
        self._build_navbar()
        self._build_content_area()
        if route:
            self._current_route = route
            self._route(*route)
        else:
            self._show_home()

    def _build_home_content(self, parent):
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
            self._bns_refresh_job = None
        body = tk.Frame(parent, bg=COLORS["bg_primary"])
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=6)
        body.grid_columnconfigure(1, weight=0)
        body.grid_columnconfigure(2, weight=4)
        body.grid_rowconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=0, minsize=130)  # Bug 17: ensure BNS panel never gets clipped
        cal_host = tk.Frame(body, bg=COLORS["bg_primary"])
        cal_host.grid(row=0, column=0, sticky="nsew", padx=(12, 4), pady=12)
        cal = MonthCalendar(cal_host, self._route,
                            advocate_id=self._advocate_id,  # Bug 20: restrict to linked advocate
                            on_date_click=lambda d: self._sidebar.show_date(d) if self._sidebar else None)
        cal.pack(fill="both", expand=True)
        tk.Frame(body, bg=COLORS["border"], width=1).grid(row=0, column=1, sticky="ns", pady=12)
        self._sidebar = TodaySidebar(body, self._route, advocate_id=self._advocate_id)  # Bug 20
        self._sidebar.grid(row=0, column=2, sticky="nsew", padx=(4, 12), pady=12)
        if not self._bns_panel_dismissed:
            bns_host = tk.Frame(body, bg=BNS_COLORS["panel_bg"])
            bns_host.grid(row=1, column=0, columnspan=3, sticky="ew")
            self._bns_panel_frame = bns_host
            self._build_bns_panel(bns_host)
            self._start_bns_refresh()

    def _dismiss_bns_panel(self):
        self._bns_panel_dismissed = True
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
            self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._bns_panel_frame.grid_remove()

    def _build_bns_panel(self, parent):
        for w in parent.winfo_children(): w.destroy()
        self._bns_panel_frame = parent
        if self._bns_section is None:
            self._bns_section = db.get_random_bns_section()
        sec = self._bns_section
        if not sec:
            tk.Label(parent, text="  \u2696  BNS \u2014 Add data to bns_sections table  \u2696",
                     font=BNS_FONT_BODY, fg=BNS_COLORS["title_fg"],
                     bg=BNS_COLORS["panel_bg"], pady=6).pack(fill="x")
            return
        self._bns_section_id = sec.get("section_id")
        hdr = tk.Frame(parent, bg=BNS_COLORS["header_bg"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="\u2696  Bhartiya Nyaya Samhita  \u2696",
                 font=BNS_FONT_TITLE, fg=BNS_COLORS["title_fg"],
                 bg=BNS_COLORS["header_bg"], padx=16, pady=6).pack(side="left")
        self._bns_timer_label = tk.Label(hdr, text="", font=BNS_FONT_BADGE,
                                          fg=BNS_COLORS["timer_fg"], bg=BNS_COLORS["header_bg"], padx=8)
        self._bns_timer_label.pack(side="right", padx=(0, 8))
        next_btn = tk.Label(hdr, text="  Next Section \u25b8  ",
                            font=BNS_FONT_BUTTON, fg=BNS_COLORS["btn_fg"],
                            bg=BNS_COLORS["btn_bg"], cursor="hand2", padx=8, pady=4)
        next_btn.pack(side="right", padx=(0, 4), pady=4)
        next_btn.bind("<Button-1>", lambda e: self._rotate_bns_section())
        close_btn = tk.Label(hdr, text="  X  ", font=BNS_FONT_BADGE,
                             fg=BNS_COLORS["title_fg"], bg=BNS_COLORS["btn_bg"],
                             cursor="hand2", padx=6, pady=4)
        close_btn.pack(side="right", padx=(0, 2), pady=4)
        close_btn.bind("<Button-1>", lambda e: self._dismiss_bns_panel())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#333333"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=BNS_COLORS["btn_bg"]))
        tk.Frame(parent, bg=BNS_COLORS["divider"], height=1).pack(fill="x")
        content = tk.Frame(parent, bg=BNS_COLORS["panel_bg"])
        content.pack(fill="x", padx=16, pady=(6, 8))
        left = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        left.pack(side="left", anchor="n", padx=(0, 20))
        tk.Label(left, text=f"Section\n{sec.get('bns_number', '---')}",
                 font=BNS_FONT_SECTION_NO, fg=BNS_COLORS["section_no_fg"],
                 bg=BNS_COLORS["panel_bg"], justify="center").pack()
        ipc = sec.get("ipc_equivalent")
        if ipc:
            tk.Label(left, text=f"IPC: {ipc}",
                     font=BNS_FONT_BADGE, fg=BNS_COLORS["ipc_fg"],
                     bg=BNS_COLORS["panel_bg"]).pack(pady=(4, 0))
        cat = sec.get("category", "")
        if cat:
            tk.Label(left, text=f" {cat} ",
                     font=BNS_FONT_BADGE, fg=BNS_COLORS["cat_fg"],
                     bg=BNS_COLORS["cat_bg"], padx=4, pady=2).pack(pady=(6, 0))

        right = tk.Frame(content, bg=BNS_COLORS["panel_bg"])
        right.pack(side="left", fill="x", expand=True, anchor="n")
        tk.Label(right, text=sec.get("section_title", ""),
                 font=BNS_FONT_SECTION_TITLE, fg=BNS_COLORS["section_title_fg"],
                 bg=BNS_COLORS["panel_bg"], anchor="w", justify="left").pack(anchor="w")
        if sec.get("summary"):
            tk.Label(right, text=sec["summary"],
                     font=BNS_FONT_BODY, fg=BNS_COLORS["body_fg"],
                     bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                     wraplength=1050).pack(anchor="w", pady=(4, 0))
        punishment = sec.get("punishment_summary")
        if punishment:
            tk.Label(right, text=f"\u2696 Punishment:  {punishment}",
                     font=BNS_FONT_BADGE, fg=BNS_COLORS["punishment_fg"],
                     bg=BNS_COLORS["panel_bg"], anchor="w", justify="left",
                     wraplength=1050).pack(anchor="w", pady=(4, 0))

    def _rotate_bns_section(self):
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
            self._bns_refresh_job = None
        if self._bns_section_id is not None:
            self._bns_section = db.get_random_bns_section_excluding(self._bns_section_id)
        else:
            self._bns_section = db.get_random_bns_section()
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._build_bns_panel(self._bns_panel_frame)
        self._start_bns_refresh()

    def _start_bns_refresh(self):
        if self._bns_refresh_job:
            try: self.after_cancel(self._bns_refresh_job)
            except Exception: pass
        self._bns_refresh_job = self.after(120_000, self._auto_refresh_bns)

    def _auto_refresh_bns(self):
        self._bns_refresh_job = None
        if self._bns_panel_frame and self._bns_panel_frame.winfo_exists():
            self._rotate_bns_section()

    def _build_navbar(self):
        bar = tk.Frame(self, bg=COLORS["navbar_bg"], height=DIMS["navbar_height"])
        bar.pack(fill="x"); bar.pack_propagate(False)
        brand = tk.Frame(bar, bg=COLORS["navbar_bg"])
        brand.pack(side="left", padx=(14, 6))
        tk.Label(brand, text="\u2696", font=FONTS["navbar_brand_icon"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(side="left", padx=(0, 8))
        txt = tk.Frame(brand, bg=COLORS["navbar_bg"])
        txt.pack(side="left")
        tk.Label(txt, text="ADVOCACY", font=FONTS["navbar_brand"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Label(txt, text="Legal Practice Management Suite",
                 font=FONTS["navbar_brand_sub"], fg=COLORS["text_muted"],
                 bg=COLORS["navbar_bg"]).pack(anchor="w")
        tk.Frame(bar, bg=COLORS["navbar_border"], width=1, height=38).pack(side="left", padx=14, pady=14)
        NavDropdown(bar, "CASE MANAGEMENT", [
            ("1.1  Case Info",     "case_info"),
            ("1.2  New Case",      "new_case"),
            ("1.3  Case Updation", "case_update"),
        ], self._route)
        NavDropdown(bar, "CLIENTS", [
            ("2.1  Cases Ongoing",    "ongoing"),
            ("2.2  Fees Tracking",    "fees"),
            ("2.3  Create Client",    "new_client"),
        ], self._route)
        NavDropdown(bar, "EXPENSES / GAIN", [
            ("3.1  Expenses",       "expenses"),
            ("3.2  Money Incoming", "incoming"),
        ], self._route)
        name = self._asst.get("full_name", "Assistant")
        initials = "".join(p[0] for p in name.split()[:2]).upper() or "AS"
        pf = tk.Frame(bar, bg=COLORS["navbar_bg"], cursor="hand2")
        pf.pack(side="right", padx=14)
        tk.Label(pf, text=f" {initials} ", font=FONTS["caption_bold"],
                 fg=COLORS["navbar_bg"], bg=COLORS["navbar_text"], padx=2, pady=2).pack(side="left", padx=(0, 6))
        nm = tk.Label(pf, text=name, font=FONTS["navbar"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"])
        nm.pack(side="left")
        for w in [pf, nm]:  # v7 Bug 14: click profile to open settings
            w.bind("<Button-1>", lambda e: self._route("settings"))
            w.bind("<Enter>", lambda e: pf.config(bg=COLORS["navbar_hover"]))
            w.bind("<Leave>", lambda e: pf.config(bg=COLORS["navbar_bg"]))
        sub = tk.Frame(self, bg=COLORS["bg_secondary"], height=26)
        sub.pack(fill="x"); sub.pack_propagate(False)
        tk.Label(sub,
                 text=f"  Assistant  \u00b7  of {self._advocate_name}  \u00b7  Limited Access",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_secondary"]).pack(side="left", padx=10)
        tk.Label(sub, text=datetime.date.today().strftime("  %d %B %Y  "),
                 font=FONTS["caption_bold"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_secondary"]).pack(side="right", padx=10)
        _build_zoom_controls(sub, self._zoom_refresh).pack(side="right", padx=6)  # v7 zoom

    def _route(self, key, case_no=None):
        self._current_route = (key, case_no)  # v7: zoom stay-on-page
        aid = self._advocate_id
        perm_key = self._PERM_KEY.get(key, "")
        if perm_key and not self._has_perm(perm_key):
            for w in self._content_area.winfo_children(): w.destroy()
            self._no_access_view(self._content_area)
            return

        def show(fn):
            for w in self._content_area.winfo_children(): w.destroy()
            fn(self._content_area)

        actions = {
            "case_info":   lambda: show(lambda p: build_case_info_view(p, self._route, self,
                                         case_no, advocate_id=aid)),
            "new_case":    lambda: show(lambda p: build_new_case_view(p, self._route, self, aid)),
            "case_update": lambda: show(lambda p: build_case_update_view(p, self._route, self, aid)),
            "ongoing":     lambda: show(lambda p: build_cases_ongoing_view(p, self._route, self, aid)),
            "fees":        lambda: show(lambda p: build_fees_tracking_view(p, self._route, self, aid)),
            "expenses":    lambda: show(lambda p: build_expenses_view(p, self._route, self, aid)),
            "incoming":    lambda: show(lambda p: build_money_incoming_view(p, self._route, self, aid)),
            "new_client":  lambda: show(lambda p: build_create_client_view(p, self._route, self, aid)),
            "settings":    lambda: show(lambda p: build_assistant_profile_view(
                p, self._asst, self)),
        }
        if key in actions: actions[key]()
        elif key == "home": self._show_home()


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 13 — LOGIN SCREEN  
# ══════════════════════════════════════════════════════════════════════════════

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ADVOCACY — Login")
        self.geometry("980x660")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_primary"])
        self._mode          = None
        self._err_label     = None
        self._login_submode = "advocate"  # v6: "advocate" or "assistant"
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=COLORS["navbar_bg"], width=440)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        tk.Frame(left, bg=COLORS["navbar_border"], width=2).pack(side="right", fill="y")

        brand = tk.Frame(left, bg=COLORS["navbar_bg"])
        brand.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(brand, text="\u2696", font=("Georgia", 72),
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack()
        tk.Label(brand, text="ADVOCACY", font=FONTS["brand"],
                 fg=COLORS["navbar_text"], bg=COLORS["navbar_bg"]).pack(pady=(4, 0))
        tk.Label(brand, text="Legal Practice Management Suite",
                 font=FONTS["brand_sub"], fg=COLORS["text_muted"],
                 bg=COLORS["navbar_bg"]).pack(pady=(2, 20))
        tk.Frame(brand, bg=COLORS["navbar_border"], height=1, width=280).pack(pady=10)
        for line in ["Dewas  \u00b7  Indore  \u00b7  Jabalpur",
                     "Advocate Prakash Singh — Chamber No. 14"]:
            tk.Label(brand, text=line, font=FONTS["caption"],
                     fg=COLORS["text_muted"], bg=COLORS["navbar_bg"]).pack()

        right = tk.Frame(self, bg=COLORS["bg_primary"])
        right.pack(side="right", fill="both", expand=True)
        self._login_panel = right
        self._show_role_picker()

    def _show_role_picker(self):
        self._clear_panel()
        panel = self._login_panel
        tk.Label(panel, text="Select Login Type", font=FONTS["heading_1"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(pady=(80, 6))
        tk.Label(panel, text="Choose your access level to continue",
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(pady=(0, 40))

        for label, icon, mode in [
            ("Advocate Login", "\u200d\u2696\ufe0f", "advocate"),
            ("Client Login",   "\U0001f464",                   "client"),
        ]:
            card = tk.Frame(panel, bg=COLORS["bg_card"],
                             highlightbackground=COLORS["border"],
                             highlightthickness=1, cursor="hand2", padx=20, pady=16)
            card.pack(fill="x", padx=60, pady=8)
            inner = tk.Frame(card, bg=COLORS["bg_card"])
            inner.pack(fill="x")
            tk.Label(inner, text=icon, font=("Segoe UI Emoji", 26),
                     bg=COLORS["bg_card"]).pack(side="left", padx=(0, 14))
            tb = tk.Frame(inner, bg=COLORS["bg_card"])
            tb.pack(side="left", fill="x", expand=True)
            tk.Label(tb, text=label, font=FONTS["heading_2"],
                     fg=COLORS["text_primary"], bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
            desc = ("Cases, Clients, Expenses" if mode == "advocate" else "View cases & pay dues")
            tk.Label(tb, text=desc, font=FONTS["caption"],
                     fg=COLORS["text_muted"], bg=COLORS["bg_card"], anchor="w").pack(anchor="w")
            tk.Label(inner, text="\u2192", font=FONTS["heading_2"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(side="right")

            def _enter(e, c=card, i=inner):
                c.config(bg=COLORS["bg_secondary"], highlightbackground=COLORS["border_strong"])
                _recursive_bg(i, COLORS["bg_secondary"])

            def _leave(e, c=card, i=inner):
                c.config(bg=COLORS["bg_card"], highlightbackground=COLORS["border"])
                _recursive_bg(i, COLORS["bg_card"])

            card.bind("<Enter>",    _enter)
            card.bind("<Leave>",    _leave)
            card.bind("<Button-1>", lambda e, m=mode: self._show_login_form(m))
            for ch in [inner] + list(inner.winfo_children()):
                ch.bind("<Button-1>", lambda e, m=mode: self._show_login_form(m))

    def _show_login_form(self, mode):
        self._mode = mode
        self._clear_panel()
        panel = self._login_panel

        back = tk.Label(panel, text="\u2190 Back", font=FONTS["caption"],
                         fg=COLORS["text_muted"], bg=COLORS["bg_primary"], cursor="hand2")
        back.pack(anchor="nw", padx=20, pady=(14, 0))
        back.bind("<Button-1>", lambda e: self._show_role_picker())
        back.bind("<Enter>",    lambda e: back.config(fg=COLORS["text_primary"]))
        back.bind("<Leave>",    lambda e: back.config(fg=COLORS["text_muted"]))

        icon  = "\u200d\u2696\ufe0f" if mode == "advocate" else "\U0001f464"
        title = "Advocate Login" if mode == "advocate" else "Client Login"
        tk.Label(panel, text=icon, font=("Segoe UI Emoji", 30),
                 bg=COLORS["bg_primary"]).pack(pady=(30, 4))
        tk.Label(panel, text=title, font=FONTS["heading_1"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack()
        tk.Label(panel,
                 text=("Enter your username and password" if mode == "advocate"
                       else "Enter your Client ID and password"),
                 font=FONTS["caption"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_primary"]).pack(pady=(4, 12))
        # v6: Advocate / Assistant toggle
        if mode == "advocate":
            self._login_submode = "advocate"
            tg = tk.Frame(panel, bg=COLORS["bg_primary"])
            tg.pack(pady=(0, 16))
            adv_pill = tk.Label(tg, text="  Advocate  ",
                                font=FONTS["caption_bold"], fg="#FFFFFF",
                                bg=COLORS["toggle_adv_bg"], cursor="hand2", padx=4, pady=3)
            adv_pill.pack(side="left")
            ast_pill = tk.Label(tg, text="  Assistant  ",
                                font=FONTS["caption_bold"], fg="#FFFFFF",
                                bg=COLORS["toggle_off"], cursor="hand2", padx=4, pady=3)
            ast_pill.pack(side="left", padx=(2, 0))
            def _set_sm(ms, ap=adv_pill, bp=ast_pill):
                self._login_submode = ms
                ap.config(bg=COLORS["toggle_adv_bg"] if ms == "advocate" else COLORS["toggle_off"])
                bp.config(bg=COLORS["accent"] if ms == "assistant" else COLORS["toggle_off"])
            adv_pill.bind("<Button-1>", lambda e: _set_sm("advocate"))
            ast_pill.bind("<Button-1>", lambda e: _set_sm("assistant"))
        # ────────────────────────────────────────────────────────────────────

        user_var = tk.StringVar()
        pass_var = tk.StringVar()
        form     = tk.Frame(panel, bg=COLORS["bg_primary"])
        form.pack(padx=60, fill="x")

        for lbl, var, show in [
            ("Username" if mode == "advocate" else "Client ID", user_var, ""),
            ("Password", pass_var, "\u2022"),
        ]:
            tk.Label(form, text=lbl, font=FONTS["body_bold"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_primary"],
                     anchor="w").pack(anchor="w", pady=(8, 2))
            ent = ctk.CTkEntry(form, textvariable=var, show=show, width=320,
                                fg_color=COLORS["entry_bg"], text_color=COLORS["text_primary"],
                                border_color=COLORS["entry_border"],
                                placeholder_text_color=COLORS["text_muted"],
                                corner_radius=DIMS["btn_corner"])
            ent.pack(anchor="w")
            if show == "\u2022":
                ent.bind("<Return>", lambda e: self._attempt_login(user_var, pass_var))

        self._err_label = tk.Label(form, text="", font=FONTS["caption"],
                                    fg="#CC2222", bg=COLORS["bg_primary"])
        self._err_label.pack(anchor="w", pady=(6, 0))

        ctk.CTkButton(
            form,
            text=f"Login as {'Advocate' if mode == 'advocate' else 'Client'}",
            command=lambda: self._attempt_login(user_var, pass_var),
            width=320, height=42,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_on_dark"], font=FONTS["body_bold"],
            corner_radius=DIMS["btn_corner"],
        ).pack(pady=(18, 0))

    def _attempt_login(self, user_var, pass_var):
        uid = user_var.get().strip()
        pwd = pass_var.get().strip()
        # v6: assistant login path
        if self._mode == "advocate" and self._login_submode == "assistant":
            user_data = db.authenticate_assistant(uid, pwd)
        elif self._mode == "advocate":
            user_data = db.authenticate_advocate(uid, pwd)
        else:
            user_data = db.authenticate_client(uid, pwd)
        if user_data:
            self._launch(uid, user_data)
        else:
            if self._err_label:
                self._err_label.config(text="\u2717  Invalid credentials. Please try again.")

    def _launch(self, uid, user_data):
        self.destroy()
        # v6: assistant launch path
        if self._mode == "advocate" and self._login_submode == "assistant":
            AssistantDashboard(user_data).mainloop()
            return
        if self._mode == "advocate":
            profile = {
                "name":        user_data.get("full_name", uid),
                "bar_no":      user_data.get("bar_number", ""),
                "court":       user_data.get("primary_court", ""),
                "chambers":    user_data.get("chambers", "") or "",
                "phone":       user_data.get("phone", "") or "",
                "email":       user_data.get("email", "") or "",
                "advocate_id": user_data.get("advocate_id", 1),
            }
            # FIX 2: check is_admin flag (or fallback to username == "admin")
            is_admin = bool(user_data.get("is_admin", 0)) or (user_data.get("username") == "admin")
            if is_admin:
                AdminDashboard(profile).mainloop()
            else:
                AdvocateDashboard(profile).mainloop()
        else:
            ClientDashboard(user_data["client_id"]).mainloop()

    def _clear_panel(self):
        for w in self._login_panel.winfo_children():
            w.destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        LoginScreen().mainloop()
    finally:
        try:
            db.close()
        except Exception:
            pass
# advocacy
