"""
CareerPath データ整合性テスト
- qa.json: 48問全件、構造、言語キー
- ui/*.json: キー一致、プレースホルダー整合
"""
import json
import os
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# ── fixtures ──

@pytest.fixture
def qa_data():
    with open(os.path.join(DATA_DIR, 'qa.json'), encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def ui_en():
    with open(os.path.join(DATA_DIR, 'ui', 'en.json'), encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def ui_ja():
    with open(os.path.join(DATA_DIR, 'ui', 'ja.json'), encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def ui_vi():
    with open(os.path.join(DATA_DIR, 'ui', 'vi.json'), encoding='utf-8') as f:
        return json.load(f)


# ── Q&A Tests ──

class TestQAData:
    def test_total_items(self, qa_data):
        """64問全部あること（業種別48問 + 共通16問）"""
        assert len(qa_data['items']) == 64

    def test_industry_counts(self, qa_data):
        """業種別の問題数が正しいこと"""
        counts = {}
        for item in qa_data['items']:
            counts[item['industry']] = counts.get(item['industry'], 0) + 1
        assert counts == {
            'food': 10,
            'manufacturing': 10,
            'construction': 10,
            'retail': 10,
            'hotel': 8,
            'common': 16,
        }

    def test_industries_metadata(self, qa_data):
        """industriesメタデータが5業種あること"""
        assert len(qa_data['industries']) == 5
        ids = [i['id'] for i in qa_data['industries']]
        assert set(ids) == {'food', 'manufacturing', 'construction', 'retail', 'hotel'}

    def test_industry_labels_have_all_langs(self, qa_data):
        """業種ラベルにja/en/viがあること"""
        for ind in qa_data['industries']:
            for lang in ['ja', 'en', 'vi']:
                assert lang in ind['label'], f"{ind['id']} missing label for {lang}"

    def test_each_item_has_required_fields(self, qa_data):
        """各Q&Aアイテムに必須フィールドがあること"""
        required = ['id', 'industry', 'question', 'model_answer', 'ng_example', 'tip']
        for item in qa_data['items']:
            for field in required:
                assert field in item, f"{item.get('id', '?')} missing {field}"

    def test_each_item_has_ja_question(self, qa_data):
        """各Q&Aの質問にjaがあること"""
        for item in qa_data['items']:
            assert item['question'].get('ja'), f"{item['id']} missing ja question"

    def test_each_item_has_en_question(self, qa_data):
        """各Q&Aの質問にenがあること"""
        for item in qa_data['items']:
            assert item['question'].get('en'), f"{item['id']} missing en question"

    def test_each_item_has_vi_question(self, qa_data):
        """各Q&Aの質問にviの翻訳が入っていること（空NG）"""
        for item in qa_data['items']:
            assert item['question'].get('vi'), f"{item['id']} has empty vi question"

    def test_each_item_has_vi_model_answer(self, qa_data):
        """各Q&Aの模範回答にviの翻訳が入っていること（空NG）"""
        for item in qa_data['items']:
            assert item['model_answer'].get('vi'), f"{item['id']} has empty vi model_answer"

    def test_each_item_has_vi_ng_example(self, qa_data):
        """各Q&AのNG例にviの翻訳が入っていること（空NG）"""
        for item in qa_data['items']:
            assert item['ng_example'].get('vi'), f"{item['id']} has empty vi ng_example"

    def test_unique_ids(self, qa_data):
        """IDが重複していないこと"""
        ids = [item['id'] for item in qa_data['items']]
        assert len(ids) == len(set(ids)), f"Duplicate IDs found: {[x for x in ids if ids.count(x) > 1]}"

    def test_id_format(self, qa_data):
        """IDがindustry-NN形式であること"""
        import re
        for item in qa_data['items']:
            assert re.match(r'^[a-z]+-\d{2}$', item['id']), f"Invalid ID format: {item['id']}"

    def test_model_answer_has_ja(self, qa_data):
        """模範回答にjaがあること"""
        for item in qa_data['items']:
            assert item['model_answer'].get('ja'), f"{item['id']} missing ja model_answer"

    def test_ng_example_has_ja(self, qa_data):
        """NG例にjaがあること"""
        for item in qa_data['items']:
            assert item['ng_example'].get('ja'), f"{item['id']} missing ja ng_example"

    def test_supported_languages(self, qa_data):
        """supported_languagesにja/en/viが含まれること"""
        assert set(qa_data['supported_languages']) == {'ja', 'en', 'vi'}

    def test_valid_industry_values(self, qa_data):
        """アイテムのindustryが定義済み業種またはcommonであること"""
        valid = {i['id'] for i in qa_data['industries']} | {'common'}
        for item in qa_data['items']:
            assert item['industry'] in valid, f"{item['id']} has invalid industry: {item['industry']}"


# ── UI Translation Tests ──

def get_all_keys(d, prefix=''):
    """JSON辞書のキーをフラットなドットパスで返す"""
    keys = set()
    for k, v in d.items():
        full = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys |= get_all_keys(v, full)
        else:
            keys.add(full)
    return keys


class TestUITranslations:
    def test_en_ja_keys_match(self, ui_en, ui_ja):
        """en.jsonとja.jsonのキーが完全一致すること"""
        en_keys = get_all_keys(ui_en)
        ja_keys = get_all_keys(ui_ja)
        missing_in_ja = en_keys - ja_keys
        missing_in_en = ja_keys - en_keys
        assert not missing_in_ja, f"Keys in en.json but not ja.json: {missing_in_ja}"
        assert not missing_in_en, f"Keys in ja.json but not en.json: {missing_in_en}"

    def test_en_vi_keys_match(self, ui_en, ui_vi):
        """en.jsonとvi.jsonのキーが完全一致すること"""
        en_keys = get_all_keys(ui_en)
        vi_keys = get_all_keys(ui_vi)
        missing_in_vi = en_keys - vi_keys
        missing_in_en = vi_keys - en_keys
        assert not missing_in_vi, f"Keys in en.json but not vi.json: {missing_in_vi}"
        assert not missing_in_en, f"Keys in vi.json but not en.json: {missing_in_en}"

    def test_no_empty_values_en(self, ui_en):
        """en.jsonに空の値がないこと"""
        empties = []
        def check(d, prefix=''):
            for k, v in d.items():
                full = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    check(v, full)
                elif isinstance(v, str) and not v.strip():
                    empties.append(full)
        check(ui_en)
        assert not empties, f"Empty values in en.json: {empties}"

    def test_no_empty_values_ja(self, ui_ja):
        """ja.jsonに空の値がないこと"""
        empties = []
        def check(d, prefix=''):
            for k, v in d.items():
                full = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    check(v, full)
                elif isinstance(v, str) and not v.strip():
                    empties.append(full)
        check(ui_ja)
        assert not empties, f"Empty values in ja.json: {empties}"

    def test_no_empty_values_vi(self, ui_vi):
        """vi.jsonに空の値がないこと"""
        empties = []
        def check(d, prefix=''):
            for k, v in d.items():
                full = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    check(v, full)
                elif isinstance(v, str) and not v.strip():
                    empties.append(full)
        check(ui_vi)
        assert not empties, f"Empty values in vi.json: {empties}"

    def test_placeholders_consistent(self, ui_en, ui_ja, ui_vi):
        """プレースホルダー({count}等)がen/ja/viで一致すること"""
        import re
        placeholder_re = re.compile(r'\{(\w+)\}')

        def get_placeholders(d, prefix=''):
            result = {}
            for k, v in d.items():
                full = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    result.update(get_placeholders(v, full))
                elif isinstance(v, str):
                    matches = set(placeholder_re.findall(v))
                    if matches:
                        result[full] = matches
            return result

        en_ph = get_placeholders(ui_en)
        ja_ph = get_placeholders(ui_ja)
        vi_ph = get_placeholders(ui_vi)

        mismatches = []
        for key, en_set in en_ph.items():
            if key in ja_ph and ja_ph[key] != en_set:
                mismatches.append(f"{key}: en={en_set}, ja={ja_ph[key]}")
            if key in vi_ph and vi_ph[key] != en_set:
                mismatches.append(f"{key}: en={en_set}, vi={vi_ph[key]}")
        assert not mismatches, f"Placeholder mismatches: {mismatches}"

    def test_json_valid(self):
        """全JSONファイルがvalidであること"""
        ui_dir = os.path.join(DATA_DIR, 'ui')
        for fname in os.listdir(ui_dir):
            if fname.endswith('.json'):
                path = os.path.join(ui_dir, fname)
                with open(path, encoding='utf-8') as f:
                    try:
                        json.load(f)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"{fname} is invalid JSON: {e}")

    def test_qa_json_valid(self):
        """qa.jsonがvalidであること"""
        path = os.path.join(DATA_DIR, 'qa.json')
        with open(path, encoding='utf-8') as f:
            try:
                json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"qa.json is invalid JSON: {e}")
