import argparse
class Merger:

    def __init__(self, list_of_index_files,pdf_names,mergedindexname):
        self.list_of_files=list_of_index_files
        self.pdf_names=pdf_names
        self.mergedindexfilename =mergedindexname

    def _read_data(self):
        indexfiles= {}
        for counter in range(len(self.list_of_files)):
            with open(self.list_of_files[counter],'r') as filedata:
                indexfiles[pdfnames[counter]] = filedata.readlines()
        return indexfiles

    def _get_indexer_dict(self,indexfile):
        index_dict={}
        for line in indexfile:
            index_dict[line.split('----')[0].strip()]=line.split('----')[1].strip()
        return  index_dict

    def _merge_indexes(self,indexfiles):
        merged_indexer={}
        keys = indexfiles.keys()
        for key1 in keys:
            index_dict=self._get_indexer_dict(indexfiles[key1])
            for word in index_dict.keys():
                if word not in merged_indexer.keys():
                    merged_indexer[word]=[]
                    merged_indexer[word].append((key1,index_dict[word]))
                else:
                    merged_indexer[word].append((key1, index_dict[word]))
        return merged_indexer

    def _sort_index(self, mergedindex):
        return dict(sorted(mergedindex.items()))

    def _write_to_file(self, mergedindex):
        with open(self.mergedindexfilename, 'a') as indexfile:
            for key in mergedindex.keys():
                indexfile.write("{}                   ----                {}\n".format(key, mergedindex[key]))

    def _printify(self, mergedindex):
        for key in mergedindex.keys():
            print("{}                   ----                {}".format(key, mergedindex[key]))

    def main(self):
        indexfiles=self._read_data()
        mergedindex=self._merge_indexes(indexfiles)
        self._printify(mergedindex)
        self._write_to_file(mergedindex)


def run(list_of_index_files,pdf_names,mergedindexname):
    if len(list_of_index_files)==len(pdf_names):
        merger = Merger(list_of_index_files,pdf_names,mergedindexname)
        merger.main()
    else:
        print("The pdf filenames are not equal to index files")

if __name__ =="__main__":
    parser = argparse.ArgumentParser(
        description="OwlStoreMerger merges index files created by Owlstore")
    parser.add_argument("--filenames", required=True, type=str, help="The filepaths of the PDF file in form of list.")
    parser.add_argument("--pdfnames", required=True, type=str,
                        help="The list of pdf names assocaited with the index files in the same order.")
    parser.add_argument("--mergedindexfilename", required=False, type=str,
                        help="The merged index filename. Default value mergredindex.txt.")
    args = parser.parse_args()
    filenames = args.filenames.split(',')
    pdfnames = args.pdfnames.split(',')
    if args.mergedindexfilename:
        mergedindexfilename = args.mergedindexfilename
    else:
        mergedindexfilename = "mergedindex.txt"
    run(filenames, pdfnames, mergedindexfilename)
