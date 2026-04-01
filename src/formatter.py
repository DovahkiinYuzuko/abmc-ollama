import re

class ModelFormatter:
    def __init__(self):
        # サイズ単位をバイト換算するためのマップ
        # 1024倍（バイナリ接頭辞）で計算するよ
        self.unit_map = {
            'TB': 1024**4,
            'GB': 1024**3,
            'MB': 1024**2,
            'KB': 1024**1,
            'B': 1024**0
        }

    def parse_ollama_list(self, raw_text: str):
        """ollama list の出力を解析して、サイズ順にソートされたリストを返す"""
        lines = raw_text.strip().split('\n')
        # ヘッダー行しかない、または空の場合は空リストを返す
        if len(lines) <= 1:
            return []

        models = []
        # 1行目はヘッダー（NAME, ID, SIZE...）だから2行目から処理
        for line in lines[1:]:
            # 2つ以上の連続する空白で分割してカラムを取り出す
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) < 3:
                continue
            
            name = parts[0]
            size_raw = parts[2]
            
            # ソートできるように数値をバイト単位に変換
            size_bytes = self._to_bytes(size_raw)
            
            models.append({
                "name": name,
                "size_raw": size_raw,
                "size_bytes": size_bytes
            })
        
        # サイズ（bytes）の昇順（小さい順）でソートして返す
        return sorted(models, key=lambda x: x['size_bytes'])

    def _to_bytes(self, size_str: str) -> int:
        """'4.7 GB' みたいな文字列を int のバイト数に変換する"""
        try:
            # 数字の部分と単位の部分を正規表現で切り分ける
            match = re.match(r'([\d.]+)\s*([a-zA-Z]+)', size_str.strip())
            if not match:
                return 0
            
            number = float(match.group(1))
            unit = match.group(2).upper()
            
            # 単位に応じた倍率をかけて計算
            multiplier = self.unit_map.get(unit, 1)
            return int(number * multiplier)
        except Exception:
            # パースに失敗したらとりあえず0にしておく
            return 0

    def filter_models(self, models: list, keyword: str):
        """キーワードが含まれるモデルだけを抽出する"""
        if not keyword:
            return models
        
        return [m for m in models if keyword.lower() in m['name'].lower()]

# 他のファイルから使いやすいようにインスタンス化
formatter = ModelFormatter()