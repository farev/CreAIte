from smolagents import Tool
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
import re

class ToolGenerator:
    def __init__(self):
        load_dotenv()
        # Configure Azure OpenAI
        self.client = AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('OPENAI_API_VERSION'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )
        
    def generate_tool(self, description: str) -> tuple[str, str, str]:
        """
        Generates a tool class and README based on user description
        
        Args:
            description: User's description of what the tool should do
        Returns:
            tuple: (str: Python code for the generated tool, 
                    str: suggested filename,
                    str: README content)
        """
        prompt = f"""
        Create a tool class for an AI agent based on this description: "{description}"
        
        The tool should:
        1. Inherit from smolagents.Tool
        2. Have name, description, inputs, and output_type class attributes
        3. Include proper initialization in __init__
        4. Have a forward method that the agent calls
        5. Include any necessary helper methods
        6. Include detailed docstrings and comments
        
        Use this Discord tool as a reference structure:
        
        ```python
        class DiscordMessageTool(Tool):
            name = "discord_message"
            description = "Sends a message to a specified Discord channel"
            inputs = {{
                "message": {{
                    "type": "string",
                    "description": "The message to send to Discord"
                }}
            }}
            output_type = "string"
            
            def __init__(self, token, channel_id):
                self.token = token
                self.channel_id = channel_id
                self.client = discord.Client(intents=discord.Intents.default())
                self.is_initialized = True # Make sure this is set to True! VERY IMPORTANT!
            
            def forward(self, message: str) -> str:
                # Implementation
                pass
        ```
        
        Generate complete, working Python code for the tool.
        Include all necessary imports at the top.
        Make sure to handle errors appropriately.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-32k",  # Use your deployed model name
            messages=[
                {"role": "system", "content": "You are an expert Python developer specializing in creating tools for AI agents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract code from response
        generated_code = response.choices[0].message.content
        
        # Clean up the code (remove markdown if present)
        code = self._clean_code(generated_code)
        
        # Extract class name using regex
        class_match = re.search(r'class\s+(\w+)', code)
        if class_match:
            filename = f"{class_match.group(1)}.py"
        else:
            filename = "generated_tool.py"
        
        # Generate README content
        readme_prompt = f"""
        Create a README.md file for this tool that includes:
        1. Brief description of what the tool does
        2. Required dependencies/imports
        3. Installation instructions
        4. Example usage code showing how to initialize and use the tool
        5. Any configuration requirements (environment variables, API keys, etc.)
        
        Use this code as reference:
        {code}
        """
        
        readme_response = self.client.chat.completions.create(
            model="gpt-4-32k",
            messages=[
                {"role": "system", "content": "You are a technical writer creating clear documentation for Python tools."},
                {"role": "user", "content": readme_prompt}
            ],
            temperature=0.7
        )
        
        readme_content = readme_response.choices[0].message.content
        
        return code, filename, readme_content
    
    def _clean_code(self, code: str) -> str:
        """Remove markdown, comments and clean up the generated code"""
        # Remove markdown code blocks if present
        code = re.sub(r'```python\n', '', code)
        code = re.sub(r'```\n?', '', code)
        
        # Remove any leading/trailing explanatory text
        code_lines = code.split('\n')
        start_idx = 0
        end_idx = len(code_lines)
        
        # Find first line of actual code (usually import or class definition)
        for i, line in enumerate(code_lines):
            if line.strip() and (line.startswith('import') or line.startswith('from') or line.startswith('class')):
                start_idx = i
                break
        
        # Find last line of actual code (looking for class closing or last method)
        for i in range(len(code_lines) - 1, -1, -1):
            line = code_lines[i].strip()
            # Check if line is actual code (not a comment or explanation)
            if line and not line.startswith('#'):
                # Make sure it's part of the class (proper indentation or class end)
                if line == '}' or line.endswith(':') or line.startswith('def ') or line.startswith('return ') or line.startswith(')'):
                    end_idx = i + 1
                    break
        
        # Extract only the actual code
        code = '\n'.join(code_lines[start_idx:end_idx])
        
        return code.strip()
    
    def save_tool(self, code: str, filename: str, readme_content: str = None):
        """
        Save the generated tool and README to files
        
        Args:
            code: The generated tool code
            filename: The Python file name
            readme_content: Optional README content
        """
        # Save the Python file
        with open(filename, 'w') as f:
            f.write(code)
        
        # Save README if provided
        if readme_content:
            # Get the directory name from the tool name
            dir_name = filename.replace('.py', '')
            
            # Create directory if it doesn't exist
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            
            # Move the Python file into the directory
            os.rename(filename, os.path.join(dir_name, filename))
            
            # Save README in the directory
            with open(os.path.join(dir_name, 'README.md'), 'w') as f:
                f.write(readme_content) 
