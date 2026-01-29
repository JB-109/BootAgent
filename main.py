import os
import sys
import config
import functions.get_files_info
import functions.get_file_content
import functions.run_python_file
import functions.write_files

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

client = genai.Client(api_key=api_key)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    prompt = input("How can I help you now? ")

if not prompt or not prompt.strip():
    print("Please provide a prompt!")
    sys.exit(1)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# "parts" is just an attribute of the Content class, but part is a class instance in the types module.
messages = [
    types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
]

functions_map = {
    "get_files_info": functions.get_files_info.get_files_info,
    "get_file_content": functions.get_file_content.get_file_content,
    "run_python_file": functions.run_python_file.run_python_file,
    "write_files": functions.write_files.write_files 
}

# here schema for each function is defined
available_functions = types.Tool(
    function_declarations=[
        functions.get_files_info.schema_get_files_info,
        functions.get_file_content.schema_get_file_content,
        functions.run_python_file.schema_run_python_file,
        functions.write_files.schema_write_files
    ]
)


def call_function(function_call_part, verbose=False):
    if function_call_part.name in functions_map:

        if verbose:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")

        # double star means unpack the dictionary into keyword arguments 
        # whereas single star means to unpack the list or tuple in positional arguments
        result = functions_map[function_call_part.name](working_dir=os.path.abspath("./calculator"), **function_call_part.args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ]
        )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# max self-talk: 15
count = 0
while count <= 14:

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=config.system_prompt,
            tools=[available_functions]
        )
    )

    has_function_calls = response.function_calls is not None and len(response.function_calls) > 0
    has_text_response = response.text is not None and response.text.strip()
    
    if not has_function_calls:
        if has_text_response:
            print(response.text)
            if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                print(f"Prompt token: {response.usage_metadata.prompt_token_count}")
                print(f"Response token: {response.usage_metadata.candidates_token_count}")
        elif len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            print(f"[DEBUG] No text response. Raw response: {response}")
        break

    function_responses = []
    for each in response.function_calls:

        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            result = call_function(each, True)
        else: 
            result = call_function(each)

        if not result.parts or not result.parts[0].function_response:
            raise Exception("empty function call result")
        
        # appending only the parts (attribute),
        # Parts attribute contain the part class instance which contains fn name and response.
        function_responses.append(result.parts[0])
    
    # Add model's response (with function_call) to maintain conversation flow,
    # it contains all the functions that llm asks to call.
    messages.append(response.candidates[0].content)
    
    messages.append(
        types.Content(
            role="tool",
            parts=function_responses
        )
    )

    count += 1
