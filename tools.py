import asyncio
import base64
import os
from typing import Optional

from agents import ToolOutputImage, ToolOutputText, function_tool
from playwright.async_api import async_playwright, Browser, Page, Playwright

# ---------------------------------------------------------------------------
# Singleton browser / page state shared across all tool calls
# ---------------------------------------------------------------------------

_playwright: Optional[Playwright] = None
_browser: Optional[Browser] = None
_page: Optional[Page] = None
_lock = asyncio.Lock()


async def _get_page() -> Page:
    global _playwright, _browser, _page
    async with _lock:
        if _page is None or _page.is_closed():
            _playwright = await async_playwright().start()
            _browser = await _playwright.chromium.launch(headless=False)
            _page = await _browser.new_page()
    return _page


async def open_duolingo_impl() -> str:
    """Open duolingo.com in the browser."""
    page = await _get_page()
    response = await page.goto("https://www.duolingo.com", wait_until="domcontentloaded")
    status = response.status if response else "unknown"
    return f"Opened duolingo.com — HTTP {status}"

open_duolingo = function_tool(open_duolingo_impl)


# ---------------------------------------------------------------------------
# Screenshot
# ---------------------------------------------------------------------------


@function_tool
async def take_screenshot() -> list[ToolOutputText | ToolOutputImage]:
    """Take a screenshot of the current browser viewport and return it as an image
    so you can see the current state of the screen.
    """
    page = await _get_page()
    png_bytes = await page.screenshot()
    data_url = "data:image/png;base64," + base64.b64encode(png_bytes).decode()
    return [
        ToolOutputText(text=f"Current URL: {page.url}"),
        ToolOutputImage(image_url=data_url, detail="high"),
    ]


# ---------------------------------------------------------------------------
# Mouse
# ---------------------------------------------------------------------------


async def click_impl(x: int, y: int) -> str:
    """Click at pixel coordinates (x, y) on the screen.

    Args:
        x: Horizontal position in pixels from the left edge of the viewport.
        y: Vertical position in pixels from the top edge of the viewport.
    """
    page = await _get_page()
    await page.mouse.click(x, y)
    return f"Clicked at ({x}, {y})"

click = function_tool(click_impl)


# ---------------------------------------------------------------------------
# Keyboard
# ---------------------------------------------------------------------------


@function_tool
async def type_text(text: str) -> str:
    """Type a string of text at the current cursor position, dispatching real
    key events for each character.

    Args:
        text: The text to type.
    """
    page = await _get_page()
    await page.keyboard.type(text)
    return f"Typed {len(text)} characters"


@function_tool
async def press_key(key: str) -> str:
    """Press a single keyboard key or chord (e.g. "Enter", "Tab", "Control+a").

    Args:
        key: Key name as understood by Playwright (e.g. "Enter", "Escape",
             "ArrowDown", "Control+a").
    """
    page = await _get_page()
    await page.keyboard.press(key)
    return f"Pressed '{key}'"


# ---------------------------------------------------------------------------
# Duolingo credential helpers
# ---------------------------------------------------------------------------


async def type_duolingo_email_impl() -> str:
    """Type the Duolingo email from the DUOLINGO_EMAIL environment variable
    into the currently focused field, one character at a time with a short delay
    between each keystroke.
    """
    email = os.environ.get("DUOLINGO_EMAIL", "")
    if not email:
        return "Error: DUOLINGO_EMAIL environment variable is not set"
    page = await _get_page()
    for char in email:
        await page.keyboard.type(char)
        await page.wait_for_timeout(50)
    return f"Typed Duolingo email ({len(email)} characters)"

type_duolingo_email = function_tool(type_duolingo_email_impl)


async def type_duolingo_password_impl() -> str:
    """Type the Duolingo password from the DUOLINGO_PASSWORD environment variable
    into the currently focused field, one character at a time with a short delay
    between each keystroke.
    """
    password = os.environ.get("DUOLINGO_PASSWORD", "")
    if not password:
        return "Error: DUOLINGO_PASSWORD environment variable is not set"
    page = await _get_page()
    for char in password:
        await page.keyboard.type(char)
        await page.wait_for_timeout(50)
    return f"Typed Duolingo password ({len(password)} characters)"

type_duolingo_password = function_tool(type_duolingo_password_impl)
