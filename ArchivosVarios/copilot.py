#### Esto es lo que me hace copilot si le revoleo todo el pdf ####	
import matplotlib.pyplot as plt
import csv
from datetime import datetime 
import os

class Central:
    def __init__(self):
        self.registered_devices = {}
        self.communication_log = []

    def register_device(self, device):
        self.registered_devices[device.phone_number] = device
        print(f"Device {device.phone_number} registered")

    def deregister_device(self, device):
        if device.phone_number in self.registered_devices:
            del self.registered_devices[device.phone_number]
            print(f"Device {device.phone_number} deregistered")
        else:
            print(f"Device {device.phone_number} not found")

    def is_device_registered(self, phone_number):
        return phone_number in self.registered_devices

    def verify_device_status(self, phone_number):
        if self.is_device_registered(phone_number):
            device = self.registered_devices[phone_number]
            return device.is_on and device.mobile_network_active
        return False

    def verify_internet_access(self, phone_number):
        if self.is_device_registered(phone_number):
            device = self.registered_devices[phone_number]
            return device.is_on and device.internet_data_active
        return False

    def handle_call(self, from_number, to_number):
        if self.verify_device_status(from_number) and self.verify_device_status(to_number):
            print(f"Connecting call from {from_number} to {to_number}")
            self.log_communication('call', from_number, to_number)
            return True
        else:
            print("One or both devices are not registered or not available")
            return False

    def handle_sms(self, from_number, to_number, message):
        if self.verify_device_status(from_number) and self.verify_device_status(to_number):
            print(f"Sending SMS from {from_number} to {to_number}: {message}")
            self.log_communication('sms', from_number, to_number, message)
            return True
        else:
            print("One or both devices are not registered or not available")
            return False

    def log_communication(self, comm_type, from_number, to_number, message=None):
        log_entry = {
            'type': comm_type,
            'from': from_number,
            'to': to_number,
            'message': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.communication_log.append(log_entry)
        self.save_log_to_csv(log_entry)


    def save_log_to_csv(self, log_entry):
        file_exists = os.path.isfile('communication_log.csv')
        with open('communication_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                # Write the header if the file does not exist
                writer.writerow(['type', 'from', 'to', 'message', 'timestamp'])
            writer.writerow(log_entry.values())

    def analyze_data(self):
        self.call_count = 0
        self.sms_count = 0
        self.communication_counts = {}

        with open('communication_log.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['type'] == 'call':
                    self.call_count += 1
                elif row['type'] == 'sms':
                    self.sms_count += 1

                if row['from'] in self.communication_counts:
                    self.communication_counts[row['from']] += 1
                else:
                    self.communication_counts[row['from']] = 1

                if row['to'] in self.communication_counts:
                    self.communication_counts[row['to']] += 1
                else:
                    self.communication_counts[row['to']] = 1

    def generate_reports(self):
        # Generate a bar chart for the number of calls and SMS
        labels = ['Calls', 'SMS']
        counts = [self.call_count, self.sms_count]

        plt.figure(figsize=(10, 5))
        plt.bar(labels, counts, color=['blue', 'green'])
        plt.xlabel('Communication Type')
        plt.ylabel('Count')
        plt.title('Number of Calls and SMS')
        plt.savefig('communication_type_counts.png')
        plt.show()

        # Generate a bar chart for the number of communications per phone number
        plt.figure(figsize=(10, 5))
        plt.bar(self.communication_counts.keys(), self.communication_counts.values(), color='purple')
        plt.xlabel('Phone Number')
        plt.ylabel('Count')
        plt.title('Number of Communications per Phone Number')
        plt.savefig('communication_counts_per_phone_number.png')
        plt.show()


class CellPhone:
    def __init__(self, id, name, model, os, os_version, ram, storage, phone_number, central):
        self.id = id
        self.name = name
        self.model = model
        self.os = os
        self.os_version = os_version
        self.ram = ram
        self.storage = storage
        self.phone_number = phone_number
        self.is_on = False
        self.is_locked = True
        self.contacts = {}
        self.sms_inbox = []
        self.call_history = []
        self.emails = []
        self.installed_apps = []
        self.mobile_network_active = False
        self.internet_data_active = False
        self.central = central

    def power_on(self):
        self.is_on = True
        self.activate_mobile_network()
        self.central.register_device(self)
        print("Phone is now ON")

    def power_off(self):
        self.is_on = False
        self.central.deregister_device(self)
        print("Phone is now OFF")

    def lock(self):
        self.is_locked = True
        print("Phone is now LOCKED")

    def unlock(self):
        self.is_locked = False
        print("Phone is now UNLOCKED")

    def make_call(self, number):
        if self.is_on and not self.is_locked:
            if self.central.handle_call(self.phone_number, number):
                print(f"Calling {number}...")
                self.call_history.append(f"Called {number}")
        else:
            print("Phone is either OFF or LOCKED")

    def receive_call(self, number):
        if self.is_on:
            print(f"Receiving call from {number}...")
            self.call_history.append(f"Received call from {number}")
        else:
            print("Phone is OFF")

    def end_call(self):
        print("Call ended")

    def add_contact(self, name, number):
        self.contacts[name] = number
        print(f"Contact {name} added")

    def update_contact(self, name, new_number):
        if name in self.contacts:
            self.contacts[name] = new_number
            print(f"Contact {name} updated")
        else:
            print(f"Contact {name} not found")

    def send_sms(self, number, message):
        if self.is_on and not self.is_locked:
            if self.central.handle_sms(self.phone_number, number, message):
                print(f"Sending SMS to {number}: {message}")
                self.sms_inbox.append({'to': number, 'message': message})
        else:
            print("Phone is either OFF or LOCKED")

    def receive_sms(self, number, message):
        if self.is_on:
            print(f"Received SMS from {number}: {message}")
            self.sms_inbox.append({'from': number, 'message': message})
        else:
            print("Phone is OFF")

    def view_sms_inbox(self):
        return self.sms_inbox

    def view_call_history(self):
        return self.call_history

    def delete_sms(self, index):
        if 0 <= index < len(self.sms_inbox):
            del self.sms_inbox[index]
            print("SMS deleted")
        else:
            print("Invalid SMS index")

    def view_emails(self, sort_by="unread"):
        if sort_by == "unread":
            return sorted(self.emails, key=lambda x: x['read'])
        elif sort_by == "date":
            return sorted(self.emails, key=lambda x: x['date'], reverse=True)

    def download_app(self, app_name):
        self.installed_apps.append(app_name)
        print(f"App {app_name} downloaded")

    def configure_phone(self, name=None, unlock_code=None):
        if name:
            self.name = name
        if unlock_code:
            self.unlock_code = unlock_code
        print("Phone configured")

    def activate_mobile_network(self):
        self.mobile_network_active = True
        print("Mobile network activated")

    def deactivate_mobile_network(self):
        self.mobile_network_active = False
        print("Mobile network deactivated")

    def activate_internet_data(self):
        self.internet_data_active = True
        print("Internet data activated")

    def deactivate_internet_data(self):
        self.internet_data_active = False
        print("Internet data deactivated")

def main():
    central = Central()

    # Create two cell phones
    phone1 = CellPhone(1, "Phone1", "ModelX", "OS1", "1.0", "4GB", "64GB", "1234567890", central)
    phone2 = CellPhone(2, "Phone2", "ModelY", "OS2", "2.0", "6GB", "128GB", "0987654321", central)

    # Power on phones
    phone1.power_on()
    phone2.power_on()

    # Unlock phones
    phone1.unlock()
    phone2.unlock()

    # Add contacts
    phone1.add_contact("Alice", "1111111111")
    phone2.add_contact("Bob", "2222222222")

    # Make a call
    phone1.make_call("0987654321")
    phone2.receive_call("1234567890")
    phone1.end_call()
    phone2.end_call()

    # Send SMS
    phone1.send_sms("0987654321", "Hello, this is a test message.")
    phone2.receive_sms("1234567890", "Hello, this is a test message.")

    # View SMS inbox and call history
    print(phone1.view_sms_inbox())
    print(phone2.view_sms_inbox())
    print(phone1.view_call_history())
    print(phone2.view_call_history())

    # Delete SMS
    phone2.delete_sms(0)

    # Power off phones
    phone1.power_off()
    phone2.power_off()

if __name__ == "__main__":
    main()