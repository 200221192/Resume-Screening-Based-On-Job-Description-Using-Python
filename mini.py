import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template


from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# Open pdf file
pdfFileObj = open('C://xampp//htdocs//my_mini_project//Resume Folder//resume.pdf','rb')

# Read file
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# Get total number of pages
num_pages = pdfReader.numPages

# Initialize a count for the number of pages
count = 0

# Initialize a text empty string variable
text = ""

# Extract text from every page on the file
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

text = text.lower()

# Remove numbers
text = re.sub(r'\d+','',text)

# Remove punctuation
text = text.translate(str.maketrans('','',string.punctuation))
terms = {'Quality/Six Sigma':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                              'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                              'pdsa','performance improvement','process improvement','quality',
                              'quality circles','quality tools','root cause','six sigma',
                              'stability analysis','statistical analysis','tqm'],
        'Blockchain':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                 'machinery','maintenance','manufacture','line balancing','oee','operations',
                                 'operations research','optimization','overall equipment effectiveness',
                                 'pfmea','process','process mapping','production','resources','safety',
                                 'stoppage','value stream mapping','utilization'],
        'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                        'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                        'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                        'third party logistics','transport','transportation','traffic','supply chain',
                        'vendor','warehouse','wip','work in progress'],
        'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                              'finance','kanban','leader','leadership','management','milestones','planning',
                              'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                          'coding','data','database','data mining','data science','deep learning','hadoop',
                          'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                          'predictive','programming','python','r','sql','tableau','text mining',
                          'visualuzation'],
        'software engineer':['computer science knowledge','programming','codeing','APIs','software design','oracle',
                              'project management','planning','problem solving','collaboration','communication',
                              'mentoring','analysis'],
         'UIUX Designer':['UX','UXD','UI','IXD','sketching','agile','architecture','GUI','wireframe',
                          'application development','collaboration','sketch app','visual design','prototyping'],
        'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                      'health care','health','hospital','human factors','medical','near misses',
                      'patient','reporting system']
         }
quality = 0
block = 0
supplychain = 0
project = 0
data = 0
healthcare = 0
software = 0
UI = 0

# Create an empty list where the scores will be stored
scores = []

# Obtain the scores for each area
for area in terms.keys():

    if area == 'Quality/Six Sigma':
        for word in terms[area]:
            if word in text:
                quality += 1
        scores.append(quality)

    elif area == 'Operations management':
        for word in terms[area]:
            if word in text:
                block += 1
        scores.append(block)

    elif area == 'Supply chain':
        for word in terms[area]:
            if word in text:
                supplychain += 1
        scores.append(supplychain)

    elif area == 'Project management':
        for word in terms[area]:
            if word in text:
                project += 1
        scores.append(project)

    elif area == 'Data analytics':
        for word in terms[area]:
            if word in text:
                data += 1
        scores.append(data)

    elif area == 'software engineer':
        for word in terms[area]:
            if word in text:
                software += 1
        scores.append(software)

    elif area == 'UIUX Designer':
        for word in terms[area]:
            if word in text:
                UI += 1
        scores.append(UI)

    else:
        for word in terms[area]:
            if word in text:
                healthcare += 1
        scores.append(healthcare)
#print(scores)
row1=('Quality/Six Sigma','Blockchain','Supply chain','Project management','Data Analytics','software enginerr','UIUX Designer','Healthcare',scores[0],scores[1],scores[2],scores[3],scores[4],scores[5],scores[6],scores[7])
row = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
#print(row)
# Create pie chart visualization
pie = plt.figure(figsize=(10,10))
plt.pie(row['score'], labels=row.index, explode = (0.1,0,0,0,0,0,0,0), autopct='%1.0f%%',shadow=True,startangle=90)
plt.title('Industrial Engineering Candidate - Resume Decomposition by Areas')
plt.axis('equal')
#plt.show()


# Save pie chart as a .png file
#pie.savefig('resume_screening_results.png')

@app.route("/")
def hello_world():
    return render_template("mainpage.html",data=row1)

app.run("localhost", port=5000, debug=True)