from blocktype import BlockType, block_to_block_type

import unittest


class TestBlockTypeHeading(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)

    def test_h2(self):
        self.assertEqual(block_to_block_type("## Subtitle"), BlockType.HEADING)

    def test_h3(self):
        self.assertEqual(block_to_block_type("### Section"), BlockType.HEADING)

    def test_h4(self):
        self.assertEqual(block_to_block_type("#### Sub"), BlockType.HEADING)

    def test_h5(self):
        self.assertEqual(block_to_block_type("##### Tiny"), BlockType.HEADING)

    def test_h6(self):
        self.assertEqual(block_to_block_type("###### Smallest"), BlockType.HEADING)

    def test_seven_hashes_is_not_heading(self):
        self.assertEqual(block_to_block_type("####### too many"), BlockType.PARAGRAPH)

    def test_hash_without_space_is_not_heading(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_hash_alone_is_not_heading(self):
        self.assertEqual(block_to_block_type("#"), BlockType.PARAGRAPH)


class TestBlockTypeCode(unittest.TestCase):
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')\n```"), BlockType.CODE)

    def test_multi_line_code_block(self):
        block = "```\ndef f():\n    return 1\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_empty_code_block(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)

    def test_code_without_trailing_fence_is_not_code(self):
        self.assertEqual(block_to_block_type("```\ncontent"), BlockType.PARAGRAPH)

    def test_code_without_leading_newline_is_not_code(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_single_backtick_line_is_not_code(self):
        self.assertEqual(block_to_block_type("`code`"), BlockType.PARAGRAPH)


class TestBlockTypeQuote(unittest.TestCase):
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type("> quoted"), BlockType.QUOTE)

    def test_multi_line_quote(self):
        self.assertEqual(
            block_to_block_type("> first\n> second\n> third"), BlockType.QUOTE
        )

    def test_quote_no_space_after_marker(self):
        self.assertEqual(block_to_block_type(">no space"), BlockType.QUOTE)

    def test_quote_broken_by_non_quote_line(self):
        self.assertEqual(
            block_to_block_type("> first\nplain\n> third"), BlockType.PARAGRAPH
        )

    def test_quote_broken_at_last_line(self):
        self.assertEqual(block_to_block_type("> a\n> b\nc"), BlockType.PARAGRAPH)


class TestBlockTypeUnorderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_multiple_items(self):
        self.assertEqual(block_to_block_type("- a\n- b\n- c"), BlockType.UNORDERED_LIST)

    def test_dash_without_space_is_not_unordered(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_one_bad_line_disqualifies(self):
        self.assertEqual(block_to_block_type("- a\n- b\nc"), BlockType.PARAGRAPH)

    def test_mixed_with_ordered_is_paragraph(self):
        self.assertEqual(block_to_block_type("- a\n1. b"), BlockType.PARAGRAPH)


class TestBlockTypeOrderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type("1. first"), BlockType.ORDERED_LIST)

    def test_three_items(self):
        self.assertEqual(
            block_to_block_type("1. a\n2. b\n3. c"), BlockType.ORDERED_LIST
        )

    def test_long_ordered_list(self):
        block = "\n".join(f"{i}. item" for i in range(1, 11))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_starts_at_two_is_not_ordered(self):
        self.assertEqual(block_to_block_type("2. b\n3. c"), BlockType.PARAGRAPH)

    def test_skipped_number_is_not_ordered(self):
        self.assertEqual(block_to_block_type("1. a\n3. c"), BlockType.PARAGRAPH)

    def test_out_of_order_is_not_ordered(self):
        self.assertEqual(block_to_block_type("1. a\n3. b\n2. c"), BlockType.PARAGRAPH)

    def test_no_space_after_dot_is_not_ordered(self):
        self.assertEqual(block_to_block_type("1.first"), BlockType.PARAGRAPH)


class TestBlockTypeParagraph(unittest.TestCase):
    def test_plain_text(self):
        self.assertEqual(block_to_block_type("just words here"), BlockType.PARAGRAPH)

    def test_multi_line_plain(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)

    def test_inline_markdown_in_paragraph(self):
        self.assertEqual(
            block_to_block_type("text with **bold** and _italic_"),
            BlockType.PARAGRAPH,
        )

    def test_empty_string_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


class TestBlockTypeReturnType(unittest.TestCase):
    def test_returns_blocktype_enum(self):
        self.assertIsInstance(block_to_block_type("# heading"), BlockType)


if __name__ == "__main__":
    unittest.main()
