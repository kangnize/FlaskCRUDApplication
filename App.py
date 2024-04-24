from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
db = SQLAlchemy(app)

# Define Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

# Ensure app context is set up before calling db.create_all()
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        new_employee = Employee(name=name, email=email, phone=phone)
        
        try:
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to the index page after adding employee
        except Exception as e:
            flash(f'An error occurred while adding employee: {str(e)}', 'danger')
            db.session.rollback()  # Rollback changes if an error occurs

    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        try:
            employee.name = request.form['name']
            employee.email = request.form['email']
            employee.phone = request.form['phone']
        
            db.session.commit()
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to the index page after editing employee
        except Exception as e:
            flash(f'An error occurred while editing employee: {str(e)}', 'danger')
            db.session.rollback()  # Rollback changes if an error occurs

    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('index'))  # Redirect to the index page after deleting employee

if __name__ == "__main__":
    app.run(debug=True)
