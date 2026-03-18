import asyncio
import tools
from agents import Agent, Runner, SessionSettings, RunConfig, trace
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

agent = Agent(
    name="Login Agent",
    instructions="You are a browser automation agent. Go to Duolingo.com, click the login button, " \
                "enter the email and password, and log in to your account." \
                "Then, start a lesson." \
                "Action plan:" \
                "1. take a screenshot" \
                "2. plan your clicks\types based on the screenshot" \
                "3. execute your plan by clicking and typing" \
                "4. take another screenshot to make sure your plan worked. Unless logged in, Repeat steps 2-4." \
                "5. If browser still loading, wait 5 seconds and take another screenshot. Do this up to 3 times before reporting an error." \
                "",
    tools=[
        tools.open_duolingo,
        tools.take_screenshot,
        tools.click,
        tools.type_text,
        tools.press_key,
        tools.type_duolingo_email,
        tools.type_duolingo_password,
    ],
)

async def main():
    with trace("Duolingo Streak Agent Run"):
        result = await Runner.run(agent,
                                  "",
                                  max_turns=30,
                                  )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())