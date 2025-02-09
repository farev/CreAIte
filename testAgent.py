from smolagents import CodeAgent, HfApiModel
import os
from dotenv import load_dotenv
from EmailSMTPTool.EmailSMTPTool import EmailSMTPTool

load_dotenv()

email_tool = EmailSMTPTool('smtp.example.com', 587, 'myemail@example.com', 'mypassword')


model = HfApiModel(token=os.getenv('HF_API_TOKEN')) # You can choose to not pass any model_id to HfApiModel to use a default free model
agent = CodeAgent(
    tools=[email_tool],
    model=model,
    add_base_tools=True
)

agent.run(
    "Can you send an email to myemail@example.com verifying that you are now capable of sending emails.",
)