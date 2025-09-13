## Philia-app

An entertaining Python app that relieves the hassle of remembering friends birthdays and helps to stay in touch with them more effectively.


## Built With

* ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
* ![CustomTinker](https://img.shields.io/badge/CustomTinker-FFD700?logo=python&logoColor=fff)
* ![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?logo=visualstudiocode&logoColor=fff)


## Getting Started

## Prerequisites

* Visual Studio Code
   * Get the latest VS Code version from the official website (<a href="https://code.visualstudio.com" target="_blank">code.visualstudio.com</a>).
   
* Python
   * Get the most recent Python version from the official website (<a href="https://www.python.org/" target="_blank">python.org</a>).
   * Start the installer & Complete the installation process.
     
* CustomTinker
   * It is a robust Python user interface module.
   * Open your VS Code terminal and enter the following to install it.
  ```sh
  pip install customtkinter
  ```

## Installation

### 1. Normal Run (with GUI)

* Just run your script:
```sh
python Philia.pyw
```
* The GUI opens, and reminders will start in the background thread.

### 2. Run in Background Always

* There are two ways to have it run automatically each time your computer boots up:
<br>🔹 Windows <br>
  1. Save your script as ```Philia.pyw```.
  2. Create a shortcut of it.
  3. Press ```Win + R```, type:```shell:startup```
  4. This opens the Startup folder.
  5. Paste the shortcut there.
  6. ```Philia.pyw``` will now operate automatically in the background each time you log in.
  
  🔹 Linux (Ubuntu etc.) <br>
  1. Add it to Startup Applications:
  ```sh
  python3 /path/to/Philia.pyw
  ```
  
  🔹 macOS <br>
  1. Use Automator → Application → Run Shell Script and point it to:
  ```sh
  python3 /path/to/Philia.pyw
  ```
  2. Then add it to Login Items in System Preferences.

## How It Operates

* Contacts are stored in a list of dictionaries called ```contacts.json```.
* Example:
```sh
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
* GUI Layer is developed using ```customtkinter``` to create a contemporary interface with a dark theme.
* Contacts are shown in aligned columns in Listbox/Textbox.
* Interaction is made possible by buttons (```Add```, ```Delete```, ```Mark Contacted```).
* Background Notifications runs every few minutes , to a separate background loop check.
* A desktop notification is triggered if a contact's interval is due or if it is their birthday today.
* ```.pyw``` doesn't display a console window, it appears to be a background application.


## Contact

Tazbik Islam - tazbikislam.work@gmail.com

Project Link: <a href="https://github.com/tazbikislam/Philia-app" target="_blank"> Philia-app </a>
