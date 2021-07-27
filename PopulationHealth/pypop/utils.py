import pandas as pd
import string
from collections import Counter

def get_chief_complaint_data():
    """"
    returns the raw chief complaints data as a Pandas DataFrame
    """
    return pd.read_csv("cc_only.txt", 
                       delimiter="\t",
                       header=None, 
                       usecols=[0]).rename(columns={0:"ChiefComplaint"})

def clean_punctuation(mystring, puncs):
    """ 
    clean_punctuation: takes a string and returns a string with all puncutations
    replaced with spaces

    mystring: a string
    puncs: a sequence containting characers to replace

    """
    newstring = mystring
    for p in puncs:
        newstring = newstring.replace(p, " ").lower().strip()
    return newstring

def get_cleaned_cfs(_cfs, puncs):
    """
    get_cleaned_cfs: takes a DataFrame with chief complaints and returns a 
    DataFrame with the original chief complaints and the cleaned chief complaints

    Args:

    _cfs: A DataFrame with chief complaints in a column named "ChiefComplaint"
    puncs: A sequence of characters to be replaced in the chief complaints

    Returns:

    new DataFrame with (at least) Columns "ChiefComplaint" and "CleanChiefComplaint"
    """
    cfs = _cfs.copy()
    cfs["CleanChiefComplaint"] = cfs.apply(lambda x: clean_punctuation(x["ChiefComplaint"], 
                                                                       string.punctuation),
                                                  axis=1)
    return cfs

def map_syndromes(_df, syndromes):
    """
    map_syndromes: Creates a new DataFrame with columns corresponding to syndromes

    Args:

    _df: a DataFrame containing a column "CleanChiefComplaint"
    _syndromes: A dictionary of syndrome labels and keywords

    Returns:

    A DataFrame with 1, 0 s
    """
    df = _df.copy()
    def _ms(s, terms):
        for t in terms:
            if t in s:
                return 1
        return 0
    for k,v in syndromes.items():
        df[k] = df.apply(lambda x: _ms(x["CleanChiefComplaint"], v), axis=1)
    return df

def get_syndrome_counts(cfs, syndromes):
    return pd.DataFrame.from_dict({k:cfs[k].sum() for k in syndromes.keys()}, 
                                  orient="index").rename(
                                          columns={0:"Counts"})

def get_sorted_df():
    df = get_chief_complaint_data()
    df = get_cleaned_cfs(df, string.punctuation)
    df["lcf"] = df.apply(lambda x: len(x["CleanChiefComplaint"]), axis=1)
    df = df.sort_values(["lcf"], ascending=False, ignore_index=True).reindex()
    return df

def get_word_counts(df):
    tmp = [xx for x in df["CleanChiefComplaint"] for xx in x.split() ]
    return pd.DataFrame.from_dict(Counter(tmp), orient="index").rename(columns={0:"Count"}).rename_axis("word")



