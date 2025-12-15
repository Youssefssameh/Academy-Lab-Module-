# Academy Lab (academy_lab) — Odoo 18 Addon

Training Academy Management System built as an Odoo 18 addon.  
The module manages Courses, Categories, and Enrollments with role-based security, state workflows, computed fields, and validations.

## Features

### Courses (`academy.course`)
- Course lifecycle states: Draft → Published → In Progress → Done / Cancelled.
- Computed fields (stored):
  - Enrolled Count (based on confirmed enrollments).
  - Available Seats (max_students - enrolled_count).
  - Is Full (available_seats <= 0).
- Constraints:
  - End date must be >= start date.
  - max_students must be > 0.
  - Course code is unique and normalized to uppercase.
- UI:
  - List view with decorations.
  - Form view with statusbar, smart button for enrollments, and chatter.
  - Kanban view.

### Categories (`academy.course.category`)
- Stores category details and related courses.
- Computed stored counter of courses.

### Enrollments (`academy.enrollment`)
- Enrollment workflow: Draft → Confirmed → Completed / Cancelled.
- Validations:
  - Prevent confirming enrollment when the course is full.
  - Prevent duplicate enrollments (same student + same course) via SQL constraint.
- Computed stored field:
  - Passed = (grade >= 60) AND (attendance >= 75).
- UI:
  - List, Search (My Enrollments / Confirmed / Completed), and Form with statusbar and chatter.

### Partner Extension (`res.partner`)
- Flags:
  - Is Student
  - Is Instructor
- Relations:
  - Student Enrollments
  - Instructor Courses
- Smart buttons:
  - Total Courses Enrolled
  - Total Courses Teaching
- Academy tab added to partner form.

## Module Info
- Name: `academy_lab`
- Version: `18.0.1.0.0`
- Dependencies: `base`, `mail`, `contacts`

## Installation
1. Copy `academy_lab` into your Odoo addons path.
2. Restart Odoo server.
3. Activate Developer Mode.
4. Apps → Update Apps List.
5. Install **Academy Lab**.

## Menu Structure
Academy (root)
- Courses
  - Courses
  - Categories
- Enrollments
  - All Enrollments
  - My Enrollments
- Configuration (Manager only)
  - (Optional) Configuration submenus for manager

## Security & Access Control

### Groups
- Academy / Student
- Academy / Instructor (implies Student)
- Academy / Manager (implies Instructor)

### Access Rules Summary
- Students:
  - Can only view published courses.
  - Can create/read/update only their own enrollments.
- Instructors:
  - Can manage courses.
  - Can read enrollments (read-only).
- Managers:
  - Full access to all models and configuration menu.

> Note: Record Rules enforce data visibility; Access Rights (ACL) enforce CRUD permissions.

## Quick Testing Checklist
Create 3 users:
- User A: Student
- User B: Instructor
- User C: Manager

Test scenarios:
1. Student can only see published courses.
2. Student can only see/edit own enrollments.
3. Instructor can create/edit courses but cannot edit enrollments.
4. Manager can see Configuration menu and has full CRUD.
5. Course full scenario:
   - Set max_students=1
   - Confirm 1 enrollment
   - Confirm 2nd enrollment → must fail
6. Duplicate enrollment:
   - Create same student + same course twice → must fail
7. Passed computation:
   - grade=60 & attendance=75 → passed=True
   - decrease any value below threshold → passed=False

## Notes
- All views use Odoo 18 `<list>` syntax (not `<tree>`).
- Chatter is enabled on courses and enrollments via `mail.thread` and `mail.activity.mixin`.
