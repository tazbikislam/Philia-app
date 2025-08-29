import json
import threading
import time
from datetime import datetime
import customtkinter as tk
from tkinter import messagebox, Listbox
from plyer import notification

contact_file = "contacts.json"
setting_file = "settings.json"
philia_font = ("Lucida Console", 13)

def show_greeting():
    popup = tk.CTkFrame(philia, corner_radius=15,  fg_color="#d5d5d5")
    popup.place(relx=0.5, rely=0.5, anchor="center")
    
    label = tk.CTkLabel(popup, text="Philia! Friends that are worth remembering", font=("Lucida Console", 16), text_color="black")
    label.pack(padx=20, pady=20)

    button = tk.CTkButton(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)

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

def search_contacts(event):
    print("Searching:", search_info.get())

def clear_placeholder(event):
    if search_entry.get() == "Search.....":
        search_entry.delete(0, "end")

def restore_placeholder(event):
    if search_entry.get() == "":
        search_entry.insert(0, "Search.....")

format_text = "DD-MM"

def on_entry_last_contact_click(event):
    if entry_last_contact.get() in ["Last Contacted", ""]:
        entry_last_contact.delete(0, tk.END)
        entry_last_contact.insert(0, format_text)
        entry_last_contact.configure()

def on_focus_out(event):
    if entry_last_contact.get() == format_text or entry_last_contact.get() == "":
        entry_last_contact.delete(0, tk.END)
        entry_last_contact.insert(0, "Last Contacted")
        entry_last_contact.configure()
    else:
        entry_last_contact.configure(text_color="white")

def on_key_press(event):
    if entry_last_contact.get() == format_text:
        entry_last_contact.delete(0, tk.END)
        entry_last_contact.configure(text_color="white")

format_text_2 = "DD-MM-YYYY"

def on_entry_birthday_click(event):
    if entry_birthday.get() in ["D.O.B", ""]:
        entry_birthday.delete(0, tk.END)
        entry_birthday.insert(0, format_text_2)
        entry_birthday.configure()

def on_focus_out_birthday(event):
    if entry_birthday.get() == format_text_2 or entry_last_contact.get() == "":
        entry_birthday.delete(0, tk.END)
        entry_birthday.insert(0, "D.O.B")
        entry_birthday.configure()
    else:
        entry_last_contact.configure(text_color="white")

def on_key_press_birthday(event):
    if entry_birthday.get() == format_text_2:
        entry_birthday.delete(0, tk.END)
        entry_birthday.configure(text_color="white")


def notification(title, msg):
    notification.notification(title=title, message=msg, timeout=10)

def background_reminder():
    while True:
        today = datetime.today()
        for contact in contacts:
            try:
                last = datetime.strptime(contact["last_contacted"], "%d-%m")
                interval = int(contact.get("notification_interval", 15))
                days_since = (today - last).days
                if days_since >= interval:
                    notification("Reach Out!", f"You haven't contacted {contact['name']} in {days_since} days")

                bday = datetime.strptime(contact["birthday"], "%d-%m-%Y").replace(year=today.year)
                if 0 <= (bday - today).days <= 7:
                    notification("Upcoming Birthday!", f"{contact['name']} on {bday.strftime('%d-%m-%Y')}")

                reminder_str = contact.get("reminder_datetime")
                if reminder_str:
                    reminder_dt = datetime.strptime(reminder_str, "%d-%m-%Y %H:%M")
                    if today >= reminder_dt and today < (reminder_dt + time(minutes=1)):
                        notification("Reminder!", f"Reminder for {contact['name']}")
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

tk.set_appearance_mode("dark")
tk.set_default_color_theme("blue")

philia = tk.CTk()
philia.title("Philia")
philia.geometry("800x600")

frame = tk.CTkFrame(philia)
frame.pack(pady=10)

philia.after(100, show_greeting)

entry_name = tk.CTkEntry(frame, placeholder_text="Name", font=philia_font)
entry_name.grid(row=0, column=0, padx=5, pady=5)

entry_birthday = tk.CTkEntry(frame, placeholder_text="D.O.B", font=philia_font)
entry_birthday.grid(row=0, column=1, padx=5, pady=5)
entry_birthday.configure(text_color="gray")
entry_birthday.bind("<FocusIn>", on_entry_birthday_click)
entry_birthday.bind("<FocusOut>", on_focus_out_birthday)
entry_birthday.bind("<Key>", on_key_press_birthday)

entry_last_contact = tk.CTkEntry(frame, placeholder_text="Last Contacted", font=philia_font)
entry_last_contact.configure(text_color="gray")
entry_last_contact.grid(row=1, column=0, padx=5, pady=5)
entry_last_contact.bind("<FocusIn>", on_entry_last_contact_click)
entry_last_contact.bind("<FocusOut>", on_focus_out)
entry_last_contact.bind("<Key>", on_key_press)

relationship_var = tk.StringVar(value="Relationship")
entry_relationship = tk.CTkOptionMenu(frame, values=["Best Friend", "Friend"], variable=relationship_var, font=philia_font)
entry_relationship.grid(row=1, column=1, padx=5, pady=5)

notify_info = tk.StringVar(value="Interval")
notification_interval_dropdown = tk.CTkOptionMenu(frame, values=["7 Days","14 Days","21 Days","30 Days"], variable=notify_info, font=philia_font)
notification_interval_dropdown.grid(row=2, column=0, padx=5, pady=5)

search_info = tk.StringVar()
search_entry = tk.CTkEntry(philia, textvariable=search_info, font=philia_font)
search_entry.insert(0, "Search.....")
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", search_contacts)
search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", restore_placeholder)

list_frame = tk.CTkFrame(philia)
list_frame.pack(pady=10, fill="both", expand=True)

contact_list = Listbox(list_frame, height=12, width=80, bg="#2b2b2b", fg="white", selectbackground="#1f6aa5")
contact_list.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame = tk.CTkFrame(philia)
btn_frame.pack(pady=10)

btn_add = tk.CTkButton(btn_frame, text="Add Contact", command=add_contact, font=philia_font)
btn_add.grid(row=0, column=0, padx=5)

btn_mark_today = tk.CTkButton(btn_frame, text="Contacted Today", command=mark_contacted_today, font=philia_font)
btn_mark_today.grid(row=0, column=1, padx=5)

btn_delete = tk.CTkButton(btn_frame, text="Delete Contact", command=delete_contact, font=philia_font)
btn_delete.grid(row=0, column=2, padx=5)

refresh_contacts()
philia.mainloop()