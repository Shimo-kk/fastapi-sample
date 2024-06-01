class CategoryValidator:
    """
    カテゴリのバリデータークラス
    """

    @staticmethod
    def validate_name(value: str) -> str:
        if not value:
            return "カテゴリ名に空の値を入力することはできません。"

        length: int = len(value)
        if length > 50:
            return "カテゴリ名に50文字より大きい値を入力することはできません。"

        return ""
