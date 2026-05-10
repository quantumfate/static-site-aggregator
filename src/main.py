import sys
from textnode import TextNode, TextType
from generate import generate_page, generate_pages_recursive, move_generated_content


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        # GH Page
        basepath = sys.argv[1]
        move_generated_content("static", "docs")
        generate_pages_recursive("content", "template.html", "docs", basepath)
    else:
        move_generated_content("static", "public")
        generate_pages_recursive("content", "template.html", "public", basepath)


if __name__ == "__main__":
    main()
