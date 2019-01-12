from gene_parser import Parser
from vcf_reader import VCFReader
import time
import json
from jinja2 import Environment, FileSystemLoader

import os
dirname, filename = os.path.split(os.path.abspath(__file__))




class Handler:
    sorted_list_reference = []

    def __init__(self, caching=False):
        # Total Time Starts
        total_start_time = time.time()

        # Call for loading VCF
        vcf_reader_start_time = time.time()
        vcf_reader_cos_id = self.load_vcf()
        vcf_reader_end_time = time.time()

        if vcf_reader_cos_id:
            pass

        vcf_reader_cos_id = self.omit_ids_already_checked(vcf_reader_cos_id)

        # Call for Parsing
        parsing_start_time = time.time()
        list_of_dicts = self.start_parsing(vcf_reader_cos_id, caching)
        parsing__stop_time = time.time()

        # Total Time Stops
        total_stop_time = time.time()

        if caching:
            print("--- CACHED RESULT = YES ---")
        print("--- VCF TIME %s seconds ---" % (vcf_reader_end_time - vcf_reader_start_time))
        print("--- PARSER TIME %s seconds ---" % (parsing__stop_time - parsing_start_time))
        print("--- TOTAL TIME %s seconds ---" % (total_stop_time - total_start_time))

        sorted_list_fathmm = self.sort_with_fathmm(list_of_dicts)
        sorted_list_reference = self.sort_with_reference(sorted_list_fathmm[:20])

        if sorted_list_reference:
            self.sorted_list_reference = sorted_list_reference

        self.save_sorted()

    def save_sorted(self):
        with open(dirname + '/cached/sorted_output.json', 'w') as outfile:
            json.dump(self.sorted_list_reference, outfile)

    @staticmethod
    # Check if cached result is there? if Yes then use it else create it.
    def load_vcf():
        try:
            with open(dirname+'/cached/vcf.json', 'r') as input_file:
                vcf_reader_cos_id = json.loads(input_file.read())

        except:
            vcf_reader = VCFReader(file='outputSiftSymtabLAGFC_HGVSc_SOMATIC.vcf', limit=0)
            vcf_reader_cos_id = vcf_reader.COS_ID

            with open(dirname+'/cached/vcf.json', 'w') as outfile:
                json.dump(vcf_reader_cos_id, outfile)

        return vcf_reader_cos_id

    @staticmethod
    def cached_results():
        with open(dirname + '/cached/parsed_output.json', 'r') as input_file:
            parsed_data = json.loads(input_file.read())

        return parsed_data

    def start_parsing(self, vcf_reader_cos_id, caching=False):
        # Start parsing
        if caching:
            return self.cached_results()

        list_of_dicts = []
        for id in vcf_reader_cos_id:
            try:
                parsed_data = Parser(id=str(id))
                if parsed_data.data_available:
                    self.save_delta_output(parsed_data.main_dict)
            except:
                print('error occured for {}'.format(id))
                pass

        return list_of_dicts

    @staticmethod
    def save_delta_output(parsed_data_dict):
        try:
            with open(dirname+'/cached/parsed_output.json', 'r') as input_file:
                parsed_data = json.loads(input_file.read())

            parsed_data.append(parsed_data_dict)

            with open(dirname+'/cached/parsed_output.json', 'w') as outfile:
                json.dump(parsed_data, outfile)
        except:
            tmp_list = []
            tmp_list.append(parsed_data_dict)
            with open(dirname+'/cached/parsed_output.json', 'w') as outfile:
                json.dump(tmp_list, outfile)

    @staticmethod
    def save_complete(list_of_dicts):
        try:
            with open(dirname+'/cached/parsed_output.json', 'w') as outfile:
                json.dump(list_of_dicts, outfile)
        except:
            pass

    @staticmethod
    def omit_ids_already_checked(vcf_reader_cos_id):
        try:
            with open(dirname+'/cached/parsed_output.json', 'r') as input_file:
                parsed_output = json.loads(input_file.read())

            parsed_output_ids = [list(i['OverView'].keys()) for i in parsed_output]
            parsed_output_ids = [ item for sub in parsed_output_ids for item in sub ]

            vcf_reader_cos_id = list(set(vcf_reader_cos_id) - set(parsed_output_ids))
            return vcf_reader_cos_id
        except:
            return vcf_reader_cos_id

    @staticmethod
    def sort_with_fathmm(list_of_dicts):
        # float(list_of_dicts[0]['OverView']['5484386']['FATHMM prediction'].split('score')[1][:-1].strip(' '))
        tmp_list = []
        for dicts in list_of_dicts:
            for key, value in dicts['OverView'].items():
                try:
                    dicts['prediction_score'] = float(value['FATHMM prediction'].split('score')[1][:-1].strip(' '))
                except:
                    dicts['prediction_score'] = float(0)

                tmp_list.append(dicts)

        new_list = sorted(tmp_list, key=lambda k:k['prediction_score'], reverse=True)

        if new_list:
            return new_list

    @staticmethod
    def sort_with_reference(list_of_dicts):
        # float(list_of_dicts[0]['OverView']['5484386']['FATHMM prediction'].split('score')[1][:-1].strip(' '))
        tmp_list = []
        for dicts in list_of_dicts:
            try:
                dicts['reference_score'] = len(dicts['Reference']['ReferenceTitle'])
            except:
                dicts['reference_score'] = float(0)

            tmp_list.append(dicts)

        new_list = sorted(tmp_list, key=lambda k: k['reference_score'], reverse=True)

        if new_list:
            return new_list


def main():
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    from time import sleep
    from bs4 import BeautifulSoup
    import requests

    chrome = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)

    handler = Handler(caching=True)
    sorted_list = handler.sorted_list_reference
    sorted_ids = [list(x['OverView'].keys())[0] for x in sorted_list]
    sorted_ids = sorted_ids[:10]

    i = 0
    soups = []
    for id in sorted_ids:
        end_point = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id="+id
        chrome.get(end_point)
        sleep(2)
        main_soup = BeautifulSoup(chrome.page_source, 'lxml')

        #Decompose
        if i>0:
            for script in main_soup.find_all('script'):
                script.decompose()

        try:
            main_soup.find('section', {'id': 'ccc'}).decompose()
        except:
            pass

        main_soup.find('h1', {'class': 'subhead'}).decompose()
        main_soup.find('footer').decompose()
        main_soup.find('header').decompose()
        main_soup.find('ul', {'class': 'slimmenu'}).decompose()
        for div in main_soup.find_all('div', {'class': 'dataTables_length'}):
            div.decompose()

        for div in main_soup.find_all('div', {'class': 'dataTables_filter'}):
            div.decompose()

        for img in main_soup.find_all('img'):
            img.decompose()

        soups.append(main_soup)
        i = i + 1

    file_loader = FileSystemLoader(dirname + '/output/templates')
    env = Environment(loader=file_loader)

    template = env.get_template('index.html')
    output = template.render(mutations=soups)

    if output:
        pass

if __name__ == "__main__":
    main()
