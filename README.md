# OWLSTORE script for indexing

## Before you start
Setup your environment first by running: 

    pip install -r requirements.txt

## Usage

    usage: owlstore.py [-h] --filename FILENAME [--password PASSWORD] [--indexfilename INDEXFILENAME] [--offset OFFSET] [--lope LOPE] [--cstw CSTW]

##### OwlStore creates a word index file from an encrypted or not encrypted PDF file.

##### options:
    -h, --help            show this help message and exit
    --filename FILENAME   The filepath of the PDF file.
    --password PASSWORD   The password of the file. Default value empty string.
    --indexfilename INDEXFILENAME
                        The index filename. Default value index.txt.
    --offset OFFSET       The offet of the pages not numbered in the pdf file. Default value 2.
    --lope LOPE           A list of pages that we want to exclude form the index . Default value [].
    --cstw CSTW           Filename of a list of custom stopwords. Default value list_of_context_specific_stopwords.txt

## Remarks 
To optimize your index add multiple times the script by adding each time the context specific stopwords to the ***list_of_context_specific_stopwords.txt*** file. 