
from instagrapi import Client
import json
import re
from typing import List, Optional, Tuple, Set
from enum import Enum

cl = Client()
# cl.load_settings('/tmp/dump.json')
cl.login("USERNAME", "PASSWORD")
# cl.dump_settings('/tmp/dump.json')


class REPORT_REASON(Enum):
    REPORT_TAG_MATCHED = 1
    SEARCHED_TAG_MATCHED = 2
    HIGH_VIEWS_AND_NO_TAGS = 3
    HIGH_VIEWS_AND_NO_TEXT = 4

tags_to_report = ['#6ixbuzznews']
# explore_page = cl.get_explore_page()

# load json file explore.json
explore_page = json.load(open('explore.json'))

def extract_tags(text: str) -> Set[str]:
    words = text.split()
    tags = [word for word in words if word.startswith("#")]
    stripped_tags = set(map(lambda x: x[1:] if len(x) > 0 and x[0] == '#' else x, tags))
    return stripped_tags.union(set(tags))

def should_report(post: dict, report_tags: List[str] = []) -> Tuple[bool, Optional[REPORT_REASON]]:
    tags = extract_tags(post)
    if len(set(report_tags).intersection(tags)) > 0:
        return (True, REPORT_REASON.REPORT_TAG_MATCHED)

    for present_tag in tags:
        for searched_tag in report_tags:
            if re.search(present_tag, searched_tag):
                return (True, REPORT_REASON.SEARCHED_TAG_MATCHED)

    return (False, None)


for item in explore_page["sectional_items"]:
    if 'fill_items' in item["layout_content"]:
        for fill_item in item["layout_content"]["fill_items"]:
            media = fill_item["media"]
            if 'caption' not in media:
                continue
            caption = media["caption"]
            print(caption)
            if caption != None:
                should_report, reason = should_report(caption["text"], tags_to_report)
                if should_report:
                    print(f"Should report {media['id']}: {reason}")

    if 'one_by_two_item' in item["layout_content"]:
        for clip in item["layout_content"]["one_by_two_item"]["clips"]["items"]:
            media = clip["media"]
            if 'caption' not in media:
                continue
            caption = media["caption"]
            if caption != None:
                report, reason = should_report(caption["text"], tags_to_report)
                if report:
                    print(f"Should report {media['id']}: {reason}")
