import os
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
    instructions=f"""
        You are a browser automation agent and a native English and {os.getenv("LEARNED_LANGUAGE", "French")} Speaker.
        You have an open browser with a Duolingo exercise you need to solve.
        If instead of an exercise you see that the lesson is done, try navigating back to the Duolingo dashboard.
        If instead of an exercise you see the Duolingo main dashboard, end your run with the string "DASHBOARD".
        After solving the exercise, continue to the next one and stop there.
        If it's a listening/speaking exercise, skip it.

        Action plan:
        1. take a screenshot
        2. describe the exercise in the screenshot and its solution, referring to coordinates of the elements you need to click/type
        3. plan your clicks/types based on the screenshot
        4. execute your plan by clicking and typing
        5. take another screenshot to make sure your plan worked.
        6. If plan did not work, end your run immediately.
        7. If plan worked, click on the "next"/"continue" button to go to the next exercise. Then, take another screenshot to make sure the next exercise loaded. If not loaded, try this step again.
        8. If new exercise loaded, end your run.

    """,
    tools=[
        tools.take_screenshot,
        tools.click,
        tools.type_text,
        tools.press_key
    ],
)
