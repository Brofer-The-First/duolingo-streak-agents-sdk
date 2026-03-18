import tools
from agents import Agent

login_agent = Agent(
    name="Login Agent",
    instructions="""
        You are a browser automation agent.
        Go to Duolingo.com, click the login button, enter the email and password, and log in to your account. Then, start a lesson.

        Action plan:
        1. take a screenshot
        2. plan your clicks/types based on the screenshot
        3. execute your plan by clicking and typing
        4. take another screenshot to make sure your plan worked. Unless logged in, Repeat steps 2-4 based on the current screenshot.
        5. If browser still loading, wait 5 seconds and take another screenshot. Do this up to 3 times before reporting an error.
    """,
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

solve_agent = Agent(
    name="Solve Agent",
    instructions="""
        You are a browser automation agent and a native English and French Speaker.
        You have an open browser with a Duolingo exercise you need to solve.
        After solving the exercise, continue to the next one and stop there.
        If it's a listening/speaking exercise, skip it.

        Action plan:
        1. take a screenshot
        2. plan your clicks/types based on the screenshot
        3. execute your plan by clicking and typing
        4. take another screenshot to make sure your plan worked. If exercise not solved, Repeat steps 2-4 based on the current screenshot.
    """,
    tools=[
        tools.take_screenshot,
        tools.click,
        tools.type_text,
        tools.press_key
    ],
)
