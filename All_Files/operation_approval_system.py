import random

class Patient:
    def __init__(self, name, age, gender, blood_type):
        self.name = name
        self.age = age
        self.gender = gender
        self.blood_type = blood_type

class OperationApprovalSystem:
    def __init__(self):
        self.patients = []

    def add_patient(self, patient):
        """Add a patient to the list of patients."""
        self.patients.append(patient)

    def can_undergo_operation(self, patient):
        """Check if a patient is eligible for the operation."""
        # Criteria for approval:
        # 1. Age >= 18
        # 2. Male gender or female gender
        if patient.age >= 18:
            return True
        else:
            return False

    def evaluate_patients(self):
        """Evaluate each patient for operation eligibility."""
        for i, patient in enumerate(self.patients, start=1):
            print(f"Evaluated Patient {i}:")
            print("-" * 20)
            print(f"Name: {patient.name}")
            print(f"Age: {patient.age}")
            print(f"Gender: {patient.gender}")
            print(f"Blood Type: {patient.blood_type}")

            if self.can_undergo_operation(patient):
                if self.is_blood_type_okay(patient.blood_type):
                    print(f"Result: {patient.name} is approved for the operation.")
                else:
                    print(f"Result: {patient.name} is not approved for the operation due to incompatible blood type ({patient.blood_type}).")
            else:
                reasons = []
                # Check individual criteria for rejection
                if patient.age < 18:
                    reasons.append("age under 18")

                print(f"Result: {patient.name} is not approved for the operation due to the following reasons: {' and '.join(reasons)}.")
            print()  # empty line for better readability

    def is_blood_type_okay(self, blood_type):
        """Check if the patient's blood type is compatible for the operation."""
        # Example: Assume only certain blood types are compatible for the operation
        # You can implement more sophisticated checks here
        if blood_type in ["A+", "B+", "AB+", "O+"]:
            return True
        else:
            return False

# Example usage
approval_system = OperationApprovalSystem()

# Input the number of patients
num_patients = int(input("Enter the number of patients to generate and evaluate: "))

# Generate patients with user-specified characteristics
for i in range(num_patients):
    name = f"Patient{i+1}"
    age = random.randint(1, 80)  # Random age between 1 and 80
    gender = random.choice(["male", "female"])  # Random gender
    blood_type = random.choice(["A+", "B+", "AB+", "O+", "A-", "B-", "AB-", "O-"])  # Random blood type
    approval_system.add_patient(Patient(name, age, gender, blood_type))

# Evaluating patients
approval_system.evaluate_patients()
