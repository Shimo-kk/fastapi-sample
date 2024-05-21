from email_validator import validate_email, EmailNotValidError


class UserValidator:
    """
    ユーザーのバリデータークラス
    """

    @staticmethod
    def validate_name(value: str) -> str:
        if not value:
            return "ユーザー名に空の値を入力することはできません。"

        length: int = len(value)
        if length > 50:
            return "ユーザー名に50文字より大きい値を入力することはできません。"

        return ""

    @staticmethod
    def validate_email(value: str) -> str:
        if not value:
            return "E-mailアドレスに空の値を入力することはできません。"

        length: int = len(value)
        if length > 256:
            return "E-mailアドレスに256文字より大きい値を入力することはできません。"

        try:
            _ = validate_email(value, check_deliverability=False)
        except EmailNotValidError:
            return "メールアドレスが不正です。"

        return ""

    @staticmethod
    def validate_password(value: str) -> str:
        if not value:
            return "E-mailアドレスに空の値を入力することはできません。"

        length: int = len(value)
        if length < 6:
            return "パスワードに6文字より小さい値を入力することはできません。"
        if length > 256:
            return "パスワードに128文字より大きい値を入力することはできません。"

        return ""
