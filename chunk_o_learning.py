__author__ = 'mrittha'
import unicodedata
import json
import wikipedia
import sentence_tagger


def get_paragraphs(section):
    """Given a list of lines, where each line is a paragraph
    transforms them into a list of lists, where each sublist represents a sentence"""
    paragraphs = []
    for line in section:
        if len(line.strip()) > 0:
            sentences = sentence_tagger.get_sentences(line)
            paragraphs.append(sentences)
    return paragraphs


def get_sections(text):
    """The sections portion of the wikipedia library doesn't seem to work,
    so this pulls out the sections"""
    sections = {}
    section_list = ['Summary']
    section = 'Summary'
    lines = text.split('\n')
    for line in lines:

        if line[-7:] == "Edit ==":
            section = line[3:-7]
            section_list.append(section)
        elif line[-8:] == "Edit ===":
            section = line[4:-8]
            section_list.append(section)
        elif line[-9:] == "Edit ====":
            section = line[5:-9]
            section_list.append(section)
        elif line[-4:] == "====":
            section = line[4:-4]
            section_list.append(section)
        elif line[-3:] == "===":
            section = line[3:-3]
            section_list.append(section)
        elif line[-2:] == "==":
            section = line[2:-2]
            section_list.append(section)
        else:
            sections[section] = sections.get(section, []) + [line]
    for s in section_list:
        sections[s] = get_paragraphs(sections[s])
    return sections, section_list


def get_paragraphs(section):
    """Given a list of lines, where each line is a paragraph
    transforms them into a list of lists, where each sublist represents a sentence"""
    paragraphs = []
    for line in section:
        if type(line) is list:
            line = ' '.join(line)
        if len(line.strip()) > 0:
            sentences = sentence_tagger.get_sentences(line)
            paragraphs.append(sentences)
    return paragraphs


def update_chunk(chunk):
    chunk_file = "subjects/" + chunk['subject'].replace(' ', '_').lower() + '.json'
    with open(chunk_file, 'w') as f:
        f.write(json.dumps(chunk, sort_keys=True, indent=2))


def make_chunk(article, subject):
    text = unicodedata.normalize('NFKD', article.content).encode('ascii', 'replace')
    sections, section_list = get_sections(text)
    chunk = {}
    chunk['subject'] = subject
    chunk['section_list'] = section_list
    chunk['sections'] = {}
    for section in section_list:
        new_section = {}
        new_section['title'] = section
        new_section['full_title'] = article.title + ":" + section
        new_section['score'] = 0.0
        new_section['paragraphs'] = sections[section]
        chunk['sections'][section] = new_section
    update_chunk(chunk)
    return chunk


if __name__ == "__main__":
    suggestions = wikipedia.search('knot theory')
    print suggestions
    article = wikipedia.page(suggestions[0])
    a_chunk = make_chunk(article, suggestions[0])
    print json.dumps(a_chunk, sort_keys=True, indent=2)
