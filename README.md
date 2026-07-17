# 🧹 Asset Cleanup Utility

A Flask-based web application designed to simplify **Software AG Managed File Transfer (MFT)** asset cleanup activities. It helps users clean exported XML assets for **Event Cleanup** and **VFS Cleanup** before migration, maintenance, or deployment.

The application provides a clean web interface where users can upload Software AG export XML files, process them using backend cleanup logic, and download the cleaned XML file with the same original filename — no manual XML editing required.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-black.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🌐 Live Demo

**🚀 Try it live:** https://assetcleaner.onrender.com/

> _Note: The free-tier Render instance may take ~30 seconds to wake up on first visit._

---

## ✨ Features

### 🗂️ Event Cleanup
- Upload Software AG **Event XML** export files.
- Automatically remove unwanted or unused Event dependencies.
- Generate a cleaned Event XML file.
- Download the cleaned file with a single click.
- User-friendly error handling for invalid uploads.

### 📁 VFS Cleanup
- Upload Software AG **VFS XML** export files.
- Enter required VFS paths manually via a clean input UI.
- **Validate VFS path format** before processing.
- Prevents empty VFS path submission.
- Displays a **custom error page** if the VFS path format is incorrect.
- Generate a cleaned VFS XML file.
- Download the cleaned file with the **original filename** preserved.

### 🎨 User Interface
- Modern **full-screen dashboard** design (no scrolling required).
- Separate dedicated pages for **Event Cleanup** and **VFS Cleanup**.
- Fully **responsive layout** for laptops, tablets, and mobile screens.
- Animated cards, glowing buttons, and **glassmorphism** style panels.
- Custom error page with clear troubleshooting suggestions.

### ☁️ Deployment
- Ready for **Render deployment** out of the box.
- Uses **Gunicorn** as the production WSGI server.
- Includes `requirements.txt` and `render.yaml` for one-click deploy.

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.10+, Flask 3.0 |
| **XML Processing** | lxml / ElementTree |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, Jinja2 |
| **UI Style** | Glassmorphism, Custom Animations |
| **WSGI Server** | Gunicorn |
| **Deployment** | Render (Free Tier) |
| **Version Control** | Git, GitHub |

---

## 📸 Screenshots

> _Add screenshots after deployment._

- 🏠 **Home Dashboard** — Choose between Event Cleanup and VFS Cleanup
- 🗂️ **Event Cleanup Page** — Upload and process Event XML
- 📁 **VFS Cleanup Page** — Upload XML + enter VFS paths
- ⚠️ **Error Page** — Friendly troubleshooting UI

---

## 📁 Project Structure

```
AssetCleaner/
│
├── main.py                     # Flask application entry point
├── EventCleanUp.py             # Event XML cleanup logic
├── VFSCleanUp.py               # VFS XML cleanup logic
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── README.md                   # Project documentation
│
├── static/
│   └── Designer.png            # Hero/logo image
│
└── templates/
    ├── home.html               # Landing page (choose cleanup type)
    ├── event.html              # Event Cleanup UI
    ├── vfs.html                # VFS Cleanup UI
    └── error.html              # Custom error page
```

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/surajprakashverma/AssetCleaner.git
cd AssetCleaner
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask app
```bash
python main.py
```

### 5. Open your browser
Visit **http://127.0.0.1:5000/**

---

## 💡 Usage

### 🗂️ For Event Cleanup

1. From the home dashboard, click **Event Cleanup**.
2. Upload your exported Software AG **Event XML** file.
3. Click **Clean & Download**.
4. The cleaned file downloads automatically with the same original filename.

### 📁 For VFS Cleanup

1. From the home dashboard, click **VFS Cleanup**.
2. Upload your exported Software AG **VFS XML** file.
3. Enter the required **VFS paths** in the input field (one or multiple).
4. Click **Clean & Download**.
5. If the VFS path format is invalid, a friendly error page appears with troubleshooting tips.
6. Otherwise, the cleaned VFS XML file downloads automatically.

### Example VFS path format
```
/RPI/BUK/RT/MDM/Customer/DataAnalytics
/RPI/BUK/RT/MDM/Customer/DataAnalyticsPII/Inbound
```

---

## ⚙️ How It Works

1. **User uploads** the Software AG exported XML file via the web UI.
2. Flask backend saves the file temporarily and passes it to the appropriate cleanup module (`EventCleanUp.py` or `VFSCleanUp.py`).
3. The cleanup module **parses the XML**, removes unnecessary dependencies (users, groups, or unwanted VFS paths), and rewrites a clean XML structure.
4. The processed XML is streamed back to the user as a downloadable file with the **original filename preserved**.
5. Any validation failure (invalid format, missing input) is caught and rendered on a custom error page with actionable guidance.

---

## ☁️ Deployment on Render

This app is deployed on **Render's free tier**. Here's the quick guide:

### Prerequisites in repo root
- `requirements.txt` (with `gunicorn` included)
- `render.yaml` (optional — for infrastructure-as-code deploys)
- `main.py` (Flask entry point)

### Steps
1. Push code to GitHub.
2. Go to [render.com](https://render.com) → **New +** → **Web Service**.
3. Connect your GitHub repo.
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app`
   - **Runtime:** Python 3
5. Click **Create Web Service** → wait ~3–5 min → **Live!** 🎉

### Auto-deploy
Every `git push` to `main` triggers an automatic redeploy on Render.

---

## 👥 Who Is This For?

- 🧑‍💼 **Software AG administrators** managing MFT environments.
- 🔧 **Integration engineers** working on webMethods deployments.
- 🚚 **SAP S/4HANA migration teams** cleaning up legacy assets.
- 🛠️ **DevOps engineers** automating XML asset preparation.
- 📦 **Anyone** who has ever manually edited MFT XML exports and wished for a faster way.

---

## ⚠️ Disclaimer

> **This is an internal utility tool.**
> Always **verify the cleaned XML output** in a non-production environment before deploying to production Software AG instances.
> The author is not responsible for any misuse or data loss caused by improper XML modifications.

---

## 👨‍💻 Author

**Suraj Prakash Verma**
- 🏢 UST Global
- 🌐 GitHub: [@surajprakashverma](https://github.com/surajprakashverma)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🌟 Show Your Support

If you found this project useful, give it a ⭐ on GitHub!

Contributions, issues, and feature requests are always welcome. 🙌
