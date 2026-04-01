# abmc-ollama
![logo](assets/logoAA.png)

## Index / 目次
* [日本語 (Japanese)](#日本語-japanese)
* [お嬢様言葉 (Polite Japanese)](#お嬢様言葉-polite-japanese)
* [English](#english)

---

## 日本語 (Japanese)

Ollamaを「ちょっと便利に（a bit more convenient）」利用するための、マルチプラットフォーム対応CLIランチャーです。
複雑なコマンド操作を排し、番号選択による直感的なモデル管理と、外部検索エンジンと連携したAI検索エージェント機能を提供します。

### 概要
abmc-ollama は、ローカルLLM実行環境であるOllamaの利便性を向上させるために開発されました。
モデルの実行・ダウンロード・削除といった基本操作に加え、軽量モデルでも高精度な回答を可能にする「4段階RAGチェーン」を用いた検索チャットモードを搭載しています。

### 主な機能
* **直感的なモデル管理**: インストール済みモデルをサイズ順にソートして一覧表示し、番号入力で即座に実行・削除が可能です。
* **AI検索チャット（エージェントモード）**: 検索クエリ生成、ウェブ検索、事実抽出、回答執筆の4ステップ（Planner, Searcher, Extractor, Writer）を自動実行し、最新情報に基づいた回答を生成します。
* **多言語対応（i18n）**: システム言語を自動検出し、日本語と英語に標準対応しています。未対応言語も自動翻訳キャッシュ機能により利用可能です。
* **マルチエンジン検索**: Brave SearchやGoogle Custom Search、SearXNGなどの外部APIと連携設定が可能です。
* **クリーンな環境維持**: PyInstallerによるビルド時、実行ファイルをプロジェクトルートへ自動配置し、中間ファイルを削除するインストーラーを提供します。

### 対応OS
* **Windows 10/11**: ユーザー環境変数（PATH）への自動登録と即時反映に対応しています。
* **macOS / Linux**: シェル設定ファイル（.zshrc, .bashrc）へのエイリアス自動登録に対応しています。

### インストール方法
#### 事前準備
1. Ollama がインストールされ、バックグラウンドで起動している必要があります。
2. Python 3.10以上 がインストールされていることを確認してください。

#### 手順
リポジトリをクローンし、各OSに対応したインストーラーを実行してください。

**Windows:**
```powershell
python install_win.py
```

**macOS:**
```bash
python3 install_mac.py
```

**Linux:**
```bash
python3 install_linux.py
```

実行完了後、新しいターミナルを開くことで `abmc-ollama` コマンドが有効になります。

### 使い方
ターミナルで以下のコマンドを入力します。
```bash
abmc-ollama
```
表示されるメインメニューから、目的の操作番号を入力してください。

---

## お嬢様言葉 (Polite Japanese)

こちらは、Ollamaを「いささか便利に（a bit more convenient）」利用するための、マルチプラットフォーム対応CLIランチャーでございますわ。
複雑なコマンド操作を排し、番号選択による直感的なモデル管理と、外部検索エンジンと連携いたしましたAI検索エージェント機能を備えておりますの。

### 概要
abmc-ollama は、ローカルLLM実行環境であるOllamaの利便性を向上させるべく開発されましたわ。
モデルの実行・ダウンロード・削除といった基本操作に加え、軽量モデルにおいても高精度な回答を可能にする「4段階RAGチェーン」を用いた検索チャットモードを搭載しております。

### 主な機能
* **直感的なモデル管理**: インストール済みモデルをサイズ順に整列して一覧表示し、番号入力にて即座に実行・削除が可能でございます。
* **AI検索チャット（エージェントモード）**: 検索クエリ生成、ウェブ検索、事実抽出、回答執筆の4段階（Planner, Searcher, Extractor, Writer）を自動実行し、最新情報に基づいた回答を生成いたします。
* **多言語対応（i18n）**: システム言語を自動検出し、日本語と英語に標準対応しておりますわ。未対応言語も自動翻訳キャッシュ機能により利用可能でございます。
* **マルチエンジン検索**: Brave SearchやGoogle Custom Search、SearXNGなどの外部APIと連携設定が可能でございます。
* **クリーンな環境維持**: PyInstallerによるビルド時、実行ファイルをプロジェクトルートへ自動配置し、中間ファイルを削除するインストーラーを提供いたします。

### 対応OS
* **Windows 10/11**: ユーザー環境変数（PATH）への自動登録と即時反映に対応しております。
* **macOS / Linux**: シェル設定ファイル（.zshrc, .bashrc）へのエイリアス自動登録に対応いたしました。

### インストール方法
#### 事前準備
1. Ollama がインストールされ、バックグラウンドで起動している必要がございます。
2. Python 3.10以上 がインストールされていることをお確かめあそばせ。

#### 手順
リポジトリをクローンし、各OSに対応したインストーラーを実行あそばせ。

**Windows:**
```powershell
python install_win.py
```

**macOS / Linux:**
```bash
python3 install_mac.py  # or install_linux.py
```

実行完了後、新しいターミナルをお開きになさって？ `abmc-ollama` コマンドが有効になりますわ。

---

## English

A multi-platform CLI launcher designed to make using Ollama "a bit more convenient" (abmc).
It eliminates complex command operations, providing intuitive model management through number selection and an AI search agent integrated with external search engines.

### Overview
abmc-ollama was developed to enhance the convenience of Ollama, a local LLM execution environment.
In addition to basic operations such as running, downloading, and deleting models, it features a search chat mode using a "4-stage RAG chain" that enables high-accuracy responses even with lightweight models.

### Key Features
* **Intuitive Model Management**: Lists installed models sorted by size, allowing immediate execution or deletion via number input.
* **AI Search Chat (Agent Mode)**: Automatically executes a 4-step process (Planner, Searcher, Extractor, Writer) including search query generation, web searching, fact extraction, and response writing to generate answers based on the latest information.
* **Multi-language Support (i18n)**: Automatically detects system language with standard support for Japanese and English. Unsupported languages are available through an automatic translation cache.
* **Multi-engine Search**: Configurable integration with external APIs such as Brave Search, Google Custom Search, and SearXNG.
* **Clean Environment Maintenance**: Provides installers that automatically relocate the executable to the project root and delete intermediate files during PyInstaller builds.

### Supported OS
* **Windows 10/11**: Supports automatic registration and immediate reflection in User Environment Variables (PATH).
* **macOS / Linux**: Supports automatic alias registration in shell configuration files (.zshrc, .bashrc).

### Installation
#### Prerequisites
1. Ollama must be installed and running in the background.
2. Ensure Python 3.10 or higher is installed.

#### Steps
Clone the repository and run the installer corresponding to your OS.

**Windows:**
```powershell
python install_win.py
```

**macOS / Linux:**
```bash
python3 install_mac.py  # or install_linux.py
```

After completion, open a new terminal to enable the `abmc-ollama` command.

### Usage
Enter the following command in your terminal:
```bash
abmc-ollama
```
Select the desired operation number from the main menu.

### Directory Structure
* **src/**: Application source code
* **assets/**: Icons and logo files
* **docs/**: Documentation such as specifications
* **data/**: Cache and configuration files (auto-generated)

### License
This project is released under the MIT License.
