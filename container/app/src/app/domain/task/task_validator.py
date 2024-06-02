from datetime import date


class TaskValidator:
    """
    タスクのバリデータークラス
    """

    @staticmethod
    def validate_title(value: str) -> str:
        if not value:
            return "タイトルに空の値を入力することはできません。"

        length: int = len(value)
        if length > 50:
            return "タイトルに50文字より大きい値を入力することはできません。"

        return ""

    @staticmethod
    def validate_start_date(value: date) -> str:
        if value is None:
            return "開始日を未設定です。"
        if value < date.today():
            return "開始日に過去の日付を設定することはできません。"

        return ""
