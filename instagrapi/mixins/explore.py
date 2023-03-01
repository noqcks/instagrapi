
class ExploreMixin:
    """ Helpers for the explore page """
    def get_explore_page(self):
        result = self.private_request("discover/topical_explore")
        return result
