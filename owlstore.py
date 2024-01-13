from pypdf import PdfReader
import re
import pandas as pd
import nltk
from nltk.tokenize import WordPunctTokenizer, word_tokenize

nltk.download('stopwords')
from nltk.corpus import stopwords

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
import argparse


class PageHandler:

    def __init__(self, page, pagenumber, offset, custom_stopwords):
        self.page = page
        self.text = self.page.extract_text()
        self.pagenumber = pagenumber
        self.offset = offset
        self.custom_stopwords = custom_stopwords

    def _get_text_tokens(self):
        return WordPunctTokenizer().tokenize(self.text)

    def _clean_text_tokens(self, data):
        clean_token = []
        for token in data:
            token = token.lower()
            # remove any value that are not alphabetical
            new_token = re.sub(r'[^a-zA-Z]+', '', token)
            # remove empty value and single character value
            if new_token != "" and len(new_token) >= 2:
                vowels = len([v for v in new_token if v in "aeiou"])
                if vowels != 0:  # remove line that only contains consonants
                    clean_token.append(new_token)
        return clean_token

    def _remove_stopwords(self, data):
        # Get the list of stop words
        stop_words = stopwords.words('english')
        # add new stopwords to the list
        stop_words.extend(["could", "though", "would", "also", "many", 'much'])
        stop_words.extend(self.custom_stopwords)
        # Remove the stopwords from the list of tokens
        tokens = [x for x in data if x not in stop_words]
        return tokens

    def get_page_index(self):
        data = self._get_text_tokens()
        clean_data = self._clean_text_tokens(data)
        listofwords = self._remove_stopwords(clean_data)
        pagenumber = self.pagenumber - self.offset + 1
        page_index = {}
        for word in listofwords:
            page_index[word] = pagenumber
        return page_index


class Reader:

    def __init__(self, filename, password=""):
        self.filename = filename
        self.password = password
        self.reader = PdfReader(stream=self.filename, password=self.password)

    def read_pdf_file(self):
        if self.reader.is_encrypted:
            self.reader.decrypt(self.password)
        index = 0
        indexed_pages = {}
        for page in self.reader.pages:
            indexed_pages[index] = page
            index = index + 1
        return indexed_pages


class IndexFactory:

    def __init__(self, filename, password="", customstopwords="", indexfilename="index.txt", list_of_pages_excluded=[],
                 offset=2):
        self.reader = Reader(filename, password=password)
        self.pages = self.reader.read_pdf_file()
        self.offset = offset
        self.custom_stopwords = self._read_custom_stop_words(customstopwords)
        self.indexfilename = indexfilename
        self.list_of_pages_exluded = list_of_pages_excluded

    def _read_custom_stop_words(self, path):
        with open(path, 'r') as words:
            stopwords = [word.rstrip() for word in words.readlines()]
        return stopwords

    def _extract_page_index(self, page, pagenumber):
        pagehandler = PageHandler(page, pagenumber, self.offset, self.custom_stopwords)
        return pagehandler.get_page_index()

    def _create_index(self):
        bookindex = {}
        for pagenumber in self.pages.keys():
            pageindex = self._extract_page_index(self.pages[pagenumber], pagenumber)
            for word in pageindex.keys():
                if pageindex[word] > 0:
                    if pageindex[word] not in self.list_of_pages_exluded:
                        if word not in bookindex.keys():
                            bookindex[word] = []
                            bookindex[word].append(pageindex[word])
                        else:
                            bookindex[word].append(pageindex[word])

        return self._sort_index(bookindex)

    def _sort_index(self, bookindex):
        return dict(sorted(bookindex.items()))

    def _write_to_file(self, bookindex):
        with open(self.indexfilename, 'a') as indexfile:
            for key in bookindex.keys():
                indexfile.write("{}                   ----                {}\n".format(key, bookindex[key]))

    def _printify(self, bookindex):
        for key in bookindex.keys():
            print("{}                   ----                {}".format(key, bookindex[key]))

    def main(self):
        bookindex = self._create_index()
        self._printify(bookindex)
        self._write_to_file(bookindex)


def run(filename, password, indexfilename, offset, lope, cstw):
    indexfactory = IndexFactory(filename=filename, password=password, indexfilename=indexfilename,
                                customstopwords=cstw, list_of_pages_excluded=lope, offset=offset)
    indexfactory.main()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="OwlStore creates a word index file from an encrypted or not encrypted PDF file.")
    parser.add_argument("--filename", required=True, type=str, help="The filepath of the PDF book")
    parser.add_argument("--password", required=False, type=str, help="The password of the file. Default value empty")
    parser.add_argument("--indexfilename", required=False, type=str, help="The index filename. Default value index.txt")
    parser.add_argument("--offset", required=False, type=int,
                        help="The offet of the pages not numbered in the pdf file. Default value 2")
    parser.add_argument("--lope", required=False, type=list,
                        help="A list of pages that we want to exclude form the index . Default value []")
    parser.add_argument("-cstw", required=False, type=str, help="Filename of a list of custom stopwords")
    args = parser.parse_args()
    filename = args.filename
    if args.password:
        password = args.password
    else:
        password = ""
    if args.indexfilename:
        indexfilename = args.indexfilename
    else:
        indexfilename = "index.txt"
    if args.offset:
        offset = args.offset
    else:
        offset = 2
    if args.lope:
        lope = args.lope
    else:
        lope = []
    if args.cstw:
        cstw = args.cstw
    else:
        cstw = "list_of_context_specific_stopwords.txt"
    run(filename,password,indexfilename,offset,lope,cstw)
