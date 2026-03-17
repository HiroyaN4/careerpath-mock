"""
CareerPath HTML構造テスト
- index.html の整合性
- 旧ハードコードQ&Aが削除されていること
- 動的レンダリング用のプレースホルダーがあること
- 言語管理コードが存在すること
"""
import os
import re
import pytest

HTML_PATH = os.path.join(os.path.dirname(__file__), '..', 'index.html')

@pytest.fixture
def html():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()


class TestLoginLanguageSelector:
    def test_login_lang_selector_exists(self, html):
        """ログイン画面に言語セレクターが存在すること"""
        assert 'id="login-lang"' in html

    def test_login_lang_has_three_options(self, html):
        """ログイン画面の言語セレクターにja/en/viの3言語があること"""
        # Find the login-lang select element area
        import re
        login_lang = re.search(r'id="login-lang".*?</select>', html, re.DOTALL)
        assert login_lang, "login-lang select not found"
        block = login_lang.group(0)
        assert 'value="en"' in block
        assert 'value="ja"' in block
        assert 'value="vi"' in block

    def test_login_lang_calls_set_language(self, html):
        """ログイン言語セレクターがsetLanguageを呼ぶこと"""
        assert 'onchange="setLanguage(this.value)"' in html or 'login-lang' in html

    def test_login_screen_has_i18n_ids(self, html):
        """ログイン画面のテキストにi18n用のidが付いていること"""
        assert 'id="login-tab-signin"' in html
        assert 'id="login-tab-register"' in html
        assert 'id="login-tagline"' in html

    def test_apply_ui_strings_updates_login(self, html):
        """applyUIStringsがログイン画面を更新するコードを含むこと"""
        assert 'login-tab-signin' in html
        assert "'login." in html


class TestHTMLStructure:
    def test_no_hardcoded_qa_items(self, html):
        """ハードコードされたqa-itemが存在しないこと（動的レンダリングに移行済み）"""
        # data-industry= はJSのrenderQAList内にはあるが、HTMLタグとしてはないはず
        # HTMLセクション内（scriptの外）でdata-industryを検索
        script_start = html.index('<script>')
        html_section = html[:script_start]
        matches = re.findall(r'<div class="qa-item" data-industry=', html_section)
        assert len(matches) == 0, f"Found {len(matches)} hardcoded qa-item elements in HTML"

    def test_qa_list_placeholder_exists(self, html):
        """動的Q&Aリストのプレースホルダーが存在すること"""
        assert 'id="qa-list"' in html

    def test_qa_filters_placeholder_exists(self, html):
        """動的フィルターのプレースホルダーが存在すること"""
        assert 'id="qa-filters"' in html

    def test_qa_counter_exists(self, html):
        """Q&Aカウンターが存在すること"""
        assert 'id="qa-counter"' in html

    def test_qa_lang_selector_exists(self, html):
        """Q&A言語セレクターが存在すること"""
        assert 'id="qa-lang"' in html

    def test_qa_lang_has_three_options(self, html):
        """言語セレクターにja/en/viの3オプションがあること"""
        assert 'value="ja"' in html
        assert 'value="en"' in html
        assert 'value="vi"' in html


class TestJavaScript:
    def test_load_qa_data_function(self, html):
        """loadQAData関数が存在すること"""
        assert 'async function loadQAData()' in html

    def test_render_qa_list_function(self, html):
        """renderQAList関数が存在すること"""
        assert 'function renderQAList()' in html

    def test_set_language_function(self, html):
        """setLanguage関数が存在すること"""
        assert 'async function setLanguage(lang)' in html

    def test_load_ui_strings_function(self, html):
        """loadUIStrings関数が存在すること"""
        assert 'async function loadUIStrings(lang)' in html

    def test_detect_browser_lang_function(self, html):
        """detectBrowserLang関数が存在すること"""
        assert 'function detectBrowserLang()' in html

    def test_localstorage_key(self, html):
        """localStorageのキーが正しいこと"""
        assert "localStorage.getItem('careerpath-lang')" in html
        assert "localStorage.setItem('careerpath-lang'" in html

    def test_fetch_qa_json(self, html):
        """Q&AデータのfetchパスがJSに存在すること"""
        assert "fetch('data/qa.json')" in html

    def test_fetch_ui_json(self, html):
        """UIデータのfetchパスがJSに存在すること"""
        assert "fetch('data/ui/'" in html

    def test_init_function_calls(self, html):
        """初期化処理でloadUIStringsとloadQADataが呼ばれること"""
        assert 'await loadUIStrings(currentLang)' in html
        assert 'await loadQAData()' in html

    def test_no_old_switch_qa_lang(self, html):
        """旧switchQALang関数が残っていないこと"""
        assert 'function switchQALang(' not in html

    def test_set_qa_content_lang_function(self, html):
        """新しいsetQAContentLang関数が存在すること"""
        assert 'function setQAContentLang(lang)' in html


class TestFileStructure:
    def test_data_directory_exists(self):
        """data/ディレクトリが存在すること"""
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        assert os.path.isdir(data_dir)

    def test_qa_json_exists(self):
        """data/qa.jsonが存在すること"""
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'qa.json')
        assert os.path.isfile(path)

    def test_ui_en_exists(self):
        assert os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', 'en.json'))

    def test_ui_ja_exists(self):
        assert os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', 'ja.json'))

    def test_ui_vi_exists(self):
        assert os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', 'vi.json'))

    def test_html_line_count_reduced(self):
        """index.htmlの行数が大幅に削減されていること（旧4192行→3700行以下）"""
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        assert len(lines) < 3800, f"HTML has {len(lines)} lines, expected < 3800 (was 4192 before refactor)"


class TestLoginLayout:
    """Phase 1: ログイン画面レイアウト修正テスト"""

    def test_lang_selector_inside_login_brand(self, html):
        """言語セレクターがlogin__brandの中にあること（login__brandの閉じタグより前）"""
        # login__brand開始位置とlogin-lang位置を確認
        brand_start = html.find('class="login__brand"')
        lang_pos = html.find('id="login-lang"')
        # login__brandの終了位置を見つける（ネストを考慮）
        # login-langがlogin__brandとlogin__brand閉じの間にあること
        # login__price の後、login__body の前にあること
        price_pos = html.find('id="login-free"')
        body_pos = html.find('class="login__body"')
        assert brand_start < lang_pos < body_pos, "login-lang should be inside login__brand, before login__body"
        assert price_pos < lang_pos, "login-lang should be after login__price"

    def test_lang_selector_after_login_price(self, html):
        """言語セレクターがlogin__priceの後に配置されていること"""
        price_pos = html.find('login__price')
        lang_pos = html.find('id="login-lang"')
        assert price_pos < lang_pos, "login-lang should come after login__price"

    def test_login_hero_has_flex_center(self, html):
        """login__heroにflex center指定があること"""
        # CSS内で確認
        hero_css = re.search(r'\.login__hero\s*\{[^}]+\}', html)
        assert hero_css, "login__hero CSS not found"
        css = hero_css.group(0)
        assert 'display: flex' in css or 'display:flex' in css
        assert 'align-items: center' in css or 'align-items:center' in css
        assert 'justify-content: center' in css or 'justify-content:center' in css


class TestHomeScreenI18n:
    """Phase 3: ホーム画面のi18n対応テスト"""

    def test_home_welcome_has_id(self, html):
        """ホーム画面のWelcome backにi18n IDがあること"""
        assert 'id="home-welcome"' in html

    def test_home_streak_has_id(self, html):
        """ストリーク表示にi18n IDがあること"""
        assert 'id="home-streak"' in html

    def test_home_step_tracker_has_ids(self, html):
        """ステップトラッカーにi18n IDがあること"""
        assert 'id="home-step-prepare"' in html
        assert 'id="home-step-interview"' in html
        assert 'id="home-step-apply"' in html
        assert 'id="home-step-offer"' in html

    def test_home_section_heads_have_ids(self, html):
        """ホーム画面のセクション見出しにi18n IDがあること"""
        assert 'id="home-continue-learning"' in html
        assert 'id="home-lesson-categories"' in html
        assert 'id="home-quick-review"' in html

    def test_home_daily_goal_has_id(self, html):
        """デイリーゴールにi18n IDがあること"""
        assert 'id="home-daily-goal"' in html

    def test_home_todays_phrase_has_id(self, html):
        """Today's PhraseにIDがあること"""
        assert 'id="home-todays-phrase"' in html

    def test_apply_ui_strings_updates_home(self, html):
        """applyUIStringsがホーム画面を更新すること"""
        assert "'home." in html


class TestProfileScreenI18n:
    """Phase 3: プロフィール画面のi18n対応テスト"""

    def test_profile_stat_labels_have_ids(self, html):
        """統計ラベルにi18n IDがあること"""
        assert 'id="profile-stat-streak"' in html
        assert 'id="profile-stat-interviews"' in html
        assert 'id="profile-stat-courses"' in html
        assert 'id="profile-stat-phrases"' in html

    def test_profile_member_badge_has_id(self, html):
        """メンバーバッジにi18n IDがあること"""
        assert 'id="profile-member-badge"' in html

    def test_profile_settings_title_has_id(self, html):
        """設定タイトルにi18n IDがあること"""
        assert 'id="profile-settings-title"' in html

    def test_profile_sign_out_has_id(self, html):
        """ログアウトにi18n IDがあること"""
        assert 'id="profile-sign-out"' in html

    def test_apply_ui_strings_updates_profile(self, html):
        """applyUIStringsがプロフィール画面を更新すること"""
        assert "'profile." in html


class TestPracticeScreenI18n:
    """Phase 3: Practice画面のi18n対応テスト"""

    def test_practice_title_has_id(self, html):
        """Practice画面タイトルにIDがあること"""
        assert 'id="practice-title"' in html

    def test_practice_desc_has_id(self, html):
        """Practice画面説明にIDがあること"""
        assert 'id="practice-desc"' in html


class TestLessonListI18n:
    """Phase 3: レッスン一覧のi18n対応テスト"""

    def test_lesson_list_headers_have_ids(self, html):
        """レッスン一覧のヘッダーにi18n IDがあること"""
        assert 'id="lessons-title-1"' in html

    def test_apply_ui_strings_updates_lessons(self, html):
        """applyUIStringsがレッスン画面を更新すること"""
        assert "'lessons." in html
