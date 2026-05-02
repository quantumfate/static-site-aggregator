from htmlnode import HTMLNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_exists(self):
        node = HTMLNode(
            None,
            None,
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        compare = node.props_to_html()
        self.assertEqual(compare, 'href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode(
            None,
            None,
            None,
            None,
        )
        compare = node.props_to_html()
        self.assertEqual(compare, "")

    def test_props_to_html_variation(self):
        node = HTMLNode(
            None,
            None,
            None,
            {
                "href": "https://www.boot.dev",
                "target": "_blank",
                "type": "image/png",
            },
        )

        compare = node.props_to_html()
        self.assertEqual(
            compare,
            'href="https://www.boot.dev" target="_blank" type="image/png"',
        )


if __name__ == "__main__":
    unittest.main()
