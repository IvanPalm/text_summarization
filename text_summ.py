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

pdf_filename = "Adhikari et al. - 2020 - Importance and strength of environmental controllers of soil organic carbon changes with scale.pdf"
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

# Manual import of text for protected pdf
text_from_pdf = """In this study the capabilities ofseven multispectral and hyperspectral satellite imagers to estimate soil variables (clay, sand, silt and organic carbon content)were investigated using data from soil spectral libraries. Four current (EO-1 ALI and Hyperion, Landsat 8 OLI, Sentinel-2 MSI) and three forthcoming (EnMAP, PRISMA and HyspIRI) satellite imagers were compared. To this aim, two soil spectra datasets that simulated each imager were obtain- ed: (i) resampled spectra according to the specific spectral response and resolution of each satellite imager and (ii) resampled spectra with declared or actual noise (radiometric and atmospheric) added. Compared with those using full spectral resolution data, the accuracy ofPartial Least Square Regression (PLSR) predictive models gen- erally decreased when using resampled spectra. In the absence of noise, the performances of hyperspectral im- agers, in terms of Ratio of Performance to Interquartile Range (RPIQ), were generally significantly better than those ofmultispectral imagers. For instance the best RPIQfor sand estimation was obtained using EnMAP simu- lated data (2.56), whereas the outcomes gained using multispectral imagers varied from 1.56 and 2.28. The ad- dition of noise to the simulated spectra brought about a decrease of statistical accuracy in all estimation models, especially for Hyperion data. Although the addition of noise reduced the performance differences be- tween multispectral and hyperspectral imagers, the forthcoming hyperspectral imagers nonetheless provided the best RPIQvalues for clay (2.16–2.33), sand (2.10–2.17), silt (2.77–2.85) and organic carbon (2.48–2.51) esti- mation. To better understand the impact ofspectral resolution and signal to noise ratio (SNR) on the estimation of soil variables, PLSR models were applied to resampled and simulated spectra, iteratively increasing the band- width to: 10, 20, 40, 80 and 160 nm. Results showed that, for a bandwidth of 40 nm, i.e., a spectral resolution lower than that of current and forthcoming imagers, the estimation accuracy was very similar to that obtained with a higher spectral resolution. Forthcoming hyperspectral imagers will therefore improve the accuracy of soil variables estimation from bare soil imagery with respect to the results achievable by current hyperspectral and multispectral imagers, however this improvement is still too limited, to allow an accurate quantitative estimation of soil texture and SOC. This work provides useful indications about what could be expected, for the estimation ofthemost important soil var- iables, from the next generation of hyperspectral satellite imagers.
"""


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
