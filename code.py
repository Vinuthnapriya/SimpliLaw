import streamlit as st
import json
import datetime
from datetime import date
import uuid

# Page configuration
st.set_page_config(
    page_title="SimpliLaw - Justice Made Simple",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 3rem 0;
        color: white;
        text-align: center;
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        height: 100%;
    }
    
    .step-card {
        background: #f9fafb;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        height: 100%;
    }
    
    .complaint-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-submitted {
        background-color: #dbeafe;
        color: #1e40af;
    }
    
    .status-review {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .status-action {
        background-color: #fed7aa;
        color: #c2410c;
    }
    
    .status-resolved {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 18px;
        margin-bottom: 0.75rem;
        max-width: 80%;
    }
    
    .user-message {
        background-color: #3b82f6;
        color: white;
        margin-left: auto;
    }
    
    .bot-message {
        background-color: #f3f4f6;
        color: #374151;
    }
    
    .contact-info {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .social-links {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .social-link {
        color: #3b82f6;
        text-decoration: none;
        font-size: 1.5rem;
    }
    
    .progress-dots {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .progress-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    
    .progress-active {
        background-color: #10b981;
    }
    
    .progress-inactive {
        background-color: #d1d5db;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'users' not in st.session_state:
    st.session_state.users = []
if 'complaints' not in st.session_state:
    st.session_state.complaints = []
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "bot", "content": "Hello! I'm your AI Legal Assistant. I can help you understand your rights, explain legal procedures, and guide you through the complaint process. How can I assist you today?"}
    ]

# Navigation
def show_navigation():
    st.markdown("""
    <div style="background: white; padding: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: -1rem -1rem 0 -1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">⚖️</span>
                <span style="font-size: 1.25rem; font-weight: bold; color: #1f2937;">SimpliLaw</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Authentication functions
def login_form():
    with st.form("login_form"):
        st.subheader("Login")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            user = next((u for u in st.session_state.users if u['email'] == email and u['password'] == password), None)
            if user:
                st.session_state.user = user
                st.success(f"Welcome back, {user['name']}!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

def register_form():
    with st.form("register_form"):
        st.subheader("Register")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Register"):
            if any(u['email'] == email for u in st.session_state.users):
                st.error("User with this email already exists.")
            else:
                new_user = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'password': password
                }
                st.session_state.users.append(new_user)
                st.session_state.user = new_user
                st.success(f"Registration successful! Welcome to SimpliLaw, {name}!")
                st.rerun()

# Main sections
def show_hero():
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3.5rem; font-weight: bold; margin-bottom: 1rem;">Justice Made Simple</h1>
        <p style="font-size: 1.25rem; margin-bottom: 2rem; max-width: 800px; margin-left: auto; margin-right: auto;">
            AI-powered legal support platform helping Indian citizens access justice easily, affordably, and in their own language.
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_how_it_works():
    st.header("How SimpliLaw Works")
    st.subheader("Three simple steps to access justice")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="step-card">
            <div style="background: #dbeafe; width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
                <span style="font-size: 1.5rem;">✏️</span>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">1. Report</h3>
            <p style="color: #6b7280;">Describe your issue in simple words or upload photos. Our AI will help generate a proper complaint.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-card">
            <div style="background: #dbeafe; width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
                <span style="font-size: 1.5rem;">🔍</span>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">2. Review</h3>
            <p style="color: #6b7280;">We automatically route your complaint to the right authority based on your location and issue type.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-card">
            <div style="background: #dbeafe; width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
                <span style="font-size: 1.5rem;">✅</span>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">3. Resolve</h3>
            <p style="color: #6b7280;">Track your complaint status in real-time and receive updates until your issue is resolved.</p>
        </div>
        """, unsafe_allow_html=True)

def show_features():
    st.header("Powerful Features")
    st.subheader("Technology that makes justice accessible to everyone")
    
    col1, col2, col3 = st.columns(3)
    
    features = [
        ("🤖", "AI-Powered Assistant", "Get instant legal guidance and complaint drafting help from our intelligent chatbot."),
        ("🌐", "Multilingual Support", "Access services in English, Hindi, Telugu, and more regional languages."),
        ("📷", "Image Recognition", "Upload photos of documents or issues - our AI will extract relevant information."),
        ("📍", "Smart Routing", "Automatically connect with the right authorities based on your location and issue type."),
        ("📊", "Real-time Tracking", "Monitor your complaint progress with live updates and status notifications."),
        ("🛡️", "Secure & Private", "Your data is encrypted and protected with enterprise-grade security measures.")
    ]
    
    for i, (icon, title, description) in enumerate(features):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 1rem;">{icon}</div>
                <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem;">{title}</h3>
                <p style="color: #6b7280;">{description}</p>
            </div>
            """, unsafe_allow_html=True)

def show_complaint_form():
    st.header("File Your Complaint")
    st.subheader("Describe your issue and let our AI help you create a proper complaint")
    
    if not st.session_state.user:
        st.warning("Please login first to submit a complaint.")
        col1, col2 = st.columns(2)
        with col1:
            login_form()
        with col2:
            register_form()
        return
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name", value=st.session_state.user['name'])
        with col2:
            phone = st.text_input("Phone Number", value=st.session_state.user.get('phone', ''))
        
        category = st.selectbox("Issue Category", [
            "", "Consumer Rights", "Property Dispute", "Employment Issue", 
            "Public Services", "Family Law", "Other"
        ])
        
        location = st.text_input("Location", placeholder="Enter your city/district")
        
        issue_description = st.text_area("Describe Your Issue", 
            placeholder="Describe your issue in detail. Our AI will help format it properly.",
            height=150)
        
        uploaded_files = st.file_uploader("Upload Supporting Documents (Optional)", 
            accept_multiple_files=True, type=['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("🪄 Generate AI Complaint"):
                if not issue_description or not category or not full_name:
                    st.error("Please fill in all required fields before generating complaint.")
                else:
                    ai_complaint = f"""
FORMAL COMPLAINT

To: The Concerned Authority
From: {full_name}
Date: {date.today().strftime('%B %d, %Y')}

Subject: {category} Issue - Request for Immediate Action

Dear Sir/Madam,

I am writing to formally lodge a complaint regarding the following issue:

{issue_description}

I request your immediate attention and appropriate action to resolve this matter. I have attached relevant documents for your reference.

I look forward to your prompt response and resolution of this issue.

Thank you for your time and consideration.

Sincerely,
{full_name}
                    """
                    st.text_area("AI-Generated Complaint", value=ai_complaint, height=300)
                    st.success("AI-generated complaint has been created! You can review and modify it before submitting.")
        
        with col2:
            if st.form_submit_button("📤 Submit Complaint"):
                if not all([full_name, phone, category, location, issue_description]):
                    st.error("Please fill in all required fields.")
                else:
                    complaint_id = f"SL{date.today().year}{str(len(st.session_state.complaints) + 1).zfill(4)}"
                    
                    complaint = {
                        'id': complaint_id,
                        'name': full_name,
                        'phone': phone,
                        'category': category,
                        'location': location,
                        'description': issue_description,
                        'status': 'Submitted',
                        'date': date.today().strftime('%B %d, %Y'),
                        'user_email': st.session_state.user['email']
                    }
                    
                    st.session_state.complaints.append(complaint)
                    st.success(f"Complaint submitted successfully! Your complaint ID is: {complaint_id}")
                    st.rerun()

def show_complaints():
    st.header("Your Complaints")
    st.subheader("View and track all your submitted complaints")
    
    if not st.session_state.user:
        st.info("Please login to view your complaints.")
        col1, col2 = st.columns(2)
        with col1:
            login_form()
        with col2:
            register_form()
        return
    
    user_complaints = [c for c in st.session_state.complaints if c['user_email'] == st.session_state.user['email']]
    
    if not user_complaints:
        st.info("No complaints submitted yet. File your first complaint above!")
        return
    
    for complaint in user_complaints:
        status_class = {
            'Submitted': 'status-submitted',
            'Under Review': 'status-review',
            'Action Taken': 'status-action',
            'Resolved': 'status-resolved'
        }.get(complaint['status'], 'status-submitted')
        
        st.markdown(f"""
        <div class="complaint-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">
                        Complaint ID: {complaint['id']}
                    </h3>
                    <p style="color: #6b7280; margin: 0;">Filed on: {complaint['date']}</p>
                </div>
                <span class="status-badge {status_class}">{complaint['status']}</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.25rem;">Category</p>
                    <p style="font-weight: 500; margin: 0;">{complaint['category']}</p>
                </div>
                <div>
                    <p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.25rem;">Location</p>
                    <p style="font-weight: 500; margin: 0;">{complaint['location']}</p>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">Issue Description</p>
                <p style="color: #1f2937;">{complaint['description'][:200]}{'...' if len(complaint['description']) > 200 else ''}</p>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="progress-dots">
                    {get_progress_dots(complaint['status'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_progress_dots(status):
    steps = ['Submitted', 'Under Review', 'Action Taken', 'Resolved']
    current_index = steps.index(status) if status in steps else 0
    
    dots = []
    for i, step in enumerate(steps):
        class_name = 'progress-active' if i <= current_index else 'progress-inactive'
        dots.append(f'<div class="progress-dot {class_name}" title="{step}"></div>')
    
    return ''.join(dots)

def show_legal_assistant():
    st.header("AI Legal Assistant")
    st.subheader("Get instant legal guidance and answers to your questions")
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 0.75rem;">
                <div class="chat-message user-message" style="background-color: #3b82f6; color: white;">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 0.75rem;">
                <div class="chat-message bot-message" style="background-color: #f3f4f6; color: #374151;">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask me about your legal rights or any legal question...", key="chat_input")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("Consumer Rights"):
            user_input = "What are my consumer rights?"
    
    with col2:
        if st.button("Property Dispute"):
            user_input = "How to file a property dispute?"
    
    with col3:
        if st.button("Employment Law"):
            user_input = "Employment law basics"
    
    with col4:
        if st.button("Send Message"):
            if user_input:
                process_chat_message(user_input)
    
    if user_input and st.session_state.get('last_input') != user_input:
        st.session_state.last_input = user_input
        process_chat_message(user_input)

def process_chat_message(message):
    st.session_state.chat_messages.append({"role": "user", "content": message})
    
    # Generate AI response
    response = generate_ai_response(message)
    st.session_state.chat_messages.append({"role": "bot", "content": response})
    
    st.rerun()

def generate_ai_response(message):
    message_lower = message.lower()
    
    if 'consumer' in message_lower or 'rights' in message_lower:
        return "As a consumer in India, you have several rights under the Consumer Protection Act 2019: Right to safety, Right to be informed, Right to choose, Right to be heard, Right to seek redressal, and Right to consumer education. You can file complaints with Consumer Forums for defective goods or deficient services."
    
    elif 'property' in message_lower or 'dispute' in message_lower:
        return "For property disputes, you can approach Civil Courts or Revenue Courts depending on the nature of dispute. Key documents needed include sale deed, title documents, survey records, and possession documents. Consider mediation before litigation as it's faster and cost-effective."
    
    elif 'employment' in message_lower or 'job' in message_lower or 'work' in message_lower:
        return "Indian employment laws cover minimum wages, working hours, leave entitlements, and termination procedures. Key acts include Industrial Disputes Act, Payment of Wages Act, and Employees Provident Fund Act. You can approach Labor Courts for employment-related disputes."
    
    else:
        return "I understand your concern. For specific legal advice, I recommend consulting with a qualified lawyer. However, I can help you understand general legal procedures and guide you through filing a complaint on our platform. What specific aspect would you like to know more about?"

def show_about():
    st.header("About SimpliLaw")
    st.subheader("We believe that justice should be accessible to everyone, regardless of their location, language, or economic status. SimpliLaw uses cutting-edge AI technology to bridge the gap between citizens and the legal system.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Our Mission
        
        To democratize access to justice by providing AI-powered legal support that helps every Indian citizen understand their rights and navigate the legal system with confidence.
        
        ✅ Simplified legal processes for all citizens  
        ✅ AI-powered complaint generation and routing  
        ✅ Real-time tracking and transparency  
        ✅ Multilingual support for rural communities
        """)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 3rem; color: #3b82f6; margin-bottom: 1rem;">👥</div>
            <h4 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">Serving Citizens Nationwide</h4>
            <p style="color: #6b7280;">From rural villages to metropolitan cities, SimpliLaw is making justice accessible to millions of Indians across all states and territories.</p>
        </div>
        """, unsafe_allow_html=True)

def show_contact():
    st.header("Contact Us")
    st.subheader("Get in touch with our team for support or partnerships")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="contact-info">
            <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1.5rem;">Get Support</h3>
            
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 1.25rem; margin-right: 1rem;">📞</span>
                <span>+91 8639225248</span>
            </div>
            
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 1.25rem; margin-right: 1rem;">📧</span>
                <span>vinuthna2024@gmail.com</span>
            </div>
            
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <span style="font-size: 1.25rem; margin-right: 1rem;">📍</span>
                <span>Hyderabad, Telangana, India</span>
            </div>
            
            <h4 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem;">Follow Us</h4>
            <div class="social-links">
                <a href="#" class="social-link">🐦</a>
                <a href="#" class="social-link">📘</a>
                <a href="https://linkedin.com/in/vinuthna-priya" target="_blank" class="social-link">💼</a>
                <a href="https://instagram.com/priyawincherry" target="_blank" class="social-link">📷</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("contact_form"):
            st.text_input("Your Name")
            st.text_input("Your Email")
            st.text_area("Your Message", height=150)
            
            if st.form_submit_button("Send Message"):
                st.success("Thank you for your message! We'll get back to you soon.")

# Main app
def main():
    show_navigation()
    
    # User authentication in sidebar
    with st.sidebar:
        if st.session_state.user:
            st.success(f"Welcome, {st.session_state.user['name']}!")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()
        else:
            st.info("Login to access all features")
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                login_form()
            
            with tab2:
                register_form()
    
    # Main navigation
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏠 Home", "ℹ️ About", "⚡ Features", "📝 File Complaint", 
        "📋 My Complaints", "🤖 Legal Assistant", "📞 Contact"
    ])
    
    with tab1:
        show_hero()
        show_how_it_works()
    
    with tab2:
        show_about()
    
    with tab3:
        show_features()
    
    with tab4:
        show_complaint_form()
    
    with tab5:
        show_complaints()
    
    with tab6:
        show_legal_assistant()
    
    with tab7:
        show_contact()

if __name__ == "__main__":
    main()
