import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QListWidget, QStyleFactory

class ContactManagementSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contact Management System")
        self.setGeometry(100, 100, 800, 600)

        self.contacts = []
        self.load_contacts()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_label.setStyleSheet("font-weight: bold;")
        self.name_entry = QLineEdit()

        self.phone_label = QLabel("Phone:")
        self.phone_label.setStyleSheet("font-weight: bold;")
        self.phone_entry = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_label.setStyleSheet("font-weight: bold;")
        self.email_entry = QLineEdit()

        self.add_button = QPushButton("Add Contact")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.add_button.clicked.connect(self.add_contact)

        self.list_button = QPushButton("List Contacts")
        self.list_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.list_button.clicked.connect(self.list_contacts)

        self.update_button = QPushButton("Update Contact")
        self.update_button.setStyleSheet("background-color: #FFC107; color: white;")
        self.update_button.clicked.connect(self.update_contact)

        self.delete_button = QPushButton("Delete Contact")
        self.delete_button.setStyleSheet("background-color: #F44336; color: white;")
        self.delete_button.clicked.connect(self.delete_contact)

        self.contact_list = QListWidget()
        self.contact_list.setStyleSheet("font-weight: bold;")
        self.contact_list.itemClicked.connect(self.select_contact)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_entry)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_entry)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_entry)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.list_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.contact_list)

        self.central_widget.setLayout(self.layout)

        self.selected_index = -1  # To track the selected index in the contact list

    def load_contacts(self):
        try:
            with open("contacts.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 3:
                        name, phone, email = values
                        contact = {'name': name, 'phone': phone, 'email': email}
                        self.contacts.append(contact)
                    else:
                        print(f"Ignored line: {line.strip()}")  # Handle improperly formatted lines
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("contacts.txt", "w") as file:
            for index, contact in enumerate(self.contacts):
                file.write(f"{index},{contact['name']},{contact['phone']},{contact['email']}\n")

    def add_contact(self):
        name = self.name_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()

        if name and phone and email:
            contact = {'name': name, 'phone': phone, 'email': email}
            self.contacts.append(contact)
            self.save_contacts()
            QMessageBox.information(self, "Success", f"Contact {name} added successfully!")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")

    def list_contacts(self):
        self.contact_list.clear()
        for contact in self.contacts:
            self.contact_list.addItem(contact['name'])

    def select_contact(self, item):
        self.selected_index = self.contact_list.currentRow()
        if 0 <= self.selected_index < len(self.contacts):
            contact = self.contacts[self.selected_index]
            self.name_entry.setText(contact['name'])
            self.phone_entry.setText(contact['phone'])
            self.email_entry.setText(contact['email'])

    def update_contact(self):
        if self.selected_index != -1:
            name = self.name_entry.text()
            phone = self.phone_entry.text()
            email = self.email_entry.text()

            if name and phone and email:
                self.contacts[self.selected_index] = {'name': name, 'phone': phone, 'email': email}
                self.save_contacts()
                QMessageBox.information(self, "Success", f"Contact at index {self.selected_index} updated successfully!")
                self.clear_fields()
                self.selected_index = -1
            else:
                QMessageBox.warning(self, "Warning", "Please fill in all fields.")

    def delete_contact(self):
        if self.selected_index != -1:
            deleted_contact = self.contacts.pop(self.selected_index)
            self.save_contacts()
            QMessageBox.information(self, "Success", f"Contact {deleted_contact['name']} at index {self.selected_index} deleted successfully!")
            self.clear_fields()
            self.selected_index = -1

    def clear_fields(self):
        self.name_entry.clear()
        self.phone_entry.clear()
        self.email_entry.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Apply a modern style
    window = ContactManagementSystemGUI()
    window.show()
    sys.exit(app.exec_())
