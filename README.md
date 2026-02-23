# MoleMonitor (Sprint 1)

MoleMonitor is an MVP app for tracking skin images over time. It’s built with **Python** and **Streamlit**—a framework that turns Python scripts into web apps without writing HTML or JavaScript.

This guide walks you through setting up and running the project from scratch, assuming you’re new to Python and Streamlit.

---

## What You’ll Need

- A computer (Windows, macOS, or Linux)
- **Python 3.10 or newer** installed
- A terminal (Command Prompt, PowerShell, or Terminal app)
- This project folder (e.g. after cloning the repo or downloading the code)

---

## Step 1: Check That Python Is Installed

Open your terminal and run:

```bash
python --version
```

You should see something like `Python 3.10.x` or higher. If you get an error or a version below 3.10:

- **Windows:** Download the installer from [python.org](https://www.python.org/downloads/) and during setup, check **“Add Python to PATH”**.
- **macOS:** Install via [python.org](https://www.python.org/downloads/) or with Homebrew: `brew install python`.
- **Linux:** Use your package manager (e.g. `sudo apt install python3.10` on Ubuntu).

Run `python --version` again after installing to confirm.

---

## Step 2: Open the Project Folder in the Terminal

Go to the folder where MoleMonitor lives. For example:

```bash
cd d:\Code\MoleMonitor
```

(Use your actual path if it’s different.)

---

## Step 3: Create a Virtual Environment (Recommended)

A **virtual environment** is an isolated Python environment for this project. It keeps the project’s packages separate from the rest of your system and avoids version conflicts.

**Create the environment:**

```bash
python -m venv .venv
```

This creates a `.venv` folder inside your project.

**Activate it:**

- **Windows (Command Prompt):**
  ```bash
  .venv\Scripts\activate.bat
  ```
- **Windows (PowerShell):**
  ```bash
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

When it’s active, you’ll usually see `(.venv)` at the start of your terminal line. From now on, run all commands in this same terminal (with the venv active).

---

## Step 4: Install the Project Dependencies

The project uses several Python packages (Streamlit, NumPy, Pandas, Pillow, OpenCV). They’re listed in `requirements.txt`.

**Install everything in one go:**

```bash
pip install -r requirements.txt
```

Wait until it finishes. If you see any errors, check that your virtual environment is activated and that you have Python 3.10+.

---

## Step 5: Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Streamlit will:

- Start a local web server
- Print a URL in the terminal (usually `http://localhost:8501`)
- Open your default browser to that URL (or you can open it yourself)

You should see the MoleMonitor app with a **sidebar** to switch between:

- **Home**
- **Register** / **Login** / **Forgot Password**
- **Instructions**
- **Image History**
- **About**

To stop the app, press **Ctrl+C** in the terminal.

---

## Step 6: Understand the Project Layout (Optional)

Getting familiar with the structure helps when you want to change or extend the app:

| Path | Purpose |
|------|--------|
| `app.py` | Entry point: runs Streamlit, sets up navigation, and loads the right page |
| `requirements.txt` | List of Python packages the project needs |
| `src/` | Main application code |
| `src/config.py` | App title, icon, and list of pages (navigation) |
| `src/pages/` | One module per page (e.g. `home.py`, `history.py`, `login.py`) |
| `src/db/` | Database setup and helpers |
| `src/state/` | Session state (e.g. history) |
| `src/ui/` | Reusable UI components |

**Streamlit in one sentence:** You write Python; Streamlit turns it into buttons, forms, images, and tables in the browser. No separate front-end code needed.

---

## Troubleshooting

- **“python” or “pip” not found**  
  Make sure Python is installed and added to your PATH. Reinstall from [python.org](https://www.python.org/downloads/) and tick “Add Python to PATH” on Windows.

- **Permission or execution errors when activating the venv**  
  On Windows PowerShell, you may need to allow scripts:  
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

- **Port 8501 already in use**  
  Another app might be using that port. Stop it or run:  
  `streamlit run app.py --server.port 8502`

- **Import or module errors when running the app**  
  Ensure you’re in the project root (where `app.py` is), the virtual environment is activated, and you ran `pip install -r requirements.txt`.

---

## Next Steps

- Change the app title or icon in `src/config.py`.
- Edit a page in `src/pages/` (e.g. `home.py`) and save—Streamlit will offer to reload the app.
- Read the [Streamlit docs](https://docs.streamlit.io/) and try the “Get started” tutorial to learn more widgets and patterns.

---

## Summary

1. Install Python 3.10+ and ensure it’s on your PATH.
2. Open the project folder in the terminal.
3. Create and activate a virtual environment: `python -m venv .venv` then activate it.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the app: `streamlit run app.py`.
6. Use the sidebar to navigate the app; stop with Ctrl+C in the terminal.

Once this works, you’re ready to experiment with the code and learn more Python and Streamlit. Have fun building.
