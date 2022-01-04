import json
from typing import List, Optional, Tuple
from unicodedata import normalize
from urllib.parse import unquote

import requests

from chalice import Chalice
from chalicelib import init_chars_repository
import parsel

app = Chalice(app_name='tibiawebscraping')
DBB = init_chars_repository()

# ---- VIEWS ----
@app.route('/char/{charname}', methods=['GET'])
def get_char_info(charname):
    if char_info := DBB.get_char_info(charname):
        return char_info

    r = requests.get(f'https://www.tibia.com/community/?name={charname}')
    if 'does not exist' in r.text:
        return {
            'statusCode': 404,
            'body': json.dumps(
                {
                    "success": False,
                    "reason": f"char <{charname}> doesn\'t exist."
                }, indent=4
            )
        }

    char_info = construct_char_info_text(
            extract_chartable_info(
                parsel.Selector(text=r.text))
    )
    DBB.insert_char_info(char_info)
    return json.dumps(char_info)

@app.route('/char/{charname}', methods=['POST'])
def insert_char_info(charname):
    i = get_char_info(unquote(charname))
    try:
        dict(i)
        if 'statusCode' in i:
            return {
                "success": False,
                "reason": f"char <{charname}> doesn\'t exist."
            }
        return {
                "success": False,
                "reason": f"char <{charname}> already inserted."
            }
    except ValueError:
        i = json.loads(i)
        DBB.insert_char_info(i)
        return {
            "success": True,
            "reason": f"info from <{i.get('Name')}> have been inserted."
        }

@app.route('/char/{charname}', methods=['DELETE'])
def delete_char_info(charname):
    DBB.delete_char_info(unquote(charname))
    return {
        "success": True,
        "reason": f"info from <{charname}> have been deleted"
    }

# ---- WEB SCRAPING CLEAN AND FILTER INFO FUNCTIONs ----

def extract_chartable_info(
        selector: parsel.selector.Selector
) -> Optional[parsel.selector.Selector]:

    for container in selector.xpath(
            '//table[@class="TableContent"]'
    ).getall():

        if 'Sex' in container:
            return parsel.Selector(container)

def construct_char_info_text(
        selector: parsel.selector.Selector
):

    texts = selector.xpath('//td//text()').getall()
    keys, values = separate_key_values(texts)
    values = mark_values_to_filter(values)
    values = clean_values(values)
    return dict(zip(keys, values))


def separate_key_values(texts: List[str]) -> Tuple[List, List]:
    keys, values = [], []
    flag = False
    for t in texts:
        if t.endswith(':') and '\n' not in t:
            keys.append(
                normalize('NFKD', t.strip(':')))
            flag = True
            continue
        if flag:
            values.append(normalize('NFKD', t))
            flag = False
        else:
            values.append(
                normalize('NFKD', '@!' + t))

    return keys, values

def mark_values_to_filter(values: List[str]) -> List[str]:
    reference = None
    for counter, value in enumerate(values):
        if value.startswith('@!'):
            if not reference:
                reference = counter - 1
            values[reference] += value.lstrip(
                '@!')
        else:
            reference = None

    return values

def clean_values(values: List[str]) -> List[str]:
    return [v for v in values if not v.startswith('@!')]
