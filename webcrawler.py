# Import libraries
import requests
from bs4 import BeautifulSoup
import os

class SustainabilityReportDownloader:
    # URL from which pdfs to be downloaded
    base_url = "https://www.responsibilityreports.com"
    company_base_url = base_url + "/Companies?search="
    search_link = '/Company/'
    pdfs_dir = "./companies"
    url = None
    company_name = None
    pdfs_path = None

    def __init__(self, company_name):
        self.company_name = company_name
        self.url = self.company_base_url + company_name
        self.pdfs_company_dir = self.pdfs_dir + "/" +  company_name + "/"
        self.mkdir(self.pdfs_dir)
        self.mkdir(self.pdfs_company_dir)
    
    def mkdir(self, dir_path):  
        # Check whether the specified path exists or not
        does_exist = os.path.exists(dir_path)
        if not does_exist:
            # Create a new directory because it does not exist
            os.makedirs(dir_path)

    def parse_company_link(self, link):
        link_href = link.get('href', [])
        if (self.search_link in link_href):
            return link_href
        return None
            
    def download_pdf(self, link):
        link_href = link.get('href', [])
        if ('.pdf' in link_href):                        
            parts = link_href.split('/')
            pdf_name = parts[-1]

            pdf_url = self.base_url + link_href
            # Get response object for link
            response = requests.get(pdf_url)
        
            # Write content in pdf file
            pdf_filename = self.pdfs_company_dir + self.company_name + "_" + pdf_name
            print(pdf_filename)
            pdf = open(pdf_filename, 'wb')
            pdf.write(response.content)
            pdf.close()

    def get_links_from_page(self, url):
        response = requests.get(url)
        # Parse text obtained
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all hyperlinks present on webpage
        links = soup.find_all('a')

        return links

    def call_company_api(self):
        links = self.get_links_from_page(self.url)
        # From all links check for pdf link and
        # if present download file
        company_href = None
        for link in links:
            company_href = self.parse_company_link(link)
            if company_href:
                break
        
        company_url = self.base_url + company_href
        company_links = self.get_links_from_page(company_url)

        for company_link in company_links:
            self.download_pdf(company_link)
            
def download_companies(companies):
    for co in companies:
        report_downloader = SustainabilityReportDownloader(co)
        report_downloader.call_company_api()

def main():
    bad_companies = ["chevron", "vistra energy", "southern company", "exxon mobil", "duke energy"]
    good_companies = ["microsoft", "schnitzer", "clif bar", "apple", "duke energy"]

    download_companies(bad_companies)
    download_companies(good_companies)

if __name__ == "__main__":
    main()