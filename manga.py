import json
import numpy as np
import os
import sys

from astropy.table import Table

metadata_path, s3_image_path, out_path = sys.argv[1:]

data = Table.read(metadata_path)
manifest = []

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

url_stub = (
    "http://s3.amazonaws.com/zooniverse-data/project_data/galaxy_zoo/{}"
).format(s3_image_path)

for row in data:
    name = str(row['dr8objid'])
    r = {
        'type': 'subject',
        'group_name': 'missing_manga',
        'group_type': 'survey',
        'coords': [row['ra'], row['dec']],
        'location': {
            'standard': '{0}/jpeg/{1}.jpeg'.format(url_stub, name),
            'inverted': '{0}/inverted/{1}.jpeg'.format(url_stub, name),
            'thumbnail': '{0}/thumbnail/{1}.jpeg'.format(url_stub, name)
        },
        'metadata': {
            'survey': 'missing_manga',
            'dr8objid': str(row['dr8objid']),
            'retire_at': 40,
            'counters': {
                'feature': 0,
                'smooth': 0,
                'star': 0,
            },
            'nsa_id': "nsa_{}".format(row['NSA_NSAID']),
            'MANGAID': str(row['MANGAID']),
            'NSA_Z': str(row['NSA_Z']),
            'petroR50_r': str(row['petroR50_r']),
            'petroR90_r': str(row['petroR90_r'])
        }
    }
    manifest.append(r)
with open(os.path.join(out_path, 'manifest.json'), 'w') as f:
    json.dump(manifest, f)
