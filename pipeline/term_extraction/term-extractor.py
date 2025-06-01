from google import generativeai as genai
from extractor import extract

resources_folder = "./resources"
extracted_text = extract(resources_folder)

API_KEY = "" #insert API key here

genai.configure(api_key=API_KEY)

model_name="gemini-1.5-flash"
system_instruction = """You are an expert in building ontologies for pre-salt petroleum reservoirs. 
You will receive a large compilation of text from research papers and theses related to pre-salt geology. 
Your goal is to extract and rank the approximately 200 most important concepts for helping select the words for building an ontology structure. 
Prioritize broader concepts over specific examples.  
The text is a compilation of multiple sources covering diverse topics within pre-salt geology.
"""

prompt = f"""You are provided with a substantial collection of text from 10 research papers and master theses on pre-salt geology and petroleum systems. 
This compilation represents a significant body of knowledge, providing ample material for extracting key concepts. 
Your task is to analyze this multilingual text (English and Portuguese) and extract, rank, and return approximately 200 of the most important concepts for building an ontology.

Instructions:

1. Multilingual Text Processing:
- Translate all Portuguese text to English.
- Maintain consistent terminology across languages.

2. Concept Extraction:
- Identify essential terms relevant to pre-salt geology and petroleum reservoirs.

3. Selection Criteria:
- Prioritize terms relevant to pre-salt geology, considering both frequency and domain importance. 
Exclude specific names such as basins names, well names, specialized data, isotopic nomenclature, and overly narrow examples. Focus on broader, general concepts.

4. Output:
- A ranked, numbered list of terms, one term per line.  Do *not* include frequency counts or other information in this initial output.  

The extracted text follows: 
{extracted_text}"""
generation_config = genai.GenerationConfig(
    temperature=0.1,
)

model = genai.GenerativeModel(model_name=model_name,
                              system_instruction=system_instruction,
                              generation_config=generation_config)

response = model.generate_content(prompt)
print(response.text)

print("total tokens: ", model.count_tokens(prompt + extracted_text))