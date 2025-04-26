import os
import PyPDF2
import google.generativeai as genai
import gradio as gr
from io import BytesIO
import time
from dotenv import load_dotenv

# Try importing moviepy, but provide fallback if not available
try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
    from moviepy.config import change_settings
    # Configure MoviePy to use ImageMagick
    change_settings({"IMAGEMAGICK_BINARY": "auto-detect"})
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("MoviePy not installed. Using HTML animation fallback. To enable video generation, run: pip install moviepy")

# Load environment variables
load_dotenv()

# Configure Gemini AI - Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file."""
    text = ""
    try:
        with BytesIO(pdf_file) as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def generate_summary(text):
    """Generate a concise summary of the answer."""
    summary_prompt = f"""
    Create a brief, clear summary of this text in 2-3 sentences:
    {text}
    Focus on the main points and key takeaways.
    """
    try:
        response = model.generate_content(summary_prompt)
        return "## Quick Summary\n" + response.text + "\n---\n"
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""

def generate_video_summary(answer):
    """Generate a short video summary from the answer text."""
    try:
        # Extract key points for video
        prompt = f"""
        Extract 3-4 key points from this text, each point should be 1-2 sentences:
        {answer}
        Format as simple bullet points.
        """
        
        response = model.generate_content(prompt)
        key_points = [point.strip().lstrip('- ') for point in response.text.split('\n') if point.strip()]
        
        if not key_points:
            return None
            
        # Video settings
        duration_per_point = 4
        total_duration = len(key_points) * duration_per_point
        
        # Create background
        background = ColorClip((800, 600), color=(255, 255, 255))
        background = background.set_duration(total_duration)
        
        # Create text clips with simplified settings
        text_clips = []
        for i, point in enumerate(key_points):
            try:
                # Simplified text clip creation without ImageMagick dependencies
                txt_clip = TextClip(
                    txt=point,
                    size=(700, None),
                    method='label',  # Changed from 'caption' to 'label'
                    font='Arial',
                    fontsize=30,
                    color='black'
                ).set_position('center')
                
                txt_clip = txt_clip.set_start(i * duration_per_point)
                txt_clip = txt_clip.set_duration(duration_per_point)
                text_clips.append(txt_clip)
            except Exception as e:
                print(f"Error creating text clip: {e}")
                continue
        
        if not text_clips:
            return None
            
        # Combine clips
        video = CompositeVideoClip([background] + text_clips)
        
        # Save video with basic settings
        video_path = "summary.mp4"
        video.write_videofile(
            video_path,
            fps=24,
            codec='libx264',
            audio=False,
            preset='ultrafast'
        )
        
        return video_path
    
    except Exception as e:
        print(f"Error generating video: {e}")
        return None

def generate_content_display(answer):
    """Generate either video or HTML animation based on availability"""
    if MOVIEPY_AVAILABLE:
        return generate_video_summary(answer)
    else:
        # Generate HTML animation fallback
        prompt = f"""
        Extract 3-4 key points from this text:
        {answer}
        """
        response = model.generate_content(prompt)
        key_points = [point.strip().lstrip('- ') for point in response.text.split('\n') if point.strip()]
        
        html_content = f"""
        <div style="padding: 20px; background: white; border-radius: 10px;">
            <style>
                @keyframes fadeInOut {{
                    0% {{ opacity: 0; }}
                    20% {{ opacity: 1; }}
                    80% {{ opacity: 1; }}
                    100% {{ opacity: 0; }}
                }}
                .point {{
                    animation: fadeInOut 3s linear infinite;
                    display: none;
                }}
                .point:nth-child(1) {{ animation-delay: 0s; }}
                .point:nth-child(2) {{ animation-delay: 3s; }}
                .point:nth-child(3) {{ animation-delay: 6s; }}
                .point:nth-child(4) {{ animation-delay: 9s; }}
            </style>
            {''.join([f'<div class="point"><h3>{point}</h3></div>' for point in key_points])}
        </div>
        """
        return html_content

def format_answer(answer):
    """Format the answer with markdown styling."""
    prompt = f"""
    Please reformat this response to be well-structured with markdown:
    - Start with a 1-sentence summary (## Summary)
    - Break into logical sections (### Section)
    - Use bullet points for key information
    - Bold important terms
    - Add horizontal rules between sections
    
    Text to format:
    {answer}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error formatting answer: {e}")
        return answer  # Return original if formatting fails

def chat_with_pdf(pdf_file, question, chat_history):
    """Process PDF and answer questions with enhanced display"""
    if pdf_file is None:
        return "Please upload a PDF file first.", chat_history, None
    
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        if not pdf_text:
            return "Could not extract text from PDF. Please try another file.", chat_history, None
        
        # Prepare context-aware prompt
        prompt = f"""
        You are an expert document analyst. Use this PDF content:
        {pdf_text[:15000]}  # Limit context window
        
        Answer this question comprehensively:
        {question}
        
        Requirements:
        - Be accurate and concise
        - Cite page numbers if available
        - Structure with headings and bullet points
        - Highlight key relationships
        - If unsure, say "The PDF doesn't contain this information"
        """
        
        # Get response with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                summary = generate_summary(response.text)
                formatted_answer = summary + format_answer(response.text)
                display_content = generate_content_display(response.text)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)  # Wait before retry
        
        # Update chat history with new message format
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": formatted_answer})
        
        return "", chat_history, display_content
    
    except Exception as e:
        error_msg = f"Error: {str(e)}. Please check your API key and internet connection."
        print(error_msg)
        return error_msg, chat_history, None

# Custom CSS for better appearance
css = """
.gradio-container {
    max-width: 1000px !important;
    margin: auto;
}
.chatbot {
    min-height: 500px;
    border-radius: 10px;
}
.markdown-text {
    font-family: 'Helvetica', Arial, sans-serif;
    line-height: 1.6;
}
"""

# Gradio interface
with gr.Blocks(title="Enhanced PDF Chat with Gemini", css=css) as app:
    gr.Markdown("""# 📄 Enhanced PDF Chat with Gemini AI
    Upload a PDF and ask questions. Get structured answers with video summaries.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(label="Upload PDF", type="binary", file_types=[".pdf"])
            question_input = gr.Textbox(
                label="Your Question", 
                placeholder="Ask something about the PDF...",
                lines=3,
                elem_classes="markdown-text"
            )
            submit_btn = gr.Button("Ask", variant="primary")
        
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="Conversation",
                type="messages",
                avatar_images=("user.png", "bot.png")
            )
            if MOVIEPY_AVAILABLE:
                content_output = gr.Video(label="Summary")
            else:
                content_output = gr.HTML(label="Summary")
    
    # Additional controls
    with gr.Row():
        clear_btn = gr.ClearButton([pdf_input, question_input, chatbot, content_output])
        examples = gr.Examples(
            examples=[
                ["What are the key findings in this document?", "Summarize the main points"],
                ["Explain the methodology used", "What are the conclusions?"]
            ],
            inputs=[question_input],
            label="Example Questions"
        )
    
    submit_btn.click(
        fn=chat_with_pdf,
        inputs=[pdf_input, question_input, chatbot],
        outputs=[question_input, chatbot, content_output]
    )

if __name__ == "__main__":
    app.launch(share=False)