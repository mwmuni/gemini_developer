# This script allows Google Gemini to act as an agent for the user.

import os
import subprocess
from ask_gemini import GeminiClient
from vertexai.preview.generative_models import GenerationResponse
import pathlib
import json

def main():
    '''Contains the main loop that allows the user to interact with the agent.'''
    
    # Initialize the GeminiClient
    gc = GeminiClient()
    
    response_text = ""
    
    
    
    # Main loop
    while True:
        
        components = []
        
        if response_text:
            # Print the response
            print(f'Agent: {response_text}')
            components = parse_message_components(response_text)
        
        command_outputs = ""
        
        for component in components:
            
            if '```bash' in component:
                # There can only be one shell command per block
                shell_command = component[7:-3]
                print(f'Shell command: {shell_command}')
                # Check if the command is a cd command
                if shell_command.strip().startswith('cd '):
                    new_dir = shell_command.strip()[3:]
                    os.chdir(new_dir)
                    print(f'Changed directory to {new_dir}')
                else:
                    # command_output = subprocess.run(shell_command.strip(), shell=True, capture_output=True, universal_newlines=True).stdout
                    # I want to capture the output of the command in realtime
                    command_output = ""
                    with subprocess.Popen(shell_command.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as p:
                        if p.stdout is not None:
                            for line in p.stdout:
                                command_output += line
                                print(line, end='')
                    command_outputs += command_output

            elif '```python' in component:
                # Filename is the first line of the Python code as a comment
                filename = component.split('\n')[1].split('# ')[1].strip()
                
                # Write the Python code to a file
                with open(filename, 'w') as f:
                    f.write(component[9:-3])
        else:
            if not command_outputs:
                command_outputs = "<<<STDOUT EMPTY>>>"
            
            # Generate the response
            response = gc.generate('<<<STDOUT BEGIN>>>' + command_outputs + '<<<STDOUT END>>>')
            
            # If the response is iterable, concatenate the text
            if not isinstance(response, GenerationResponse):
                response_text = ''.join([response.text for response in response])
            else:
                response_text = response.text
        if not components:
            # Get the user's input
            user_input = input('You: ')
            
            # Check if the user wants to exit
            if user_input.lower() == 'exit':
                break
            
            # Generate a response
            response = gc.generate(user_input)
            
            # If the response is iterable, concatenate the text
            if not isinstance(response, GenerationResponse):
                response_text = ''.join([r.text for r in response])
            else:
                response_text = response.text

def parse_message_components(message: str):
    '''Parses the message into its components.'''
    components = []
    
    if '```' not in message:
        return []
    
    # Find the start of the first component
    start = message.index('```')
    # start = message.index('\n', start) + 1
    
    while start != -1:
        # Find the end of the first component
        end = message.index('```', start + 3)
        
        # Add the component to the list
        components.append(message[start:end + 3].strip())
        
        # Find the start of the next component
        try:
            start = message.index('```', end + 3)
        except ValueError:
            start = -1
    
    return components

if __name__ == '__main__':
    main()