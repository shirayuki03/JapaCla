"""JapaCla source preprocessor for the Clambon Web UI runtime."""


JP2EN = {
    "待つ": "wait",
    "ずっと": "forever",
    "もし": "if",
    "でなければ": "else",
    "繰り返し": "repeat",
    "乱数": "random",
    "かつ": "and",
    "または": "or",
    "ではない": "not",
    "剰余": "mod",
    "四捨五入": "round",
    "絶対値": "abs",
    "切り下げ": "floor",
    "切り上げ": "ceiling",
    "平方根": "sqrt",
    "正弦": "sin",
    "余弦": "cos",
    "正接": "tan",
    "逆正弦": "asin",
    "逆余弦": "acos",
    "逆正接": "atan",
    "自然対数": "ln",
    "対数": "log",
    "真": "true",
    "偽": "false",
    "変数": "var",
    "リスト": "list",
    "追加": "add",
    "削除": "delete",
    "挿入": "insert",
    "長さ": "length",
    "含む": "contains",
    "出力": "print",
    "定義": "define",
    "返す": "return",
    "すべて": "all",
    "結合": "join",
    "文字": "letter",
    "から": "to",
    "の": "of",
}


# Try longer words first so, for example, ではない is handled as one token.
_KEYWORDS = tuple(sorted(JP2EN, key=len, reverse=True))


def _translated_keyword(source, index):
    """Return (replacement, consumed characters), or (None, 0)."""
    if source.startswith("位置", index):
        # Clambon uses `item` after a dot and `at` inside insert(... at ...).
        prefix = source[:index].rstrip()
        return ("item" if prefix.endswith(".") else "at", len("位置"))

    for japanese in _KEYWORDS:
        if source.startswith(japanese, index):
            return JP2EN[japanese], len(japanese)
    return None, 0


def JapaCla_preprocess_source(source):
    """Translate JapaCla keywords while preserving quoted string contents."""
    output = []
    index = 0
    quote = None
    escaped = False

    while index < len(source):
        character = source[index]

        if quote is not None:
            output.append(character)
            index += 1
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue

        if character in ('"', "'"):
            quote = character
            output.append(character)
            index += 1
            continue

        replacement, consumed = _translated_keyword(source, index)
        if replacement is not None:
            output.append(replacement)
            index += consumed
            continue

        output.append(character)
        index += 1

    return "".join(output)


class JapaCla_main:
    """Marker mixin required by the Web UI extension runtime."""

    def JapaCla_setup(self):
        pass
