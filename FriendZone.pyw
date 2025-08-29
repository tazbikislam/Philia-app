import json
import threading
import time
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, Listbox
from plyer import notification

contact_file = "contacts.json"
setting_file = "settings.json"

def load_contacts():
    try:
        with open(contact_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_contacts(contacts):
    with open(contact_file, "w") as f:
        json.dump(contacts, f, indent=4)

def load_settings():
    try:
        with open(setting_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"reminder_datetime": None}

def save_settings(settings):
    with open(setting_file, "w") as f:
        json.dump(settings, f, indent=4)

contacts = load_contacts()
settings = load_settings()

def clear_placeholder(event):
    if search_entry.get() == "Search Contacts":
        search_entry.delete(0, "end")

def restore_placeholder(event):
    if search_entry.get() == "":
        search_entry.insert(0, "Search Contacts")

def notification(title, msg):
    notification.notification(title=title, message=msg, timeout=10)

def background_reminder():
    while True:
        today = datetime.today()
        for contact in contacts:
            try:
                last = datetime.strptime(contact["last_contacted"], "%d-%m-%Y")
                interval = int(contact.get("notification_interval", 15))
                days_since = (today - last).days
                if days_since >= interval:
                    notification("Reach Out 💖", f"You haven't contacted {contact['name']} in {days_since} days")

                bday = datetime.strptime(contact["birthday"], "%d-%m-%Y").replace(year=today.year)
                if 0 <= (bday - today).days <= 7:
                    notification("Upcoming Birthday 🎂", f"{contact['name']} on {bday.strftime('%d-%m-%Y')}")

                reminder_str = contact.get("reminder_datetime")
                if reminder_str:
                    reminder_dt = datetime.strptime(reminder_str, "%d-%m-%Y %H:%M")
                    if today >= reminder_dt and today < (reminder_dt + time(minutes=1)):
                        notification("Reminder ⏰", f"Reminder for {contact['name']}")
                        contact["reminder_datetime"] = None
                        save_contacts(contacts)

            except:
                pass
        time.sleep(30)


threading.Thread(target=background_reminder, daemon=True).start()

def refresh_contacts():
    contact_list.delete(0, "end")
    contact_list.insert("end", f"{'Name':20} | {'Relationship':20} | {'Last Contacted':12} | {'Interval':8}")
    contact_list.insert("end", "-"*70)
    for c in contacts:
        contact_list.insert(
            "end",
            f"{c['name']:20} | {c['relationship']:20} | {c['last_contact']:12} | {c.get('notification_interval',15):8}"
        )

def add_contact():
    name = entry_name.get()
    birthday = entry_birthday.get()
    last_contact = entry_last_contact.get()
    relationship = relationship_var.get()
    interval = notify_info.get()

    if not name or not birthday or not last_contact or interval == "Intervals":
        messagebox.showwarning("Input Error", "Please fill in all fields and select an interval")
        return

    contact = {
        "name": name,
        "birthday": birthday,
        "last_contact": last_contact,
        "relationship": relationship,
        "notification_interval": interval
    }

    contacts.append(contact)
    save_contacts(contacts)
    refresh_contacts()

def mark_contacted_today():
    try:
        selection = contact_list.get(contact_list.curselection())
        name = selection.split("|")[0].strip()
        for contact in contacts:
            if contact["name"] == name:
                contact["last_contact"] = datetime.today().strftime("%d-%m-%Y")
                save_contacts(contacts)
                refresh_contacts()
                messagebox.showinfo("Updated", f"{name} marked as contacted today")
                return
    except:
        messagebox.showwarning("Select Contact", "Please select a contact first")

def delete_contact():
    try:
        selection = contact_list.get(contact_list.curselection())
        name = selection.split("|")[0].strip()
        confirm = messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {name}?")
        if confirm:
            global contacts
            contacts = [c for c in contacts if c["name"] != name]
            save_contacts(contacts)
            refresh_contacts()
            messagebox.showinfo("Deleted", f"{name} has been deleted successfully")
    except:
        messagebox.showwarning("Select Contact", "Please select a contact first")

def search_contacts(event=None):
    query = search_info.get().lower()
    contact_list.delete(0, "end")
    contact_list.insert("end", f"{'Name':20} | {'Relationship':20} | {'Last Contacted':12} | {'Interval':8}")
    contact_list.insert("end", "-"*70)
    for c in contacts:
        if query in c['name'].lower():
            contact_list.insert(
                "end",
                f"{c['name']:20} | {c['relationship']:20} | {c['last_contact']:12} | {c.get('notification_interval',15):8}"
            )

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

friendzoner = ctk.CTk()
friendzoner.title("FriendZone")
friendzoner.geometry("700x600")

frame = ctk.CTkFrame(friendzoner)
frame.pack(pady=10)

entry_name = ctk.CTkEntry(frame, placeholder_text="Name")
entry_name.grid(row=0, column=0, padx=5, pady=5)

entry_birthday = ctk.CTkEntry(frame, placeholder_text="D.O.B (DD-MM-YYYY)")
entry_birthday.grid(row=0, column=1, padx=5, pady=5)

entry_last_contact = ctk.CTkEntry(frame, placeholder_text="Last Contacted (DD-MM-YYYY)")
entry_last_contact.grid(row=1, column=0, padx=5, pady=5)

relationship_var = ctk.StringVar(value="Relationship")
entry_relationship = ctk.CTkOptionMenu(frame, values=["Best Friend", "Friend"], variable=relationship_var)
entry_relationship.grid(row=1, column=1, padx=5, pady=5)

notify_info = ctk.StringVar(value="Days of Interval")
notification_interval_dropdown = ctk.CTkOptionMenu(frame, values=["7 Days","14 Days","21 Days","30 Days"], variable=notify_info)
notification_interval_dropdown.grid(row=2, column=0, padx=5, pady=5)

search_info = ctk.StringVar()
search_entry = ctk.CTkEntry(friendzoner, textvariable=search_info)
search_entry.insert(0, "Search...")
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", search_contacts)
search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", restore_placeholder)

list_frame = ctk.CTkFrame(friendzoner)
list_frame.pack(pady=10, fill="both", expand=True)

contact_list = Listbox(list_frame, height=12, width=80, bg="#2b2b2b", fg="white", selectbackground="#1f6aa5")
contact_list.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame = ctk.CTkFrame(friendzoner)
btn_frame.pack(pady=10)

btn_add = ctk.CTkButton(btn_frame, text="Add Contact", command=add_contact)
btn_add.grid(row=0, column=0, padx=5)

btn_mark_today = ctk.CTkButton(btn_frame, text="Contacted Today", command=mark_contacted_today)
btn_mark_today.grid(row=0, column=1, padx=5)

btn_delete = ctk.CTkButton(btn_frame, text="Delete Contact", command=delete_contact)
btn_delete.grid(row=0, column=2, padx=5)

refresh_contacts()
friendzoner.mainloop()