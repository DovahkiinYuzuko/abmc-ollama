# abmc_ollama_variable_function_spec_20260401_1522.md

## Project Overview
**abmc-ollama** is a terminal-based manager for Ollama models featuring multi-language support, model lifecycle management (pull, run, remove, status), and an integrated AI Search Chat (Chain Agent Mode) that utilizes external search APIs.

---

## 1. i18n.py (Internationalization Manager)
Handles UI strings, translation, and local caching of translated text.

### Class: `I18nManager`
* **`__init__(self)`**: Initializes cache path, detects system locale (defaults to 'en'), and loads the message dictionary (English and Japanese presets).
* **`_load_cache(self) -> Dict[str, Any]`**: Loads the `cache_languages.json` file.
* **`_save_cache(self)`**: Saves the current translation cache to disk.
* **`get(self, key: str) -> str`**: Retrieves a message by key. Checks preset dictionaries first, then the local cache, then triggers auto-translation if not found.
* **`_auto_translate(self, key: str) -> str`**: Uses `GoogleTranslator` to translate English base text to the target language and saves it to the cache.

### Global Variables
* **`i18n`**: A singleton instance of `I18nManager`.

---

## 2. main.py (Application Core)
Handles the CLI menu logic and user interaction.

### Class: `AbmcApp`
* **`__init__(self)`**: Sets initial filters and resolves the logo resource path.
* **`display_logo(self)`**: Prints the ASCII art logo from `logoAA.txt`.
* **`clear_screen(self)`**: Clears the terminal console.
* **`menu_run_chat(self)`**: Menu [1]. Lists models and allows the user to start an `ollama run` session.
* **`start_model(self, model_name)`**: Prompts for additional CLI options and executes the model.
* **`menu_pull(self)`**: Menu [2]. Prompts for a model name to download via `ollama pull`.
* **`menu_remove(self)`**: Menu [3]. Lists installed models and allows deletion.
* **`menu_status(self)`**: Menu [4]. Shows currently running models using `ollama ps`.
* **`menu_search_chat(self)`**: Menu [5]. Selection screen for the AI Search Agent mode.
* **`start_search_session(self, model_name)`**: The main interactive loop for the RAG-based search chat.
* **`menu_search_settings(self)`**: Menu [6]. Configuration screen for search providers (Brave, Google, etc.).
* **`run(self)`**: The main entry loop that displays the primary menu.

---

## 3. manager.py (Ollama & Search Logic)
Interface for subprocess commands and the Chain-of-Thought RAG agent.

### Class: `OllamaManager`
* **`__init__(self)`**: Sets up paths for model/search caches and loads configuration.
* **`check_ollama(self)`**: Verifies if the `ollama` executable is available in the system PATH.
* **`get_remote_models(self)`**: Executes `ollama list` and returns the raw output string.
* **`load_cache(self)`**: Loads `cache_models.json`.
* **`save_cache(self, models_data, last_used=None)`**: Updates the model cache and stores the last used model name.
* **`load_search_config(self)`**: Loads `search_config.json`.
* **`save_search_config(self, config)`**: Saves the current search provider and API keys.
* **`run_model(self, m, opt="")`**: Runs a model in a subprocess using `ollama run`.
* **`pull_model(self, m)`**: Downloads a model via `ollama pull`.
* **`remove_model(self, m)`**: Deletes a model via `ollama rm`.
* **`show_status(self)`**: Displays running models via `ollama ps`.
* **`web_search(self, query)`**: Fetches results from Brave API or DuckDuckGo depending on the active provider.
* **`_call_phase(self, model_name, system_prompt, user_content, is_json=True)`**: Internal helper to call the Ollama Python library for specific agent phases (Planner, Extractor, Writer).
* **`chat_with_search(self, model_name, user_input, messages)`**: The 4-step Chain Agent logic:
    1.  **Planner**: Generates search queries.
    2.  **Searcher**: Executes web searches.
    3.  **Extractor**: Validates and extracts facts from search results.
    4.  **Writer**: Composes the final response based on facts.

### Global Variables
* **`ollama_mgr`**: A singleton instance of `OllamaManager`.

---

## 4. formatter.py (Data Formatting)
Parses CLI output and handles unit conversions.

### Class: `ModelFormatter`
* **`__init__(self)`**: Defines a `unit_map` for converting TB, GB, MB, KB to bytes.
* **`parse_ollama_list(self, raw_text: str)`**: Parses the raw table from `ollama list` into a sorted list of model dictionaries.
* **`_to_bytes(self, size_str: str) -> int`**: Converts human-readable sizes (e.g., "4.7 GB") into integer bytes for sorting.
* **`filter_models(self, models: list, keyword: str)`**: Filters a list of models by a search keyword.

### Global Variables
* **`formatter`**: A singleton instance of `ModelFormatter`.

---

## 5. utils.py (Utility Functions)
General helpers for pathing and text processing.

* **`get_resource_path(relative_path)`**: Resolves paths for read-only bundled assets (used with PyInstaller `_MEIPASS`).
* **`get_writable_path(relative_path)`**: Resolves paths for writable files in the user's AppData (Windows) or Home (Linux/Mac) directory.
* **`clean_text(text)`**: Removes HTML tags and normalizes whitespace/entities to optimize text for small-scale LLMs.

---

## 6. Installation Scripts (install_win.py, install_mac.py, install_linux.py)
Automate the build and environment setup process.

### Common Functions
* **`run_command(command, description_jp, description_en)`**: Executes a shell command with logging.
* **`install()`**: Performs the following:
    1.  Cleans previous build artifacts (`build/`, `dist/`, `.spec`).
    2.  Installs Python dependencies via `pip`.
    3.  Runs `pyinstaller` to create a standalone executable.
    4.  Moves the executable to the project root.
    5.  **Windows**: Adds the project directory to the User PATH via PowerShell and broadcasts the environment change.
    6.  **macOS/Linux**: Adds an alias to `.zshrc` or `.bashrc`.