import os
import PyPDF2
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session
from io import BytesIO
import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv
import time
import hashlib
from functools import lru_cache
import base64
import re

# Load environment variables
load_dotenv()

# Configure Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'diagrams')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Increase to 50MB
app.config['MAX_BUFFER_SIZE'] = 50 * 1024 * 1024  # Add buffer size config
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add custom error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Maximum file size is 50MB.'}), 413

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Add caching decorator
@lru_cache(maxsize=100)
def cached_generate_content(prompt):
    return model.generate_content(prompt)

def clean_text(text):
    """Clean and normalize text content"""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.replace('\n', ' ').strip()
    return text[:5000]  # Limit text length

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file."""
    try:
        with BytesIO(pdf_file) as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            # Only process first 5 pages
            for page in reader.pages[:5]:
                text += page.extract_text() + " "
            return clean_text(text)
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None

def generate_summary(text):
    """Generate a concise summary of the answer."""
    # Limit input text size
    text = text[:5000]
    summary_prompt = f"""
    Extract 2-3 key points from this text. Be very concise:
    {text}
    """
    try:
        response = cached_generate_content(summary_prompt)
        return response.text + "\n"
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""

def generate_diagram(answer):
    """Generate a concept diagram from the answer text."""
    try:
        # Limit input text size
        answer = answer[:3000]
        # Cache diagram based on input hash
        hash_key = hashlib.md5(answer.encode()).hexdigest()
        diagram_filename = f"diagram_{hash_key}.png"
        diagram_path = os.path.join(app.config['UPLOAD_FOLDER'], diagram_filename)
        
        if os.path.exists(diagram_path):
            return diagram_filename
        
        # Create a directed graph
        G = nx.DiGraph()
        
        prompt = f"""
        Create a simple, hierarchical breakdown of the main concepts from this text:
        {answer}
        
        Return ONLY key relationships in this format (max 5-7 points):
        - [Main Point] -> [Supporting Point] : [Connection]
        Focus on the most important relationships for easy understanding.
        """
        
        response = cached_generate_content(prompt)
        relationships = [line.strip() for line in response.text.split('\n') if '->' in line]
        
        for rel in relationships:
            try:
                parts = rel.split(':')
                nodes_part = parts[0].split('->')
                source = nodes_part[0].strip().lstrip('- ').strip()
                target = nodes_part[1].strip()
                relationship = parts[1].strip() if len(parts) > 1 else "related"
                
                G.add_edge(source, target, label=relationship)
            except Exception as e:
                print(f"Skipping malformed relationship: {rel} - Error: {e}")
                continue
        
        if len(G.edges()) == 0:
            return None
        
        # Draw the diagram with improved layout
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=1.5, iterations=100)
        
        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', alpha=0.9)
        nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
        
        plt.axis('off')
        plt.tight_layout()
        
        # Save the image
        plt.savefig(diagram_path, bbox_inches='tight', dpi=150)
        plt.close()
        
        return diagram_filename
    
    except Exception as e:
        print(f"Error generating diagram: {e}")
        return None

def format_answer(answer):
    """Format the answer with enhanced visual structure."""
    prompt = f"""
    Reorganize this information in an extremely clear, easy-to-read format:

    📌 OVERVIEW
    [Single sentence summary]

    🎯 MAIN POINTS
    1️⃣ [First main point]
      • [Supporting detail]
      • [Supporting detail]

    2️⃣ [Second main point]
      • [Supporting detail]
      • [Supporting detail]

    3️⃣ [Third main point]
      • [Supporting detail]
      • [Supporting detail]

    📚 DETAILED EXPLANATION
    • [Additional important detail]
    • [Additional important detail]

    💡 KEY TERMS
    • **Term 1**: [Brief definition]
    • **Term 2**: [Brief definition]

    Format the response exactly like this template, replacing the bracketed text.
    Use bullet points and emojis as shown above.
    Make each point concise and clear.
    Bold any important terms using **.

    Text to format: {answer}
    """
    try:
        response = cached_generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error formatting answer: {e}")
        return answer

def format_response_for_user(text):
    """Format the response in a clean, structured way"""
    prompt = f"""
    Format the response in these exact sections:

    Simple Explanation:
    [One clear sentence explanation]
    [Why it's important]

    Key Points:
    1. [First main point]
    - [Clear explanation]
    - [Practical importance]
    - [Real example]

    2. [Second main point]
    - [Clear explanation]
    - [Practical importance]
    - [Real example]

    3. [Third main point]
    - [Clear explanation]
    - [Practical importance]
    - [Real example]

    Practical Examples:
    - Business: [industry application]
    - Daily Life: [everyday use]
    - Future: [upcoming trends]

    Learning Resources:
    - Basic: [beginner guide]
    - Advanced: [detailed tutorial]
    - Practice: [hands-on exercise]

    Key Takeaways:
    - Main Point: [core learning]
    - Practical Tip: [application]
    - Remember: [key note]

    Use plain text without special characters.
    Keep sections clearly separated with line breaks.
    Make examples specific and relatable.

    Text to format: {text}
    """
    try:
        response = cached_generate_content(prompt)
        # Clean up the text
        cleaned_text = response.text
        cleaned_text = re.sub(r'[^\w\s\-:.,()[\]1-9]', '', cleaned_text)
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        return cleaned_text.strip()
    except Exception as e:
        return text

def chat_with_pdf(pdf_file, question, chat_history):
    """Process PDF and generate enriched responses"""
    try:
        # Extract or get cached text
        pdf_hash = hashlib.md5(pdf_file).hexdigest()
        if 'pdf_text' not in session or session['pdf_hash'] != pdf_hash:
            pdf_text = extract_text_from_pdf(pdf_file)
            session['pdf_text'] = pdf_text
            session['pdf_hash'] = pdf_hash
        else:
            pdf_text = session['pdf_text']

        if not pdf_text:
            return "Could not process PDF content.", [], None

        prompt = f"""
        Based on this PDF content, provide a comprehensive answer:
        
        Content: {pdf_text}
        Question: {question}

        Requirements:
        1. Start with a crystal-clear explanation
        2. Break down into main points
        3. Include multiple real-world examples:
           - Business applications
           - Daily life scenarios
           - Current events
           - Future trends
        4. Suggest relevant learning resources:
           - Video tutorials (basic to advanced)
           - Articles and guides
           - Industry examples
        5. Use simple language throughout
        6. Make all examples current and relatable
        
        Focus on practical understanding and real-world applications.
        """
        
        response = model.generate_content(prompt)
        formatted_answer = format_response_for_user(response.text)
        
        return formatted_answer, chat_history, None

    except Exception as e:
        print(f"Chat error: {e}")
        return "An error occurred. Please try again.", [], None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'})
        
        file = request.files['pdf_file']
        pdf_file = file.read()
        question = request.form.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Please enter a question'})
            
        answer, history, _ = chat_with_pdf(pdf_file, question, [])
        
        return jsonify({
            'answer': answer,
            'chat_history': history
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
