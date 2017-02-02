from astropy.table import Table
import numpy as np
import json

data = Table.read('ferengi2_metadata.csv')
manafest = []


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

# url_stub = "http://www.galaxyzoo.org.s3.amazonaws.com/subjects/ferengi_2"
url_stub = "http://s3.amazonaws.com/zooniverse-data/project_data/galaxy_zoo/ferengi_2"
for row in data:
    name = row['img_filename'].split('.')[0]
    r = {
        'type': 'subject',
        'group_name': 'ferengi_2',
        'group_type': 'survey',
        'coords': [row['RA'], row['DEC']],
        'location': {
            'standard': '{0}/Images/{1}.jpg'.format(url_stub, name),
            'inverted': '{0}/Inverted/{1}_inverted.jpg'.format(url_stub, name),
            'thumbnail': '{0}/Thumbnails/{1}_thumbnail.jpg'.format(url_stub, name)
        },
        'metadata': {
            'survey': 'Ferengi_2',
            'sdss_dr12_objid': str(row['dr12objid']),
            'retire_at': 40,
            'redshift': {
                'original': row['original_redshift'],
                'simulated': row['simulated_redshift']
            },
            'counters': {
                'feature': 0,
                'smooth': 0,
                'star': 0,
            }
        }
    }
    manafest.append(r)
fname = 'ferengi2_manifest.json'
with open(fname, 'w') as f:
    json.dump(manafest, f)
