import re

from typing import Literal


GITHUB_URL = "github.com"
RAW_GITHUB_URL = "raw.githubusercontent.com"

USERNAME_PATTERN = r"[a-zA-Z0-9_-]+"
REPOSITORY_PATTERN = r"[a-zA-Z0-9_.-]+"
BRANCH_PATTERN = r"[a-zA-Z0-9_.-]+"
PATH_PATTERN = r"(.*)"

COMMON_TLDS = {
    "com",
    "org",
    "net",
    "edu",
    "gov",
    "io",
    "co",
    "uk",
    "fr",
    "de",
    "jp",
    "au",
    "ca",
    "cm",
    "us",
    "info",
    "biz",
    "app",
    "dev",
}


def __get_link_type_pattern(link_type: Literal["blob", "tree", "both"]) -> str:
    """
    Get the type specifier pattern based on link_type.

    :param link_type: The type of link to check for. Can be "blob", "tree" or "both".
    :return: The type specifier pattern.
    """

    if link_type == "blob":
        return r"blob"
    elif link_type == "tree":
        return r"tree"
    else:  # "both"
        return r"(?:blob|tree)"


def __is_likely_domain(path: str) -> bool:
    """
    Determine if a path is likely a domain name (e.g., facebook.com, www.example.org).

    :param path: The path to check
    :return: True if the path is likely a domain name, False otherwise
    """
    if path.startswith(("./", "../", "/")):
        return False  # Paths starting with ./, ../, or / are not domains
    if "." not in path:
        return False  # Domains must contain at least one dot
    # Split the path to check the TLD
    parts = path.split(".")
    if len(parts) < 2:
        return False
    tld = parts[-1].lower()
    # Check if the TLD is in our list of common TLDs
    return tld in COMMON_TLDS


def is_valid_github_absolute_url_pattern(url: str, link_type: Literal["blob", "tree", "both"] = "both") -> bool:
    """
    Check if a URL is a valid absolute GitHub URL.

    :param url: The URL to check.
    :param link_type: The type of link to check for. Can be "blob", "tree" or "both".
    :return: True if the URL is a valid absolute GitHub URL, False otherwise.
    """

    # Determine type specifier pattern based on link_type
    type_specifier = __get_link_type_pattern(link_type)

    # Pattern for absolute GitHub URLs
    absolute_url_pattern = (
        r"^(?:https?://)?"  # Protocol (optional)
        r"(?:www\.)?"  # www prefix (optional)
        r"github\.com/"  # Domain
        f"({USERNAME_PATTERN})/"  # Username
        f"({REPOSITORY_PATTERN})"  # Repository name
        r"/?(?:"  # Optional trailing slash, then begin group
        r"/(" + type_specifier + r")/"  # Type specifier (blob/tree) based on link_type
        f"({BRANCH_PATTERN})"  # Branch name
        f"(?:/({PATH_PATTERN}))?"  # Optional path within repo
        r")?"  # End optional group
        r"$"  # End of string
    )

    return bool(re.match(absolute_url_pattern, url))


def is_valid_github_relative_url_pattern(url: str, link_type: Literal["blob", "tree", "both"] = "both") -> bool:
    """
    Check if a URL is a valid relative GitHub URL.

    :param url: The URL to check.
    :param link_type: The type of link to check for. Can be "blob", "tree" or "both".
    :return: True if the URL is a valid relative GitHub URL, False otherwise.
    """

    # Determine type specifier pattern based on link_type
    type_specifier = __get_link_type_pattern(link_type)

    # Pattern for relative GitHub URLs
    relative_url_pattern = (
        r"^/"  # Starting with /
        f"({USERNAME_PATTERN})/"  # Username
        f"({REPOSITORY_PATTERN})"  # Repository name
        r"/?(?:"  # Optional trailing slash, then begin group
        r"/(" + type_specifier + r")/"  # Type specifier (blob/tree) based on link_type
        f"({BRANCH_PATTERN})"  # Branch name
        f"(?:/({PATH_PATTERN}))?"  # Optional path within repo
        r")?"  # End optional group
        r"$"  # End of string
    )

    return bool(re.match(relative_url_pattern, url))


def is_valid_git_url_pattern(url: str, link_type: Literal["blob", "tree", "both"] = "both") -> bool:
    """
    Check if a URL is a valid git URL.

    :param url: The URL to check.
    :param link_type: The type of link to check for. Can be "blob", "tree" or "both".
    :return: True if the URL is a valid git URL, False otherwise.
    """

    return is_valid_github_absolute_url_pattern(url, link_type) or is_valid_github_relative_url_pattern(url, link_type)


def normalize_github_url(url: str, link_type: Literal["blob", "tree", "both"] = "both") -> str | None:
    """
    Validates a GitHub URL and normalizes relative URLs to absolute ones.

    :param url: The URL to normalize.
    :param link_type: The type of link to check for. Can be "blob", "tree" or "both".
    :return: The normalized URL if it is valid, None otherwise
    ---
    Examples:
        >>> normalize_github_url("https://github.com/username/repo")
        'https://github.com/username/repo'
        >>> normalize_github_url("/username/repo")
        'https://github.com/username/repo'
        >>> normalize_github_url("invalid-url")
        None
    """

    # Check if URL is a valid absolute GitHub URL
    if is_valid_github_absolute_url_pattern(url, link_type=link_type):
        # Ensure the URL has https:// prefix
        if not url.startswith(("http://", "https://")):
            return "https://" + url.removeprefix("www.")
        return url

    # Check if URL is a valid relative GitHub URL
    if is_valid_github_relative_url_pattern(url, link_type=link_type):
        # Convert to absolute URL by extracting components and building the URL
        # We can assume the URL is valid since is_valid_github_relative_url_pattern passed

        # Remove leading slash
        relative_path = url.lstrip("/")

        # Construct absolute URL
        return f"https://{GITHUB_URL}/{relative_path}"

    # URL is not valid according to either pattern
    return None


def convert_to_raw_url(github_url: str) -> str | None:
    """
    Convert a GitHub URL to its raw.githubusercontent.com equivalent.

    :param github_url: A GitHub URL (e.g., https://github.com/username/repo/blob/main/file.py)
    :return: The raw.githubusercontent.com URL if the input is a valid blob URL, None otherwise
    ---
    Examples:
        >>> convert_to_raw_url("https://github.com/Hugues-DTANKOUO/problems/blob/main/README.md")
        'https://raw.githubusercontent.com/Hugues-DTANKOUO/problems/main/README.md'
    """
    # Normalize URL to ensure it's absolute and properly formatted
    normalized_url = normalize_github_url(github_url, link_type="blob")
    if not normalized_url:
        return None

    # Extract components using regex
    match = re.match(
        r"https://github\.com/"
        r"([a-zA-Z0-9_-]+)/"  # username
        r"([a-zA-Z0-9_.-]+)"  # repository
        r"/blob/"  # blob indicator
        r"([a-zA-Z0-9_.-]+)"  # branch
        r"/(.+)",  # file path
        normalized_url,
    )

    assert match is not None, f"Invalid URL: {normalized_url}"

    username, repo, branch, file_path = match.groups()

    # Construct raw URL
    return f"https://{RAW_GITHUB_URL}/{username}/{repo}/{branch}/{file_path}"


def convert_markdown_links_to_absolute(content: str, github_path: str) -> str:
    """
    Convert relative paths in Markdown content to absolute GitHub paths or raw URLs if is an image link.

    :param content: The raw Markdown content
    :param github_path: The absolute GitHub path of the current file
    :return: Updated Markdown content with relative links converted to absolute paths
    """
    # Extract components from the github_path
    # Example path: https://github.com/username/repo/blob/main/folder/file.md
    path_parts = github_path.split("/")

    # Ensure we have at least 7 parts for a valid GitHub URL with blob/tree + branch
    if len(path_parts) < 7:
        return content

    # Extract the important parts of the URL
    # The first 5 parts: https:, "", github.com, username, repo
    repo_base = "/".join(path_parts[:5])

    # The repo section with blob/tree and branch
    repo_section = f"/{path_parts[5]}/{path_parts[6]}"  # /blob/main or /tree/main

    # The directory part (without the file)
    dir_path = "/".join(path_parts[:-1])

    # Define a regex pattern to find all markdown links
    # Capture all paths inside parentheses, but ignore links that start with #
    pattern = r"\]\(([^#][^)]*)\)"

    def replace_link(match: re.Match[str]) -> str:
        """
        Replace the relative path with an absolute GitHub path.

        :param match: The match object
        :return: The updated link with the absolute path
        """
        rel_path = match.group(1)

        # If the path is an absolute URL (starts with http:// or https://), leave it unchanged
        if rel_path.startswith(("http://", "https://")):
            return f"]({rel_path})"

        # If the path is likely a domain name without protocol (e.g., linkedin.com, www.example.org), leave it unchanged
        if __is_likely_domain(rel_path):
            return f"]({rel_path})"

        # Handle explicit relative path formats (starting with ./, ../, or /)
        if rel_path.startswith("./"):
            # Same directory reference
            abs_path = f"{dir_path}/{rel_path.removeprefix('./')}"

        elif rel_path.startswith("../"):
            # Parent directory reference
            path_segments = dir_path.split("/")
            target_segments = rel_path.split("/")

            # Count parent directory references
            parent_count = sum(1 for segment in target_segments if segment == "..")

            # Find the minimum index to preserve the blob/tree and branch
            # Example: https://github.com/username/repo/blob/main/folder/file.md
            # We need to preserve up to element 7 (main), which is index 0-6 inclusive
            min_index = 7  # Preserve up to the branch name

            # Calculate how many segments we can remove without affecting the branch
            path_after_branch = path_segments[min_index:]  # Segments after branch
            max_remove = len(path_after_branch)  # Maximum segments we can remove

            if parent_count > max_remove:
                # Can't go up beyond the branch, so limit parent_count
                parent_count = max_remove

            # Remove the appropriate number of segments from the end
            new_path_segments = path_segments[:min_index]  # Preserve up to branch
            remaining_segments = path_after_branch[:-parent_count] if parent_count > 0 else path_after_branch
            new_path_segments.extend(remaining_segments)

            # Add the remaining path after the ../ parts
            remaining_segments = [s for s in target_segments if s != ".."]
            new_path_segments.extend(remaining_segments)

            abs_path = "/".join(new_path_segments)

        elif rel_path.startswith("/"):
            # Root of the repo reference
            abs_path = f"{repo_base}{repo_section}{rel_path}"

        else:
            # Path without explicit relative prefix (e.g., readme.md, folder/file.txt)
            # Same directory reference
            abs_path = f"{dir_path}/{rel_path.removeprefix('./')}"

        # Clean up multiple slashes that might have been introduced
        abs_path = re.sub(r"/{2,}", "/", abs_path).replace("https:/github.com", "https://github.com")

        return f"]({abs_path})"

    # Apply the replacements to the content
    updated_content = re.sub(pattern, replace_link, content)

    # Define a regex pattern to find image links (e.g., ![alt text](url))
    image_pattern = r"!\[.*?\]\(((?:https?://github\.com/[^)]+)|(?:/[^)]+))\)"

    def replace_image_link(match: re.Match[str]) -> str:
        """
        Replace GitHub URLs in image links with raw.githubusercontent.com URLs.

        :param match: The match object
        :return: The updated image link with the raw URL if applicable
        """
        url = match.group(1)
        # Try to convert the URL to a raw URL
        raw_url = convert_to_raw_url(url)

        if raw_url:
            alt_text = match.group(0)[2 : match.group(0).index("]")]
            return f"![{alt_text}]({raw_url})"
        # If conversion fails (e.g., not a valid GitHub blob URL), leave unchanged
        return match.group(0)

    # Apply the replacements to convert GitHub URLs in image links to raw URLs
    final_content = re.sub(image_pattern, replace_image_link, updated_content)

    # Return the final updated content
    return final_content


def convert_html_image_links_to_raw(content: str, github_path: str) -> str:
    """
    Convert relative image paths in HTML src attributes to absolute raw GitHub URLs.

    :param content: The raw Markdown content containing HTML image tags
    :param github_path: The absolute GitHub path of the current file
    :return: Updated content with relative src attributes converted to raw GitHub URLs
    """
    # Check if the github_path is valid
    path_parts = github_path.split("/")
    if len(path_parts) < 7:
        return content

    # Extract path components
    repo_base = "/".join(path_parts[:5])  # https://github.com/username/repo
    repo_section = f"/{path_parts[5]}/{path_parts[6]}"  # /blob/main
    dir_path = "/".join(path_parts[:-1])  # Current directory path

    # Regex pattern to capture src attributes in HTML tags
    pattern = r'src=["\']([^"\']+)["\']'

    def replace_src(match: re.Match[str]) -> str:
        """
        Replace relative src paths with raw GitHub URLs.

        :param match: The match object containing the src attribute
        :return: The updated src attribute with a raw URL if applicable
        """
        src_path = match.group(1)  # Extract the path from the src attribute

        # If the path is already an absolute URL (http:// or https://), leave it unchanged
        if src_path.startswith(("http://", "https://")):
            return f'src="{src_path}"'

        # Build the absolute GitHub path for relative paths
        if src_path.startswith("./"):
            abs_path = f"{dir_path}/{src_path.removeprefix('./')}"
        elif src_path.startswith("../"):
            path_segments = dir_path.split("/")
            target_segments = src_path.split("/")
            parent_count = sum(1 for segment in target_segments if segment == "..")
            min_index = 7  # Preserve up to the branch level
            path_after_branch = path_segments[min_index:]
            max_remove = len(path_after_branch)
            if parent_count > max_remove:
                parent_count = max_remove
            new_path_segments = path_segments[:min_index]
            remaining_segments = path_after_branch[:-parent_count] if parent_count > 0 else path_after_branch
            new_path_segments.extend(remaining_segments)
            remaining_segments = [s for s in target_segments if s != ".."]
            new_path_segments.extend(remaining_segments)
            abs_path = "/".join(new_path_segments)
        elif src_path.startswith("/"):
            abs_path = f"{repo_base}{repo_section}{src_path}"
        else:
            # Relative path without prefix (e.g., "images/file.jpg")
            abs_path = f"{dir_path}/{src_path}"

        # Clean up double slashes
        abs_path = re.sub(r"/{2,}", "/", abs_path).replace("https:/github.com", "https://github.com")

        # Convert to raw URL
        raw_url = convert_to_raw_url(abs_path)
        if raw_url:
            return f'src="{raw_url}"'
        return match.group(0)  # Return unchanged if conversion fails

    # Apply the replacements
    updated_content = re.sub(pattern, replace_src, content)
    return updated_content


def convert_markdown_github_link_to_inner_link(content: str, base_path: str) -> str:
    """
    Convert GitHub links in Markdown content to inner links.

    :param content: The raw Markdown content
    :param base_path: The base path in gityes (e.g., "/gityes")
    :return: Updated Markdown content with GitHub links converted to inner links
    ---
    Examples:
        >>> convert_markdown_github_link_to_inner_link(
            "[Link](https://github.com/user/repo/blob/main/docs/file.md)", "/gityes"
        )
        '[Link](/gityes/user/repo/blob/main/docs/file.md)'
        >>> convert_markdown_github_link_to_inner_link("[Link](/user/repo/blob/main/docs/file.md)", "/gityes")
        '[Link](/gityes/user/repo/blob/main/docs/file.md)'
    """

    # Define a regex pattern to find all markdown links
    # Capture GitHub paths (absolute URLs starting with https://github.com or relative paths starting with /)
    pattern = r"\]\(((?:https?://github\.com/[^)]+)|(?:/[^)]+))\)"

    base_path = base_path.rstrip("/")  # Remove trailing slashes from base_path

    def replace_github_link(match: re.Match[str]) -> str:
        """
        Replace GitHub URLs with inner links based on base_path.

        :param match: The match object
        :return: The updated Markdown link with the inner path
        """
        url = match.group(1)  # Extract the captured URL (group 1)

        # If the URL is an absolute GitHub URL, replace https://github.com/ with base_path/
        if url.startswith(("https://github.com/", "http://github.com/")):
            inner_path = url.replace("https://github.com/", f"{base_path}/").replace(
                "http://github.com/", f"{base_path}/"
            )
        # If the URL is a relative GitHub path (starts with /), prefix it with base_path
        elif url.startswith("/"):
            inner_path = f"{base_path}{url}"
        else:
            # This case should not occur with the current pattern, but included for robustness
            inner_path = url

        # Return the updated Markdown link
        return f"]({inner_path})"

    # Apply the replacements to the content
    updated_content = re.sub(pattern, replace_github_link, content)

    # Return the updated content
    return updated_content
