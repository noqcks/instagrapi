import urllib
from instagrapi.extractors import (
    extract_i_dont_like_report_serialized_data
)

class ReportMixin:
    def report_post_i_dont_like(self, media_id: str):
        # step 1: get the serialized state data for reporting
        data = {
            "trigger_event_type": "ig_report_button_clicked",
            "trigger_session_id": self.generate_uuid(),
            "ig_container_module": "feed_timeline",
            "entry_point": "chevron_button",
            "preloading_enabled": "1",
            "ig_object_value": media_id,
            "ig_object_type": "1",
            "location": "ig_feed",
        }
        clicked_report_button = self.bloks_action(action='com.bloks.www.ig.ixt.triggers.bottom_sheet.ig_content', data=data, with_signature=False)
        serialized_data = extract_i_dont_like_report_serialized_data(clicked_report_button)

        # step 2: report the post
        params={
            "client_input_params":{
                "tags":["ig_i_dont_like_it_v3"]
            },
            "server_params":{
                "show_tag_search":1,
                "serialized_state":serialized_data,
                "is_bloks":1,
                "tag_source":"tag_selection_screen",

            }
        }
        data = urllib.parse.urlencode({'params': params})
        result = self.bloks_action_raw(action='com.bloks.www.instagram_bloks_bottom_sheet.ixt.screen.frx_tag_selection_screen', data=data, with_signature=False)
        print("====REPORT POST ACTION RESULT===")
        print(result)
        return result['status'] == 'ok'
