"""Check Japanese catalogue coverage and runtime placeholders without Android tools."""
import json
import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'app/src/main'

class JapaneseResources(unittest.TestCase):
    def test_android_resources_and_format_arguments(self):
        source = {x.attrib['name']: x for x in ElementTree.parse(MAIN/'res/values/strings.xml').getroot()}
        translated = {x.attrib['name']: x for x in ElementTree.parse(MAIN/'res/values-ja/strings.xml').getroot()}
        required = {k for k,v in source.items() if v.attrib.get('translatable') != 'false'}
        self.assertTrue(required <= translated.keys(), sorted(required-translated.keys()))
        for key, element in translated.items():
            with self.subTest(key=key):
                self.assertIn(key, source)
                args = lambda e: re.findall(r'%(?:\d+\$)?[dsf]', ''.join(e.itertext()))
                original_args = args(source[key])
                if element.tag == 'plurals':
                    original_args = list(set(original_args))
                    self.assertTrue(any(x.attrib.get('quantity') == 'other' for x in element))
                self.assertEqual(sorted(original_args), sorted(args(element)))
                if element.tag == 'string-array':
                    self.assertEqual(len(source[key]), len(element))

    def test_source_catalogues_and_placeholders(self):
        for source_name, translated_name in [('en','ja'), ('own_en','own_ja')]:
            source = json.loads((MAIN/f'assets/sources/i18n/{source_name}.json').read_text())
            translated = json.loads((MAIN/f'assets/sources/i18n/{translated_name}.json').read_text())
            self.assertEqual(source.keys(), translated.keys())
            for key, original in source.items():
                with self.subTest(catalogue=translated_name,key=key):
                    actual = translated[key]
                    self.assertIsInstance(actual, type(original))
                    if isinstance(actual,str):
                        self.assertTrue(actual.strip())
                        self.assertEqual(original.count('{}'), actual.count('{}'))
                    else:
                        self.assertIn('other', actual)
                        for quantity, text in actual.items():
                            self.assertEqual(original.get(quantity,original['other']).count('{}'),text.count('{}'))

    def test_japanese_can_be_selected_in_both_interfaces(self):
        languages = (MAIN/'java/io/github/bl3xand/apkcloner/settings/AppLanguage.kt').read_text()
        environment = (MAIN/'java/io/github/bl3xand/apkcloner/sources/data/SourcesEnvironment.kt').read_text()
        self.assertIn('JAPANESE("ja", "日本語")', languages)
        self.assertIn('"ja" -> "ja"', environment)
        config = ElementTree.parse(MAIN/'res/xml/locales_config.xml').getroot()
        self.assertIn('ja', [x.attrib['{http://schemas.android.com/apk/res/android}name'] for x in config])

    def test_shown_onboarding_and_settings_have_japanese_explanations(self):
        catalogue = {x.attrib['name']: ''.join(x.itertext()) for x in ElementTree.parse(MAIN/'res/values-ja/strings.xml').getroot()}
        for key in ['access_title','access_description','install_access_title','install_access_description','settings_check_updates_description','settings_check_on_start_description','settings_check_clones_description']:
            self.assertRegex(catalogue[key],r'[ぁ-んァ-ヶ一-龯]')

if __name__ == '__main__':
    unittest.main()
