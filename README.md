#  G20-MAJOR_CSE-25  
**Major Project Repository – CSE Batch 2025**  
*A BERT-based question-answering and summarization system for health policy documents, with dynamic question generation using T5.*

---

##  Requirements

- **Python 3.10** (Recommended for compatibility with machine learning libraries used)
- **Streamlit**
- **Virtual Environment** (`venv`)
- **Git**

>  Using Python 3.11 or higher?  
Update `requirements.txt` and reinstall packages accordingly.

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/G20-MAJOR_CSE-25.git
cd G20-MAJOR_CSE-25


### 2. Create Virtual Environment

```bash
python3.10 -m venv venv
```

### 3. Activate Virtual Environment

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Run the Application

Make sure your virtual environment is activated, then run:

```bash
streamlit run app.py
```

---

##  Project Structure

```
G20-MAJOR_CSE-25/
│
├── app.py                  # Streamlit frontend + controller
├── auth.py                 # Authentication logic
├── database.py             # SQLite database handling
├── question_generator.py   # T5-based dynamic question generation
├── terms_summarizer.db     # SQLite database file
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

---

##  Features

-  **BERT-based QA** for extracting specific details from lengthy policy documents  
-  **T5-powered question generator** to dynamically create hot-point questions  
-  **Streamlit interface** for easy interaction  
-  **Local SQLite database** for saving summaries and user sessions  
-  Validated by multiple domain experts for accuracy and usefulness  

---

##  Notes

- Keep Python version consistent (3.10 recommended) across environments.  
- To update dependencies after any changes, run:

```bash
pip freeze > requirements.txt
```

---

---

##  Contact

For any query, you can contact: **shivanshjain3333@gmail.com**


Let me know if you want a badge (like “Made with ❤️ using BERT + T5”) or a credits section too!
