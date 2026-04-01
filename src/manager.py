import subprocess
import shlex
import json
import os
import sys
import requests
import ollama
from datetime import datetime
from i18n import i18n
from utils import get_writable_path, clean_text

class OllamaManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_path = get_writable_path('data/cache_models.json')
        self.config_path = get_writable_path('data/search_config.json')
        self.search_config = self.load_search_config()
        
    def check_ollama(self):
        try:
            if subprocess.run(['ollama', '--version'], capture_output=True).returncode != 0:
                print(i18n.get('ollama_not_found'))
                sys.exit(1)
        except Exception:
            print(i18n.get('ollama_not_found'))
            sys.exit(1)

    def get_remote_models(self):
        try:
            return subprocess.run(['ollama', 'list'], capture_output=True, text=True, encoding='utf-8').stdout
        except Exception:
            return ""

    def load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_cache(self, models_data, last_used=None):
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_used": last_used,
            "models": models_data
        }
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_search_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"active_provider": "ollama", "api_keys": {"brave": ""}}

    def save_search_config(self, config):
        self.search_config = config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def run_model(self, m, opt=""):
        self.save_cache([], last_used=m)
        try:
            subprocess.run(['ollama', 'run', m] + shlex.split(opt))
        except Exception:
            pass

    def pull_model(self, m):
        subprocess.run(['ollama', 'pull', m])
        
    def remove_model(self, m):
        subprocess.run(['ollama', 'rm', m])
        
    def show_status(self):
        subprocess.run(['ollama', 'ps'])

    def web_search(self, query):
        provider = self.search_config.get("active_provider", "ollama")
        keys = self.search_config.get("api_keys", {})
        results = []
        try:
            if provider == "brave" and keys.get("brave"):
                headers = {"X-Subscription-Token": keys["brave"]}
                resp = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params={"q": query}).json()
                for it in resp.get("web", {}).get("results", []):
                    results.append({"title": it.get("title"), "url": it.get("url"), "content": it.get("description")})
            else:
                resp = requests.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_html": 1}).json()
                if resp.get("AbstractText"):
                    results.append({"title": "DDG", "url": "https://duckduckgo.com", "content": resp["AbstractText"]})
        except Exception:
            pass
        return results

    def _call_phase(self, model_name, system_prompt, user_content, is_json=True):
        msgs = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_content}
        ]
        if is_json:
            resp = ollama.chat(model=model_name, messages=msgs, format='json')
        else:
            resp = ollama.chat(model=model_name, messages=msgs)
        return resp['message']['content']

    def chat_with_search(self, model_name, user_input, messages):
        now = datetime.now().strftime("%Y-%m-%d (%A)")
        all_facts = []
        source_links = []

        try:
            # --- Step 1: 計画 (Planner) ---
            print(f"\n{i18n.get('status_planner')}")
            planner_prompt = i18n.get('planner_prompt').format(now)
            plan_raw = self._call_phase(model_name, planner_prompt, f"Input: {user_input}")
            
            try:
                plan = json.loads(plan_raw)
            except json.JSONDecodeError:
                plan = {"queries": []}
                
            queries = plan.get('queries', [])[:5]
            
            # --- Step 2: 収集 (Searcher / Python) ---
            raw_snippets = []
            if queries:
                for idx, q in enumerate(queries):
                    print(f"{i18n.get('searching').format(q, idx+1, len(queries))}")
                    found = self.web_search(q)
                    for f in found:
                        raw_snippets.append(f"Title: {f['title']}\nContent: {f['content']}")
                        source_links.append(f"* [{f['title']}]({f['url']})")
            
            # --- Step 3: 事実抽出 (Extractor) ---
            if raw_snippets:
                print(f"\n{i18n.get('status_extractor')}")
                extractor_prompt = i18n.get('extractor_prompt').format(now)
                extract_input = f"Raw Data:\n" + "\n---\n".join(raw_snippets)
                facts_raw = self._call_phase(model_name, extractor_prompt, extract_input)
                
                try:
                    extract_res = json.loads(facts_raw)
                except json.JSONDecodeError:
                    extract_res = {"facts": []}
                
                all_facts = extract_res.get('facts', [])
                
                if all_facts:
                    print("-" * 20 + f"\n{i18n.get('search_result')}:\n" + "\n".join(all_facts) + "\n" + "-" * 20)

            # --- Step 4: 執筆 (Writer) ---
            print(f"\n{i18n.get('status_writer')}")
            if all_facts:
                writer_prompt = i18n.get('writer_prompt').format(", ".join(all_facts))
            else:
                writer_prompt = i18n.get('writer_prompt').format("有効な事実が見つかりませんでした。(No valid facts found.)")
                
            final_content = self._call_phase(model_name, writer_prompt, user_input, is_json=False)
            
            if source_links:
                final_content += i18n.get('sources_label') + "\n" + "\n".join(list(set(source_links))[:5])
            
            messages.append({'role': 'user', 'content': user_input})
            messages.append({'role': 'assistant', 'content': final_content})
            
            return final_content, messages

        except Exception as e:
            return f"Chain Agent Error: {str(e)}", messages

ollama_mgr = OllamaManager()