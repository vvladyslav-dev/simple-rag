## Setup and Run

- **Create a virtual environment**
```bash
python3 -m venv .venv
```

- **Activate the environment (macOS/Linux)**
```bash
source .venv/bin/activate
```

- **Check Python version**
```bash
python -V
```

- **Install dependencies**
```bash
pip install -r requirements.txt
```

- **Deactivate the environment (if needed)**
```bash
deactivate
```

## Notes
- The `.env` file contains environment variables (example: `ENV=development`).
- If `python3` points to the correct version, use it; otherwise, specify the path to Python 3.12.
