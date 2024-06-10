# This script allows Google Gemini to act as an agent for the user.

import os
import subprocess
from ask_gemini import GeminiClient
from vertexai.preview.generative_models import GenerationResponse
import pathlib
import json

file_types = [
    'python', 'sh', 'txt', 'html', 'css', 'js', 'json', 'xml', 'yaml', 'yml', 'md', 'csv', 'tsv', 'sql', 'java', 'c', 'cpp', 'h', 'hpp', 'cs', 'php', 'rb', 'pl', 'go', 'rs', 'swift', 'kt', 'clj', 'cljs', 'r', 'm', 'jl', 'groovy', 'scala', 'dart', 'asm', 'asmx', 'aspx', 'jsp', 'php', 'php3', 'php4', 'php5', 'php7', 'php8', 'phps', 'phtml', 'py', 'ipynb'
]

file_ext = {
    'python': 'py', 'sh': 'sh', 'txt': 'txt', 'html': 'html', 'css': 'css', 'js': 'js', 'json': 'json', 'xml': 'xml', 'yaml': 'yaml', 'yml': 'yml', 'md': 'md', 'csv': 'csv', 'tsv': 'tsv', 'sql': 'sql', 'java': 'java', 'c': 'c', 'cpp': 'cpp', 'h': 'h', 'hpp': 'hpp', 'cs': 'cs', 'php': 'php', 'rb': 'rb', 'pl': 'pl', 'go': 'go', 'rs': 'rs', 'swift': 'swift', 'kt': 'kt', 'clj': 'clj', 'cljs': 'cljs', 'r': 'r', 'm': 'm', 'jl': 'jl', 'groovy': 'groovy', 'scala': 'scala', 'dart': 'dart', 'asm': 'asm', 'asmx': 'asmx', 'aspx': 'aspx', 'jsp': 'jsp', 'php3': 'php3', 'php4': 'php4', 'php5': 'php5', 'php7': 'php7', 'php8': 'php8', 'phps': 'phps', 'phtml': 'phtml', 'py': 'py', 'ipynb': 'ipynb'
}

file_comments = {
    'python': '#', 'sh': '#', 'txt': '', 'html': '<!-- -->', 'css': '/* */', 'js': '/* */', 'json': '/* */', 'xml': '<!-- -->', 'yaml': '#', 'yml': '#', 'md': '<!-- -->', 'csv': '#', 'tsv': '#', 'sql': '--', 'java': '//', 'c': '//', 'cpp': '//', 'h': '//', 'hpp': '//', 'cs': '//', 'php': '//', 'rb': '#', 'pl': '#', 'go': '//', 'rs': '//', 'swift': '//', 'kt': '//', 'clj': ';;', 'cljs': ';;', 'r': '#', 'm': '#', 'jl': '#', 'groovy': '//', 'scala': '//', 'dart': '//', 'asm': ';', 'asmx': ';', 'aspx': '<!-- -->', 'jsp': '<!-- -->', 'php3': '//', 'php4': '//', 'php5': '//', 'php7': '//', 'php8': '//', 'phps': '//', 'phtml': '<!-- -->', 'py': '#', 'ipynb': '#'
}

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
                continue
            elif '```tool_code' in component:
                # We want to execute this as python code
                python_code = component[12:-3]
                print(f'Python code: {python_code}')
                exec(python_code)

            lines = component.split('\n')
            name = lines[0][3:]
            if name in file_types:
                # Find the location of the comment on the second line
                comment = lines[1]
                # If the comment has a space, treat it as start and end
                comment_syntax = file_comments[name]
                if len(token := comment_syntax.split(' ')) == 2:
                    comment_start, comment_end = token
                    if comment.startswith(comment_start) and comment.endswith(comment_end):
                        filename = comment[len(comment_start):-len(comment_end)+1].strip()
                else:
                    filename = comment[len(comment_syntax):].strip()
                if filename:
                    # Write the code to a file
                    with open(f'{filename}', 'w') as f:
                        f.write(component[len(''.join(lines[:2]))+2:-3])
            
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