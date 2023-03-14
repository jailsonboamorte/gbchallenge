from app.spotify import get_podcasts
from pprint import pprint

pod_casts= get_podcasts()
pprint(pod_casts)