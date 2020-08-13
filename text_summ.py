from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

# Set dir and filename
bibliodir = "/home/ivan/Documents/biblio/"
bibliodir_mendeley = "/home/ivan/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded/"

pdf_filename = "Zhang et al. - 2019 - Prediction of soil organic carbon based on Landsat 8 monthly NDVI data for the Jianghan Plain in Hubei Province, C.pdf"
page_range = [0]


# Import and read PDF file
def pdf_text_reader(pdf_file_name, pages=None):
    if pages:
        pagenums = set(pages)
    else:
        pagenums = set()

    ## 1) Initiate the Pdf text converter and interpreter
    textOutput = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, textOutput, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    ## 2) Extract text from file using the interpreter
    infile = open(pdf_file_name, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()

    ## 3) Extract the paragraphs and close the connections
    paras = textOutput.getvalue()
    converter.close()
    textOutput.close

    return paras

try:
    text_from_pdf = pdf_text_reader(bibliodir + pdf_filename, pages=page_range)
except:
    text_from_pdf = pdf_text_reader(bibliodir_mendeley + pdf_filename, pages=page_range)

# Summarize text
extra_words=list(STOP_WORDS)+list(punctuation)+['\n']
nlp=spacy.load('en')
doc = text_from_pdf
docx = nlp(doc)

all_words=[word.text for word in docx]
Freq_word={}
for w in all_words:
    w1=w.lower()
    if w1 not in extra_words and w1.isalpha():
        if w1 in Freq_word.keys():
            Freq_word[w1]+=1
        else:
            Freq_word[w1]=1

val=sorted(Freq_word.values())
max_freq=val[-3:]
print("Brief summary of given text:")
for word,freq in Freq_word.items():
      if freq in max_freq:
          print(word ,end=" ")
      else:
          continue

for word in Freq_word.keys():
       Freq_word[word] = (Freq_word[word]/max_freq[-1])

sent_strength={}
for sent in docx.sents:
    for word in sent :
        if word.text.lower() in Freq_word.keys():
            if sent in sent_strength.keys():
                sent_strength[sent]+=Freq_word[word.text.lower()]
            else:
                sent_strength[sent]=Freq_word[word.text.lower()]
        else:
            continue

top_sentences=(sorted(sent_strength.values())[::-1])
top30percent_sentence=int(0.3*len(top_sentences))
top_sent=top_sentences[:top30percent_sentence]

summary=[]
for sent,strength in sent_strength.items():
       if strength in top_sent:
          summary.append(sent)
       else:
          continue

for i in summary:
    print(i, end="")
