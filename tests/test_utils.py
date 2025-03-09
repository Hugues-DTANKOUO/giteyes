from giteyes.utils import (
    convert_html_image_links_to_raw,
    convert_markdown_github_link_to_inner_link,
    convert_markdown_links_to_absolute,
    convert_to_raw_url,
    is_valid_git_url_pattern,
    normalize_github_url,
)


def test_is_valid_git_url_pattern_when_relative_url_is_valid_then_true() -> None:
    """
    GIVEN a valid relative git URL
    WHEN the URL is checked
    THEN it should return True.
    """

    assert is_valid_git_url_pattern("/Hugues-DTANKOUO/problems") is True

    assert is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/tree/main") is True

    assert is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/blob/main/README.md") is True

    assert is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/tree/main/src") is True


def test_is_valid_git_url_pattern_when_absolute_url_is_valid_then_true() -> None:
    """
    GIVEN a valid absolute git URL
    WHEN the URL is checked
    THEN it should return True.
    """

    assert is_valid_git_url_pattern("https://github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/") is True

    assert is_valid_git_url_pattern("https://www.github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/tree/main") is True

    assert (
        is_valid_git_url_pattern("https://www.github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/blob/main/README.md") is True
    )

    assert (
        is_valid_git_url_pattern("https://github.com/Hugues-DTANKOUO/problems/blob/main/src/problems/anagram.py")
        is True
    )


def test_is_valid_git_blob_url_pattern_when_url_is_valid_then_true() -> None:
    """
    GIVEN a valid git blob URL
    WHEN the URL is checked
    THEN it should return True.
    """

    assert (
        is_valid_git_url_pattern(
            "https://www.github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/blob/main/README.md", link_type="blob"
        )
        is True
    )

    assert (
        is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/blob/main/src/problems/anagram.py", link_type="blob")
        is True
    )


def test_is_valid_git_tree_url_pattern_when_url_is_valid_then_true() -> None:
    """
    GIVEN a valid git tree URL
    WHEN the URL is checked
    THEN it should return True.
    """

    assert (
        is_valid_git_url_pattern(
            "https://www.github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/tree/main/src/problems", link_type="tree"
        )
        is True
    )

    assert is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/tree/main/src/problems", link_type="tree") is True


def test_is_valid_git_url_pattern_when_url_is_invalid_then_false() -> None:
    """
    GIVEN an invalid git URL
    WHEN the URL is checked
    THEN it should return False.
    """

    assert is_valid_git_url_pattern("https://github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/README.md") is False

    assert is_valid_git_url_pattern("github.com/user/repo/file.txt") is False

    assert is_valid_git_url_pattern("/user/repo/file.txt") is False

    assert is_valid_git_url_pattern("example.com/user/repo/tree/main/file.txt") is False

    assert (
        is_valid_git_url_pattern("https://www.github.com/Hugues-DTANKOUO/Hugues-DTANKOUO/tree/main", link_type="blob")
        is False
    )

    assert (
        is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/blob/main/src/problems/anagram.py", link_type="tree")
        is False
    )

    assert (
        is_valid_git_url_pattern("/Hugues-DTANKOUO/problems/blob/main/src/problems/anagram.py", link_type="tree")
        is False
    )


def test_normalize_github_url_when_absolute_url_then_return_normalized() -> None:
    """
    GIVEN an absolute GitHub URL
    WHEN normalizing the URL
    THEN it should return the normalized URL.
    """
    assert normalize_github_url("github.com/user/repo") == "https://github.com/user/repo"
    assert normalize_github_url("www.github.com/user/repo") == "https://github.com/user/repo"
    assert normalize_github_url("https://github.com/user/repo") == "https://github.com/user/repo"
    assert normalize_github_url("http://github.com/user/repo") == "http://github.com/user/repo"


def test_normalize_github_url_when_relative_url_then_return_absolute() -> None:
    """
    GIVEN a relative GitHub URL
    WHEN normalizing the URL
    THEN it should return the absolute URL.
    """
    assert normalize_github_url("/user/repo") == "https://github.com/user/repo"
    assert normalize_github_url("/user/repo/tree/main") == "https://github.com/user/repo/tree/main"
    assert normalize_github_url("/user/repo/blob/main/README.md") == "https://github.com/user/repo/blob/main/README.md"


def test_normalize_github_url_when_invalid_url_then_return_none() -> None:
    """
    GIVEN an invalid GitHub URL
    WHEN normalizing the URL
    THEN it should return None.
    """
    assert normalize_github_url("invalid-url") is None
    assert normalize_github_url("example.com/user/repo") is None
    assert normalize_github_url("github.com/invalid/url/format") is None


def test_convert_to_raw_url_when_valid_blob_url_then_return_raw_url() -> None:
    """
    GIVEN a valid GitHub blob URL
    WHEN converting to raw URL
    THEN it should return the correct raw.githubusercontent.com URL.
    """
    # Test with absolute URLs
    assert (
        convert_to_raw_url("https://github.com/user/repo/blob/main/file.py")
        == "https://raw.githubusercontent.com/user/repo/main/file.py"
    )

    assert (
        convert_to_raw_url("https://github.com/Hugues-DTANKOUO/problems/blob/main/README.md")
        == "https://raw.githubusercontent.com/Hugues-DTANKOUO/problems/main/README.md"
    )

    # Test with relative URLs
    assert (
        convert_to_raw_url("/user/repo/blob/main/file.py") == "https://raw.githubusercontent.com/user/repo/main/file.py"
    )

    assert (
        convert_to_raw_url("/Hugues-DTANKOUO/problems/blob/main/src/problems/anagram.py")
        == "https://raw.githubusercontent.com/Hugues-DTANKOUO/problems/main/src/problems/anagram.py"
    )


def test_convert_to_raw_url_when_invalid_url_then_return_none() -> None:
    """
    GIVEN an invalid GitHub URL
    WHEN converting to raw URL
    THEN it should return None.
    """
    assert convert_to_raw_url("invalid-url") is None
    assert convert_to_raw_url("github.com/invalid/url/format") is None
    assert convert_to_raw_url("https://github.com/user/repo/tree/main") is None
    assert convert_to_raw_url("/user/repo/tree/main/src") is None


def test_convert_markdown_links_to_absolute_with_same_dir_links():
    """
    GIVEN markdown content with links in the same directory
    WHEN converting links to absolute
    THEN it should convert them correctly while preserving /blob/main/.
    """
    content = "Check out [this file](./README.md) and [this image](./images/logo.png)"
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "Check out [this file](https://github.com/user/repo/blob/main/docs/README.md) and [this image](https://github.com/user/repo/blob/main/docs/images/logo.png)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_parent_dir_links():
    """
    GIVEN markdown content with links to parent directories
    WHEN converting links to absolute
    THEN it should navigate up correctly while preserving /blob/main/.
    """
    content = "See [parent file](../README.md) or [other dir](../src/utils.py)"
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "See [parent file](https://github.com/user/repo/blob/main/README.md) or [other dir](https://github.com/user/repo/blob/main/src/utils.py)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_root_links():
    """
    GIVEN markdown content with links to the repo root
    WHEN converting links to absolute
    THEN it should handle root paths correctly while preserving /blob/main/.
    """
    content = "View the [license](/LICENSE) or [readme](/README.md)"
    github_path = "https://github.com/user/repo/blob/main/deep/nested/file.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "View the [license](https://github.com/user/repo/blob/main/LICENSE) or [readme](https://github.com/user/repo/blob/main/README.md)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_multiple_parent_dirs():
    """
    GIVEN markdown content with links going multiple levels up
    WHEN converting links to absolute
    THEN it should navigate up correctly while preserving /blob/main/.
    """
    content = "Look at [this file](../../other/file.md)"
    github_path = "https://github.com/user/repo/blob/main/nested/deep/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "Look at [this file](https://github.com/user/repo/blob/main/other/file.md)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_mixed_links():
    """
    GIVEN markdown content with mixed types of links
    WHEN converting links to absolute
    THEN it should handle all types correctly while preserving /blob/main/.
    """
    content = """
# Documentation
- [Same dir](./utils.md)
- [Parent dir](../README.md)
- [Root](/LICENSE)
- [Already absolute](https://github.com/other/repo/blob/main/file.md)
- [External](https://example.com)
- [No change needed](utils.md)
"""
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = """
# Documentation
- [Same dir](https://github.com/user/repo/blob/main/docs/utils.md)
- [Parent dir](https://github.com/user/repo/blob/main/README.md)
- [Root](https://github.com/user/repo/blob/main/LICENSE)
- [Already absolute](https://github.com/other/repo/blob/main/file.md)
- [External](https://example.com)
- [No change needed](https://github.com/user/repo/blob/main/docs/utils.md)
"""
    assert result == expected


def test_convert_markdown_links_to_absolute_with_no_links():
    """
    GIVEN markdown content without any relative links
    WHEN converting links to absolute
    THEN it should return the original content unchanged.
    """
    content = """
# Title
Regular text without any links.

```python
# Even code blocks should be untouched
def hello():
    print("Hello world")
```
"""
    github_path = "https://github.com/user/repo/blob/main/README.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    assert result == content


def test_convert_markdown_links_to_absolute_respect_blob_main():
    """
    GIVEN markdown content with links trying to go beyond /blob/main/
    WHEN converting links to absolute
    THEN it should never go higher than the /blob/main/ part.
    """
    content = "Too far [up](../../../../outside.md)"
    github_path = "https://github.com/user/repo/blob/main/a/b/c/file.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    # Should not go beyond /blob/main/
    expected = "Too far [up](https://github.com/user/repo/blob/main/outside.md)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_different_branch():
    """
    GIVEN markdown content with links and a GitHub path with a different branch
    WHEN converting links to absolute
    THEN it should preserve the branch name.
    """
    content = "Check out [this file](./README.md) and [parent](../LICENSE)"
    github_path = "https://github.com/user/repo/blob/develop/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "Check out [this file](https://github.com/user/repo/blob/develop/docs/README.md) and [parent](https://github.com/user/repo/blob/develop/LICENSE)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_invalid_github_path():
    """
    GIVEN markdown content and an invalid GitHub path (too short)
    WHEN converting links to absolute
    THEN it should return the original content unchanged.
    """
    content = "Check out [this file](./README.md) and [parent dir](../LICENSE)"

    # Invalid GitHub path (less than 7 parts)
    github_path = "https://github.com/user/repo"

    result = convert_markdown_links_to_absolute(content, github_path)

    # Should return the original content unchanged
    assert result == content

    # Another invalid path example
    github_path = "https://github.com/user/repo/blob"
    result = convert_markdown_links_to_absolute(content, github_path)
    assert result == content


def test_convert_markdown_links_to_absolute_with_too_many_parent_refs():
    """
    GIVEN markdown content with links going too many levels up
    WHEN converting links to absolute
    THEN it should limit the parent navigation to preserve the branch.
    """
    # A path with 20 parent directory references (far beyond repo root)
    content = "Too many levels [up](../../../../../../../../../../../../../../../../../../../../../file.md)"
    github_path = "https://github.com/user/repo/blob/main/a/b/c/d/e/file.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    # Should limit parent navigation to preserve blob/branch
    expected = "Too many levels [up](https://github.com/user/repo/blob/main/file.md)"
    assert result == expected

    # Test at edge of repository
    content = "Almost too far [up](../../../file.md)"
    github_path = "https://github.com/user/repo/blob/main/a/b/file.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    # Should navigate up to the repo root but not beyond
    expected = "Almost too far [up](https://github.com/user/repo/blob/main/file.md)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_tree_instead_of_blob():
    """
    GIVEN markdown content and a GitHub path using tree instead of blob
    WHEN converting links to absolute
    THEN it should correctly preserve the tree part.
    """
    content = "Check out [this file](./README.md) and [parent](../LICENSE)"
    github_path = "https://github.com/user/repo/tree/main/docs/guide"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "Check out [this file](https://github.com/user/repo/tree/main/docs/README.md) and [parent](https://github.com/user/repo/tree/main/LICENSE)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_custom_branch_name():
    """
    GIVEN markdown content and a GitHub path with a custom branch name
    WHEN converting links to absolute
    THEN it should preserve the custom branch name.
    """
    content = "Check out [this file](./README.md) and [parent](../src)"
    github_path = "https://github.com/user/repo/blob/feature/new-design/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "Check out [this file](https://github.com/user/repo/blob/feature/new-design/docs/README.md) and [parent](https://github.com/user/repo/blob/feature/new-design/src)"
    assert result == expected

    # Test with a branch name containing special characters
    content = "Check out [this file](./README.md)"
    github_path = "https://github.com/user/repo/blob/v1.0.0-beta.1/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = "Check out [this file](https://github.com/user/repo/blob/v1.0.0-beta.1/docs/README.md)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_relative_paths_without_prefix():
    """
    GIVEN markdown content with relative paths without ./ or ../ prefix
    WHEN converting links to absolute
    THEN it should handle them correctly by appending to the current directory while preserving /blob/main/.
    """
    content = "Check out [this file](README.md) and [this image](images/logo.png)"
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    # Expected behavior: relative paths without ./ or ../ are appended to the current directory
    expected = "Check out [this file](https://github.com/user/repo/blob/main/docs/README.md) and [this image](https://github.com/user/repo/blob/main/docs/images/logo.png)"
    assert result == expected


def test_convert_markdown_links_to_absolute_with_image_links():
    """
    GIVEN markdown content with image links containing GitHub URLs
    WHEN converting links to absolute and processing image links
    THEN it should convert GitHub URLs in image links to raw.githubusercontent.com URLs,
         while leaving other links unchanged.
    """
    content = """
# Documentation
- [File link](https://github.com/user/repo/blob/main/docs/file.txt)
- ![Image link](https://github.com/user/repo/blob/main/docs/image.png)
- ![External image](https://example.com/image.jpg)
- ![Relative image](./image.png)
"""
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"

    result = convert_markdown_links_to_absolute(content, github_path)

    expected = """
# Documentation
- [File link](https://github.com/user/repo/blob/main/docs/file.txt)
- ![Image link](https://raw.githubusercontent.com/user/repo/main/docs/image.png)
- ![External image](https://example.com/image.jpg)
- ![Relative image](https://raw.githubusercontent.com/user/repo/main/docs/image.png)
"""
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_absolute_link():
    """
    GIVEN markdown content with an absolute GitHub link
    WHEN converting to inner link
    THEN it should replace https://github.com/ with base_path.
    """
    content = "[Link](https://github.com/user/repo/blob/main/docs/file.md)"
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "[Link](/gityes/user/repo/blob/main/docs/file.md)"
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_http_absolute_link():
    """
    GIVEN markdown content with an absolute GitHub link using http
    WHEN converting to inner link
    THEN it should replace http://github.com/ with base_path.
    """
    content = "[Link](http://github.com/user/repo/blob/main/docs/file.md)"
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "[Link](/gityes/user/repo/blob/main/docs/file.md)"
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_relative_link():
    """
    GIVEN markdown content with a relative GitHub link
    WHEN converting to inner link
    THEN it should prefix the path with base_path.
    """
    content = "[Link](/user/repo/blob/main/docs/file.md)"
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "[Link](/gityes/user/repo/blob/main/docs/file.md)"
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_non_github_link():
    """
    GIVEN markdown content with a non-GitHub link
    WHEN converting to inner link
    THEN it should leave the link unchanged.
    """
    content = "[External](https://example.com/page)"
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "[External](https://example.com/page)"
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_mixed_links():
    """
    GIVEN markdown content with mixed GitHub and non-GitHub links
    WHEN converting to inner link
    THEN it should convert only GitHub links to inner links.
    """
    content = """
# Documentation
- [GitHub](https://github.com/user/repo/blob/main/docs/file.md)
- [Relative GitHub](/user/repo/blob/main/docs/other.md)
- [External](https://example.com)
- [Local](local/file.md)
"""
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = """
# Documentation
- [GitHub](/gityes/user/repo/blob/main/docs/file.md)
- [Relative GitHub](/gityes/user/repo/blob/main/docs/other.md)
- [External](https://example.com)
- [Local](local/file.md)
"""
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_image_link():
    """
    GIVEN markdown content with an image link to GitHub
    WHEN converting to inner link
    THEN it should replace the GitHub URL with base_path.
    """
    content = "![Image](https://github.com/user/repo/blob/main/images/pic.png)"
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "![Image](/gityes/user/repo/blob/main/images/pic.png)"
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_base_path_trailing_slash():
    """
    GIVEN a base_path with trailing slashes
    WHEN converting to inner link
    THEN it should strip trailing slashes and convert correctly.
    """
    content = "[Link](https://github.com/user/repo/blob/main/docs/file.md)"
    base_path = "/gityes///"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "[Link](/gityes/user/repo/blob/main/docs/file.md)"
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_no_links():
    """
    GIVEN markdown content with no links
    WHEN converting to inner link
    THEN it should return the content unchanged.
    """
    content = """
# Title
No links here.
"""
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = """
# Title
No links here.
"""
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_empty_content():
    """
    GIVEN empty markdown content
    WHEN converting to inner link
    THEN it should return an empty string.
    """
    content = ""
    base_path = "/gityes"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = ""
    assert result == expected


def test_convert_markdown_github_link_to_inner_link_with_custom_base_path():
    """
    GIVEN markdown content with a GitHub link and a custom base_path
    WHEN converting to inner link
    THEN it should use the custom base_path correctly.
    """
    content = "[Link](https://github.com/user/repo/blob/main/docs/file.md)"
    base_path = "/custom/path"
    result = convert_markdown_github_link_to_inner_link(content, base_path)
    expected = "[Link](/custom/path/user/repo/blob/main/docs/file.md)"
    assert result == expected


def test_convert_html_image_links_to_raw_with_relative_no_prefix():
    """
    GIVEN HTML content with an image src attribute using a relative path without prefix
    WHEN converting to raw URLs
    THEN it should convert the path to a raw GitHub URL based on the current directory.
    """
    content = '<img src="images/CookbookCover.jpg" alt="Cover">'
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/main/docs/images/CookbookCover.jpg" alt="Cover">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_same_dir():
    """
    GIVEN HTML content with an image src attribute using a ./ relative path
    WHEN converting to raw URLs
    THEN it should convert the path to a raw GitHub URL based on the current directory.
    """
    content = '<img src="./images/logo.png" alt="Logo">'
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/main/docs/images/logo.png" alt="Logo">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_parent_dir():
    """
    GIVEN HTML content with an image src attribute using a ../ relative path
    WHEN converting to raw URLs
    THEN it should navigate up correctly and convert to a raw GitHub URL.
    """
    content = '<img src="../images/cover.png" alt="Cover">'
    github_path = "https://github.com/user/repo/blob/main/docs/sub/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/main/docs/images/cover.png" alt="Cover">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_root_path():
    """
    GIVEN HTML content with an image src attribute using a root-relative path
    WHEN converting to raw URLs
    THEN it should convert the path to a raw GitHub URL from the repository root.
    """
    content = '<img src="/images/root.jpg" alt="Root">'
    github_path = "https://github.com/user/repo/blob/main/docs/sub/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/main/images/root.jpg" alt="Root">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_absolute_url():
    """
    GIVEN HTML content with an image src attribute using an absolute URL
    WHEN converting to raw URLs
    THEN it should leave the URL unchanged.
    """
    content = '<img src="https://example.com/images/external.jpg" alt="External">'
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://example.com/images/external.jpg" alt="External">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_mixed_content():
    """
    GIVEN HTML content with mixed image src attributes (relative and absolute)
    WHEN converting to raw URLs
    THEN it should convert only relative paths to raw GitHub URLs.
    """
    content = """
<div>
    <img src="images/local.jpg" alt="Local">
    <img src="./sub/image.png" alt="Sub">
    <img src="../parent/cover.jpg" alt="Parent">
    <img src="/root/pic.jpg" alt="Root">
    <img src="https://example.com/external.jpg" alt="External">
</div>
"""
    github_path = "https://github.com/user/repo/blob/main/docs/sub/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = """
<div>
    <img src="https://raw.githubusercontent.com/user/repo/main/docs/sub/images/local.jpg" alt="Local">
    <img src="https://raw.githubusercontent.com/user/repo/main/docs/sub/sub/image.png" alt="Sub">
    <img src="https://raw.githubusercontent.com/user/repo/main/docs/parent/cover.jpg" alt="Parent">
    <img src="https://raw.githubusercontent.com/user/repo/main/root/pic.jpg" alt="Root">
    <img src="https://example.com/external.jpg" alt="External">
</div>
"""
    assert result == expected


def test_convert_html_image_links_to_raw_with_invalid_github_path():
    """
    GIVEN HTML content and an invalid GitHub path
    WHEN converting to raw URLs
    THEN it should return the content unchanged.
    """
    content = '<img src="images/CookbookCover.jpg" alt="Cover">'
    github_path = "https://github.com/user/repo"  # Trop court
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="images/CookbookCover.jpg" alt="Cover">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_multiple_parent_dirs():
    """
    GIVEN HTML content with an image src attribute going multiple levels up
    WHEN converting to raw URLs
    THEN it should navigate up correctly without exceeding the branch level.
    """
    content = '<img src="../../images/cover.png" alt="Cover">'
    github_path = "https://github.com/user/repo/blob/main/docs/sub/deep/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/main/docs/images/cover.png" alt="Cover">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_too_many_parent_dirs():
    """
    GIVEN HTML content with an image src attribute going beyond the branch level
    WHEN converting to raw URLs
    THEN it should limit navigation to the branch level.
    """
    content = '<img src="../../../../images/cover.png" alt="Cover">'
    github_path = "https://github.com/user/repo/blob/main/docs/sub/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/main/images/cover.png" alt="Cover">'
    assert result == expected


def test_convert_html_image_links_to_raw_with_no_src_attributes():
    """
    GIVEN content with no src attributes
    WHEN converting to raw URLs
    THEN it should return the content unchanged.
    """
    content = """
# Title
<p>No images here.</p>
"""
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = """
# Title
<p>No images here.</p>
"""
    assert result == expected


def test_convert_html_image_links_to_raw_with_empty_content():
    """
    GIVEN empty content
    WHEN converting to raw URLs
    THEN it should return an empty string.
    """
    content = ""
    github_path = "https://github.com/user/repo/blob/main/docs/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = ""
    assert result == expected


def test_convert_html_image_links_to_raw_with_different_branch():
    """
    GIVEN HTML content and a GitHub path with a different branch
    WHEN converting to raw URLs
    THEN it should preserve the branch name in the raw URL.
    """
    content = '<img src="images/cover.png" alt="Cover">'
    github_path = "https://github.com/user/repo/blob/develop/docs/guide.md"
    result = convert_html_image_links_to_raw(content, github_path)
    expected = '<img src="https://raw.githubusercontent.com/user/repo/develop/docs/images/cover.png" alt="Cover">'
    assert result == expected
