from collections import defaultdict, Counter

from main.models import Recipe


#
ALL_DOCUMENTS = set()

#
INDEX = defaultdict(set)

#
STATISTICAL_THESAURUS = defaultdict(set)


def build_index():
    """
    This function fetches recipes from database and indexes them to a global variable
    :return: None
    """
    global INDEX, ALL_DOCUMENTS

    for recipe_pk, words in Recipe.objects.values_list('pk', 'words'):
        for word in words:
            INDEX[word].add(recipe_pk)

        ALL_DOCUMENTS.add(recipe_pk)


def build_statistical_thesaurus():
    global INDEX, ALL_DOCUMENTS, STATISTICAL_THESAURUS

    # Find most common words. (Eliminate words that occur in 30% of the documents)
    common_words = set(word for word, docs in INDEX.items() if len(docs) > (len(ALL_DOCUMENTS) * 30/100))

    # Build the statistical-thesaurus by taking most relevant 3 words.
    for word1, docs1 in INDEX.items():
        count_dict = defaultdict(int)
        for word2, docs2 in INDEX.items():
            if word1 != word2 and word2 not in common_words:
                count_dict[word2] = len(docs1 & docs2)  # Intersect the document sets

        STATISTICAL_THESAURUS[word1] = set(i[0] for i in Counter(count_dict).most_common(3))
