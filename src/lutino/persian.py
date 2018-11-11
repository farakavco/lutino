# -*- coding: utf-8 -*-

_character_map = str.maketrans({
    'ي': 'ی',
    'ي': 'ی',
    'ى': 'ی',
    'ك': 'ک',
    'ة': 'ه',
    'ۀ': 'ه',
    'ؤ': 'و',
    'إ': 'ا',
    'أ': 'ا',
    'ء': '',
    'ّ': '',
    'ِ': '',
    'ُ': '',
    'َ': '',

    # Eastern Arabic-Indic digits (Persian and Urdu) U+06Fn: ۰۱۲۳۴۵۶۷۸۹
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',

    # Arabic-Indic digits: U+066n: ٠١٢٣٤٥٦٧٨٩
    '٠': '0',
    '١': '1',
    '٢': '2',
    '٣': '3',
    '٤': '4',
    '٥': '5',
    '٦': '6',
    '٧': '7',
    '٨': '8',
    '٩': '9',

})


def purify(s):
    return s.strip().translate(_character_map)


if __name__ == '__main__':
    sample_input = '  يكةۀ ۱۲۳۴'
    expected_output = 'یکهه 1234'

    assert purify(sample_input) == expected_output
    print('success')
