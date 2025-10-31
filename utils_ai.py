from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

def get_roadmap(user_responses):
    """
    Generate a comprehensive career roadmap based on user survey responses
    """
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            max_tokens=3000
        )
    except Exception as e:
        return f"❌ Error initializing AI model: {str(e)}\n\nPlease check your GOOGLE_API_KEY in the .env file."
    
    # Format user responses for better readability
    formatted_responses = json.dumps(user_responses, indent=2)
    
    # Extract timeline for phase calculation
    timeline = user_responses.get('Timeline', '3-6 months')
    budget = user_responses.get('Budget', 'Flexible')
    learning_style = user_responses.get('Learning Style', 'Mixed Approach')
    career_goal = user_responses.get('Career Goal', 'your career goal')
    
    prompt = f"""
You are an expert career counselor and learning path architect with years of experience in guiding people towards successful careers.

Based on the following user profile, create a comprehensive, personalized, and actionable career roadmap.

USER PROFILE:
{formatted_responses}

Generate a detailed roadmap using this EXACT structure:

# 🎯 Career Goal Overview
**Target Role:** [Their career goal]
**Current Status:** [Brief analysis of where they are now]
**Gap Analysis:** [What skills/experience they need to acquire]
**Estimated Timeline:** [Based on their time commitment and target timeline]

---

# 📊 Learning Roadmap

## Phase 1: Foundation Building (First few months)

### 🎓 Core Skills to Master
1. **[Skill Name]** (Priority: High/Medium/Low)
   - Why it matters: [Brief explanation]
   - Time to learn: [Weeks/Months]
   
2. **[Skill Name]** (Priority: High/Medium/Low)
   - Why it matters: [Brief explanation]
   - Time to learn: [Weeks/Months]

### 📚 Recommended Learning Resources
Based on learning style: {learning_style}
Budget consideration: {budget}

1. **[Resource Name]**
   - Type: [Free Course/Paid Course/Book/Video Series/Tutorial]
   - Platform: [Coursera/Udemy/YouTube/etc.]
   - Cost: [Free/$X]
   - Duration: [Hours/Weeks]
   - Link: [If available, provide actual working URL]

2. **[Resource Name]**
   [Same structure]

### 🛠️ Hands-On Projects
1. **[Project Name]**
   - Description: [What you'll build]
   - Skills applied: [List skills]
   - Difficulty: [Beginner/Intermediate]
   - Estimated time: [Days/Weeks]

2. **[Project Name]**
   [Same structure]

### ✅ Phase 1 Milestone
By the end of this phase, you should be able to:
- [Specific achievement 1]
- [Specific achievement 2]
- [Specific achievement 3]

---

## Phase 2: Intermediate Development (Next phase)

[Same structure as Phase 1 with intermediate-level content]

### 🎓 Advanced Skills
[List 3-4 intermediate skills]

### 📚 Resources
[List 3-4 intermediate resources]

### 🛠️ Projects
[List 2-3 intermediate projects]

### 💼 Professional Development
- Start building your portfolio/GitHub
- Join relevant communities ([Specific communities])
- Attend virtual meetups/webinars
- Consider contributing to open-source projects

### ✅ Phase 2 Milestone
[What you should achieve]

---

## Phase 3: Advanced Specialization (Months X-Y)

[Same structure with advanced content]

### 🎓 Specialized Skills
[List advanced/specialized skills]

### 📚 Resources
[Advanced courses, certifications]

### 🛠️ Capstone Projects
[1-2 complex, portfolio-worthy projects]

### 💼 Career Preparation
- Polish LinkedIn profile
- Create professional portfolio website
- Prepare resume tailored to {career_goal}
- Practice technical interviews
- Apply for internships/junior positions

### ✅ Phase 3 Milestone
[What you should achieve]

---

## Phase 4: Career Launch (Final Stage)

### 🎯 Job Search Strategy
1. Target companies: [Types of companies to apply to]
2. Networking approach: [How to network in this field]
3. Application strategy: [Tips specific to their goal]

### 💼 Internship/Job Opportunities
- [Specific roles to look for]
- [Where to find opportunities]
- [How to stand out]

### 🎤 Interview Preparation
- Technical topics to review
- Common interview questions
- Behavioral interview tips

### ✅ Final Milestone
[Career goal achieved - specific outcome]

---

# 🎓 Recommended Certifications
(In order of priority)

1. **[Certification Name]**
   - Provider: [Organization]
   - Cost: [Price]
   - Value: [Why it's important]
   - When to get it: [Phase 2/3/4]

2. **[Certification Name]**
   [Same structure]

---

# 💡 Personalized Success Tips

Based on your learning style ({learning_style}):
- [Tip 1 specific to their style]
- [Tip 2]

Based on your time commitment ({user_responses.get('Time Commitment', '')}):
- [Tip 1 about time management]
- [Tip 2]

General advice:
- [Tip 1]
- [Tip 2]
- [Tip 3]

---

# ⚠️ Common Pitfalls to Avoid
1. [Pitfall 1 specific to their career path]
2. [Pitfall 2]
3. [Pitfall 3]

---

# 📈 Progress Tracking Checkpoints

**Month 3:** [What you should have accomplished]
**Month 6:** [What you should have accomplished]
**Month 12:** [What you should have accomplished]
**Month 18:** [What you should have accomplished]
**Month 24:** [Final goal status]

---

# 🌟 Motivation & Final Words
[Personalized encouraging message based on their profile]

---

IMPORTANT REQUIREMENTS:
1. Make the roadmap specific to: {career_goal}
2. Consider their education level: {user_responses.get('Education Level', 'current level')}
3. Respect their budget: {budget}
4. Match their learning style: {learning_style}
5. Be realistic about timeline based on: {user_responses.get('Time Commitment', 'time available')}
6. Provide ACTUAL working URLs when possible (real courses, not placeholders)
7. Include both free and paid resources
8. Make projects progressively challenging
9. Be encouraging but realistic
10. Format everything in clean Markdown with emojis

Return the complete roadmap in the exact format above.
"""
    
    try:
        result = model.invoke(prompt)
        return result.content
    except Exception as e:
        error_msg = f"""
❌ **Error Generating Roadmap**

{str(e)}

**Troubleshooting Steps:**
1. Check if your GOOGLE_API_KEY is correctly set in the .env file
2. Verify you have internet connection
3. Ensure your API key has sufficient quota
4. Try again in a few moments

**Your Responses (saved):**
{formatted_responses}
"""
        return error_msg


def analyze_user_readiness(user_responses):
    """
    Analyze if the user has provided enough information for a good roadmap
    """
    required_fields = ["Career Goal", "Skills", "Interest"]
    missing = []
    
    for field in required_fields:
        if field not in user_responses or not user_responses[field] or user_responses[field].strip() == "":
            missing.append(field)
    
    if missing:
        return False, f"⚠️ Please provide: {', '.join(missing)}"
    
    return True, "✅ Ready to generate your personalized roadmap!"


def get_quick_insights(user_responses):
    """
    Generate quick insights about the user's career path
    """
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.8,
            max_tokens=200
        )
        
        prompt = f"""
Based on this career profile:
- Goal: {user_responses.get('Career Goal', 'Not specified')}
- Current Skills: {user_responses.get('Skills', 'Not specified')}
- Interest: {user_responses.get('Interest', 'Not specified')}
- Time Commitment: {user_responses.get('Time Commitment', 'Not specified')}
- Timeline: {user_responses.get('Timeline', 'Not specified')}

Generate 2-3 sentences of personalized, encouraging insights about their career journey.
Be specific, motivating, and realistic. Mention their specific goal and timeline.
"""
        
        result = model.invoke(prompt)
        return result.content
        
    except Exception as e:
        # Fallback insight if AI fails
        career = user_responses.get('Career Goal', 'your chosen career')
        timeline = user_responses.get('Timeline', 'your target timeline')
        return f"🌟 Your journey to becoming a {career} is achievable with dedication and the right plan. With {timeline} and consistent effort, you're on the path to success!"


def validate_api_key():
    """
    Check if Google API key is properly configured
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        return False, "❌ GOOGLE_API_KEY not found in .env file"
    
    if len(api_key) < 20:
        return False, "❌ GOOGLE_API_KEY seems invalid (too short)"
    
    return True, "✅ API Key configured"


def get_sample_roadmap():
    """
    Return a sample roadmap for demonstration purposes
    """
    return """
# 🎯 Sample Career Roadmap - Full Stack Developer

This is a sample roadmap. Generate your personalized version by completing the survey!

## Phase 1: Foundation (Months 1-3)
- Learn HTML, CSS, JavaScript basics
- Build 3 simple projects
- Complete freeCodeCamp curriculum

## Phase 2: Intermediate (Months 4-6)
- Learn React.js
- Backend with Node.js
- Build a full-stack application

## Phase 3: Advanced (Months 7-12)
- Learn database design
- Deploy applications
- Build portfolio website
- Start job applications

**Get your personalized roadmap by completing the survey above!**
"""