from flask import Flask, render_template, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Print out the environment variables to verify they are loaded correctly
groq_api_key = os.getenv("GROQ_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# Check if the keys are loaded correctly and print them
if groq_api_key and langchain_api_key:
    print(f"GROQ_API_KEY: {groq_api_key}")
    print(f"LANGCHAIN_API_KEY: {langchain_api_key}")
else:
    print("Error: One or more API keys are missing from the .env file.")

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# LangChain config
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a kawaii anime chatbot. Answer based on the image context and question."),
    ("user", "Image description: {context}\nQuestion: {question}")
])
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192"
)
chain = prompt | llm | StrOutputParser()

# Load image captioning model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Store image context globally (or per-session if needed)
image_context = ""

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image uploads
@app.route('/upload-image', methods=['POST'])
def upload_image():
    global image_context
    file = request.files['image']
    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # Generate caption/description for the image
        raw_image = Image.open(image_path).convert('RGB')
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        image_context = processor.decode(out[0], skip_special_tokens=True)

        return jsonify({
            "message": "Image uploaded successfully!",
            "context": image_context,
            "image_url": f"/static/uploads/{file.filename}"
        })
    return jsonify({"error": "No file received"}), 400

# Route to handle user questions based on the uploaded image
@app.route('/ask', methods=['POST'])
def ask():
    global image_context
    data = request.get_json()
    question = data.get("question")
    response = chain.invoke({
        "question": question,
        "context": image_context
    })
    return jsonify({"response": response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
