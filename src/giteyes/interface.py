from pathlib import Path

import requests

from fastapi import FastAPI, Path as PathParam
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from giteyes.utils import (
    convert_html_image_links_to_raw,
    convert_markdown_github_link_to_inner_link,
    convert_markdown_links_to_absolute,
    convert_to_raw_url,
    is_valid_github_absolute_url_pattern,
    normalize_github_url,
)


CURRENT_DIR = Path(__file__).parent


app = FastAPI(docs_url=None, redoc_url=None)


app.mount("/static", StaticFiles(directory=CURRENT_DIR / "static"), name="static")


templates = Jinja2Templates(directory=CURRENT_DIR / "templates")


@app.get("/docs")
async def docs() -> RedirectResponse:
    """
    Redirect to the home page.
    """
    return RedirectResponse("/", status_code=302)


@app.get("/redoc")
async def redoc() -> RedirectResponse:
    """
    Redirect to the home page.
    """
    return RedirectResponse("/", status_code=302)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """
    Get the home page.

    :param request: The request object.
    :return: The home page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/check-raw-url-content/{github_url:path}")
async def check_raw_url_content(github_url: str = PathParam(..., title="GitHub URL")) -> dict[str, str | None]:
    """
    Check the raw content of a GitHub URL.

    :param github_url: The GitHub URL to check.
    :return: The url of the raw content if it exists, and the relative GitHub path.
    """
    # Normalize the URL if needed
    normalized_url = normalize_github_url(github_url, link_type="blob")
    if not normalized_url:
        return {"raw_url": None, "github_path": None}

    # Extract the relative path from the normalized URL
    # Remove the 'https://github.com/' prefix if present
    github_path = normalized_url
    if github_path.startswith("https://github.com/"):
        github_path = github_path.removeprefix("https://github.com/")

    # Convert to raw URL
    raw_url = convert_to_raw_url(normalized_url)
    if not raw_url:
        return {"raw_url": None, "github_path": None}

    # Check if the raw URL is accessible
    response = requests.get(raw_url)
    if response.status_code == 200:
        return {"raw_url": raw_url, "github_path": github_path}
    else:
        return {"raw_url": None, "github_path": None}


@app.get("/view/{github_path:path}", response_class=HTMLResponse)
async def view_markdown(request: Request, github_path: str) -> HTMLResponse:
    """
    View GitHub markdown content.

    :param request: The request object
    :param github_path: The GitHub path to the markdown file
    :return: The rendered markdown template
    """
    try:
        if not is_valid_github_absolute_url_pattern(github_path, link_type="blob"):
            if not github_path.startswith("/"):
                github_path = f"/{github_path}"

        # Normalize and validate the GitHub URL
        normalized_url = normalize_github_url(github_path, link_type="blob")
        if not normalized_url:
            return templates.TemplateResponse(
                "error.html", {"request": request, "message": f"Invalid GitHub URL format. : {github_path}"}
            )

        # Convert to raw URL to fetch content
        raw_url = convert_to_raw_url(normalized_url)
        if not raw_url:
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "message": "Could not generate raw URL. Please ensure this is a valid GitHub file URL.",
                },
            )

        # Fetch the raw markdown content
        response = requests.get(raw_url)
        if response.status_code != 200:
            return templates.TemplateResponse(
                "error.html", {"request": request, "message": f"Failed to fetch content: HTTP {response.status_code}"}
            )

        # Get file information
        content = response.text.replace("`", r"\`")

        # Convert relative path into content to github absolute path
        content = convert_markdown_links_to_absolute(content, normalized_url)

        # Convert HTML image links to raw
        content = convert_html_image_links_to_raw(content, normalized_url)

        # Convert GitHub markdown links to inner links
        base_url = str(request.base_url)
        content = convert_markdown_github_link_to_inner_link(content, f"{base_url}view")

        file_name = github_path.split("/")[-1] if "/" in github_path else github_path

        # Render the markdown template
        return templates.TemplateResponse(
            "markdown-viewer.html",
            {
                "request": request,
                "content": content,
                "file_name": file_name,
                "file_path": github_path,
                "raw_url": raw_url,
                "title": f"GitEyes - {file_name}",
            },
        )
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"An error occurred: {str(e)}"})
