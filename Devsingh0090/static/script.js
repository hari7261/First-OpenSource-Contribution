let currentSpeech = null;
const speechSynthesis = window.speechSynthesis;

// Helper function to clean text for speech
function prepareTextForSpeech(text) {
    return text.replace(/[•*]/g, '')
              .replace(/\n/g, '. ')
              .replace(/\s+/g, ' ')
              .replace(/[[\]]/g, '')  // Remove brackets
              .replace(/[📌🎯💡🌟❗]/g, '')  // Remove emojis
              .trim();
}

// Add typing animation function
function typewriterEffect(text, element, speed = 10) {
    let index = 0;
    element.innerHTML = '';
    
    return new Promise((resolve) => {
        function type() {
            if (index < text.length) {
                if (text.slice(index).startsWith('<div')) {
                    const endIndex = text.indexOf('>', index) + 1;
                    element.innerHTML += text.slice(index, endIndex);
                    index = endIndex;
                } else {
                    element.innerHTML += text[index];
                    index++;
                }
                setTimeout(type, speed);
            } else {
                resolve();
            }
        }
        type();
    });
}

// Automatically start speaking when new response arrives
function autoSpeak(text) {
    if (currentSpeech && speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }

    const avatar = document.querySelector('.assistant-avatar');
    avatar.classList.add('speaking');
    
    text = prepareTextForSpeech(text);
    currentSpeech = new SpeechSynthesisUtterance(text);
    
    // Get available voices and select a female voice if available
    let voices = speechSynthesis.getVoices();
    let femaleVoice = voices.find(voice => voice.name.includes('female') || voice.name.includes('woman'));
    if (femaleVoice) currentSpeech.voice = femaleVoice;
    
    currentSpeech.rate = 1;
    currentSpeech.pitch = 1;

    // Add dynamic avatar animation
    currentSpeech.onboundary = function(event) {
        avatar.style.transform = 'scale(1.1)';
        setTimeout(() => {
            avatar.style.transform = 'scale(1)';
        }, 150);
    };
    
    currentSpeech.onend = () => {
        avatar.classList.remove('speaking');
        avatar.style.transform = 'scale(1)';
    };
    
    speechSynthesis.speak(currentSpeech);
}

document.addEventListener('DOMContentLoaded', () => {
    const avatar = document.querySelector('.assistant-avatar');
    const tooltip = document.querySelector('.avatar-tooltip');
    
    // Show tooltip on hover
    avatar.addEventListener('mouseenter', () => {
        tooltip.classList.add('visible');
    });
    
    avatar.addEventListener('mouseleave', () => {
        tooltip.classList.remove('visible');
    });

    avatar.addEventListener('click', () => {
        const lastResponse = document.querySelector('.message.assistant:last-child');
        if (lastResponse) {
            // Clear existing content
            const content = lastResponse.innerHTML;
            lastResponse.innerHTML = '';
            
            // Start typing animation and speech
            typewriterEffect(content, lastResponse, 10);
            autoSpeak(lastResponse.textContent);
            
            // Add animation class to avatar
            avatar.classList.add('speaking');
        }
    });
});

document.getElementById('pdf-input').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('upload-status').classList.remove('hidden');
        document.getElementById('upload-label').textContent = 'Change PDF';
    }
});

document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const pdfFile = document.getElementById('pdf-input').files[0];
    const question = document.getElementById('question-input').value.trim();
    
    if (!pdfFile || !question) {
        alert('Please provide both a PDF file and a question');
        return;
    }
    
    formData.append('pdf_file', pdfFile);
    formData.append('question', question);
    
    // Show loading state
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = 'Processing...';
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000);
        
        const response = await fetch('/chat', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            },
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error('Server error');
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Update chat display with typing effect
        const chatMessages = document.getElementById('chat-messages');
        const userMessage = `<div class="message user">${question}</div>`;
        chatMessages.innerHTML += userMessage;

        // Create assistant message container
        const assistantMessage = document.createElement('div');
        assistantMessage.className = 'message assistant';
        chatMessages.appendChild(assistantMessage);

        // Start avatar animation
        const avatar = document.querySelector('.assistant-avatar');
        avatar.classList.add('speaking');

        // Format the response with clean HTML
        const formattedResponse = data.answer.split('\n').map(line => {
            line = line.trim();
            if (!line) return '';
            
            if (line.startsWith('Simple Explanation:')) {
                return `<div class="section main-section">${line}`;
            }
            if (line.startsWith('Key Points:')) {
                return `<div class="section header-section">${line}`;
            }
            if (line.match(/^\d\./)) {
                return `<div class="point-section">${line}`;
            }
            if (line.startsWith('-')) {
                return `<div class="sub-point">${line}</div>`;
            }
            if (line.startsWith('Practical Examples:')) {
                return `<div class="section example-section">${line}`;
            }
            if (line.startsWith('Learning Resources:')) {
                return `<div class="section resources-section">${line}`;
            }
            if (line.startsWith('Key Takeaways:')) {
                return `<div class="section takeaway-section">${line}`;
            }
            
            // Close sections appropriately
            if (['Key Points:', 'Practical Examples:', 'Learning Resources:', 'Key Takeaways:'].some(header => 
                line.startsWith(header))) {
                return `</div><div class="section">${line}`;
            }
            
            return `<div class="text-line">${line}</div>`;
        }).filter(Boolean).join('');

        // Put the formatted response in a container
        const assistantContent = `
            <div class="assistant-content">
                ${formattedResponse}
            </div>
        `;

        assistantMessage.innerHTML = assistantContent;

        // Start typing effect and speech
        typewriterEffect(formattedResponse, assistantMessage, 10);
        autoSpeak(data.answer);

        // Update diagram if available
        if (data.diagram) {
            document.getElementById('diagram-container').innerHTML = 
                `<img src="${data.diagram}" alt="Concept Diagram">`;
        }
        
        // Clear input
        document.getElementById('question-input').value = '';
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'An error occurred. Please try again.');
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    }
});

document.getElementById('clear-btn').addEventListener('click', () => {
    document.getElementById('pdf-input').value = '';
    document.getElementById('question-input').value = '';
    document.getElementById('chat-messages').innerHTML = '';
    document.getElementById('diagram-container').innerHTML = '';
    document.getElementById('upload-status').classList.add('hidden');
    document.getElementById('upload-label').textContent = 'Upload PDF';

    if (speechSynthesis && speechSynthesis.speaking) {
        speechSynthesis.cancel();
        document.getElementById('speak-button').classList.remove('speaking');
    }
});

// Update voice control handlers
document.getElementById('speak-button').addEventListener('click', function() {
    const latestResponse = document.querySelector('.message.assistant:last-child');
    if (!latestResponse) return;
    
    if (currentSpeech && speechSynthesis.speaking) {
        speechSynthesis.cancel();
        document.querySelector('.assistant-avatar').classList.remove('speaking');
        return;
    }
    
    autoSpeak(latestResponse.textContent);
});

document.getElementById('stop-button').addEventListener('click', function() {
    if (currentSpeech && speechSynthesis.speaking) {
        speechSynthesis.cancel();
        document.querySelector('.assistant-avatar').classList.remove('speaking');
    }
});
