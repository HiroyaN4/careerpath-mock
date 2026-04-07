"""
田中さんフィードバック4件の検証テスト

1. プロフィールページ: 日本語設定でも英語になる
2. Q&A言語切替: 英語設定でQ&Aが日本語になる
3. 管理画面: 人気の質問が英語表記
4. 管理画面: 業種がアイコンだけで違和感
"""
import json
import os
import re
import pytest

HTML_PATH = os.path.join(os.path.dirname(__file__), '..', 'index.html')
ADMIN_PATH = os.path.join(os.path.dirname(__file__), '..', 'docs', 'admin-dashboard.html')
UI_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'ui')


@pytest.fixture
def html():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def admin_html():
    with open(ADMIN_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def load_ui_json(lang):
    path = os.path.join(UI_DIR, f'{lang}.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_keys(d, prefix=''):
    """JSONのキーをフラットなドットパスで返す"""
    keys = set()
    for k, v in d.items():
        full = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.update(get_all_keys(v, full))
        else:
            keys.add(full)
    return keys


# ==============================================================
# 指摘1: プロフィールページの多言語化
# ==============================================================
class TestProfileI18nComplete:
    """プロフィール画面の全テキスト要素にi18n対応があるか"""

    def _get_profile_section(self, html):
        """screen-profile セクションのHTMLを抽出"""
        start = html.find('id="screen-profile"')
        assert start != -1, "screen-profile not found"
        end = html.find('<nav class="nav"', start)
        if end == -1:
            end = len(html)
        return html[start:end]

    def test_profile_stat_labels_have_i18n_ids(self, html):
        """統計ラベル(Day Streak等)にi18n IDが付いていること"""
        profile = self._get_profile_section(html)
        required_ids = [
            'profile-stat-streak',
            'profile-stat-interviews',
            'profile-stat-courses',
            'profile-stat-phrases',
        ]
        for id_name in required_ids:
            assert f'id="{id_name}"' in profile, \
                f"Profile stat label '{id_name}' missing i18n ID"

    def test_profile_member_badge_has_i18n_id(self, html):
        """メンバーバッジにi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-member-badge"' in profile

    def test_profile_settings_title_has_i18n_id(self, html):
        """設定タイトルにi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-settings-title"' in profile

    def test_profile_sign_out_has_i18n_id(self, html):
        """サインアウトにi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-sign-out"' in profile

    def test_profile_job_progress_has_i18n_id(self, html):
        """就職活動進捗タイトルにi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-job-progress"' in profile

    def test_profile_phase_labels_have_i18n_ids(self, html):
        """フェーズラベル(Prepare/Apply/Interview/Offer)にi18n IDがあること"""
        profile = self._get_profile_section(html)
        for phase in ['prepare', 'apply', 'interview', 'offer']:
            assert f'id="profile-phase-{phase}"' in profile, \
                f"Profile phase '{phase}' missing i18n ID"

    def test_profile_badges_have_data_i18n(self, html):
        """バッジ名にdata-i18n属性があること"""
        profile = self._get_profile_section(html)
        expected_badges = [
            'profile.badge_first_lesson',
            'profile.badge_week_streak',
            'profile.badge_grooming_master',
            'profile.badge_50_phrases',
            'profile.badge_mock_interview',
            'profile.badge_all_industries',
        ]
        for badge_key in expected_badges:
            assert f'data-i18n="{badge_key}"' in profile, \
                f"Badge '{badge_key}' missing data-i18n attribute"

    def test_profile_lang_settings_have_i18n_ids(self, html):
        """言語設定にi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-lang-label"' in profile
        assert 'id="profile-lang-desc"' in profile

    def test_profile_notification_settings_have_i18n_ids(self, html):
        """通知設定にi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-notif-label"' in profile
        assert 'id="profile-notif-desc"' in profile

    def test_profile_joined_has_i18n_id(self, html):
        """参加日にi18n IDがあること"""
        profile = self._get_profile_section(html)
        assert 'id="profile-joined"' in profile

    def test_apply_ui_strings_updates_all_profile_elements(self, html):
        """applyUIStringsがプロフィール画面の主要要素を全て更新すること"""
        # applyUIStrings内のprofile系の更新を確認
        profile_ids_in_apply = [
            'profile-member-badge',
            'profile-stat-streak',
            'profile-stat-interviews',
            'profile-stat-courses',
            'profile-stat-phrases',
            'profile-job-progress',
            'profile-badges-title',
            'profile-settings-title',
            'profile-lang-label',
            'profile-notif-label',
            'profile-notif-desc',
            'profile-sign-out',
            'profile-phase-prepare',
            'profile-phase-apply',
            'profile-phase-interview',
            'profile-phase-offer',
        ]
        for id_name in profile_ids_in_apply:
            assert f"'{id_name}'" in html, \
                f"applyUIStrings should update '{id_name}'"

    def test_profile_keys_exist_in_all_langs(self):
        """profile.*キーが3言語全てに存在すること"""
        for lang in ['ja', 'en', 'vi']:
            data = load_ui_json(lang)
            assert 'profile' in data, f"{lang}.json missing 'profile' key"
            profile = data['profile']
            required_keys = [
                'member_badge', 'stat_streak', 'stat_interviews',
                'stat_courses', 'stat_phrases', 'job_hunting_progress',
                'settings', 'language', 'language_desc',
                'notifications', 'notifications_desc', 'sign_out',
                'phase_prepare', 'phase_apply', 'phase_interview', 'phase_offer',
                'badges', 'badge_first_lesson', 'badge_week_streak',
                'badge_grooming_master', 'badge_50_phrases',
                'badge_mock_interview', 'badge_all_industries',
            ]
            for key in required_keys:
                assert key in profile, \
                    f"{lang}.json profile.{key} is missing"

    def test_profile_keys_not_empty_in_ja(self):
        """日本語のprofileキーが空でないこと（田中さんの指摘：日本語でも英語になる）"""
        data = load_ui_json('ja')
        profile = data['profile']
        for key, val in profile.items():
            if isinstance(val, str):
                assert val.strip(), f"ja.json profile.{key} is empty"

    def test_profile_ja_values_are_japanese(self):
        """日本語のprofile値が実際に日本語であること（英語のままになっていないか）"""
        data = load_ui_json('ja')
        profile = data['profile']
        # 主要テキストが日本語であることを確認
        japanese_checks = {
            'stat_streak': '連続',
            'stat_courses': 'コース',
            'settings': '設定',
            'sign_out': 'ログアウト',
            'member_badge': 'メンバー',
        }
        for key, expected_substr in japanese_checks.items():
            assert expected_substr in profile[key], \
                f"ja.json profile.{key} = '{profile[key]}' doesn't contain expected Japanese text '{expected_substr}'"


# ==============================================================
# 指摘2: Q&A言語切替の整合性
# ==============================================================
class TestQALanguageSync:
    """Q&Aの言語がUI言語と正しく連動するか"""

    def test_set_language_updates_qa_content_lang(self, html):
        """setLanguage関数内でqaContentLangが更新されること"""
        # setLanguage関数を抽出
        start = html.find('async function setLanguage(lang)')
        assert start != -1, "setLanguage function not found"
        end = html.find('\n}', start) + 2
        func_body = html[start:end]
        assert 'qaContentLang = lang' in func_body, \
            "setLanguage should update qaContentLang to the new language"

    def test_qa_content_lang_not_hardcoded(self, html):
        """qaContentLangの初期値がハードコードされていないこと"""
        # qaContentLangの初期化行を確認
        init_match = re.search(r'let qaContentLang\s*=\s*(.+?);', html)
        assert init_match, "qaContentLang declaration not found"
        init_value = init_match.group(1)
        # ハードコードされた単一言語ではないこと
        assert init_value != "'ja'", "qaContentLang should not be hardcoded to 'ja'"
        assert init_value != "'en'", "qaContentLang should not be hardcoded to 'en'"
        assert init_value != "'vi'", "qaContentLang should not be hardcoded to 'vi'"
        # localStorageまたはdetectBrowserLangを使っていること
        assert 'localStorage' in init_value or 'detectBrowserLang' in init_value, \
            "qaContentLang should be initialized from localStorage or browser detection"

    def test_qa_content_lang_used_in_render(self, html):
        """renderQAList内でqaContentLangが質問表示に使われていること"""
        start = html.find('function renderQAList()')
        assert start != -1, "renderQAList function not found"
        end = html.find('\nfunction ', start + 20)
        if end == -1:
            end = html.find('\nasync function ', start + 20)
        func_body = html[start:end] if end != -1 else html[start:start+3000]
        assert 'qaContentLang' in func_body, \
            "renderQAList should use qaContentLang for displaying questions"

    def test_set_qa_content_lang_updates_and_rerenders(self, html):
        """setQAContentLang関数がqaContentLangを更新してリレンダーすること"""
        start = html.find('function setQAContentLang(lang)')
        assert start != -1, "setQAContentLang function not found"
        end = html.find('\n}', start) + 2
        func_body = html[start:end]
        assert 'qaContentLang = lang' in func_body, \
            "setQAContentLang should update qaContentLang"
        # setQAContentLangはsetLanguage経由でリレンダーする（setLanguage内でrenderQAListが呼ばれる）
        assert 'setLanguage' in func_body, \
            "setQAContentLang should call setLanguage (which triggers renderQAList)"

    def test_qa_lang_selector_exists_with_options(self, html):
        """Q&A言語セレクターが3言語オプション付きで存在すること"""
        qa_lang_match = re.search(r'id="qa-lang".*?</select>', html, re.DOTALL)
        assert qa_lang_match, "qa-lang select not found"
        block = qa_lang_match.group(0)
        assert 'value="ja"' in block, "qa-lang missing ja option"
        assert 'value="en"' in block, "qa-lang missing en option"
        assert 'value="vi"' in block, "qa-lang missing vi option"

    def test_qa_data_has_all_lang_question_keys(self):
        """qa.jsonの全アイテムにja/en/viの質問テキストがあること"""
        qa_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'qa.json')
        with open(qa_path, 'r', encoding='utf-8') as f:
            qa_data = json.load(f)
        for item in qa_data['items']:
            for lang in ['ja', 'en', 'vi']:
                assert item['question'].get(lang), \
                    f"{item['id']} missing {lang} question"

    def test_qa_data_has_ja_vi_model_answers(self):
        """qa.jsonの全アイテムにja/viの模範回答・NG例があること（en翻訳は未完了を許容）"""
        qa_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'qa.json')
        with open(qa_path, 'r', encoding='utf-8') as f:
            qa_data = json.load(f)
        for item in qa_data['items']:
            assert item['model_answer'].get('ja'), \
                f"{item['id']} missing ja model_answer"
            assert item['model_answer'].get('vi'), \
                f"{item['id']} missing vi model_answer"
            assert item['ng_example'].get('ja'), \
                f"{item['id']} missing ja ng_example"
            assert item['ng_example'].get('vi'), \
                f"{item['id']} missing vi ng_example"

    def test_qa_render_fallback_to_japanese(self, html):
        """renderQAListが常に日本語をメイン表示し、翻訳をサブテキストとして表示すること"""
        start = html.find('function renderQAList()')
        assert start != -1
        end = html.find('\nfunction ', start + 20)
        if end == -1:
            end = html.find('\nasync function ', start + 20)
        func_body = html[start:end] if end != -1 else html[start:start+3000]
        # 日本語をメインで表示する設計であること
        assert 'model_answer.ja' in func_body or "model_answer['ja']" in func_body, \
            "renderQAList should use Japanese as the primary display language for answers"

    def test_qa_ui_labels_exist_in_all_langs(self):
        """Q&AのUIラベル(title, subtitle, filter等)が3言語に存在すること"""
        for lang in ['ja', 'en', 'vi']:
            data = load_ui_json(lang)
            assert 'qa' in data, f"{lang}.json missing 'qa' key"
            qa = data['qa']
            required = [
                'title', 'subtitle', 'filter_all',
                'model_answer', 'ng_example', 'tip',
            ]
            for key in required:
                assert key in qa, f"{lang}.json qa.{key} is missing"
                assert qa[key].strip(), f"{lang}.json qa.{key} is empty"


# ==============================================================
# 指摘3: 管理画面の人気の質問が英語表記
# ==============================================================
class TestAdminPopularQuestions:
    """管理画面の「人気の質問」テーブルが日本語であること"""

    def test_popular_questions_title_is_japanese(self, admin_html):
        """人気の質問セクションのタイトルが日本語であること"""
        assert '人気の質問' in admin_html, \
            "Popular questions section title should be in Japanese"

    def test_popular_questions_table_headers_are_japanese(self, admin_html):
        """テーブルヘッダーが日本語であること"""
        # 人気の質問テーブル付近を確認
        start = admin_html.find('人気の質問')
        assert start != -1
        end = admin_html.find('</table>', start)
        section = admin_html[start:end]
        assert '質問' in section, "Table header should contain '質問'"
        assert '業種' in section, "Table header should contain '業種'"
        assert '閲覧数' in section, "Table header should contain '閲覧数'"

    def test_popular_questions_content_is_japanese(self, admin_html):
        """人気の質問の内容が日本語であること（英語ハードコードでないこと）"""
        start = admin_html.find('人気の質問')
        assert start != -1
        end = admin_html.find('</table>', start)
        section = admin_html[start:end]
        # 英語の質問テキストが含まれていないこと
        assert 'Why do you want to work' not in section, \
            "Question text should be in Japanese, not English"
        assert 'Do you have any questions' not in section, \
            "Question text should be in Japanese, not English"
        # 日本語の質問テキストが含まれていること
        assert 'ですか' in section or 'ますか' in section, \
            "Questions should contain Japanese text"

    def test_no_hardcoded_english_headers_in_qa_tables(self, admin_html):
        """Q&A関連テーブルのヘッダーに英語ハードコードがないこと"""
        # "Question", "Industry", "Views" などの英語ヘッダーがないこと
        # テーブルヘッダー(th)のみを検査
        th_pattern = re.findall(r'<th[^>]*>(.*?)</th>', admin_html)
        english_headers = ['Question', 'Industry', 'Views', 'Score', 'Popular']
        for header in th_pattern:
            header_text = header.strip()
            for eng in english_headers:
                assert eng != header_text, \
                    f"Table header should be Japanese, found English: '{header_text}'"

    def test_wrong_answer_questions_title_is_japanese(self, admin_html):
        """間違いが多い質問のタイトルが日本語であること"""
        assert '間違いが多い質問' in admin_html, \
            "Wrong answer questions section title should be in Japanese"

    def test_wrong_answer_table_headers_are_japanese(self, admin_html):
        """間違いが多いQ&Aテーブルのヘッダーが日本語であること"""
        start = admin_html.find('間違いが多い質問')
        assert start != -1
        end = admin_html.find('</table>', start)
        section = admin_html[start:end]
        assert '正答率' in section, "Table should have '正答率' column"
        assert '回答数' in section, "Table should have '回答数' column"


# ==============================================================
# 指摘4: 管理画面の業種がアイコンだけ
# ==============================================================
class TestAdminIndustryLabels:
    """管理画面の業種表示にアイコン+テキスト名が含まれていること"""

    def test_industry_qa_section_has_text_names(self, admin_html):
        """業種別Q&A閲覧状況にテキスト名があること（アイコンだけでないこと）"""
        start = admin_html.find('業種別 Q&A 閲覧状況')
        assert start != -1, "Industry Q&A section not found"
        end = admin_html.find('</div>\n      </div>', start)
        section = admin_html[start:end]
        industry_names = ['建設', '製造', '外食', '宿泊']
        for name in industry_names:
            assert name in section, \
                f"Industry Q&A section should contain text name '{name}', not just icon"

    def test_popular_questions_industry_column_has_text(self, admin_html):
        """人気の質問テーブルの業種列にテキスト名があること"""
        start = admin_html.find('人気の質問')
        assert start != -1
        end = admin_html.find('</table>', start)
        section = admin_html[start:end]
        # 業種列（td）にテキスト名があるか
        # パターン: アイコン + テキスト名
        industry_text_found = False
        for name in ['飲食', '製造', '建設', '小売', '宿泊']:
            if name in section:
                industry_text_found = True
                break
        assert industry_text_found, \
            "Industry column in popular questions should contain text names, not just icons"

    def test_wrong_answer_industry_column_has_text(self, admin_html):
        """間違いが多い質問テーブルの業種列にテキスト名があること"""
        start = admin_html.find('間違いが多い質問')
        assert start != -1
        end = admin_html.find('</table>', start)
        section = admin_html[start:end]
        industry_text_found = False
        for name in ['飲食', '製造', '建設', '小売', '宿泊']:
            if name in section:
                industry_text_found = True
                break
        assert industry_text_found, \
            "Industry column in wrong-answer questions should contain text names"

    def test_industry_cells_are_not_icon_only(self, admin_html):
        """業種セル(td)がアイコンのみでないこと（emoji + テキストの組み合わせ）"""
        # テーブル内のtdを検査して、emojiのみの業種表示がないか確認
        # 人気の質問テーブルの業種列
        start = admin_html.find('人気の質問')
        end = admin_html.find('</table>', start)
        section = admin_html[start:end]

        # <td>🍽</td> のようなアイコンのみのセルがないか
        icon_only_pattern = re.findall(r'<td>([^<]+)</td>', section)
        for cell in icon_only_pattern:
            cell_stripped = cell.strip()
            # 絵文字のみ（日本語テキストなし）のセルを検出
            if cell_stripped and not any(
                '\u3000' <= c <= '\u9fff' or '\u30a0' <= c <= '\u30ff'
                for c in cell_stripped
            ):
                # 数字やランクは除外
                if not cell_stripped.replace(' ', '').isdigit():
                    # emojiのみかどうかチェック（2文字以下でasciiでなければアイコンのみの可能性）
                    if len(cell_stripped) <= 2 and not cell_stripped.isascii():
                        pytest.fail(
                            f"Found icon-only industry cell: '{cell_stripped}' — should include text name"
                        )

    def test_sidebar_menu_items_are_japanese(self, admin_html):
        """サイドバーメニュー項目が日本語であること"""
        expected_ja = ['ダッシュボード', 'ユーザー管理', 'コース管理', 'Q&A管理']
        for item in expected_ja:
            assert item in admin_html, \
                f"Sidebar should contain Japanese menu item '{item}'"

    def test_admin_section_titles_are_japanese(self, admin_html):
        """管理画面の各セクションタイトルが日本語であること"""
        expected_titles = [
            '業種別 Q&A 閲覧状況',
            '人気の質問',
            '間違いが多い質問',
        ]
        for title in expected_titles:
            assert title in admin_html, \
                f"Admin dashboard should contain Japanese section title '{title}'"


# ==============================================================
# 横断テスト: i18n JSONキーの整合性
# ==============================================================
class TestI18nKeyConsistency:
    """3言語のJSONキー構造が完全一致すること"""

    def test_all_top_level_keys_match(self):
        """トップレベルキーが3言語で一致すること"""
        keys_by_lang = {}
        for lang in ['en', 'ja', 'vi']:
            data = load_ui_json(lang)
            keys_by_lang[lang] = set(data.keys())
        assert keys_by_lang['en'] == keys_by_lang['ja'], \
            f"en/ja top-level mismatch: en-only={keys_by_lang['en'] - keys_by_lang['ja']}, ja-only={keys_by_lang['ja'] - keys_by_lang['en']}"
        assert keys_by_lang['en'] == keys_by_lang['vi'], \
            f"en/vi top-level mismatch: en-only={keys_by_lang['en'] - keys_by_lang['vi']}, vi-only={keys_by_lang['vi'] - keys_by_lang['en']}"

    def test_all_nested_keys_match(self):
        """全てのネストされたキーが3言語で一致すること"""
        keys_by_lang = {}
        for lang in ['en', 'ja', 'vi']:
            data = load_ui_json(lang)
            keys_by_lang[lang] = get_all_keys(data)
        assert keys_by_lang['en'] == keys_by_lang['ja'], \
            f"en/ja key mismatch: en-only={keys_by_lang['en'] - keys_by_lang['ja']}, ja-only={keys_by_lang['ja'] - keys_by_lang['en']}"
        assert keys_by_lang['en'] == keys_by_lang['vi'], \
            f"en/vi key mismatch: en-only={keys_by_lang['en'] - keys_by_lang['vi']}, vi-only={keys_by_lang['vi'] - keys_by_lang['en']}"
