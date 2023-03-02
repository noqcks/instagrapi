
class ExploreMixin:
    """ Helpers for the explore page """
    def get_explore_page(self):
        result = self.private_request("discover/topical_explore")
        return result

    def report_explore_media(self, media_pk: str):
        params = {
            'm_pk': media_pk,
        }
        result = self.private_request("discover/explore_report/", params=params)
        return result['explore_report_status'] == "OK"
