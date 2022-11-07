import xml.etree.ElementTree as ET

li = lambda string: '\n\t\t<li>%s</li>' % (string)

def getAdditionalMetadataRec(child, string):
    for subchild in child:
        if subchild is not None:
            getAdditionalMetadataRec(subchild, string)
        string += li(subchild.tag + " " + subchild.text)
    return string

def getAdditionalMetadata(root):
    additionalMetadata = root.find('additionalMetadata')
    string = ''
    if additionalMetadata is not None:
        string += '\n\t\t<li>Additional Metadata</li>\n\t<ul>\n\t'
        string += getAdditionalMetadataRec(additionalMetadata, '')
        string += '\n\t\t</ul>'
    return string

def getDatasetRec(child, string):
    for subchild in child:
        if subchild is not None:
            getDatasetRec(subchild, string)
        string += li(subchild.tag + " " + subchild.text)
    return string

def getDataset(root):
    dataset = root.find('dataset')
    string = ''
    if dataset is not None:
        string += '\n\t\t<li>Dataset</li>\n\t<ul>\n\t'
        string += getDatasetRec(dataset, '')
        string += '\n\t\t</ul>'
    return string

def getAllow(allow):
    return li("Principal: " + allow.find('principal').text) + li("Permission: " + allow.find('permission').text)

def getAccessRec(access):
    string = ''
    for allow in access.findall('allow'):
        string += getAllow(allow)
        
    return string

def getAccess(root):
    access = root.find('access')
    if access is not None:
        openUl = '\n\t\t<li>Access</li>\n\t<ul>\n\t'
        closeUl = '\n\t\t</ul>'
        return openUl + getAccessRec(access) + closeUl
    else:
        return ''

def EMLParser(path_to_file):
    with open(path_to_file, 'rb') as eml_file:
        tree = ET.parse(eml_file)
    root = tree.getroot()
    string = ''
    string += getAccess(root)
    string += getDataset(root)
    string += getAdditionalMetadata(root)

    return string


class EMLtoHTML:

    sep = lambda self, x: '\n' + x * '\t'

    html_head = '''<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8" />
        <meta name="author" content="Alejandro Campa Martínez" />
        <meta name="description" content="Ejemplo de la red social convertida a HTML desde un XML." />
        <meta name="keywords" content="html,xml" />
        <meta name="viewport" content ="width=device-width, initial scale=1.0" />
        <title> Red Social por Alejandro Campa</title>
        <link rel="stylesheet" type="text/css" href="../estilos.css" />
    </head>
    <body>
        <h1> Red Social </h1>
        <ul>%s
        </ul>
    </body>
</html>'''

    def __init__(self, eml_file, html_file):
        self.eml_parser = EMLParser(eml_file)
        self.html = self.html_head % self.eml_parser
        open(html_file, 'w', encoding='utf-8').write(self.html)



# Main methods of the program

def main():
    eml_file = 'archivoEML.xml'
    html_file = 'archivoHTML.html'

    try:
        EMLtoHTML(eml_file, html_file)
    except FileNotFoundError:
        print("El archivo no existe")
        exit()



if __name__ == '__main__':
    main()