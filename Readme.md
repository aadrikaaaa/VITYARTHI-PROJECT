# Student Grading App (Python CLI)

A simple, interactive command-line **grading system** built using Python.  
This application allows an administrator to:

- Add student records  
- Calculate grades based on videos, assignments, certificates, and HackerRank stars  
- Generate detailed reports  
- Freeze/unfreeze records  
- Edit existing data  
- View all students sorted by total marks  
- Search students by initial letter  

All data is stored in runtime (no database required).

---

## Features

### 🔐 Admin Login
- Secure login using the password: **vtop**
- Provides a password hint on incorrect attempts.

### 📝 Student Data Stored
Each student record stores:
- Name  
- VITYARTHI lecture videos  
- Assignments completed  
- Certificate submission date  
- HackerRank 5-star achievement  
- Total score  
- Percentage  
- Grade  
- Pass/Fail status  

---

## Certificate Scoring Logic

Certificate marks depend on how many days late they were submitted:

| Days Late | Score |
|----------:|------:|
| 0         | 10    |
| 1         | 9     |
| 2         | 8     |
| 3         | 7     |
| 4         | 6     |
| 5–10      | 5     |
| >10       | 2     |
| Not Submitted | 0 |

---

## Grade Calculation

| Percentage | Grade |
|-----------|--------|
| ≥ 90      | A      |
| ≥ 75      | B      |
| ≥ 60      | C      |
| ≥ 33      | D      |
| < 33      | F      |

---

## Main Menu Options

1. Add Student  
2. View All Students  
3. Detailed Report  
4. Edit Report  
5. Freeze/Unfreeze Student  
6. Search by Initial  
7. Exit  

Frozen students **cannot be edited** until unfrozen.

---

## How to Run

### 1. Clone or download the script
```bash
git clone <your-repo-url>
cd grading-app
```

### 2. Run the program
```bash
python3 finalmain.py
```

## Dependencies

Uses only standard Python libraries:
- datetime
- time
- getpass

No external modules required.