# import streamlit as st
# from transformers import BertTokenizer, BertForQuestionAnswering
# import torch
# from database import SessionLocal, User, Summary
# from auth import verify_password, get_password_hash, create_access_token
# import PyPDF2  # Add this to extract text from PDF files

# # Load the BERT model and tokenizer
# @st.cache_resource
# def load_model():
#     tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     return tokenizer, model

# def summarize_terms(text, question):
#     tokenizer, model = load_model()
    
#     inputs = tokenizer.encode_plus(question, text, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]

#     outputs = model(**inputs)
#     answer_start = torch.argmax(outputs.start_logits)
#     answer_end = torch.argmax(outputs.end_logits) + 1

#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     return answer

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# def init_session_state():
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False
#     if 'username' not in st.session_state:
#         st.session_state.username = None

# def login_user(username: str, password: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.username == username).first()
#     if user and verify_password(password, user.password_hash):
#         st.session_state.logged_in = True
#         st.session_state.username = username
#         return True
#     return False

# def register_user(username: str, email: str, password: str):
#     db = SessionLocal()
#     if db.query(User).filter(User.username == username).first():
#         return False, "Username already exists"
#     if db.query(User).filter(User.email == email).first():
#         return False, "Email already exists"
    
#     hashed_password = get_password_hash(password)
#     new_user = User(username=username, email=email, password_hash=hashed_password)
#     db.add(new_user)
#     db.commit()
#     return True, "Registration successful"

# def save_summary(username: str, original_text: str, question: str, summary: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.username == username).first()
#     if user:
#         new_summary = Summary(
#             user_id=user.id,
#             original_text=original_text,
#             question=question,
#             summary=summary
#         )
#         db.add(new_summary)
#         db.commit()

# def main():
#     st.title("Pratyaksh - Terms and Conditions Comprehension")
#     init_session_state()

#     if not st.session_state.logged_in:
#         tab1, tab2 = st.tabs(["Login", "Register"])
        
#         with tab1:
#             st.subheader("Login")
#             username = st.text_input("Username", key="login_username")
#             password = st.text_input("Password", type="password", key="login_password")
#             if st.button("Login"):
#                 if login_user(username, password):
#                     st.success("Logged in successfully!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password")

#         with tab2:
#             st.subheader("Register")
#             new_username = st.text_input("Username", key="reg_username")
#             new_email = st.text_input("Email", key="reg_email")
#             new_password = st.text_input("Password", type="password", key="reg_password")
#             if st.button("Register"):
#                 success, message = register_user(new_username, new_email, new_password)
#                 if success:
#                     st.success(message)
#                 else:
#                     st.error(message)

#     else:
#         st.write(f"Welcome, {st.session_state.username}!")
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.username = None
#             st.rerun()

#         tab1, tab2 = st.tabs(["Summarize", "History"])

#         with tab1:
#             input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"])

#             if input_option == "Text Input":
#                 terms = st.text_area("Enter the Terms and Conditions Text")
#             else:
#                 uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])
#                 if uploaded_file:
#                     terms = extract_text_from_pdf(uploaded_file)
#                     st.text_area("Extracted Text", terms, height=200)

#             question = st.text_input("What information are you looking for?", 
#                                    "sum insured?")

#             if st.button("Get Insights"):
#                 if terms:
#                     summary = summarize_terms(terms, question)
#                     st.subheader("Comprehension:")
#                     st.write(summary)
                    
#                     # Save the summary to database
#                     save_summary(st.session_state.username, terms, question, summary)
#                 else:
#                     st.error("Please provide input text or upload a PDF file.")
#         with tab1:
#              input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"])

#              terms = ""  # Initialize terms as an empty string
#              if input_option == "Text Input":
#                    terms = st.text_area("Enter the Terms and Conditions Text")
#              elif input_option == "PDF Upload":
#                  uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])
#                  if uploaded_file:
#                     terms = extract_text_from_pdf(uploaded_file)
#                     st.text_area("Extracted Text", terms, height=200)

#              question = st.text_input("What information are you looking for?", "sum insured?")

#     # Move the button to ensure it works for both inputs
#              if st.button("Get Insights"):
#                   if terms.strip():  # Ensure terms is not empty
#                       summary = summarize_terms(terms, question)
#                       st.subheader("Comprehension:")
#                       st.write(summary)

#             # Save the summary to database
#                       save_summary(st.session_state.username, terms, question, summary)
#                   else:
#                       st.error("Please provide input text or upload a PDF file.")

#         with tab2:
#             st.subheader("Your Summary History")
#             db = SessionLocal()
#             user = db.query(User).filter(User.username == st.session_state.username).first()
#             if user:
#                 summaries = db.query(Summary).filter(Summary.user_id == user.id).order_by(Summary.timestamp.desc()).all()
#                 for summary in summaries:
#                     with st.expander(f"Summary from {summary.timestamp}"):
#                         st.write("Question:", summary.question)
#                         st.write("Summary:", summary.summary)
#                         if st.button("Show Original Text", key=f"original_{summary.id}"):
#                             st.write("Original Text:", summary.original_text)

# if __name__ == "__main__":
#     main()

# import streamlit as st
# from transformers import BertTokenizer, BertForQuestionAnswering
# import torch
# from database import SessionLocal, User, Summary
# from auth import verify_password, get_password_hash, create_access_token
# import PyPDF2
# from question_generator import generate_questions  # Import the question generator

# @st.cache_resource
# def load_model():
#     tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     return tokenizer, model

# def summarize_terms(text, question):
#     tokenizer, model = load_model()
    
#     inputs = tokenizer.encode_plus(question, text, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]

#     outputs = model(**inputs)
#     answer_start = torch.argmax(outputs.start_logits)
#     answer_end = torch.argmax(outputs.end_logits) + 1

#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     return answer

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# def main():
#     st.title("Pratyaksh - Terms and Conditions Comprehension")

#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         st.warning("Please log in to access features.")
#         return

#     tab1, tab2 = st.tabs(["Summarize", "History"])

#     with tab1:
#         input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"])
#         terms = ""

#         if input_option == "Text Input":
#             terms = st.text_area("Enter the Terms and Conditions Text")
#         elif input_option == "PDF Upload":
#             uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])
#             if uploaded_file:
#                 terms = extract_text_from_pdf(uploaded_file)
#                 st.text_area("Extracted Text", terms, height=200)

#         # Initialize session state for storing generated questions
#         if "suggested_questions" not in st.session_state:
#             st.session_state.suggested_questions = []

#         # Display "Generate Questions" button only if terms are provided
#         if terms.strip():
#             if st.button("🔍 Generate Questions"):
#                 st.session_state.suggested_questions = generate_questions(terms, num_questions=5)
        
#         # Show suggested questions only if generated
#         if st.session_state.suggested_questions:
#             st.subheader("Suggested Questions:")
#             selected_question = st.selectbox(
#                 "Select a question or type your own:",
#                 ["Type your own question..."] + st.session_state.suggested_questions
#             )
#         else:
#             selected_question = "Type your own question..."

#         # Text input for manual question entry
#         question = st.text_input("What information are you looking for?", selected_question)

#         if st.button("💡 Get Insights"):
#             if terms.strip():
#                 summary = summarize_terms(terms, question)
#                 st.subheader("Comprehension:")
#                 st.write(summary)
#                 save_summary(st.session_state.username, terms, question, summary)
#             else:
#                 st.error("Please provide input text or upload a PDF file.")

#     with tab2:
#         st.subheader("Your Summary History")
#         db = SessionLocal()
#         user = db.query(User).filter(User.username == st.session_state.username).first()
#         if user:
#             summaries = db.query(Summary).filter(Summary.user_id == user.id).order_by(Summary.timestamp.desc()).all()
#             for summary in summaries:
#                 with st.expander(f"Summary from {summary.timestamp}"):
#                     st.write("Question:", summary.question)
#                     st.write("Summary:", summary.summary)


# import streamlit as st
# from transformers import BertTokenizer, BertForQuestionAnswering
# import torch
# from database import SessionLocal, User, Summary
# from auth import verify_password, get_password_hash, create_access_token
# import PyPDF2
# from question_generator import generate_questions  # Import the question generator

# @st.cache_resource
# def load_model():
#     tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     return tokenizer, model

# def summarize_terms(text, question):
#     tokenizer, model = load_model()
    
#     inputs = tokenizer.encode_plus(question, text, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]

#     outputs = model(**inputs)
#     answer_start = torch.argmax(outputs.start_logits)
#     answer_end = torch.argmax(outputs.end_logits) + 1

#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     return answer

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
#     return text

# def save_summary(username: str, original_text: str, question: str, summary: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.username == username).first()
#     if user:
#         new_summary = Summary(
#             user_id=user.id,
#             original_text=original_text,
#             question=question,
#             summary=summary
#         )
#         db.add(new_summary)
#         db.commit()

# def main():
#     st.title("Pratyaksh - Terms and Conditions Comprehension")

#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         st.warning("Please log in to access features.")
#         return

#     tab1, tab2 = st.tabs(["Summarize", "History"])

#     with tab1:
#         # Unique key added
#         input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"], key="input_option_radio")
#         terms = ""

#         if input_option == "Text Input":
#             terms = st.text_area("Enter the Terms and Conditions Text", key="text_area_terms")
#         elif input_option == "PDF Upload":
#             uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"], key="pdf_upload")
#             if uploaded_file:
#                 terms = extract_text_from_pdf(uploaded_file)
#                 st.text_area("Extracted Text", terms, height=200, key="extracted_text_area", disabled=True)

#         # Initialize session state for storing generated questions
#         if "suggested_questions" not in st.session_state:
#             st.session_state.suggested_questions = []

#         # Display "Generate Questions" button only if terms are provided
#         if terms.strip():
#             if st.button("🔍 Generate Questions", key="btn_generate_questions"):
#                 st.session_state.suggested_questions = generate_questions(terms, num_questions=5)
        
#         # Show suggested questions only if generated
#         if st.session_state.suggested_questions:
#             st.subheader("Suggested Questions:")
#             selected_question = st.selectbox(
#                 "Select a question or type your own:",
#                 ["Type your own question..."] + st.session_state.suggested_questions,
#                 key="selectbox_question"
#             )
#         else:
#             selected_question = "Type your own question..."

#         # Text input for manual question entry
#         question = st.text_input("What information are you looking for?", selected_question, key="text_input_question")

#         if st.button("💡 Get Insights", key="btn_get_insights"):
#             if terms.strip():
#                 summary = summarize_terms(terms, question)
#                 st.subheader("Comprehension:")
#                 st.write(summary)
#                 save_summary(st.session_state.username, terms, question, summary)
#             else:
#                 st.error("Please provide input text or upload a PDF file.")

#     with tab2:
#         st.subheader("Your Summary History")
#         db = SessionLocal()
#         user = db.query(User).filter(User.username == st.session_state.username).first()
#         if user:
#             summaries = db.query(Summary).filter(Summary.user_id == user.id).order_by(Summary.timestamp.desc()).all()
#             for summary in summaries:
#                 with st.expander(f"Summary from {summary.timestamp}", expanded=False):
#                     st.write("**Question:**", summary.question)
#                     st.write("**Summary:**", summary.summary)

# if __name__ == "__main__":
#     main()

# import streamlit as st
# from transformers import BertTokenizer, BertForQuestionAnswering
# import torch
# from database import SessionLocal, User, Summary
# from auth import verify_password, get_password_hash, create_access_token
# import PyPDF2
# from question_generator import generate_questions  # Import the question generator

# @st.cache_resource
# def load_model():
#     tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     return tokenizer, model

# def summarize_terms(text, question):
#     tokenizer, model = load_model()
    
#     inputs = tokenizer.encode_plus(question, text, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]

#     outputs = model(**inputs)
#     answer_start = torch.argmax(outputs.start_logits)
#     answer_end = torch.argmax(outputs.end_logits) + 1

#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     return answer

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
#     return text

# def save_summary(username: str, original_text: str, question: str, summary: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.username == username).first()
#     if user:
#         new_summary = Summary(
#             user_id=user.id,
#             original_text=original_text,
#             question=question,
#             summary=summary
#         )
#         db.add(new_summary)
#         db.commit()

# def main():
#     st.title("Pratyaksh - Terms and Conditions Comprehension")

#     # Initialize session state
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False
#     if "suggested_questions" not in st.session_state:
#         st.session_state.suggested_questions = []
#     if "selected_question" not in st.session_state:
#         st.session_state.selected_question = "Type your own question..."

#     # Prevents duplicate keys by using unique identifiers for dynamic elements
#     if not st.session_state.logged_in:
#         st.warning("Please log in to access features.")
#         return

#     tab1, tab2 = st.tabs(["Summarize", "History"])

#     with tab1:
#         input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"], key="input_option_radio_1")
#         terms = ""

#         if input_option == "Text Input":
#             terms = st.text_area("Enter the Terms and Conditions Text", key="text_area_terms_1")
#         elif input_option == "PDF Upload":
#             uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"], key="pdf_upload_1")
#             if uploaded_file:
#                 terms = extract_text_from_pdf(uploaded_file)
#                 st.text_area("Extracted Text", terms, height=200, key="extracted_text_area_1", disabled=True)

#         # Display "Generate Questions" button only if terms are provided
#         if terms.strip():
#             if st.button("🔍 Generate Questions", key="btn_generate_questions_1"):
#                 st.session_state.suggested_questions = generate_questions(terms, num_questions=5)
        
#         # Show suggested questions only if generated
#         if st.session_state.suggested_questions:
#             st.subheader("Suggested Questions:")
#             selected_question_index = st.selectbox(
#                 "Select a question or type your own:",
#                 ["Type your own question..."] + st.session_state.suggested_questions,
#                 key="selectbox_question_1"
#             )
#             st.session_state.selected_question = selected_question_index

#         # Text input for manual question entry
#         question = st.text_input("What information are you looking for?", st.session_state.selected_question, key="text_input_question_1")

#         if st.button("💡 Get Insights", key="btn_get_insights_1"):
#             if terms.strip():
#                 summary = summarize_terms(terms, question)
#                 st.subheader("Comprehension:")
#                 st.write(summary)
#                 save_summary(st.session_state.username, terms, question, summary)
#             else:
#                 st.error("Please provide input text or upload a PDF file.")

#     with tab2:
#         st.subheader("Your Summary History")
#         db = SessionLocal()
#         user = db.query(User).filter(User.username == st.session_state.username).first()
#         if user:
#             summaries = db.query(Summary).filter(Summary.user_id == user.id).order_by(Summary.timestamp.desc()).all()
#             for summary in summaries:
#                 with st.expander(f"Summary from {summary.timestamp}", expanded=False):
#                     st.write("**Question:**", summary.question)
#                     st.write("**Summary:**", summary.summary)

# if __name__ == "__main__":
#     main()

# import asyncio
# import sys

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# import streamlit as st
# from transformers import BertTokenizer, BertForQuestionAnswering
# import torch
# from database import SessionLocal, User, Summary
# from auth import verify_password
# import PyPDF2
# from question_generator import generate_questions

# @st.cache_resource
# def load_model():
#     tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
#     return tokenizer, model

# def summarize_terms(text, question):
#     tokenizer, model = load_model()
#     inputs = tokenizer.encode_plus(question, text, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]
#     outputs = model(**inputs)
#     answer_start = torch.argmax(outputs.start_logits)
#     answer_end = torch.argmax(outputs.end_logits) + 1
#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     return answer

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
#     return text

# def save_summary(username: str, original_text: str, question: str, summary: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.username == username).first()
#     if user:
#         new_summary = Summary(
#             user_id=user.id,
#             original_text=original_text,
#             question=question,
#             summary=summary
#         )
#         db.add(new_summary)
#         db.commit()

# def login_screen():
#     st.title("🔐 Login to Pratyaksh")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         db = SessionLocal()
#         user = db.query(User).filter(User.username == username).first()
#         if user and verify_password(password, user.password_hash):
#             st.session_state.logged_in = True
#             st.session_state.username = username
#             st.success(f"Welcome, {username}!")
#             st.stop()
#         else:
#             st.error("Invalid username or password")

# def main_app():
#     st.title("📘 Pratyaksh - Terms and Conditions Comprehension")

#     st.write("✅ Logged In:", st.session_state.logged_in)
#     st.write("👤 Username:", st.session_state.username)

#     if "suggested_questions" not in st.session_state:
#         st.session_state.suggested_questions = []
#     if "selected_question" not in st.session_state:
#         st.session_state.selected_question = "Type your own question..."

#     tab1, tab2 = st.tabs(["Summarize", "History"])

#     with tab1:
#         input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"], key="unique_input_selector")
#         terms = ""

#         if input_option == "Text Input":
#             terms = st.text_area("Enter the Terms and Conditions Text")
#         elif input_option == "PDF Upload":
#             uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])
#             if uploaded_file:
#                 terms = extract_text_from_pdf(uploaded_file)
#                 st.text_area("Extracted Text", terms, height=200, disabled=True)

#         if terms.strip():
#             if st.button("🔍 Generate Questions"):
#                 st.session_state.suggested_questions = generate_questions(terms, num_questions=5)

#         if st.session_state.suggested_questions:
#             st.subheader("Suggested Questions:")
#             selected_question_index = st.selectbox(
#                 "Select a question or type your own:",
#                 ["Type your own question..."] + st.session_state.suggested_questions
#             )
#             st.session_state.selected_question = selected_question_index

#         question = st.text_input("What information are you looking for?", st.session_state.selected_question)

#         if st.button("💡 Get Insights"):
#             if terms.strip():
#                 summary = summarize_terms(terms, question)
#                 st.subheader("Comprehension:")
#                 st.write(summary)
#                 save_summary(st.session_state.username, terms, question, summary)
#             else:
#                 st.error("Please provide input text or upload a PDF file.")

#     with tab2:
#         st.subheader("Your Summary History")
#         db = SessionLocal()
#         user = db.query(User).filter(User.username == st.session_state.username).first()
#         if user:
#             summaries = db.query(Summary).filter(Summary.user_id == user.id).order_by(Summary.timestamp.desc()).all()
#             for summary in summaries:
#                 with st.expander(f"Summary from {summary.timestamp}", expanded=False):
#                     st.write("**Question:**", summary.question)
#                     st.write("**Summary:**", summary.summary)

# def main():
#     # Initialize session state
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False
#     if "username" not in st.session_state:
#         st.session_state.username = ""

#     if not st.session_state.logged_in:
#         login_screen()
#     else:
#         main_app()

# if __name__ == "__main__":
#     main()

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
from database import SessionLocal, User, Summary
from auth import verify_password, get_password_hash
import PyPDF2
from question_generator import generate_questions

@st.cache_resource
def load_model():
    tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
    model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
    return tokenizer, model

def summarize_terms(text, question):
    tokenizer, model = load_model()
    inputs = tokenizer.encode_plus(question, text, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    outputs = model(**inputs)
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def save_summary(username: str, original_text: str, question: str, summary: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        new_summary = Summary(
            user_id=user.id,
            original_text=original_text,
            question=question,
            summary=summary
        )
        db.add(new_summary)
        db.commit()

def login_screen():
    st.title("🔐 Welcome to Pratyaksh")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.password_hash):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("Choose a username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Choose a password", type="password", key="reg_password")

        if st.button("Create Account"):
            db = SessionLocal()
            if db.query(User).filter(User.username == new_username).first():
                st.error("Username already exists")
            elif db.query(User).filter(User.email == new_email).first():
                st.error("Email already exists")
            else:
                hashed_pw = get_password_hash(new_password)
                new_user = User(username=new_username, email=new_email, password_hash=hashed_pw)
                db.add(new_user)
                db.commit()
                st.success("Account created! You can now log in.")

def main_app():
    st.title("📘 Pratyaksh - Terms and Conditions Comprehension")

    # 🚪 Logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    st.write("✅ Logged In:", st.session_state.logged_in)
    st.write("👤 Username:", st.session_state.username)

    if "suggested_questions" not in st.session_state:
        st.session_state.suggested_questions = []
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = "Type your own question..."

    tab1, tab2 = st.tabs(["Summarize", "History"])

    with tab1:
        input_option = st.radio("Choose Input Type", ["Text Input", "PDF Upload"], key="unique_input_selector")
        terms = ""

        if input_option == "Text Input":
            terms = st.text_area("Enter the Terms and Conditions Text")
        elif input_option == "PDF Upload":
            uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])
            if uploaded_file:
                terms = extract_text_from_pdf(uploaded_file)
                st.text_area("Extracted Text", terms, height=200, disabled=True)

        if terms.strip():
            if st.button("🔍 Generate Questions"):
                st.session_state.suggested_questions = generate_questions(terms, num_questions=5)

        if st.session_state.suggested_questions:
            st.subheader("Suggested Questions:")
            selected_question_index = st.selectbox(
                "Select a question or type your own:",
                ["Type your own question..."] + st.session_state.suggested_questions
            )
            st.session_state.selected_question = selected_question_index

        question = st.text_input("What information are you looking for?", st.session_state.selected_question)

        if st.button("💡 Get Insights"):
            if terms.strip():
                summary = summarize_terms(terms, question)
                st.subheader("Comprehension:")
                st.write(summary)
                save_summary(st.session_state.username, terms, question, summary)
            else:
                st.error("Please provide input text or upload a PDF file.")

    with tab2:
        st.subheader("Your Summary History")
        db = SessionLocal()
        user = db.query(User).filter(User.username == st.session_state.username).first()
        if user:
            summaries = db.query(Summary).filter(Summary.user_id == user.id).order_by(Summary.timestamp.desc()).all()
            for summary in summaries:
                with st.expander(f"Summary from {summary.timestamp}", expanded=False):
                    st.write("**Question:**", summary.question)
                    st.write("**Summary:**", summary.summary)

def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.logged_in:
        login_screen()
    else:
        main_app()

if __name__ == "__main__":
    main()
