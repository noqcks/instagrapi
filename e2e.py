
from instagrapi import Client
import json
import re
from typing import List, Optional, Tuple, Set
from enum import Enum
from datetime import datetime

cl = Client()
cl.load_settings('/tmp/dump.json')
cl.login("USERNAME", "PASSWORD")
# cl.dump_settings('/tmp/dump.json')

tags_to_report = [
    "#architecture",
    "#interiordesigner",
    "#furnituredesign",
    "#homedesign",
    "#interiordesign",
    "#homedecor",
    "#apartmentdecor",
    "#bedroominspo",
    "#livingroomdecor"
]
tags_to_like = []
repeat_loop_amount = 5

class REPORT_REASON(Enum):
    REPORT_TAG_MATCHED = 1
    SEARCHED_TAG_MATCHED = 2
    HIGH_VIEWS_AND_NO_TAGS = 3
    HIGH_VIEWS_AND_NO_TEXT = 4


def extract_tags(text: str) -> Set[str]:
    words = text.split()
    tags = [word for word in words if word.startswith("#")]
    return set(tags)
    # stripped_tags = set(map(lambda x: x[1:] if len(x) > 0 and x[0] == '#' else x, tags))
    # return stripped_tags.union(set(tags))

def should_report(tags: Set[str], report_tags: List[str] = []) -> Tuple[bool, Optional[REPORT_REASON]]:
    if len(set(report_tags).intersection(tags)) > 0:
        return (True, REPORT_REASON.REPORT_TAG_MATCHED)

    for present_tag in tags:
        for searched_tag in report_tags:
            if re.search(present_tag, searched_tag):
                return (True, REPORT_REASON.SEARCHED_TAG_MATCHED)

    return (False, None)

def should_like(tags: Set[str], like_tags: List[str] = []) -> bool:
    return len(set(like_tags).intersection(tags)) > 0

def handle_media(media, tags_to_report, tags_to_like, analytics, do_actions):
    media_pk = media["id"].split("_")[0]
    caption = cl.media_info(media_pk).caption_text
    if caption is not None:
        tags = extract_tags(caption)
        # print("TAGS: ", tags)
        do_report, reason = should_report(tags, tags_to_report)
        if do_report and do_actions:
            print("REPORTING MEDIA: ", media["id"], " because: ", reason)
            cl.report_post_i_dont_like(media["id"])
            analytics["reported"] += 1
        do_like = should_like(tags, tags_to_like)
        if do_like and do_actions:
            print("LIKING MEDIA: ", media["id"])
            cl.media_like(media["id"])
            analytics["liked"] += 1
            analytics["liked_tags_seen"].append(extract_tags(caption))

        # update hashtags_seen_count
        for tag in tags:
            if tag in analytics["hashtags_seen_count"]:
                analytics["hashtags_seen_count"][tag] += 1
            else:
                analytics["hashtags_seen_count"][tag] = 1

def event_loop(do_actions = True):
    analytics = {
        "liked": 0,
        "reported": 0,
        "liked_tags_seen": [],
        "hashtags_seen": [],
        "hashtags_seen_count": {},
    }
    explore_page = cl.get_explore_page()
    for item in explore_page["sectional_items"]:
        layout_content = item["layout_content"]
        media_list = []
        if 'fill_items' in layout_content:
            media_list = layout_content["fill_items"]
        elif 'one_by_two_item' in layout_content:
            media_list = layout_content["one_by_two_item"]["clips"]["items"]
        for media_obj in media_list:
            print("ANALYZING  MEDIA: ", media_obj["media"]["id"])
            media = media_obj["media"]
            handle_media(media, tags_to_report, tags_to_like, analytics, do_actions)

    return analytics


print("====STARTING E2E API TESTS===")
print("TIME: ", datetime.now())
print("LOOP AMOUNT: ", repeat_loop_amount)
print("TAGS TO REPORT: ", tags_to_report)
print("TAGS TO LIKE: ", tags_to_like)
print("==============================")
print("== BEFORE RUN ANALYSIS == ")

before_analytics = event_loop(do_actions=False)
before_hashtags_seen_count = {tag: before_analytics["hashtags_seen_count"].get(tag, 0) for tag in tags_to_like}
print(before_analytics)
print("==============================")

for i in range(repeat_loop_amount):
    print("====RUNNING LOOP: ", i)
    analytics = event_loop()
    print(analytics)
    print("==============================")

print("== AFTER RUN ANALYSIS == ")
after_analytics = event_loop(do_actions=False)
after_hashtags_seen_count = {tag: after_analytics["hashtags_seen_count"].get(tag, 0) for tag in tags_to_like}

print(after_analytics)
print("==== HASHTAH COUNT DIFFERENCE")

hashtag_count_diff = {}

for hashtag in before_hashtags_seen_count:
    before_count = before_hashtags_seen_count[hashtag]
    after_count = after_hashtags_seen_count.get(hashtag, 0)
    count_diff = after_count - before_count
    if before_count > 0 and after_count == 0:
        count_diff = -1 * before_count
    elif before_count == 0 and after_count > 0:
        count_diff = after_count
    hashtag_count_diff[hashtag] = count_diff

for tag, count_diff in hashtag_count_diff.items():
    sign = "+" if count_diff > 0 else ""
    print(f"{tag}: {sign}{count_diff}")
print("==============================")
print("====FINISHED E2E API TESTS===")
