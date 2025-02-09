# AI Tool Generator

A Python-based tool generator that creates custom tools for AI agents based on natural language descriptions.

## Features

- Generates complete Python tool classes based on text descriptions
- Automatically creates documentation for each tool
- Inherits from the `smolagents.Tool` base class
- Generates proper initialization, forward methods, and error handling
- Creates README files for each generated tool

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-tool-generator.git
cd ai-tool-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Azure OpenAI credentials:
```
AZURE_OPENAI_API_KEY=your_api_key
OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_ENDPOINT=your_endpoint
```

## Usage

Here's a simple example of how to use the tool generator:

```python
from ToolGenerator import ToolGenerator

# Initialize the generator
generator = ToolGenerator()

# Generate a tool based on a description
description = "Create a tool that can send emails using SMTP"
code, filename, readme = generator.generate_tool(description)

# Save the generated tool and its documentation
generator.save_tool(code, filename, readme)
```

## Project Structure

```
ai-tool-generator/
├── ToolGenerator.py        # Main tool generation class
├── requirements.txt        # Project dependencies
├── .env                   # Environment variables (not tracked)
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 