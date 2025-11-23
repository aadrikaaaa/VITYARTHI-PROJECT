import datetime
import getpass
import time

# Colors
C_RESET = "\033[0m"
C_OK = "\033[92m"
C_ERR = "\033[91m"
C_WARN = "\033[93m"
C_HDR = "\033[96m"
C_BOLD = "\033[1m"

def col(t, c):
    return f"{c}{t}{C_RESET}"

# login
ADMIN_PASSWORD = "vtop"
PASSWORD_HINT = "Hint: VIT at top."

# Certificates
CERTS = [
    "SoloLearn Python Course",
    "GreatLearning Python Course",
    "HackerRank PS (Basic)",
    "HackerRank PS (Intermediate)",
    "HackerRank Python (Basic)"
]

students = []
assigned_date = None

# defining functions
def pause(msg="Press Enter to continue..."):
    input(col(msg, C_HDR))

def loading(msg="Processing", dur=1.5, steps=3):
    print(msg, end="")
    for _ in range(steps):
        print(".", end="", flush=True)
        time.sleep(dur / steps)
    print()

def read_int(prompt, minv=0, maxv=9999, default=None):
    while True:
        s = input(prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            n = int(s)
            if minv <= n <= maxv:
                return n
            print(col(f"Enter number {minv}-{maxv}.", C_WARN))
        except ValueError:
            print(col("Invalid number.", C_WARN))

def read_date(prompt, allow_no=False):
    while True:
        s = input(prompt).strip()
        if allow_no and s.lower() == "no":
            return None
        try:
            return datetime.datetime.strptime(s, "%d-%m-%Y").date()
        except ValueError:
            print(col("In DD-MM-YYYY Format", C_WARN))

def cert_score(days):
    if days is None:
        return 0
    if days <= 0:
        return 10
    elif days == 1:
        return 9
    elif days == 2:
        return 8
    elif days == 3:
        return 7
    elif days == 4:
        return 6
    elif 5 <= days <= 10:
        return 5
    else:
        return 2

def grade(p):
    if p >= 90:
        return "A"
    elif p >= 75:
        return "B"
    elif p >= 60:
        return "C"
    elif p >= 33:
        return "D"
    else:
        return "F"

# Welcome
print(col("WELCOME TO MY GRADING APP !!!", C_BOLD + C_HDR))

# Login
def login():
    print(col("\n=== ADMIN LOGIN ===", C_BOLD + C_HDR))
    while True:
        pw = getpass.getpass("Enter password: ")
        if pw == ADMIN_PASSWORD:
            print(col("Login successful!\n", C_OK))
            return True
        else:
            print(col("Incorrect password. " + PASSWORD_HINT, C_WARN))

# Assigned date
def ensure_assigned():
    global assigned_date
    if assigned_date is None:
        print(col("\nEnter the certificates due date", C_HDR))
        assigned_date = read_date("Due Date (In DD-MM-YYYY Format): ")
    return assigned_date

# Adding student
def add_student():
    ensure_assigned()
    print(col("\n--- Add Student ---", C_HDR))
    name = input("Name: ").strip()
    if not name:
        print(col("Name required.", C_WARN))
        return

    vids = read_int("VITYARTHI Lecture videos seen (0-15): ", 0, 15)
    assigns = read_int("Assignments completed (0-25): ", 0, 25)
    print(col("\nEnter submission date of certificates", C_HDR))
    sub = read_date("Submitted date (In DD-MM-YYYY Format) or 'no': ", allow_no=True)

    certs_dict = {}
    days_dict = {}
    if sub is None:
        for c in CERTS:
            certs_dict[c] = 0
            days_dict[c] = None
    else:
        days = (sub - assigned_date).days
        days = max(0, days)
        for c in CERTS:
            certs_dict[c] = cert_score(days)
            days_dict[c] = days

    star = input("Achieved 5-star in HackerRank ? (yes/no): ").strip().lower()
    star_marks = 10 if star.startswith("y") else 0

    total = vids + assigns + sum(certs_dict.values()) + star_marks
    total = min(max(total, 0), 100)
    pct = total
    grd = grade(pct)
    res = "PASS" if pct >= 33 else "FAIL"

    students.append({
        "name": name,
        "VITYARTHI videos": vids,
        "VITYARTHI vid_marks": vids,
        "assignments": assigns,
        "assignment_marks": assigns,
        "certs": certs_dict,
        "cert_days": days_dict,
        "submitted": sub,
        "star": star_marks,
        "total": total,
        "pct": pct,
        "grade": grd,
        "result": res,
        "frozen": False
    })

    loading("Adding student")
    print(col("Student added successfully!\n", C_OK))

# To View all
def view_all():
    if not students:
        print(col("No students.\n", C_WARN))
        return

    loading("Fetching all students")
    print(col("\n--- All Students ---", C_HDR))
    sorted_students = sorted(students, key=lambda x: x["total"], reverse=True)
    for i, s in enumerate(sorted_students, 1):
        tag = " (FROZEN)" if s.get("frozen") else ""
        colr = C_OK if s["result"] == "PASS" else C_ERR
        print(f"{i}. {s['name']}{tag} - {s['total']}/100 - {col(s['result'], colr)}")
    print()

# Detailed Report
def detailed_report():
    if not students:
        print(col("No students.\n", C_WARN))
        return
    name = input("Student name: ").strip()
    for s in students:
        if s["name"].lower() == name.lower():
            loading("Generating report")
            print(col("\n------------- STUDENT REPORT -------------", C_HDR))
            print(f"Name: {s['name']}")
            print(f"VITYARTHI: {s['VITYARTHI videos']} ×1 = {s['VITYARTHI vid_marks']} / 15")
            print(f"Assignments: {s['assignments']} ×1 = {s['assignment_marks']} / 25\n")
            print(col("Certificates (10 marks each):", C_BOLD))

            assigned_str = assigned_date.strftime("%d-%m-%Y") if assigned_date else "N/A"
            submitted_str = s["submitted"].strftime("%d-%m-%Y") if s["submitted"] else "Not submitted"
            print(f"Assigned date: {assigned_str}\nStudent submitted: {submitted_str}")

            for c, sc in s["certs"].items():
                d = s["cert_days"][c]
                if d is None:
                    print(f" - {c}: NOT SUBMITTED → 0 /10")
                else:
                    print(f" - {c}: {d} day(s) late → {sc} /10")

            print(f"\nHackerRank 5-star: {s['star']} /10")
            print(col(f"\nTOTAL: {s['total']} /100", C_HDR))
            print(f"PERCENTAGE: {s['pct']}%")
            print(f"GRADE: {s['grade']}")
            print(f"STATUS: {col(s['result'], C_OK if s['result'] == 'PASS' else C_ERR)}")

            if s.get("frozen"):
                print(col("NOTE: This student is FROZEN and cannot be edited.", C_WARN))

            print(col("------------------------------------------\n", C_HDR))
            return
    print(col("Student not found.\n", C_WARN))

# Edit student
def edit_student():
    if not students:
        print(col("No students.\n", C_WARN))
        return
    name = input("Name to edit: ").strip()
    for s in students:
        if s["name"].lower() == name.lower():
            if s.get("frozen"):
                print(col("Sorry you cant edit, Record has been frozen.\n", C_WARN))
                return

            print(col("Leave it blank to keep value.", C_HDR))
            new_name = input(f"Name ({s['name']}): ").strip()
            if new_name:
                s['name'] = new_name

            # Videos
            v = input(f"Videos ({s['VITYARTHI videos']}): ").strip()
            if v:
                try:
                    s['VITYARTHI videos'] = min(int(v), 15)
                except ValueError:
                    pass
            s['VITYARTHI vid_marks'] = s['VITYARTHI videos']

            # Assignments
            a = input(f"Assignments ({s['assignments']}): ").strip()
            if a:
                try:
                    s['assignments'] = min(int(a), 25)
                except ValueError:
                    pass
            s['assignment_marks'] = s['assignments']

            # Certificate submission date
            nd = input("New submission date (In DD-MM-YYYY Format) or blank: ").strip()
            if nd:
                try:
                    d = datetime.datetime.strptime(ns, "%d-%m-%Y").date()
                    s['submitted'] = d
                    days = max((d - assigned_date).days, 0)
                    for c in s['certs']:
                        s['certs'][c] = cert_score(days)
                        s['cert_days'][c] = days
                except ValueError:
                    print(col("Invalid date format, skipped.", C_WARN))

            # HackerRank 5-star
            star = input(f"5-star? (yes/no) ({'yes' if s['star'] == 10 else 'no'}): ").strip().lower()
            if star:
                s['star'] = 10 if star.startswith("y") else 0

            # Recalculate total
            s['total'] = min(s['VITYARTHI vid_marks'] + s['assignment_marks'] + sum(s['certs'].values()) + s['star'], 100)
            s['pct'] = s['total']
            s['grade'] = grade(s['pct'])
            s['result'] = "PASS" if s['pct'] >= 33 else "FAIL"

            loading("Updating student")
            print(col("Updated.\n", C_OK))
            return
    print(col("Student not found.\n", C_WARN))

# Freeze/Defreeze Student
def freeze_unfreeze():
    if not students:
        print(col("No students.\n", C_WARN))
        return
    name = input("Name to freeze/unfreeze: ").strip()
    for s in students:
        if s['name'].lower() == name.lower():
            s['frozen'] = not s.get('frozen', False)
            loading("Updating student status")
            print(col(f"{'Frozen' if s['frozen'] else 'Unfrozen'}: {s['name']}\n", C_OK))
            return
    print(col("Student not found.\n", C_WARN))

# Search by initial
def search_initial():
    if not students:
        print(col("No students.\n", C_WARN))
        return
    ch = input("Starting letter: ").strip().lower()
    if not ch:
        print(col("No letter.\n", C_WARN))
        return
    found = [s for s in students if s['name'].lower().startswith(ch)]
    if not found:
        print(col("No matches.\n", C_WARN))
        return
    print(col(f"\nStudents name starting with '{ch.upper()}':", C_HDR))
    for s in found:
        print(f"- {s['name']} - {s['total']}/100 - {col(s['result'], C_OK if s['result'] == 'PASS' else C_ERR)}")
    print()

# Main Menu
def main():
    login()
    ensure_assigned()
    while True:
        print(col("\nMenu:", C_BOLD + C_HDR))
        print("1) Add student")
        print("2) View all students")
        print("3) Detailed report")
        print("4) Edit report")
        print("5) Freeze/unfreeze student")
        print("6) Search by initial letter")
        print("7) Exit")
        ch = input("Choose (1-7): ").strip()
        if ch == "1":
            add_student()
        elif ch == "2":
            view_all()
        elif ch == "3":
            detailed_report()
        elif ch == "4":
            edit_student()
        elif ch == "5":
            freeze_unfreeze()
        elif ch == "6":
            search_initial()
        elif ch == "7":
            print(col("\nGoodbye!\n", C_HDR))
            break
        else:
            print(col("Invalid choice.\n", C_WARN))

if __name__ == "__main__":
    main()