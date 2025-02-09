from ToolGenerator import ToolGenerator

def main():
    generator = ToolGenerator()
    
    # Example tool descriptions
    descriptions = [
        "Create a tool that can send emails using SMTP",
    ]
    
    for i, description in enumerate(descriptions):
        print(f"\nGenerating tool for: {description}")
        
        # Generate the tool code
        code, filename, readme = generator.generate_tool(description)
        
        # Save to file
        #filename = f"generated_tool_{i+1}.py"
        generator.save_tool(code, filename, readme)
        print(f"Tool saved to {filename}")
        
        # Print the generated code
        print("\nGenerated Code:")
        print("=" * 50)
        print(code)
        print("=" * 50)

if __name__ == "__main__":
    main() 