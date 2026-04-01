import os
import sys
import io
from i18n import i18n 
from manager import ollama_mgr
from formatter import formatter
from utils import get_resource_path

# --- システム設定：Windows環境での文字化けガード ---
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stdin.encoding != 'utf-8':
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

class AbmcApp:
    def __init__(self):
        """アプリ初期化：ロゴのパス解決とフィルタの準備"""
        self.current_filter = ""
        # PyInstallerで固めてもロゴファイルを見失わないように設定
        self.logo_path = get_resource_path('logoAA.txt')

    def display_logo(self):
        """ロゴAAを表示する（コンビニの看板みたいなもん）"""
        if os.path.exists(self.logo_path):
            try:
                with open(self.logo_path, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception: pass
        print("-" * 40)

    def clear_screen(self):
        """画面を掃除してスッキリさせる"""
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- [1] 実行 / チャット (標準モード) ---
    def menu_run_chat(self):
        """Ollama標準の対話モード（ollama run）を起動する"""
        self.current_filter = ""
        while True:
            self.clear_screen()
            self.display_logo()
            
            # モデルリストの取得と表示
            raw_list = ollama_mgr.get_remote_models()
            models = formatter.parse_ollama_list(raw_list)
            cache = ollama_mgr.load_cache()
            last_used = cache.get('last_used', "")
            display_models = formatter.filter_models(models, self.current_filter)

            if self.current_filter:
                print(f"\n{i18n.get('current_filter')} \"{self.current_filter}\" ({i18n.get('clear_filter')})")

            # 前回使った子を0番で呼び出せるショートカット
            exists_last_used = any(m['name'] == last_used for m in models)
            if last_used and exists_last_used:
                print(f" 0. [ {last_used} ] ({i18n.get('last_used')})")

            for idx, m in enumerate(display_models, 1):
                print(f" {idx}. {m['name']} ({m['size_raw']})")

            print(f"\n{i18n.get('exit')}")
            
            try:
                user_input = input(f"\n{i18n.get('select_model')} ").strip()
            except (KeyboardInterrupt, EOFError): break

            if user_input == "":
                if self.current_filter:
                    self.current_filter = ""
                    continue
                elif last_used and exists_last_used:
                    self.start_model(last_used)
                    continue
            elif user_input == "0" and last_used and exists_last_used:
                self.start_model(last_used)
            elif user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(display_models):
                    self.start_model(display_models[idx]['name'])
                else: print(i18n.get('invalid_input'))
            else: self.current_filter = user_input

    def start_model(self, model_name):
        """追加オプションを確認して実際にモデルを動かす"""
        print(f"\n[Selected: {model_name}]")
        try:
            options = input(f"{i18n.get('options_prompt')} ").strip()
            ollama_mgr.run_model(model_name, options)
        except (KeyboardInterrupt, EOFError): pass

    # --- [2] モデル追加 / [3] モデル削除 / [4] ステータス ---
    def menu_pull(self):
        """新しいモデルをネットから拾ってくる"""
        self.clear_screen(); self.display_logo()
        try:
            model_name = input(f"\n{i18n.get('pull_prompt')} ").strip()
            if model_name:
                ollama_mgr.pull_model(model_name)
                input(f"\n{i18n.get('press_enter')}")
        except (KeyboardInterrupt, EOFError): pass

    def menu_remove(self):
        """いらなくなったモデルを消去する"""
        while True:
            self.clear_screen(); self.display_logo()
            models = formatter.parse_ollama_list(ollama_mgr.get_remote_models())
            for idx, m in enumerate(models, 1):
                print(f" {idx}. {m['name']} ({m['size_raw']})")
            print(f"\n{i18n.get('exit')}")
            try:
                user_input = input(f"\n{i18n.get('remove_prompt')} ").strip()
                if user_input.isdigit():
                    idx = int(user_input) - 1
                    if 0 <= idx < len(models):
                        target = models[idx]['name']
                        confirm = input(f"\n{i18n.get('remove_confirm').format(target)} ").lower()
                        if confirm == 'y':
                            ollama_mgr.remove_model(target)
                            input(f"\n{i18n.get('press_enter')}"); break
                    else: print(i18n.get('invalid_input'))
                else: break
            except (KeyboardInterrupt, EOFError): break

    def menu_status(self):
        """現在VRAMで動いてるモデルをチェックする"""
        self.clear_screen(); self.display_logo()
        ollama_mgr.show_status()
        input(f"\n{i18n.get('press_enter')}")

    # --- [5] AI検索チャット (エージェントモード) ---
    def menu_search_chat(self):
        """検索ツールが使えるモデルを選んで対話を開始する"""
        self.current_filter = ""
        while True:
            self.clear_screen(); self.display_logo()
            print(f"\n{i18n.get('search_chat_title')}")
            print(f"{i18n.get('search_disclaimer')}") # 対応モデルが必要だよっていう注意書き

            models = formatter.parse_ollama_list(ollama_mgr.get_remote_models())
            display_models = formatter.filter_models(models, self.current_filter)

            for idx, m in enumerate(display_models, 1):
                print(f" {idx}. {m['name']} ({m['size_raw']})")

            print(f"\n{i18n.get('exit')}")
            try:
                user_input = input(f"\n{i18n.get('select_model')} ").strip()
            except (KeyboardInterrupt, EOFError): break

            if user_input == "" and self.current_filter:
                self.current_filter = ""; continue
            elif user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(display_models):
                    self.start_search_session(display_models[idx]['name'])
                else: print(i18n.get('invalid_input'))
            else: self.current_filter = user_input

    def start_search_session(self, model_name):
        """AIと1対1で、検索ありの対話ループを回す"""
        messages = []
        self.clear_screen(); self.display_logo()
        print(f"\n[Model: {model_name} (Search Agent Mode)]")
        print(f"({i18n.get('exit')})")

        while True:
            try:
                user_input = input(f"\nUser > ").strip()
                if not user_input: continue
                # manager側で定義した検索ツールをAIに渡して実行
                response, messages = ollama_mgr.chat_with_search(model_name, user_input, messages)
                print(f"\nAI > {response}")
            except (KeyboardInterrupt, EOFError): break

    # --- [6] 検索設定 (フルスペックAPIセレクター) ---
    def menu_search_settings(self):
        """使う検索エンジンとAPIキーを設定する画面"""
        while True:
            self.clear_screen(); self.display_logo()
            print(f"\n{i18n.get('settings_title')}")
            config = ollama_mgr.search_config
            print(i18n.get('current_provider').format(config.get('active_provider')))
            
            print(f"\n{i18n.get('select_provider')}")
            print(f"({i18n.get('exit')})")
            
            try:
                choice = input("\nChoice > ").strip()
                if choice == "1": # Ollama公式
                    config['active_provider'] = "ollama"
                elif choice == "2": # Brave
                    config['active_provider'] = "brave"
                    key = input(i18n.get('enter_api_key').format("Brave")).strip()
                    if key: config['api_keys']['brave'] = key
                elif choice == "3": # Google
                    config['active_provider'] = "google"
                    key = input(i18n.get('enter_api_key').format("Google")).strip()
                    cx = input(i18n.get('enter_cx_id')).strip()
                    if key: config['api_keys']['google'] = key
                    if cx: config['google_cx'] = cx
                elif choice == "4": # SearXNG
                    config['active_provider'] = "searxng"
                    url = input(i18n.get('enter_url')).strip()
                    key = input(i18n.get('enter_api_key').format("SearXNG (Optional)")).strip()
                    if url: config['searxng_url'] = url
                    if key: config['api_keys']['searxng'] = key
                elif choice == "5": # DuckDuckGo
                    config['active_provider'] = "duckduckgo"
                else: break
                
                ollama_mgr.save_search_config(config) # 設定をJSONに保存
                print(f"\n{i18n.get('settings_saved')}")
                input(i18n.get('press_enter')); break
            except (KeyboardInterrupt, EOFError): break

    # --- アプリ起動のメインループ ---
    def run(self):
        """メインメニューを表示し、ユーザーの選択に応じて各機能へ飛ばす"""
        try:
            ollama_mgr.check_ollama()
            while True:
                self.clear_screen(); self.display_logo()
                print(f"\n{i18n.get('menu_title')}")
                print(f" {i18n.get('menu_run')}")
                print(f" {i18n.get('menu_pull')}")
                print(f" {i18n.get('menu_remove')}")
                print(f" {i18n.get('menu_status')}")
                print(f" {i18n.get('menu_search')}")   # 5: エージェント
                print(f" {i18n.get('menu_settings')}") # 6: 検索設定
                print(f" {i18n.get('menu_exit')}")     # 7: 終了
                
                try:
                    choice = input(f"\n{i18n.get('select_option')} ").strip()
                    if choice == "1": self.menu_run_chat()
                    elif choice == "2": self.menu_pull()
                    elif choice == "3": self.menu_remove()
                    elif choice == "4": self.menu_status()
                    elif choice == "5": self.menu_search_chat()
                    elif choice == "6": self.menu_search_settings()
                    elif choice == "7": break
                except (KeyboardInterrupt, EOFError): break
        finally:
            print(f"\nBye! / またね！")
            input(f"\n{i18n.get('press_enter')}")
            sys.exit(0)

if __name__ == "__main__":
    import traceback
    app = AbmcApp()
    try:
        app.run()
    except SystemExit:
        # sys.exit() での正常終了なら何もしない
        pass
    except Exception:
        # ここでエラーを捕まえて、画面に表示して止める！
        print("\n" + "!" * 30)
        print("エラーが発生 / An error occurred:")
        traceback.print_exc() # エラーの詳細を書き出す
        print("!" * 30)
        
        try:
            input("\n何かキーを押して終了してください / Press Enter to exit...")
        except:
            pass
        sys.exit(1)