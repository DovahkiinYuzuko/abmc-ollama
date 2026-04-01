import os
import sys
import re
import html

def get_resource_path(relative_path):
    """ロゴなどの『読み取り専用』リソース用（exe内部を優先）"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_writable_path(relative_path):
    """キャッシュや設定ファイルなどの『書き込み用』ファイル用（AppDataに保存）"""
    if os.name == 'nt':
        base_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'abmc-ollama')
    else:
        base_dir = os.path.expanduser('~/.abmc-ollama')
    
    full_path = os.path.join(base_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

def clean_text(text):
    """AIが読みやすいようにHTMLタグや特殊文字を掃除する。4bモデルの混乱を防ぐための必須機能。"""
    if not text:
        return ""
    # &gt; や &amp; を普通の文字に戻す
    text = html.unescape(text)
    # <... > で囲まれたHTMLタグを削除してテキストだけにする
    text = re.sub(r'<[^>]+>', '', text)
    # 余計な空白や改行を一つにまとめて情報の密度を上げる
    text = " ".join(text.split())
    return text.strip()