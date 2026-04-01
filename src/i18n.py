import locale
import json
import os
from typing import Dict, Any
from deep_translator import GoogleTranslator
from utils import get_writable_path

class I18nManager:
    def __init__(self):
        self.cache_path = get_writable_path('data/cache_languages.json')
        try:
            default_locale = locale.getdefaultlocale()[0]
            self.lang = default_locale.split('_')[0] if default_locale else 'en'
        except Exception:
            self.lang = 'en'
        
        self.cache = self._load_cache()
        
        # ANSIエスケープシーケンス（環境依存なしの文字装飾）
        YELLOW = "\033[33m"
        CYAN = "\033[36m"
        MAGENTA = "\033[35m"
        GREEN = "\033[32m"
        RESET = "\033[0m"
        
        self.messages: Dict[str, Dict[str, str]] = {
            'en': {
                'menu_title': '=== abmc-ollama Main Menu ===',
                'menu_run': '1. Run / Chat',
                'menu_pull': '2. Pull / Download ',
                'menu_remove': '3. Remove / Delete ',
                'menu_status': '4. Status / PS ',
                'menu_search': '5. AI Search Chat (Beta)',
                'menu_settings': '6. Search Settings',
                'menu_exit': '7. Exit ',
                'select_option': 'Select an option (1-7):',
                'pull_prompt': 'Enter model name to pull (e.g. qwen2.5):',
                'remove_prompt': 'Select a model to remove (Number):',
                'remove_confirm': 'Are you sure you want to remove "{}"? [y/N]:',
                'press_enter': 'Press Enter to return to menu...',
                'select_model': 'Choose a model (Number or Filter):',
                'search_chat_title': '=== AI Search Chat (Chain Agent Mode) ===',
                'search_prompt': 'Search is enabled. Type your question:',
                'searching': f"{CYAN}[Searcher] Searching: {{}} ({{}}/{{}}){RESET}",
                'ollama_not_found': 'Ollama not found. Please make sure it is running.',
                'current_filter': 'Current Filter:',
                'last_used': 'last used',
                'no_models': 'No models found.',
                'invalid_input': 'Invalid input.',
                'clear_filter': 'Press Enter to clear filter.',
                'exit': 'Ctrl+C to back to menu.',
                'options_prompt': 'Additional options? (e.g., --think=false / Enter for none):',
                'search_disclaimer': '* Note: Single-pass RAG Chain mode (Optimized for lightweight models).',
                'settings_title': '=== Search API Settings ===',
                'current_provider': 'Current Provider: {}',
                'select_provider': 'Select Search Provider (1. Ollama Cloud, 2. Brave, 3. Google, 4. SearXNG, 5. DuckDuckGo):',
                'enter_api_key': 'Enter API Key for {}:',
                'enter_cx_id': 'Enter Google Search Engine ID (CX ID):',
                'enter_url': 'Enter SearXNG Instance URL (e.g., https://search.example.com):',
                'settings_saved': 'Settings saved successfully!',
                'key_required': 'This provider requires configuration.',
                'search_result': f"{MAGENTA}[Extracted Facts]{RESET}",
                'no_result': '[No valid facts found]',
                'sources_label': '\n\n**Sources:**',
                # --- Progress Labels ---
                'status_planner': f"{YELLOW}[Planner] Creating an investigation plan...{RESET}",
                'status_extractor': f"{MAGENTA}[Extractor] Extracting and verifying facts...{RESET}",
                'status_writer': f"{GREEN}[Writer] Composing the final response...{RESET}",
                # --- Chain Prompts ---
                'planner_prompt': (
                    "You are a Planner. Today is {}. Create up to 5 search queries in JSON format: {{\"queries\": [\"query1\", ...]}}. "
                    "Stay focused on the user's specific location and topic. Do not broaden the search to nearby regions unless necessary."
                ),
                'extractor_prompt': (
                    "You are a Fact Extractor. Current Date: {}. Extract facts relevant to the user's query from raw data into JSON: {{\"facts\": [\"fact1\", ...]}}. "
                    "STRICT RULES:\n"
                    "1. DATE CHECK: If the query is time-sensitive (e.g., weather, news), ONLY use data matching the Current Date. For history or general knowledge, extract all relevant facts regardless of date.\n"
                    "2. NUMBER VALIDATION: Pay close attention to numbers and their labels (e.g., ensure you do not mistake precipitation '0mm' for temperature '0 degrees').\n"
                    "3. LOCALITY: Ensure facts belong to the specific location requested."
                ),
                'writer_prompt': "You are a Writer. Based ONLY on these facts, answer the user in English: {}"
            },
            'ja': {
                'menu_title': '=== abmc-ollama メインメニュー ===',
                'menu_run': '1. 実行 / チャット',
                'menu_pull': '2. モデル追加 (Pull)',
                'menu_remove': '3. モデル削除 (Remove)',
                'menu_status': '4. ステータス確認 (Status)',
                'menu_search': '5. AI検索チャット (ベータ版)',
                'menu_settings': '6. 検索設定',
                'menu_exit': '7. 終了',
                'select_option': 'メニュー番号を選んでください (1-7):',
                'pull_prompt': '追加するモデル名を入力してください (例: qwen2.5):',
                'remove_prompt': '削除するモデルの番号を選んでください:',
                'remove_confirm': '本当に "{}" を削除しますか？ [y/N]:',
                'press_enter': 'Enterキーでメニューに戻ります...',
                'select_model': 'モデルを選んでください（番号またはフィルタ入力）:',
                'search_chat_title': '=== AI検索チャット (チェーン・エージェント・モード) ===',
                'search_prompt': '検索機能が有効です。質問を入力してください:',
                'searching': f"{CYAN}[Searcher] 調査中: {{}} ({{}}/{{}}){RESET}",
                'ollama_not_found': 'Ollamaが見つかりません。起動しているか確認してください。',
                'current_filter': '現在のフィルタ:',
                'last_used': '前回使用',
                'no_models': 'モデルが見つかりませんでした。',
                'invalid_input': '入力が正しくありません。',
                'clear_filter': 'Enterキーでフィルタ解除',
                'exit': 'Ctrl+Cでメニューに戻る',
                'options_prompt': '追加オプションを入力（例: --think=false / なければEnter）:',
                'search_disclaimer': '* 注意: 1パスRAGチェーン構成（軽量モデル向け最適化）。',
                'settings_title': '=== 検索API設定 ===',
                'current_provider': '現在のエンジン: {}',
                'select_provider': 'エンジンを選択 (1. Ollama公式, 2. Brave, 3. Google, 4. SearXNG, 5. DuckDuckGo):',
                'enter_api_key': '{} のAPIキーを入力してください:',
                'enter_cx_id': 'Google検索エンジンID (CX ID) を入力してください:',
                'enter_url': 'SearXNG インスタンスのURLを入力してください (例: https://search.example.com):',
                'settings_saved': '設定を保存しました！',
                'key_required': 'このエンジンには追加の設定が必要です。',
                'search_result': f"{MAGENTA}[抽出された事実]{RESET}",
                'no_result': '[有効な事実が見つかりませんでした]',
                'sources_label': '\n\n**参照元:**',
                # --- Progress Labels ---
                'status_planner': f"{YELLOW}[Planner] 調査プランを作成中...{RESET}",
                'status_extractor': f"{MAGENTA}[Extractor] 事実の抽出と検証を行っています...{RESET}",
                'status_writer': f"{GREEN}[Writer] 回答を執筆しています...{RESET}",
                # --- Chain Prompts ---
                'planner_prompt': (
                    "あなたは計画担当です。今日の日付は {} です。質問を解決するための検索クエリを最大5つJSON形式で作成してください: {{\"queries\": [\"クエリ1\", ...]}} "
                    "対象となる場所やトピックから逸れないようにしてください。必要がない限り、近隣地域へ検索を広げないでください。"
                ),
                'extractor_prompt': (
                    "あなたは事実抽出担当です。現在の日付: {}。生データからユーザーの質問に関連する事実を抽出し、JSON形式で出力してください: {{\"facts\": [\"事実1\", ...]}}。"
                    "【厳守ルール】:\n"
                    "1. 日付検証: 天気やニュース等の『現在情報』が求められている場合は、現在の日付に一致する情報のみを採用し、古いキャッシュは破棄してください。歴史や一般知識の場合は日付を問わず抽出してください。\n"
                    "2. 数値の整合性: 数値とそのラベル（例: 降水量 0mm と 気温 0度）を混同しないよう、文脈を正確に読み取ってください。\n"
                    "3. 地域性: 事実が指定された場所に属していることを確認してください。"
                ),
                'writer_prompt': "あなたは執筆担当です。提供された事実のみに基づき、日本語でユーザーに回答してください。事実: {}"
            }
        }

    def _load_cache(self) -> Dict[str, Any]:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception: return {}
        return {}

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception: pass

    def get(self, key: str) -> str:
        if self.lang in self.messages:
            return self.messages[self.lang].get(key, self.messages['en'].get(key, key))
        if self.lang in self.cache and key in self.cache[self.lang]:
            return self.cache[self.lang][key]
        return self._auto_translate(key)

    def _auto_translate(self, key: str) -> str:
        base_text = str(self.messages['en'].get(key, key))
        try:
            translated = GoogleTranslator(source='en', target=self.lang).translate(base_text)
            if not translated: return base_text
            final_text = f"[Auto-translated] {translated}"
            if self.lang not in self.cache: self.cache[self.lang] = {}
            self.cache[self.lang][key] = final_text
            self._save_cache()
            return final_text
        except Exception: return base_text

i18n = I18nManager()