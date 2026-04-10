```markdown

## 🚀 Overview

This scraper allows users to input multiple URLs, interactively select specific HTML tags for extraction, and save the cleaned data into structured formats. It follows a **pipeline-based architecture**:

**Fetch Page** ➔ **Check Robots.txt** ➔ **Parse HTML** ➔ **User Selection** ➔ **Extract** ➔ **Save**

## ⚙️ Project Structure

```text
web_scraper/
│
├── scraper/
│   ├── main.py          # Entry point & orchestration logic
│   ├── fetcher.py       # HTTP requests & robots.txt handling
│   ├── parser.py        # BeautifulSoup logic & tag extraction
│   ├── saver.py         # JSON & CSV export functionality
│   └── requirements.txt # Project dependencies
│
├── README.md            # Documentation
└── .gitignore           # Files to exclude from Git
```

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/web-scraper.git](https://github.com/your-username/web-scraper.git)
   cd web-scraper
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r scraper/requirements.txt
   ```

---

## 📋 Features & Functionality

### 1. Smart Fetching
* **User-Agent Spoofing:** Uses `fake-useragent` to mimic real browser requests.
* **Polite Scraping:** Implements `time.sleep()` to prevent overwhelming target servers.
* **Robots Compliance:** Automatically checks `urllib.robotparser` to ensure the scraper follows site-specific rules.

### 2. Interactive Extraction
* The script parses the HTML and presents a unique list of available tags (e.g., `h1`, `p`, `a`).
* Users can choose exactly what data they want to extract in real-time.

### 3. Data Storage
* **JSON:** Ideal for hierarchical data and web applications.
* **CSV:** Perfect for data analysis in Excel or Pandas.

---

## 🕹️ Usage

Run the main script to start the interactive session:

```bash
python scraper/main.py
```

**Workflow:**
1. Enter the URLs you wish to scrape (comma-separated).
2. The system will validate `robots.txt` for each domain.
3. Review the list of discovered HTML tags.
4. Input the tags you want to extract (e.g., `h1, p, div`).
5. Choose your preferred output format.

---

## 📦 Technologies Used

* **[Requests]:** For handling HTTP communication.
* **[BeautifulSoup4]:** For navigating and parsing the HTML tree.
* **[Fake-Useragent]:** To rotate headers and avoid bot detection.
* **Python Standard Libraries:** `json`, `csv`, `time`, `urllib.robotparser`.

---

