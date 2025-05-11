# shittyline ticket Loader

A Python bot to help you automatically buy tickets for your favorite concerts on Cityline or similar ticketing websites. The bot opens the ticket page in your chosen browser, waits for the sale, and clicks the buy button as soon as it appears, then notifies you to complete the purchase manually.

## Features
- Always opens the ticket URL in your chosen browser (Chrome or Edge, set in `config.ini`)
- In **non-debug mode**, waits until 1 second before the sale start time, then refreshes every 0.1 seconds; after the sale starts, keeps searching and refreshing for the buy button until it's pressed
- In **debug mode**, skips waiting for the start time and searches for the buy button up to 2 times, then refreshes and repeats until the button is found and clicked
- Plays a sound notification when the buy button is pressed, so you can complete the purchase manually
- Auto-exits if you close the browser window
- All actions are logged to `ticket_bot.log`

### How to Use the .exe
1. **Download `ticket_bot.exe`** from the Releases page and place it in a folder of your choice.
2. **Copy `config.example.ini` to `config.ini`** in the same folder, and edit your settings (URL, time, etc.).
3. **Make sure your `sound.mp3` file** (or whatever you set as `NOTIFY_SOUND`) is in the same folder as the `.exe`.
4. **Double-click `ticket_bot.exe`** to run. A command window will appear showing live logs. The icon is embedded in the `.exe`.

> **Note:** No Python or pipenv is required for the `.exe`. If you want to run from source or on other platforms, see below.

---

## Setup (For Developers & Advanced Users)

### 1. Clone or Download
Place all files in a folder on your computer.

### 2. Install Python & Pipenv
- Make sure you have Python 3.8+ installed
- Install pipenv: `pip install pipenv`

### 3. Install Dependencies
```
pipenv install
```

### 4. Configure `config.ini`

A template config file is provided as `config.example.ini`. For your own setup:

1. **Copy `config.example.ini` to `config.ini`:**
   ```
   cp config.example.ini config.ini
   ```
   (Or manually copy/paste if on Windows)

2. **Edit `config.ini`** to set your preferences under the `[ticket]` section:
   - `TICKET_URL`: The full URL of the ticket page
   - `START_TIME`: When ticket sales open (format: `YYYY-MM-DD HH:MM:SS`)
   - `NOTIFY_SOUND`: Path to a sound file (e.g., `sound.wav` or `sound.mp3`)
   - `DEBUG`: `1` or `true` to skip waiting for start time (for testing), `0` or `false` for normal
   - `BROWSER`: `chrome` (default) or `edge`

> **Note:**
> - `config.ini` is in `.gitignore` and should NOT be committed to git. Use `config.example.ini` as the public template for sharing or pushing to repositories.
> - `ticket_bot.log` is also ignored by git to keep logs out of version control.

### 5. Run the Bot
```
pipenv run python ticket_bot.py
```

## How It Works
1. Loads your settings from `config.ini`.
2. Opens the browser (Chrome or Edge, as set in `config.ini`) and navigates to the ticket page.
3. **Non-debug mode:**
    - Waits until 1 second before the sale start time.
    - Refreshes the page every 0.1 seconds until the sale starts.
    - After the sale starts, keeps refreshing and searching for the buy button every 0.1 seconds until it is found and clicked.
4. **Debug mode:**
    - Skips waiting for the start time.
    - Searches for the buy button up to 2 times, then refreshes and repeats until the button is found and clicked.
5. When the buy button is pressed, plays a sound (using `NOTIFY_SOUND`) and logs the event.
6. Lets you complete the purchase manually.
7. If you close the browser window, the bot will exit automatically.
8. All actions are logged to `ticket_bot.log`.

## Tips
- Make sure your system time is accurate (sync with internet time).
- Use a wired connection for lower latency.
- Use debug mode for testing (skips waiting for sale time).
- You can switch browsers by changing `BROWSER` in `config.ini`.
- The refresh interval and attempt counts are set in the code for optimal speed and reliability.
- If you close the browser window, the bot will exit automatically.

## Troubleshooting
- If you get `cannot find Chrome binary`, install Google Chrome or set `BROWSER=edge` and use Microsoft Edge.
- If you get driver errors, make sure your browser is up to date.
- For any issues, check `ticket_bot.log` for detailed logs.

## License
MIT License
