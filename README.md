
# 🧾 Simple QR Code Renamer App
A lightweight TUI (Text User Interface) application that automatically **detects QR codes in images** and **renames or organizes files** based on their decoded text.
Built with [Textual](https://textual.textualize.io/) and [OpenCV](https://opencv.org/).
---
## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/Pepepop0/Simple-QR-Code-renamer-app.git
   cd simple-qr-code-renamer-app
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   python app.py
   ```

---

## How It Works

1. Place your images in the `imgs-raw` folder.
2. Launch the app.
3. Press **▶ Start Processing** to detect QR codes.
4. Files are automatically copied and renamed inside the `images_new` folder.
5. View progress, results, and errors in real time.
