import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Try to import the google generativeai package
try:
    import google.generativeai as genai
    HAS_GEMINI_SDK = True
except ImportError:
    HAS_GEMINI_SDK = False
    logger.warning("google-generativeai SDK is not installed. Falling back to local summary generator.")

# A dictionary of pre-authored high-quality mock reviews/summaries for our seeded books
MOCK_SUMMARIES = {
    "The Pragmatic Programmer": {
        "summary": "A classic guide for software developer professionals. It covers topics ranging from personal responsibility and career development to architectural techniques for keeping your code flexible and easy to adapt and reuse.",
        "themes": [
            "Continuous Learning: You must invest in your knowledge portfolio constantly.",
            "Orthogonality: Designing systems where changes in one part do not impact another.",
            "Dry Principle: Don't Repeat Yourself - avoiding duplicate representations of knowledge.",
            "Quality Code: Knowing when to stop, Refactoring, and writing automated tests."
        ],
        "recommendation": "Essential reading for anyone looking to transition from a code coder to an expert software craftsman."
    },
    "Clean Code": {
        "summary": "A comprehensive guide to software craftsmanship, focusing on writing clean, readable, and highly maintainable code. It demonstrates how to identify 'bad' code and systematically refactor it into clean solutions.",
        "themes": [
            "Readability: Code is read far more often than it is written.",
            "Meaningful Names: Naming variables, functions, and classes with absolute clarity.",
            "Single Responsibility: Functions and classes should do one thing and do it well.",
            "TDD: Test-driven development is key to stable codebases."
        ],
        "recommendation": "Perfect for software engineers of all levels who want to elevate the clarity and stability of their codebases."
    },
    "A Brief History of Time": {
        "summary": "Stephen Hawking's landmark work designed for non-scientists. It explains the complex concepts of cosmology, quantum mechanics, black holes, and the nature of time itself in a language that is easy to comprehend.",
        "themes": [
            "The Expansion of the Universe: How space and time are dynamic rather than fixed.",
            "Quantum Mechanics vs General Relativity: The ongoing quest for a unified Theory of Everything.",
            "Black Holes: The fascinating science of massive singularities and space-time warps."
        ],
        "recommendation": "Highly recommended for curious minds who want to understand the origins of the cosmos and the fundamental laws of physics."
    },
    "Dune": {
        "summary": "A monumental sci-fi epic set on the desert planet Arrakis. It tells the story of Paul Atreides and explores complex intersections of ecology, religion, politics, and human potential in a futuristic space empire.",
        "themes": [
            "Ecology and Resource Scarcity: The life-sustaining value of water and spice.",
            "Power and Corruption: The danger of blind devotion to charismatic leaders.",
            "Human Adaptation: Unlocking latent mental capacities through strict physical training."
        ],
        "recommendation": "A must-read masterpiece for fans of deep world-building, political intrigue, and philosophical science fiction."
    },
    "Steve Jobs": {
        "summary": "Walter Isaacson's definitive biography of the Apple co-founder. Based on more than forty interviews with Jobs conducted over two years, it paints a portrait of a creative, driven, and sometimes abrasive visionary.",
        "themes": [
            "Product Integration: Merging beautiful design with cutting-edge engineering.",
            "Intellectual Honesty: Challenging convention and striving for absolute perfection.",
            "The Reality Distortion Field: Pushing people to achieve things they thought were impossible."
        ],
        "recommendation": "A fascinating study of creativity, leadership, and entrepreneurship for product managers, founders, and designers."
    }
}

def generate_book_summary(title, author, description=""):
    """
    Generates a book summary using Google Gemini API.
    If the API is unconfigured, or the key is missing, or an error occurs,
    it falls back to a high-quality local generator.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    
    if api_key and HAS_GEMINI_SDK:
        try:
            logger.info(f"Attempting to generate AI summary for '{title}' using Gemini API...")
            genai.configure(api_key=api_key)
            
            # Using the fast, reliable gemini-1.5-flash model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are an expert literary critic and librarian. Generate a beautiful, engaging summary and breakdown for the book:
            Title: {title}
            Author: {author}
            Description Context: {description}
            
            Please respond in exactly the following structured format using valid markdown. Do not include introductory text like "Sure, here's your summary:". Go straight into the markdown sections:

            ### Executive Summary
            [Provide a compelling 3-4 sentence overview of the book's core premise, narrative, or educational focus.]

            ### Key Themes & Takeaways
            - **[Theme/Takeaway 1]**: [Detailed explanation of why it matters.]
            - **[Theme/Takeaway 2]**: [Detailed explanation of why it matters.]
            - **[Theme/Takeaway 3]**: [Detailed explanation of why it matters.]
            - **[Theme/Takeaway 4]**: [Detailed explanation of why it matters.]

            ### Target Audience & Recommendation
            [A couple of sentences outlining who would benefit most from reading this book and why it stands out in its genre.]
            """
            
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}. Falling back to local generator.")
            # Let code execution flow downward to the fallback
            pass

    # LOCAL FALLBACK GENERATOR LOGIC
    # 1. If we have a pre-authored local summary, format it beautifully in the same markdown layout
    for key, data in MOCK_SUMMARIES.items():
        if key.lower() in title.lower():
            themes_str = "\n".join([f"- **{t.split(':')[0]}**: {t.split(':')[1] if ':' in t else t}" for t in data["themes"]])
            return f"""### Executive Summary
{data['summary']}

### Key Themes & Takeaways
{themes_str}

### Target Audience & Recommendation
{data['recommendation']}
(Note: Generated using local high-fidelity fallback because the Gemini API Key is not set or reached its limit)."""

    # 2. For any other book, generate a beautiful dynamic template summary based on the description
    desc_context = description if description else "a fascinating journey into its subject matter."
    if len(desc_context) > 200:
        short_desc = desc_context[:200] + "..."
    else:
        short_desc = desc_context

    return f"""### Executive Summary
*"{title}"* is a remarkable book written by **{author}**. It explores {short_desc} The author provides comprehensive coverage and expert insights into these concepts, building a systematic understanding that challenges the reader to think deeply.

### Key Themes & Takeaways
- **Insightful Exploration**: An in-depth analysis of the central concepts behind {title}.
- **Authoritative Perspective**: Written by {author}, utilizing years of expertise and specialized knowledge.
- **Structured Knowledge**: Systematically guides the reader from fundamental theories to advanced practical applications.
- **Practical Application**: Clear strategies to apply these core learnings in everyday life and professional careers.

### Target Audience & Recommendation
This book is highly recommended for professionals, students, and readers interested in this domain who want to quickly gain a solid, intelligent overview of the subject.
*(Note: Generated using local high-fidelity fallback because the Gemini API Key is not set or reached its limit).*"""
