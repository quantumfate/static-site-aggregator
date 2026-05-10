from textnode import TextNode, TextType
from generate import generate_page, move_generated_content


def main():
    move_generated_content("static", "public")
    generate_page("content/index.md", "public/index.html", "template.html")
    generate_page(
        "content/blog/glorfindel/index.md",
        "public/blog/glorfindel/index.html",
        "template.html",
    )
    generate_page(
        "content/blog/majesty/index.md",
        "public/blog/majesty/index.html",
        "template.html",
    )
    generate_page(
        "content/blog/tom/index.md", "public/blog/tom/index.html", "template.html"
    )
    generate_page(
        "content/contact/index.md", "public/contact/index.html", "template.html"
    )


if __name__ == "__main__":
    main()
