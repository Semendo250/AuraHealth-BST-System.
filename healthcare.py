from flask import Flask, render_template, request, redirect, url_for, flash


# --- THE ENGINE (Binary Search Tree) ---


class PatientNode:
    def __init__(self, patient_id, patient_name):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.left = None
        self.right = None


class PatientBST:
    def __init__(self):
        self.root = None

    def insert(self, patient_id, patient_name):
        if self.root is None:
            self.root = PatientNode(patient_id, patient_name)
        else:
            self._insert_recursive(self.root, patient_id, patient_name)

    def _insert_recursive(self, current, patient_id, patient_name):
        if patient_id < current.patient_id:
            if current.left is None:
                current.left = PatientNode(patient_id, patient_name)
            else:
                self._insert_recursive(current.left, patient_id, patient_name)
        elif patient_id > current.patient_id:
            if current.right is None:
                current.right = PatientNode(patient_id, patient_name)
            else:
                self._insert_recursive(current.right, patient_id, patient_name)

    def search(self, current, patient_id):
        # Base Case: Not found or empty tree
        if current is None:
            return None
        # Success Case: Found the patient
        if current.patient_id == patient_id:
            return current
        # Recursive Case: Go left or right
        if patient_id < current.patient_id:
            return self.search(current.left, patient_id)
        else:
            return self.search(current.right, patient_id)

    def get_inorder(self, current, report_list):
        if current:
            self.get_inorder(current.left, report_list)
            report_list.append({"id": current.patient_id, "name": current.patient_name})
            self.get_inorder(current.right, report_list)
        return report_list


# --- THE BRIDGE (Flask Application) ---

app = Flask(__name__)
app.secret_key = "aura_health_key_2024"  # Required for flash messages
hospital_system = PatientBST()
app = Flask(__name__)
app.secret_key = "any_random_string_here" # <--- THIS MUST BE THERE


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/insert', methods=['POST'])
def insert():
    p_id = request.form.get('patient_id')
    p_name = request.form.get('patient_name')

    if p_id and p_name:
        hospital_system.insert(int(p_id), p_name)
        flash(f"✅ Patient {p_name} (ID: {p_id}) registered successfully!")

    return redirect(url_for('home'))


@app.route('/patients')
def show_patients():
    report = []
    # Fetch all patients from the BST in sorted order
    all_patients = hospital_system.get_inorder(hospital_system.root, report)
    return render_template('patients.html', patients=all_patients)


@app.route('/search', methods=['POST'])
def search():
    search_id = request.form.get('search_id')

    if search_id and search_id.isdigit():
        target_id = int(search_id)
        result = hospital_system.search(hospital_system.root, target_id)

        if result:
            flash(f"🔍 Found: {result.patient_name} is registered under ID {result.patient_id}")
        else:
            flash(f"❌ ID {target_id} was not found in the system.")

    return redirect(url_for('show_patients'))


import os

# ... rest of your code ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
