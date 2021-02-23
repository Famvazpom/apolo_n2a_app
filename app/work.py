import pandas as pd
import os
import textract
import re
import numpy as np
import PyPDF2

def search_data(page,maxpages,pdfReader):
    import re
    if page > maxpages:
        return 
    pageObj = pdfReader.getPage(page)
    text = pageObj.extractText()
    clavereg = r'[A-Z]{2}[0-9]{4}'
    cicloreg = re.search(r'[1-4] - [1-4]',text)
    if cicloreg:
        ciclo = text[cicloreg.start():cicloreg.end()]
        clave = re.findall(clavereg,text[cicloreg.end():])[0]
        ind = re.search(clave, text).end()
        creditos = text[ind]
        return clave,creditos

    else:
        return search_data(page+1,maxpages,pdfReader)

if 
directorios = {}
palabras = {}
values = {}
ocurrencia = {}
df_unicas = pd.DataFrame(columns=['archivo','palabras'])
df_datos = pd.DataFrame(columns=['Ciclo','Materia','Clave','Creditos'])

# Obtencion de los subdirectorios
root = 'app/bd'
for name in os.listdir(root):
    name = os.path.join(root, name)
    directorios[name] = []        

for i in directorios.keys():
    for root,dirs,files in os.walk(i):
        for file in files:
            if file not in directorios[i] :
                directorios[i].append(file)




for ciclo in directorios.keys():
    total = 0
    for materia in directorios[ciclo]:
        print('Procesando: ',materia)
        text = textract.process(os.path.join(ciclo,materia)).decode('utf-8')
        words = re.findall(r"[^\W0-9_]+", text, re.MULTILINE) # Lista de palabras
        total += len(words)
        palabras[materia] = np.array(words)
    values[ciclo] = total

palabras_ciclo = pd.DataFrame(values.items(),columns=['Ciclo','Palabras totales'])


for i in directorios.keys():
    for j in directorios[i]:
        for word in palabras[j]:
            ocurrencia[i,word] = ocurrencia.get((i,word),0) + 1
ocurrencias = pd.DataFrame.from_dict(ocurrencia, orient='index')
ocurrencias = ocurrencias.rename(columns={'0': 'Ocurrencia'})
sortd = ocurrencias.sort_values(0,ascending=False)


for i in palabras.keys():
    val = np.unique(palabras[i])
    df_unicas = df_unicas.append({'archivo': i, 'palabras':val},ignore_index=True)



for ciclo in directorios.keys():
    for file in directorios[ciclo]:
        pdfFileObj = open(os.path.join(ciclo,file),'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        clave,creditos = search_data(0,pdfReader.getNumPages(),pdfReader)
        ciclo_df = ciclo.replace('./bd/','')
        file = file.replace('.pdf','')
        file = file.replace(clave,'')
        df_datos = df_datos.append({'Ciclo':ciclo_df,'Materia':file,'Clave':clave,'Creditos':creditos},ignore_index=True)
        
        pdfFileObj.close()