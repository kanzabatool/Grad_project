from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from time import sleep
from bs4 import BeautifulSoup
import requests

chrome = webdriver.Remote(
          command_executor='http://localhost:4444/wd/hub',
          desired_capabilities=DesiredCapabilities.CHROME)


class OverViewParser:
    id = None
    url = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id="
    soup = ""
    overview_dict = dict()
    data_available = False


    def __init__(self, id="6261085"):
        self.id = id
        self.url = self.url+self.id
        end_point = self.url
        chrome.get(end_point)
        sleep(2)
        main_soup = BeautifulSoup(chrome.page_source, 'lxml')
        self.soup = main_soup
        self.check_if_snp()
        self.get_main_dict()

    def check_if_snp(self):
        if self.soup:
            try:
                if "has been flagged as a SNP" in self.soup.find('p', class_='quote').text:
                    self.data_available = False
            except:
                self.data_available = True

    def get_main_dict(self):
        if self.data_available:
            field_name = self.chops_main_table_returns_field_name()
            field_value = self.chops_main_table_returns_value()

            # This is our main dict
            dict_main_fields = dict(zip(field_name, field_value))

            self.overview_dict = self.put_everything_in_main_dict(value=dict_main_fields)

    def chops_main_table_returns_field_name(self):
        if self.data_available:
            # chops the main table that occurs on the top of the page. Very Necessary
            first_entry_table = self.soup.find('dl', class_='inline')
            try:
                # chops up the individual fields like Mutation ID, Gene name, AA mutation etc etc.
                field_name = [link.string for link in first_entry_table.find_all('dt')]
            except Exception as ex:
                raise Exception("Internet Connection is Down: Therefore: {}".format(ex))

            return field_name

    def chops_main_table_returns_value(self):
        if self.data_available:
            # chops up the individual values like COSM6261085, etc etc
            field_value = []
            first_entry_table = self.soup.find('dl', class_='inline')
            f_value = first_entry_table.find_all('dd')

            for fv in f_value:
                tmp_dict = dict()
                if fv.find_all('a'):
                    for fv_hrefs in fv.find_all('a'):
                        try:
                            tester_tag = fv_hrefs.contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                            tester_link = fv_hrefs['href']
                            tmp_dict[tester_tag] = tester_link
                        except:
                            pass
                    field_value.append(tmp_dict)
                else:
                    try:
                        data = fv.find_all('p')[0].text.replace('\n', ' ').strip(' ')
                        field_value.append(data)
                    except:
                        data = fv.text.replace('\n', ' ').strip(' ')
                        field_value.append(data)

            return field_value

    def put_everything_in_main_dict(self, value=None):
        if self.data_available and value:
            main_dict = dict()
            main_dict[self.soup.find('h2').text.replace('COSM', '')] = value

            return main_dict


class TissueDistributionParser(OverViewParser):
    tissue_distribution_dict = dict()

    def __init__(self, id="6261085"):
        super().__init__(id=id)
        self.set_tissue_distribution_dict()

    def set_tissue_distribution_dict(self):
        if self.data_available:
            all_tissues_even_odd = self.soup.find_all('div', class_='section-content')[2].find_all('tr', {"class": ["even", "odd"]})
            tmp_dict = dict()
            for all in all_tissues_even_odd:
                all_tissues = all.find_all('a')
                for tissues in all_tissues:
                    link = tissues['href']
                    if 'tissue' in link:
                        link_name = tissues.contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                        tmp_dict[link_name] = link

            self.tissue_distribution_dict = tmp_dict


class SampleParser(TissueDistributionParser):
    sample_dict = dict()

    def __init__(self, id="6261085"):
        super().__init__(id=id)
        self.set_sample_parser_dict()

    def set_sample_parser_dict(self):
        if self.data_available:
            field_values = self.chops_sample_table_returns_field_value()
            field_name = self.chop_sample_table_returns_field_name()

            dict_sample_fields = {k: field_values[i::len(field_name)] for i, k in enumerate(field_name)}

            self.sample_dict = dict_sample_fields

    def chops_sample_table_returns_field_value(self):
        if self.data_available:
            # chops up the individual values like CHG-13-09220T, etc etc
            field_value = []

            for f_even_odd in self.soup.find_all('div', class_='section-content')[2].find_all('tr', {"class": ["even", "odd"]}):
                f_value = f_even_odd.find_all('td')
                for fv in f_value:
                    tmp_dict = dict()
                    if fv.find_all('a'):
                        for fv_hrefs in fv.find_all('a'):
                            try:
                                tester_tag = fv_hrefs.contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                                tester_link = fv_hrefs['href']
                                tmp_dict[tester_tag] = tester_link
                            except:
                                tester_tag = fv_hrefs.contents[0].contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                                tester_link = fv_hrefs['href']
                                tmp_dict[tester_tag] = tester_link
                        field_value.append(tmp_dict)
                    else:
                        try:
                            data = fv.find_all('p')[0].text.replace('\n', ' ').strip(' ')
                            field_value.append(data)
                        except:
                            data = fv.text.replace('\n', ' ').strip(' ')
                            field_value.append(data)


            return field_value

    def chop_sample_table_returns_field_name(self):
        if self.data_available:
            # chops up the individual values like SAMPLE NAME, GENE NAME, etc etc
            field_name = []
            f_name = self.soup.find_all('div', class_='section-content')[2].find('tr').find_all('th')

            for fn in f_name:
                name = fn.contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                field_name.append(name)

            return field_name


class ReferenceParser(SampleParser):
    reference_dict = dict()

    def __init__(self, id="6261085"):
        super().__init__(id=id)
        self.set_reference_parser_dict()

    def set_reference_parser_dict(self):
        if self.data_available:
            field_values = self.chops_reference_table_returns_field_value()
            field_name = self.chop_reference_table_returns_field_name()

            dict_reference_fields = {k: field_values[i::len(field_name)] for i, k in enumerate(field_name)}

            self.reference_dict = dict_reference_fields

    def chops_reference_table_returns_field_value(self):
        if self.data_available:
            # chops up the individual values like CHG-13-09220T, etc etc
            field_value = []

            for f_even_odd in self.soup.find_all('div', class_='section-content')[2].find_all('tr', {"class": ["even", "odd"]}):
                f_value = f_even_odd.find_all('td')
                for fv in f_value:
                    tmp_dict = dict()
                    if fv.find_all('a'):
                        for fv_hrefs in fv.find_all('a'):
                            try:
                                tester_tag = fv_hrefs.contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                                tester_link = fv_hrefs['href']
                                tmp_dict[tester_tag] = tester_link
                            except:
                                tester_tag = fv_hrefs.contents[0].contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                                tester_link = fv_hrefs['href']
                                tmp_dict[tester_tag] = tester_link
                        field_value.append(tmp_dict)
                    else:
                        try:
                            data = fv.find_all('p')[0].text.replace('\n', ' ').strip(' ')
                            field_value.append(data)
                        except:
                            data = fv.text.replace('\n', ' ').strip(' ')
                            field_value.append(data)

            return field_value

    def chop_reference_table_returns_field_name(self):
        if self.data_available:
            # chops up the individual values like SAMPLE NAME, GENE NAME, etc etc
            field_name = []
            f_name = self.soup.find_all('div', class_='section-content')[3].find('tr').find_all('th')

            for fn in f_name:
                name = fn.contents[0].strip(' ').replace('\n', " ").replace(" ", "")
                field_name.append(name)

            return field_name


class Parser(ReferenceParser):
    main_dict = dict()

    def __init__(self, id="6261085"):
        super().__init__(id=id)
        self.main_dict['OverView'] = self.overview_dict
        self.main_dict['Tissue'] = self.tissue_distribution_dict
        self.main_dict['Sample'] = self.sample_dict
        self.main_dict['Reference'] = self.reference_dict


# p = Chopper(id=str(4745787))
# if p:
#     pass
