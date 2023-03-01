from instagrapi import Client

cl = Client()
# cl.load_settings('/tmp/dump.json')
cl.login("USERNAME", "PASSWORD")
# cl.dump_settings('/tmp/dump.json')

print(cl.report_post_i_dont_like("3048169374003022095_8396426917"))
