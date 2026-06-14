## Step 1: Installation

Check if already installed:
```bash
obliteratus --version 2>/dev/null && echo "INSTALLED" || echo "NOT INSTALLED"
```

If not installed, clone and install from GitHub:
```bash
git clone https://github.com/elder-plinius/OBLITERATUS.git
cd OBLITERATUS
pip install -e .