<div align="center">

# 🎓 Academy Lab - Odoo 18

### Complete Training Academy Management System

[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-blue.svg)](https://www.odoo.com)
[![License](https://img.shields.io/badge/License-LGPL--3-green.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

*A comprehensive academy management addon for Odoo 18 with advanced features including course management, enrollment workflows, commercial integration, and intelligent reporting.*

[Features](#-features) • [Installation](#-installation) • [Documentation](#-documentation) • [Testing](#-testing)

---

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Module Architecture](#-module-architecture)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [User Guide](#-user-guide)
- [Security & Access Control](#-security--access-control)
- [Commercial Integration](#-commercial-integration)
- [Reports](#-reports)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

---

## 🌟 Overview

**Academy Lab** is a professional Odoo 18 addon designed to manage training academies, educational institutions, and course providers. It provides a complete solution for:

- 📚 **Course Management** - Create, publish, and manage courses with lifecycle states
- 👥 **Enrollment System** - Track student enrollments with automated workflows
- 💰 **Sales Integration** - Sell courses as products with automated enrollment
- 📊 **Advanced Reporting** - Generate enrollment reports and student transcripts
- 🔒 **Role-Based Security** - Fine-grained access control for students, instructors, and managers
- 📧 **Communication** - Built-in chatter for collaboration and tracking

---

## 🚀 Key Features

### Core Functionality

<table>
<tr>
<td width="50%">

#### 📚 Course Management
- Multi-state lifecycle
- Automatic seat calculation
- Course categorization
- Instructor assignment
- Smart buttons
- Kanban & List views
- Built-in chatter

</td>
<td width="50%">

#### 🎓 Enrollment System
- Automated workflows
- Grade tracking
- Attendance tracking
- Pass/Fail computation
- Duplicate prevention
- Capacity validation
- Invoice linking

</td>
</tr>
<tr>
<td width="50%">

#### 👤 Partner Integration
- Student & Instructor flags
- Enrollment history
- Teaching portfolio
- Academy tab
- Smart buttons
- Transcript printing

</td>
<td width="50%">

#### 💼 Commercial Features
- Product generation wizard
- Auto-enrollment on SO
- Auto-confirm on invoice
- Sales integration
- Invoice linking
- Revenue tracking

</td>
</tr>
</table>

### 📊 Advanced Reporting

| Report | Description | Access |
|--------|-------------|--------|
| **Enrollment Report** | Date-filtered with statistics | Manager, Instructor |
| **Student Transcript** | Academic record with GPA | Student (own), Manager (all) |

---

## 🏗️ Module Architecture

### File Structure

```
academy_lab/
├── __init__.py
├── __manifest__.py
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── academy_course.py
│   ├── academy_course_category.py
│   ├── academy_enrollment.py
│   ├── res_partner.py
│   ├── product_template.py
│   ├── sale_order.py
│   └── account_move.py
│
├── wizard/
│   ├── __init__.py
│   ├── academy_product_wizard.py
│   ├── academy_product_wizard_view.xml
│   ├── enrollment_report_wizard.py
│   └── enrollment_report_wizard_view.xml
│
├── reports/
│   ├── __init__.py
│   ├── report_actions.xml
│   ├── report_templates.xml
│   ├── enrollment_report.py
│   ├── student_transcript_report.py
│   └── student_transcript_template.xml
│
├── views/
│   ├── academy_actions.xml
│   ├── academy_course_views.xml
│   ├── academy_category_views.xml
│   ├── academy_enrollment_views.xml
│   └── res_partner_views.xml
│
├── security/
│   ├── academy_security.xml
│   ├── ir.model.access.csv
│   └── academy_record_rules.xml
│
└── static/
    └── description/
        ├── icon.png
        └── index.html
```

### Data Model

```
res.partner                    academy.course
┌──────────────┐              ┌───────────────┐
│ Students     │◄─────────────┤ Enrollments   │
│ Instructors  │  student_id  │ Courses       │
│              │              │               │
│ • is_student │              │ • name        │
│ • enrollments│              │ • code        │
│ • courses    │              │ • max_students│
└──────┬───────┘              │ • state       │
       │                      │ • product_id  │
       │                      └───────┬───────┘
       │ instructor_id                │
       └──────────────────────────────┘

academy.enrollment            product.template
┌───────────────┐            ┌──────────────┐
│ • student_id  │            │ Service      │
│ • course_id   │◄───────────┤ Products     │
│ • grade       │ product_id │              │
│ • attendance  │            │ • course_id  │
│ • passed      │            │ • list_price │
│ • invoice_id  │            └──────────────┘
│ • state       │
└───────┬───────┘
        │
        │                   sale.order
        │                   ┌──────────┐
        │                   │ Orders   │
        │                   └────┬─────┘
        │                        │
        │                   account.move
        └───────────────────┤ Invoices │
               invoice_id   └──────────┘
```

---

## 📦 Installation Guide

### Prerequisites

- Odoo 18.0+
- Python 3.10+
- Required modules: base, mail, contacts, sale, account

### Installation Steps

#### 1️⃣ Copy Module

```bash
cd /path/to/odoo/addons/
cp -r academy_lab/ .
```

#### 2️⃣ Restart Odoo

```bash
docker compose restart
# OR
sudo systemctl restart odoo
```

#### 3️⃣ Install

1. Settings → Activate Developer Mode
2. Apps → Update Apps List
3. Search "Academy Lab"
4. Click Install

---

## ⚙️ Configuration

### Create User Groups

| User | Group | Email |
|------|-------|-------|
| Ahmed | Academy / Student | student@test.com |
| Sara | Academy / Instructor | instructor@test.com |
| Admin | Academy / Manager | manager@test.com |

### Create Sample Course

```
Name: Python Programming
Code: PY101
Max Students: 20
State: Published
```

---

## 👥 User Guide

### For Students

#### View Courses
- Academy → Courses (Published only)

#### Enroll
- Via Sales Order → Auto-enrollment

#### Check Progress
- Academy → My Enrollments
- View grade, attendance, pass status

#### Print Transcript
- Contacts → Self → Academy Tab → Print Transcript

---

### For Instructors

#### Manage Courses
- Create courses
- Generate products
- Track enrollments

#### Grade Students
- Academy → Enrollments
- Enter grade & attendance
- Passed auto-computed: (grade ≥ 60) AND (attendance ≥ 75)

---

### For Managers

#### Full Access
- All CRUD operations
- Configuration menu
- All reports
- All transcripts

---

## 🔒 Security & Access Control

### Groups Hierarchy

```
Academy / Manager
  ↓ implies
Academy / Instructor
  ↓ implies
Academy / Student
  ↓ implies
Employee
```

### Access Matrix

| Model | Student | Instructor | Manager |
|-------|---------|------------|---------|
| Course | Read | Full | Full |
| Category | Read | Read | Full |
| Enrollment | Read+Create | Read+Write | Full |

### Record Rules

- Students: Published courses only, own enrollments only
- Instructors: All courses, all enrollments (read-only)
- Managers: Everything

---

## 💼 Commercial Integration

### Flow

```
1. Course → Generate Product
   ↓
2. Sales Order (with product) → Confirm
   ↓ AUTO-CREATE
3. Enrollment (Draft state)
   ↓
4. Invoice → Post
   ↓ AUTO-CONFIRM
5. Enrollment (Confirmed + invoice linked)
```

### Technical Details

**sale_order.py - action_confirm override:**
- Loops through order lines
- Creates enrollment for products linked to courses
- Prevents duplicates

**account_move.py - action_post override:**
- Loops through invoice lines
- Finds matching enrollment
- Confirms enrollment + links invoice

---

## 📊 Reports

### 1️⃣ Enrollment Report

**Access:** Academy → Enrollments → Print Report

**Features:**
- Date range filter
- Course filter
- Statistics per course
- PDF output

**Implementation:**
- Wizard: TransientModel
- Report: AbstractModel
- Template: QWeb

---

### 2️⃣ Student Transcript

**Access:** Partner → Academy Tab → Print Transcript

**Features:**
- All enrollments
- Statistics (total courses, avg grade)
- Top 3 courses (by grade)
- Full history

**Access Control:**
- Students: Own only
- Managers: Any student
- Built-in security check in AbstractModel

**Code Example:**

```python
class StudentTranscriptReport(models.AbstractModel):
    _name = 'report.academy_lab.student_transcript_template'

    def _get_report_values(self, docids, data=None):
        # Security check
        if self.env.user.has_group('academy_lab.academy_group_student'):
            for student in students:
                if student.id != self.env.user.partner_id.id:
                    raise AccessError("Own transcript only!")

        # Calculate stats
        enrollments = ...
        avg_grade = ...
        top_3 = ...

        return {...}
```

---

## 🧪 Testing

### Course Constraints

```python
# End date validation
course.end_date < course.start_date  # ❌ Error

# Max students > 0
course.max_students = 0  # ❌ Error

# Unique code
duplicate_code  # ❌ IntegrityError
```

### Enrollment Validation

```python
# Course full
course.max_students = 1
confirm_enrollment_1  # ✅
confirm_enrollment_2  # ❌ "Course is full"

# Duplicate
same_student + same_course  # ❌ IntegrityError
```

### Computed Fields

```python
# Passed
grade = 60, attendance = 75  # ✅ passed = True
grade = 59, attendance = 75  # ❌ passed = False
```

### Commercial Flow

```python
1. Create Course
2. Generate Product
3. Create SO → Confirm  # ✅ Enrollment created (draft)
4. Create Invoice → Post  # ✅ Enrollment confirmed
5. Check enrollment.invoice_id  # ✅ Linked
```

---

## 🐛 Troubleshooting

### Module Not Appearing
```bash
# Check path
ls /path/to/addons/ | grep academy_lab

# Restart
docker compose restart

# Update list (Developer Mode)
Apps → Update Apps List
```

### Access Denied
- Check user groups assignment
- Verify record rules
- Check access rights CSV

### Report Not Generating
```bash
# Check wkhtmltopdf
which wkhtmltopdf

# Install if missing
sudo apt-get install wkhtmltopdf
```

### Commercial Integration
- Verify sale & account modules installed
- Check method overrides
- Verify product.course_id link

---

## 📚 API Reference

### Course Model

```python
academy.course
- name (Char, required)
- code (Char, required, unique)
- max_students (Integer)
- state (Selection)
- enrolled_count (Integer, computed, stored)
- available_seats (Integer, computed, stored)
- is_full (Boolean, computed, stored)

Methods:
- action_publish()
- action_start()
- action_done()
- action_cancel()
```

### Enrollment Model

```python
academy.enrollment
- student_id (Many2one res.partner, required)
- course_id (Many2one academy.course, required)
- grade (Float)
- attendance_percentage (Float)
- passed (Boolean, computed, stored)
- invoice_id (Many2one account.move)
- state (Selection)

Methods:
- action_confirm()
- action_complete()
- action_cancel()
```

---

## 📝 Changelog

### v18.0.1.0.0 (2026-01-03)

#### Features
- Complete course management
- Enrollment workflows
- Commercial integration
- Enrollment report with wizard
- Student transcript with access control
- Role-based security
- Partner extension
- Smart buttons

#### Security
- Record rules
- Access rights
- Transcript access control

#### Reports
- Enrollment Report (wizard)
- Student Transcript
- QWeb templates
- Statistics



<div align="center">

### ⭐ Star this repository if you find it useful! ⭐

**Made with ❤️ for Odoo 18**

</div>
