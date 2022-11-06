import xml.etree.ElementTree as ET




def addCoordenadaToHTML(child, kml_file, i, persona):
    sep = lambda x: x * '\t'
    name = sep(i) + "<name> Lugar de " + child.get('tipo') + " de " + persona.find('datos').get('nombre') + " "  + persona.find('datos').get('apellidos') + "</name>\n"

    if (child.get('tipo') == 'nacimiento'):
        descripcion = sep(i) + "<description> " + persona.find('datos').get('nombre') + " "  + persona.find('datos').get('apellidos') + " nació el " + persona.find('datos').get('fechaNacimiento') + "</description>\n"
    else:
        descripcion = sep(i) + "<description> Se desconoce desde cuando reside en su lugar actual de residencia </description>\n"
    coordenada = sep(i) + "<Point>\n" + sep(i+1) + "<coordinates>" + child.get('longitud') + "," + child.get('latitud') + "," + child.get('altitud') + "</coordinates>\n" + sep(i) + "</Point>\n"

    kml_file.write(i * '\t' + '<Placemark>\n')
    kml_file.write(name)
    kml_file.write(descripcion)
    kml_file.write(coordenada)
    kml_file.write(i * '\t' + '</Placemark>\n')


def addPersonToHTML(child, kml_file, i, persona):
    if child.tag == 'coordenada':
        addCoordenadaToHTML(child, kml_file, i, persona)
    

def getPersonaRecursivo(persona, kml_file, i=0):
    if persona is not None:
        for child in persona:
            if child.tag == 'persona':
                getPersonaRecursivo(child, kml_file, i+1)
            else:
                addPersonToHTML(child, kml_file, i, persona)
                

def getAllPersonas(root, kml_file):
    personaPrincipal = root.find('persona')
    getPersonaRecursivo(personaPrincipal, kml_file)

def createHTML(kml_file):
    kml_file.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name> Red Social - Lugares de residencia y nacimiento </name>
<open>1</open>

''')

def closeKML(kml_file):
    kml_file.write('''</Document>
</kml>''')

def toHtml(xml_file, kml_file):
    try:
        with open(xml_file, 'rb') as xml_file:
            tree = ET.parse(xml_file)
        root = tree.getroot()
        kml_file = open(kml_file, 'w')
        createHTML(kml_file)
        getAllPersonas(root, kml_file)
        closeKML(kml_file)

    except IOError:
        print('XML not found')
        exit()
    except ET.ParseError:
        print('Error parsing the XML file')
        exit()


def main():
    xml_file = 'redSocial.xml'
    kml_file = 'redSocial.kml'

    toHtml(xml_file, kml_file)


if __name__ == '__main__':
    main()