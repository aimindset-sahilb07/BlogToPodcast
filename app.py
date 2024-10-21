import gradio as gr
from main import text_to_speech

def generate_podcast(text):
    """
    Generate a podcast (audio file) from the given text.
    Args:
    text (str): The input text to be converted to speech.
    Returns:
    str or None: The path to the generated audio file if successful, None if an error occurred.
    """
    output_file = "podcast.wav"
    result = text_to_speech(text, output_file)
    if result:
        return output_file
    else:
        return None

# Create the Gradio interface
iface = gr.Interface(
    # Specify the function to be called when the interface is used
    fn=generate_podcast,
    
    # Define the input component: a text box for user input
    inputs=gr.Textbox(lines=10, label="Paste your text here. Upto 10 lines of text only"),
    
    # Define the output component: an audio player to play the generated podcast
    outputs=gr.Audio(label="Generated Podcast"),
    
    # Set the title of the interface
    title="Blog to Podcast Converter",
    
    # Provide a description of what the interface does
    description="1-Click Podcast from your text",

     # Disable Flag Button
     allow_flagging="never",
    
    # Provide example inputs for users to try
    examples=[
        ["Artificial Intelligence is rapidly evolving, transforming industries and our daily lives. From self-driving cars to advanced language models, AI is pushing the boundaries of what's possible."],
        ["The importance of sustainable living cannot be overstated. By making small changes in our daily habits, we can contribute to a healthier planet and a brighter future for generations to come."]
    ]

   
)

# This block only runs if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    # Launch the Gradio interface
    iface.launch()