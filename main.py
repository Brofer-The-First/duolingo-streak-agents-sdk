import asyncio
import os
from agents import Runner, RunConfig, trace
from agents_def import login_agent, solve_agent
from dotenv import load_dotenv
from tools import (
    open_duolingo_impl,
    click_impl,
    type_duolingo_email_impl,
    type_duolingo_password_impl,
)

load_dotenv()

agentic_login = os.getenv("AGENTIC_LOGIN", "false").lower() == "true"

async def manual_login():
    await open_duolingo_impl() # Open duolingo.com
    await asyncio.sleep(2)
    await click_impl(924, 443) # "I already have an account"
    await asyncio.sleep(2)
    await click_impl(575, 196) # Click email field
    await type_duolingo_email_impl()
    await click_impl(589, 267) # Click password field
    await type_duolingo_password_impl()
    await click_impl(633, 332) # Click login button
    await asyncio.sleep(10)
    await click_impl(558, 313) # Click lesson button
    await asyncio.sleep(1)
    await click_impl(565, 501) # Click start lesson
    await asyncio.sleep(10) # Wait for lesson to load 


async def main():
    with trace("Duolingo Streak Agent Run"):
        if agentic_login:
            await Runner.run(
                login_agent,
                "",
                max_turns=30,
                run_config=RunConfig(model="gpt-4.1"),
            )
        else:
            await manual_login()

        done = False

        while done==False:
            result = await Runner.run(
                solve_agent,
                "",
                max_turns=30,
                run_config=RunConfig(model="gpt-5.4"),
            )

            if result.final_output == "DASHBOARD":
                done = True

        print("All done! Streak successfully extended!")

if __name__ == "__main__":
    asyncio.run(main())
