import unittest

from main import JP2EN, JapaCla_preprocess_source


class JapaClaPreprocessorTests(unittest.TestCase):
    def test_every_registered_keyword(self):
        for japanese, english in JP2EN.items():
            with self.subTest(japanese=japanese):
                self.assertEqual(JapaCla_preprocess_source(japanese), english)

    def test_control_and_expression_keywords(self):
        source = """変数 score = 乱数(1 から 3)
もし <<score > 1> かつ <真 == 真>> {
    印刷(平方根(score))
} でなければ {
    待つ(1)
}
"""
        expected = """var score = random(1 to 3)
if <<score > 1> and <true == true>> {
    print(sqrt(score))
} else {
    wait(1)
}
"""
        self.assertEqual(JapaCla_preprocess_source(source), expected)

    def test_strings_and_escapes_are_not_translated(self):
        source = '印刷("待つ \\\"真\\\" 追加")'
        self.assertEqual(
            JapaCla_preprocess_source(source),
            'print("待つ \\\"真\\\" 追加")',
        )

    def test_list_member_keywords_and_position_context(self):
        source = """リスト values = [1]
values.追加(2)
values.挿入(3 位置 1)
変数 index = values.位置(2)
変数 size = values.長さ
values.削除(すべて)
"""
        expected = """list values = [1]
values.add(2)
values.insert(3 at 1)
var index = values.item(2)
var size = values.length
values.delete(all)
"""
        self.assertEqual(JapaCla_preprocess_source(source), expected)

    def test_english_and_e_are_unchanged(self):
        source = "var base = e\n印刷(base)"
        self.assertEqual(JapaCla_preprocess_source(source), "var base = e\nprint(base)")

    def test_position_has_two_contextual_translations(self):
        self.assertEqual(JapaCla_preprocess_source("values.位置(2)"), "values.item(2)")
        self.assertEqual(JapaCla_preprocess_source("3 位置 1"), "3 at 1")


if __name__ == "__main__":
    unittest.main()
