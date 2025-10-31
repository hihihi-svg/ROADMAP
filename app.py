import streamlit as st
from utils_ai import get_roadmap, analyze_user_readiness, get_quick_insights, validate_api_key
import time

# Page configuration
st.set_page_config(
    page_title="AI Career Roadmap Generator", 
    page_icon="🧭", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main app background - BLACK */
    .stApp {
        background: #000000;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 0, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.1) 0%, transparent 50%);
    }
    
    /* Container styling with dark theme */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
        background: rgba(20, 20, 20, 0.95);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(138, 43, 226, 0.3);
        border: 1px solid rgba(138, 43, 226, 0.2);
    }
    
    /* Button styling - PURPLE */
    .stButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, #9F7AEA 0%, #8B5CF6 50%, #7C3AED 100%);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Input fields - Dark theme */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #333333;
        padding: 0.75rem;
        font-size: 1rem;
        background: #1a1a1a;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8B5CF6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
        background: #222222;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #666666;
    }
    
    /* Select boxes - Dark theme */
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #333333;
        padding: 0.75rem;
        font-size: 1rem;
        background: #1a1a1a;
        color: #ffffff;
    }
    
    .stSelectbox>div>div>select:focus {
        border-color: #8B5CF6;
        background: #222222;
    }
    
    /* Labels - Light color for dark background */
    .stTextInput>label, .stSelectbox>label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Success/Warning/Info boxes - Dark theme */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 5px solid #10b981;
        border-radius: 10px;
        padding: 1rem;
        color: #a7f3d0;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 5px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem;
        color: #fde68a;
    }
    
    .stInfo {
        background-color: rgba(139, 92, 246, 0.1);
        border-left: 5px solid #8B5CF6;
        border-radius: 10px;
        padding: 1rem;
        color: #ddd6fe;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
        color: #fecaca;
    }
    
    /* Markdown styling - Dark theme */
    .markdown-text-container {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #333333;
        color: #e0e0e0;
    }
    
    /* Headers - Light color */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Paragraph text */
    p, li, span {
        color: #e0e0e0;
    }
    
    /* Expander - Dark theme */
    .streamlit-expanderHeader {
        background-color: #1a1a1a;
        border-radius: 10px;
        font-weight: 600;
        color: #e0e0e0 !important;
        border: 1px solid #333333;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #222222;
        border-color: #8B5CF6;
    }
    
    /* Spinner - Purple */
    .stSpinner>div {
        border-top-color: #8B5CF6 !important;
    }
    
    /* Download button - Purple */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        border: none;
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #9F7AEA 0%, #8B5CF6 100%);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Section divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #8B5CF6, transparent);
    }
    
    /* Sidebar - Dark theme */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #0a0a0a;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'roadmap_generated' not in st.session_state:
    st.session_state.roadmap_generated = False
if 'roadmap_content' not in st.session_state:
    st.session_state.roadmap_content = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Header
st.title("🧭 AI Career Roadmap Generator")
st.markdown("### *Your Personalized Learning Journey Starts Here*")
st.markdown("---")

# API Key validation check
is_valid, api_message = validate_api_key()
if not is_valid:
    st.error(api_message)
    st.info("💡 **How to fix:** Create a `.env` file in your project directory with: `GOOGLE_API_KEY=your_key_here`")
    st.stop()

# Welcome message
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%); 
            padding: 1.5rem; 
            border-radius: 15px; 
            border-left: 5px solid #8B5CF6;
            margin-bottom: 2rem;'>
    <h3 style='margin:0; color: #ffffff;'>👋 Welcome!</h3>
    <p style='margin: 0.5rem 0 0 0; color: #e0e0e0;'>
        Answer a few questions and get a comprehensive, AI-powered roadmap tailored to your goals, 
        skills, and learning style. Let's build your future together!
    </p>
</div>
""", unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Career & Skills")
    career_goal = st.text_input(
        "What is your dream career?",
        placeholder="e.g., Data Scientist, Full Stack Developer",
        help="Be specific about the role you want to achieve"
    )
    
    skills = st.text_input(
        "What skills do you already have?",
        placeholder="e.g., Python, Communication, Problem Solving",
        help="List your current technical and soft skills"
    )
    
    interest_area = st.text_input(
        "Which field interests you the most?",
        placeholder="e.g., AI/ML, Web Development, Cloud Computing",
        help="What domain excites you?"
    )

with col2:
    st.markdown("#### 📚 Learning Preferences")
    education_level = st.selectbox(
        "What's your current education level?",
        ["-- Select --", "High School Student", "Undergraduate", "Graduate", "Working Professional", "Career Changer"],
        help="Your current academic or professional status"
    )
    
    time_commitment = st.selectbox(
        "How much time can you dedicate per week?",
        ["-- Select --", "Less than 5 hours", "5-10 hours", "10-20 hours", "20+ hours", "Full-time learner"],
        help="Realistic weekly time commitment"
    )
    
    learning_style = st.selectbox(
        "How do you prefer to learn?",
        ["-- Select --", "Video Tutorials", "Reading Books/Articles", "Hands-on Projects", "Interactive Courses", "Mixed Approach"],
        help="Your preferred learning method"
    )

# Additional inputs
st.markdown("#### 💰 Budget & Timeline")
col3, col4 = st.columns(2)

with col3:
    budget = st.selectbox(
        "What's your learning budget?",
        ["-- Select --", "Free resources only", "Under $50/month", "$50-200/month", "$200-500/month", "No budget limit"],
        help="Monthly budget for courses and resources"
    )

with col4:
    timeline = st.selectbox(
        "Target timeline to reach your goal:",
        ["-- Select --", "3-6 months", "6-12 months", "1-2 years", "2-3 years", "3+ years"],
        help="When do you want to achieve your career goal?"
    )

st.markdown("---")

# Generate roadmap button
if st.button("🚀 Generate My Personalized Roadmap", use_container_width=True):
    # Validation
    if not career_goal or not skills or not interest_area:
        st.warning("⚠️ Please fill in at least: Career Goal, Current Skills, and Interest Area")
    elif education_level == "-- Select --" or time_commitment == "-- Select --" or learning_style == "-- Select --":
        st.warning("⚠️ Please select all dropdown options")
    elif budget == "-- Select --" or timeline == "-- Select --":
        st.warning("⚠️ Please complete Budget and Timeline selections")
    else:
        # Prepare responses
        responses = {
            "Career Goal": career_goal,
            "Skills": skills,
            "Interest": interest_area,
            "Time Commitment": time_commitment,
            "Learning Style": learning_style,
            "Education Level": education_level,
            "Budget": budget,
            "Timeline": timeline
        }
        
        # Show loading message
        with st.spinner("🔮 Analyzing your profile..."):
            time.sleep(1)
            
            # Get quick insights first
            insights = get_quick_insights(responses)
            st.info(f"💭 **Quick Insight:** {insights}")
            
        with st.spinner("✨ Crafting your personalized roadmap... This may take 30-60 seconds."):
            # Generate roadmap
            roadmap = get_roadmap(responses)
            st.session_state.roadmap_content = roadmap
            st.session_state.roadmap_generated = True
            st.session_state.user_name = career_goal.replace(" ", "_")

# Display roadmap if generated
if st.session_state.roadmap_generated and st.session_state.roadmap_content:
    st.markdown("---")
    st.success("✅ Your personalized roadmap is ready!")
    
    # Show summary in expander
    with st.expander("📋 View Your Survey Responses", expanded=False):
        if 'responses' in locals():
            for key, value in responses.items():
                st.markdown(f"**{key}:** {value}")
    
    st.markdown("---")
    
    # Display the roadmap
    st.markdown(st.session_state.roadmap_content)
    
    st.markdown("---")
    
    # Action buttons
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Download button
        st.download_button(
            label="📥 Download Roadmap (Markdown)",
            data=st.session_state.roadmap_content,
            file_name=f"{st.session_state.user_name}_career_roadmap.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col_b:
        # Reset button
        if st.button("🔄 Create New Roadmap", use_container_width=True):
            st.session_state.roadmap_generated = False
            st.session_state.roadmap_content = ""
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999999; font-size: 0.9rem;'>
    <p>Built with ❤️ using Streamlit & Google Gemini AI</p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem; color: #666666;'>
        💡 <b>Tip:</b> Save your roadmap and track your progress regularly!
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with help
with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Fill in all fields** with accurate information
    2. **Click Generate** to create your roadmap
    3. **Review** the comprehensive plan
    4. **Download** for offline reference
    5. **Track** your progress monthly
    
    ### 💡 Tips for Best Results
    - Be specific about your career goal
    - List all relevant skills you have
    - Choose realistic time commitments
    - Be honest about your budget
    
    ### 🆘 Need Help?
    - Make sure your `.env` file has GOOGLE_API_KEY
    - All fields are required for best results
    - Generation takes 30-60 seconds
    """)
    
    st.markdown("---")
    st.markdown("### 🌟 Example Careers")
    st.markdown("""
    - Data Scientist
    - Full Stack Developer
    - Product Manager
    - UI/UX Designer
    - Cloud Engineer
    - Machine Learning Engineer
    - DevOps Engineer
    - Cybersecurity Analyst
    """)