# controllers/employee_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.employee_model import employees

employee_bp = Blueprint("employee_bp", __name__)


# READ ALL -> GET /employees
@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(employees), 200


# READ ONE -> GET /employees/<id>
@employee_bp.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    for employee in employees:
        if employee["id"] == id:
            return jsonify(employee), 200
    return jsonify({"error": "Employee tidak ditemukan"}), 404


# FORM TAMBAH EMPLOYEE
@employee_bp.route("/employees/new", methods=["GET"])
def show_form():
    return render_template("form.html", employees=employees)


# SIMPAN EMPLOYEE BARU
@employee_bp.route("/employees/new", methods=["POST"])
def submit_form():
    name = request.form.get("name", "").strip()
    position = request.form.get("position", "Staff").strip() or "Staff"
    salary = request.form.get("salary", "0")

    if not name:
        return "Nama wajib diisi!", 400

    try:
        salary_value = int(salary or 0)
        if salary_value < 0:
            return "Gaji tidak boleh negatif!", 400
    except ValueError:
        return "Gaji harus berupa angka!", 400

    new_id = max((e["id"] for e in employees), default=0) + 1
    employees.append({
        "id": new_id,
        "name": name,
        "position": position,
        "salary": salary_value,
    })
    return redirect(url_for("employee_bp.show_form"))


# TAMPILKAN FORM UPDATE
@employee_bp.route("/employees/<int:id>/edit", methods=["GET"])
def edit_form(id):
    employee = next((e for e in employees if e["id"] == id), None)
    if employee is None:
        return "Employee tidak ditemukan", 404
    return render_template("edit_employee.html", employee=employee)


# PROSES UPDATE EMPLOYEE
@employee_bp.route("/employees/<int:id>/edit", methods=["POST"])
def update_employee(id):
    employee = next((e for e in employees if e["id"] == id), None)
    if employee is None:
        return "Employee tidak ditemukan", 404

    name = request.form.get("name", "").strip()
    position = request.form.get("position", "Staff").strip() or "Staff"
    salary = request.form.get("salary", "0")

    if not name:
        return "Nama wajib diisi!", 400

    try:
        salary_value = int(salary or 0)
        if salary_value < 0:
            return "Gaji tidak boleh negatif!", 400
    except ValueError:
        return "Gaji harus berupa angka!", 400

    employee["name"] = name
    employee["position"] = position
    employee["salary"] = salary_value
    return redirect(url_for("employee_bp.show_form"))


# DELETE EMPLOYEE
@employee_bp.route("/employees/<int:id>/delete", methods=["POST"])
def delete_employee(id):
    employee = next((e for e in employees if e["id"] == id), None)
    if employee is None:
        return "Employee tidak ditemukan", 404

    employees.remove(employee)
    return redirect(url_for("employee_bp.show_form"))
