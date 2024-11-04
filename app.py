# app.py
import gradio as gr
from main import TextToSpeechConverter
import os

class PodcastGenerator:
    def __init__(self):
        # Initialize the converter
        self.converter = TextToSpeechConverter()
        
    def generate_podcast(self, text):
        """
        Generate a conversational podcast from input text.
        
        Args:
            text (str): Input text to convert to conversation
        Returns:
            tuple: (audio_file_path, status_message)
        """
        if not text:
            return None, "Please enter some text to convert"
            
        try:
            # Create output directory if it doesn't exist
            os.makedirs('output', exist_ok=True)
            
            # Generate unique output filename in the output directory
            output_file = os.path.join('output', f"podcast_conversation_{hash(text)}.wav")
            
            # Generate conversational audio
            success, result, message = self.converter.create_conversation_audio(
                text=text,
                output_file=output_file
            )
            
            if success:
                return result, "✓ Podcast generated successfully!"
            else:
                return None, f"⚠ Error: {message}"
                
        except Exception as e:
            return None, f"⚠ Error: {str(e)}"

def create_interface():
    """Creates and configures the Gradio interface"""
    generator = PodcastGenerator()
    
    # Create the interface
    iface = gr.Interface(
        fn=generator.generate_podcast,
        inputs=[
            gr.Textbox(
                lines=10,
                label="Paste your text here",
                placeholder="Enter the text you want to convert into a conversational podcast...",
                info="Your text will be converted into a natural conversation between Alex and Sarah"
            )
        ],
        outputs=[
            gr.Audio(label="Generated Podcast"),
            gr.Textbox(label="Status")
        ],
        title="Conversational Blog to Podcast Converter",
        description="""Convert your text into an engaging conversation between two hosts (Alex and Sarah).
        The content will be intelligently processed into a natural dialogue while maintaining key messages.""",
        examples=[
            ["AI is transforming content creation. New tools and technologies enable creators to produce high-quality content more efficiently than ever before. These developments are changing how we think about content production."],
            ["The future of work is being reshaped by artificial intelligence. Companies are adopting AI tools to streamline operations and boost productivity. This shift is creating new opportunities and challenges for workers."]
        ],
        # Updated deprecated parameter
        flagging_mode=None,
        theme=gr.themes.Soft(),
        article="""### How it works:
        1. Enter your text in the input box
        2. The AI processes it into a natural conversation
        3. Two different voices bring the conversation to life
        4. Download the generated podcast audio file
        """
    )
    
    return iface

if __name__ == "__main__":
    # Create and launch the interface
    iface = create_interface()
    # Launch with share=True to get a public URL
    iface.launch(share=True)