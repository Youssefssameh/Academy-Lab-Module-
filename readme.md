# Academy Lab (academy_lab) — Odoo 18 Addon

Training Academy Management System built as an Odoo 18 addon. [file:2]  
The module manages Courses, Categories, and Enrollments with role-based security, state workflows, computed fields, validations, and commercial integration with Sales & Invoicing. [file:2]

---

## Features

### Courses (`academy.course`)
- Course lifecycle states: Draft → Published → In Progress → Done / Cancelled.
- Computed fields (stored):
  - Enrolled Count (based on confirmed enrollments).
  - Available Seats (`max_students - enrolled_count`).
  - Is Full (`available_seats <= 0`).
- Constraints:
  - End date must be >= start date.
  - `max_students` must be > 0.
  - Course code is unique and normalized to uppercase.
- UI:
  - List view with decorations.
  - Form view with statusbar, smart button for enrollments, and chatter.
  - Kanban view.
- Commercial fields:
  - `product_id` (Many2one to `product.product`, readonly) to link the course to a sellable Service Product. [file:2]
- Smart buttons:
  - **Sales**: opens Sales Orders that contain the product linked to this course. [file:2]

### Categories (`academy.course.category`)
- Stores category details and related courses.
- Computed stored counter of courses.

### Enrollments (`academy.enrollment`)
- Enrollment workflow: Draft → Confirmed → Completed / Cancelled.
- Validations:
  - Prevent confirming enrollment when the course is full.
  - Prevent duplicate enrollments (same student + same course) via SQL constraint.
- Computed stored field:
  - Passed = (`grade >= 60`) AND (`attendance >= 75`).
- Commercial fields:
  - `invoice_id` (Many2one to `account.move`, readonly) links the enrollment to the posted invoice. [file:2]
- UI:
  - List, Search (My Enrollments / Confirmed / Completed), and Form with statusbar and chatter.
- Smart buttons:
  - **Invoice**: opens the related Invoice form view; visible only if `invoice_id` is set. [file:2]

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

---

## Commercial Integration (Sales & Invoicing)

This module integrates Courses with Odoo Sales and Accounting to support selling courses and validating enrollments based on payments. [file:2]

### Configuration
- Update `__manifest__.py` dependencies to include:
  - `sale`
  - `account` [file:2]

### Product Generation Wizard
- Wizard: `academy.product.wizard` (TransientModel) with fields:
  - `name` (Char, required)
  - `price` (Float, required) [file:2]
- Course form header button: **Generate Product**
  - Opens the wizard in a popup (`target="new"`).
  - Prefills the wizard `name` from the course name. [file:2]
- Wizard behavior (Create):
  - Creates a new `product.product` as a Service with the provided name and list price.
  - Links product ↔ course via:
    - `academy.course.product_id`
    - `product.template.course_id` [file:2]

### Automated Enrollment on Sales Confirmation
- Override `sale.order.action_confirm`:
  - After confirmation, for each order line whose product is linked to a course, create a new `academy.enrollment`.
  - Enrollment is created for the Sales Order customer (`partner_id`) and starts in draft (or a custom unpaid state).
  - Prevent duplicate enrollments for the same student in the same course. [file:2]

### Enrollment Confirmation on Invoice Post
- Override `account.move.action_post`:
  - After posting, check invoice lines for products linked to courses.
  - Find the corresponding enrollment (matching Student + Course).
  - Set enrollment state to `confirmed` and link the posted invoice into `invoice_id`. [file:2]

---

## Module Info
- Name: `academy_lab`
- Version: `18.0.1.0.0`
- Dependencies: `base`, `mail`, `contacts`, `sale`, `account`. [file:2]

---

## Installation
1. Copy `academy_lab` into your Odoo addons path.
2. Restart Odoo server.
3. Activate Developer Mode.
4. Apps → Update Apps List.
5. Install **Academy Lab**.

---

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

---

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

> Record Rules enforce data visibility; Access Rights (ACL) enforce CRUD permissions.

---

## Quick Testing Checklist

Create 3 users:
- User A: Student
- User B: Instructor
- User C: Manager

Test scenarios:
- Student can only see published courses.
- Student can only see/edit own enrollments.
- Instructor can create/edit courses but cannot edit enrollments.
- Manager can see Configuration menu and has full CRUD.

Course full scenario:
- Set `max_students = 1`
- Confirm 1 enrollment
- Confirm 2nd enrollment → must fail

Duplicate enrollment:
- Create same student + same course twice → must fail

Passed computation:
- `grade = 60` & `attendance = 75` → `passed = True`
- Decrease any value below threshold → `passed = False`

Commercial flow:
- Create a Course → Generate Product.
- Create a Sales Order with that product → Confirm SO → Draft enrollment created.
- Create invoice from SO → Post invoice → Enrollment becomes Confirmed and `invoice_id` is linked. [file:2]

---

## Notes
- All views use Odoo 18 `<list>` syntax (not `<tree>`).
- Chatter is enabled on courses and enrollments via `mail.thread` and `mail.activity.mixin`.
