# FriendZone-app
An entertaining Python app that relieves the hassle of remembering friends birthdays and helps to stay in touch with them more effectively.

# Features

1. **Add/Delete Contacts**
   
  * Contacts are stored in a `contacts.json` file, which contains the following information:
     * Name
     * Relationship
     * Birthday
     * Last Contacted Date
     * Reminder Interval (7, 14, 21, 28 days)

2. **Search Bar**

   * Allows you to type a contact's name to find them easily.

3. **Notifications**

   * Displays desktop notifications with `plyer.notification`.

4. **Mark Contacted Today**

   * To mark a contact as contacted today, simply click the button; the date will be instantly updated.

8. **Delete Contact**

   * Deletes a chosen contact from the database.

---

## How It Works

1. **Data Storage**

* Contacts are stored in a list of dictionaries called `contacts.json`.
* Example:

     ```json
     [
      {
        "name": "Max Willier",
        "birthday": "01-01-2000",
        "last_contact": "01-08-2025",
        "relationship": "Best Friend",
        "notification_interval": "7 Days"
      }
     ]
     ```

2. **GUI Layer**

 * Developed using `customtkinter` to create a contemporary interface with a dark theme.
 * Contacts are shown in aligned columns in Listbox/Textbox.
 *  Interaction is made possible by buttons ({Add`, `Delete`, `Mark Contacted`).

3. **Background Notifications**

 * Every few minutes, a separate background loop checks.
 * A desktop notification is triggered if a contact's interval is due or if it is their birthday today.
   
---

### How to Run It

1. **Normal Run** (with GUI)

Just run your script:

```bash
python FriendZone.pyw
```

()

The GUI opens, and reminders will start in the background thread.

2. **Run in Background Always**

There are two ways to have it run automatically each time your computer boots up:

#### 🔹 Windows

1. Save your script as `FriendZone.pyw` (no console).
2. Create a shortcut of it.
3. Press `Win + R`, type:

   ```
   shell:startup
   ```

   → This opens the Startup folder.
4. Paste the shortcut there.
5. `FriendZone.pyw` will now operate automatically in the background each time you log in.

#### 🔹 Linux (Ubuntu etc.)

* Add it to **Startup Applications**:

  ```bash
  python3 /path/to/FriendZone.pyw 
  ```

#### 🔹 macOS

* Use **Automator → Application → Run Shell Script** and point it to:

  ```bash
  python3 /path/to/FriendZone.pyw
  ```
* Then add it to **Login Items** in System Preferences.

---

## Why It Can Run in Background

* The script uses **threads**:
  * Main thread → GUI
  * Background thread → notifications
* The GUI may remain reduced when you close it (if coded to do so).
*  Because `.pyw` doesn't display a console window, it appears to be a background application.
