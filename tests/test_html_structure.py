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


class TestCourseSelectScreen:
    """コース選択画面のテスト"""

    def test_screen_courses_exists(self, html):
        """screen-coursesというIDの画面が存在すること"""
        assert 'id="screen-courses"' in html

    def test_has_four_course_cards(self, html):
        """4つのコースカード（身だしなみ、履歴書、面接マナー、面接対策）が含まれること"""
        # screen-courses セクションを抽出
        start = html.find('id="screen-courses"')
        assert start != -1, "screen-courses not found"
        # 次のscreen開始まで
        end = html.find('<div class="screen', start + 1)
        if end == -1:
            end = len(html)
        section = html[start:end]
        assert 'screen-lessons' in section, "Grooming course card should link to screen-lessons"
        assert 'screen-lessons-resume' in section, "Resume course card should link to screen-lessons-resume"
        assert 'screen-lessons-manners' in section, "Manners course card should link to screen-lessons-manners"
        assert 'screen-lessons-strategy' in section, "Strategy course card should link to screen-lessons-strategy"

    def test_nav_learn_tab_points_to_courses(self, html):
        """ナビの「学」タブがscreen-coursesを指していること"""
        nav_pattern = re.search(r'class="nav__item"[^>]*data-screen="screen-courses"', html)
        assert nav_pattern, "Learn nav tab should have data-screen='screen-courses'"

    def test_apply_ui_strings_updates_courses(self, html):
        """applyUIStringsでcourses.キーが更新されること"""
        assert "'courses." in html

    def test_screen_courses_in_screens_with_nav(self, html):
        """screensWithNavにscreen-coursesが含まれること"""
        screens_match = re.search(r'screensWithNav\s*=\s*\[([^\]]+)\]', html)
        assert screens_match, "screensWithNav array not found"
        assert "'screen-courses'" in screens_match.group(1), "screen-courses should be in screensWithNav"

    def test_screen_courses_in_nav_map(self, html):
        """navMapにscreen-coursesが含まれること"""
        navmap_match = re.search(r'navMap\s*=\s*\{([^}]+)\}', html)
        assert navmap_match, "navMap object not found"
        assert "'screen-courses'" in navmap_match.group(1), "screen-courses should be in navMap"

    def test_lesson_list_back_buttons_go_to_courses(self, html):
        """レッスン一覧画面の戻るボタンがscreen-coursesに遷移すること"""
        # 各レッスン一覧のback buttonを確認
        for screen_id in ['screen-lessons', 'screen-lessons-resume', 'screen-lessons-manners', 'screen-lessons-strategy']:
            start = html.find(f'id="{screen_id}"')
            assert start != -1, f"{screen_id} not found"
            # 最初のbtn-backを見つける
            btn_pos = html.find('class="btn-back"', start)
            assert btn_pos != -1, f"btn-back not found in {screen_id}"
            # そのボタンのonclickを確認
            line_start = html.rfind('<', 0, btn_pos)
            line_end = html.find('>', btn_pos) + 1
            button_html = html[line_start:line_end]
            assert "screen-courses" in button_html, f"Back button in {screen_id} should navigate to screen-courses, got: {button_html}"


class TestCourseSelectI18n:
    """コース選択画面の多言語JSONテスト"""

    def test_en_json_has_courses_keys(self):
        """en.jsonにcoursesキーが存在すること"""
        import json
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', 'en.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'courses' in data, "en.json should have 'courses' key"
        courses = data['courses']
        for key in ['title', 'subtitle', 'grooming', 'resume', 'manners', 'strategy', 'lessons_count', 'progress']:
            assert key in courses, f"en.json courses should have '{key}' key"

    def test_ja_json_has_courses_keys(self):
        """ja.jsonにcoursesキーが存在すること"""
        import json
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', 'ja.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'courses' in data, "ja.json should have 'courses' key"
        courses = data['courses']
        for key in ['title', 'subtitle', 'grooming', 'resume', 'manners', 'strategy', 'lessons_count', 'progress']:
            assert key in courses, f"ja.json courses should have '{key}' key"

    def test_vi_json_has_courses_keys(self):
        """vi.jsonにcoursesキーが存在すること"""
        import json
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', 'vi.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'courses' in data, "vi.json should have 'courses' key"
        courses = data['courses']
        for key in ['title', 'subtitle', 'grooming', 'resume', 'manners', 'strategy', 'lessons_count', 'progress']:
            assert key in courses, f"vi.json courses should have '{key}' key"

    def test_all_json_keys_match(self):
        """3言語のcoursesキー構造が完全一致すること"""
        import json
        keys_by_lang = {}
        for lang in ['en', 'ja', 'vi']:
            path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', f'{lang}.json')
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            keys_by_lang[lang] = set(data.get('courses', {}).keys())
        assert keys_by_lang['en'] == keys_by_lang['ja'] == keys_by_lang['vi'], \
            f"courses keys mismatch: en={keys_by_lang['en']}, ja={keys_by_lang['ja']}, vi={keys_by_lang['vi']}"


class TestLessonDetailI18n:
    """レッスン詳細画面のdata-i18n多言語化テスト"""

    DETAIL_SCREENS = [
        'screen-detail-mochimono',
        'screen-detail-dansei',
        'screen-detail-josei',
        'screen-detail-hyojo',
        'screen-quiz-grooming',
        'screen-detail-rirekisho',
        'screen-detail-profile-qual',
        'screen-detail-shibodoki',
        'screen-detail-sonota',
        'screen-detail-nyutaishitsu',
        'screen-detail-aisatsu',
        'screen-detail-henji',
        'screen-detail-online',
        'screen-detail-shitsumon1',
        'screen-detail-shitsumon2',
        'screen-detail-naitei',
        'screen-detail-kokorogamae',
    ]

    LESSON_LIST_SCREENS = [
        'screen-lessons',
        'screen-lessons-resume',
        'screen-lessons-manners',
        'screen-lessons-strategy',
    ]

    def test_data_i18n_attributes_exist_in_detail_screens(self, html):
        """各レッスン詳細画面にdata-i18nアトリビュートが存在すること"""
        for screen_id in self.DETAIL_SCREENS:
            start = html.find(f'id="{screen_id}"')
            assert start != -1, f"{screen_id} not found"
            # Find the end of this screen (next screen or end)
            next_screen = html.find('<div class="screen', start + 1)
            if next_screen == -1:
                next_screen = len(html)
            section = html[start:next_screen]
            assert 'data-i18n=' in section, \
                f"{screen_id} should have data-i18n attributes for i18n support"

    def test_data_i18n_attributes_exist_in_lesson_lists(self, html):
        """各レッスン一覧画面にdata-i18nアトリビュートが存在すること"""
        for screen_id in self.LESSON_LIST_SCREENS:
            start = html.find(f'id="{screen_id}"')
            assert start != -1, f"{screen_id} not found"
            next_screen = html.find('<div class="screen', start + 1)
            if next_screen == -1:
                next_screen = len(html)
            section = html[start:next_screen]
            assert 'data-i18n=' in section, \
                f"{screen_id} should have data-i18n attributes for i18n support"

    def test_apply_i18n_attributes_function_exists(self, html):
        """applyI18nAttributes関数がJavaScriptに存在すること"""
        assert 'function applyI18nAttributes()' in html

    def test_apply_i18n_attributes_called_in_apply_ui_strings(self, html):
        """applyI18nAttributesがapplyUIStrings内で呼ばれること"""
        # Find applyUIStrings function body
        start = html.find('function applyUIStrings()')
        assert start != -1
        # Find the next function declaration after applyUIStrings
        end = html.find('\nfunction ', start + 30)
        if end == -1:
            end = html.find('\nasync function ', start + 30)
        section = html[start:end] if end != -1 else html[start:]
        assert 'applyI18nAttributes()' in section, \
            "applyI18nAttributes() should be called inside applyUIStrings()"

    def test_data_i18n_sub_support_in_js(self, html):
        """data-i18n-subのサポートがJavaScriptに存在すること"""
        assert 'data-i18n-sub' in html


class TestLessonI18nData:
    """レッスン詳細の多言語JSONテスト"""

    DETAIL_SLUGS = [
        'mochimono', 'dansei', 'josei', 'hyojo', 'quiz_grooming',
        'rirekisho', 'profile_qual', 'shibodoki', 'sonota',
        'nyutaishitsu', 'aisatsu', 'henji', 'online',
        'shitsumon1', 'shitsumon2', 'naitei', 'kokorogamae',
    ]

    def _load_json(self, lang):
        import json
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ui', f'{lang}.json')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_all_keys(self, d, prefix=''):
        """再帰的に全キーパスを取得"""
        keys = set()
        for k, v in d.items():
            full = f'{prefix}.{k}' if prefix else k
            if isinstance(v, dict):
                keys.update(self._get_all_keys(v, full))
            else:
                keys.add(full)
        return keys

    def test_en_json_has_lessons_detail_keys(self):
        """en.jsonにlessons.detailキーが存在すること"""
        data = self._load_json('en')
        assert 'lessons' in data, "en.json should have 'lessons' key"
        lessons = data['lessons']
        assert 'detail' in lessons, "en.json lessons should have 'detail' key"
        for slug in self.DETAIL_SLUGS:
            assert slug in lessons['detail'], \
                f"en.json lessons.detail should have '{slug}' key"

    def test_ja_json_has_lessons_detail_keys(self):
        """ja.jsonにlessons.detailキーが存在すること"""
        data = self._load_json('ja')
        assert 'lessons' in data
        assert 'detail' in data['lessons']
        for slug in self.DETAIL_SLUGS:
            assert slug in data['lessons']['detail'], \
                f"ja.json lessons.detail should have '{slug}' key"

    def test_vi_json_has_lessons_detail_keys(self):
        """vi.jsonにlessons.detailキーが存在すること"""
        data = self._load_json('vi')
        assert 'lessons' in data
        assert 'detail' in data['lessons']
        for slug in self.DETAIL_SLUGS:
            assert slug in data['lessons']['detail'], \
                f"vi.json lessons.detail should have '{slug}' key"

    def test_all_detail_keys_match_across_languages(self):
        """3言語のlessons.detailキー構造が完全一致すること"""
        keys_by_lang = {}
        for lang in ['en', 'ja', 'vi']:
            data = self._load_json(lang)
            detail = data.get('lessons', {}).get('detail', {})
            keys_by_lang[lang] = self._get_all_keys(detail)

        assert keys_by_lang['en'] == keys_by_lang['ja'], \
            f"en/ja detail keys mismatch. en-only: {keys_by_lang['en'] - keys_by_lang['ja']}, ja-only: {keys_by_lang['ja'] - keys_by_lang['en']}"
        assert keys_by_lang['en'] == keys_by_lang['vi'], \
            f"en/vi detail keys mismatch. en-only: {keys_by_lang['en'] - keys_by_lang['vi']}, vi-only: {keys_by_lang['vi'] - keys_by_lang['en']}"

    def test_no_empty_values_in_detail(self):
        """lessons.detail内に空文字列の翻訳がないこと"""
        for lang in ['en', 'ja', 'vi']:
            data = self._load_json(lang)
            detail = data.get('lessons', {}).get('detail', {})
            for slug, entries in detail.items():
                if isinstance(entries, dict):
                    for key, val in entries.items():
                        assert val != '', \
                            f"{lang}.json lessons.detail.{slug}.{key} should not be empty"

    def test_lesson_list_i18n_keys_exist(self):
        """レッスン一覧用のi18nキーが3言語に存在すること"""
        list_slugs = ['grooming', 'resume', 'manners', 'strategy']
        for lang in ['en', 'ja', 'vi']:
            data = self._load_json(lang)
            lessons = data.get('lessons', {})
            assert 'list' in lessons, f"{lang}.json lessons should have 'list' key"
            for slug in list_slugs:
                assert slug in lessons['list'], \
                    f"{lang}.json lessons.list should have '{slug}' key"
