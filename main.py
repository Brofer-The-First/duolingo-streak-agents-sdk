import asyncio
from agents import Runner, RunConfig, trace
from agents_def import login_agent, solve_agent
from dotenv import load_dotenv

load_dotenv()


async def main():
    with trace("Duolingo Streak Agent Run"):
        await Runner.run(
            login_agent,
            "",
            max_turns=30,
            run_config=RunConfig(model="gpt-4.1"),
        )
        while True:
            await Runner.run(
                solve_agent,
                "",
                max_turns=30,
                run_config=RunConfig(model="gpt-4.1"),
            )


if __name__ == "__main__":
    asyncio.run(main())
