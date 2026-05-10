from textnode import TextNode, TextType
from generate import move_generated_content


def main():
    move_generated_content("static", "public")


if __name__ == "__main__":
    main()
