import re
from urllib.request import urlopen
import os

here = os.path.dirname(os.path.abspath(__file__))


class VCFReader:
    file_name = ""
    service_url = ""
    mutation_url = ""
    ID = []
    URL = []
    file_handler = None
    cosmic_id_list = []
    COS_ID = None
    mutation_urls = None
    limit = None

    def __init__(self, file=None, limit=900):
        if file:
            self.file_name = os.path.join(here, file)
            self.limit = limit
            self.service_url = 'https://clinicaltables.nlm.nih.gov/api/cosmic/v3/search?terms='
            self.mutation_url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?id='
            self.file_handler = open(self.file_name)

            self.get_id()
            self.make_urls()
            self.set_cosmic_ids()
            self.get_overview_ids_list()

    def get_overview_ids_list(self):
        return self.COS_ID

    def get_id(self):
        chunks = []
        for line in self.file_handler:
            line = line.strip()
            data = re.findall('[a-z]\s([A-Z].*)\s[a-z-].*:([a-z].+>[A-Z])', line)
            if data:
                chunks.append(data)

        self.file_handler.close()

        for c in chunks:
            for iterator in c:
                self.ID.append(iterator)

    def make_urls(self):
        for i in range(len(self.ID) - self.limit):
            a = self.service_url + self.ID[i][0] + '+' + self.ID[i][1]
            self.URL.append(a)

            self.URL = [s.replace('>', '%3E') for s in self.URL]

    def set_cosmic_ids(self):
        for url in self.URL:
            content = urlopen(url)
            cosmic_id = content.read()
            if cosmic_id != b'[0,[],null,[]]':
                self.cosmic_id_list.append(cosmic_id.decode())

        # Regex all the COSMIC IDs
        y = re.findall('COSM([0-9]{7})', str(self.cosmic_id_list))

        # Retain only unique IDs
        self.COS_ID = list(set(y))


