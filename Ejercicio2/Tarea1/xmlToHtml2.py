import xml.etree.ElementTree as ET


def addDatosToHTML(child, html_file, i):
    sep = lambda x: x * '\t'
    nombre = sep(i) + "<p>Nombre: " + child.get('nombre') + "</p>\n"
    apellidos = sep(i) + "<p>Apellidos: " + child.get('apellidos') + "</p>\n"
    fechaNacimiento = sep(i) + "<p>Fecha de nacimiento: " + child.get('fechaNacimiento') + "</p>\n"
    lugarNacimiento = sep(i) + "<p>Lugar de nacimiento: " + child.get('lugarNacimiento') + "</p>\n"
    residencia = sep(i) + "<p>Residencia: " + child.get('residencia') + "</p>\n"
    comentarios = sep(i) + "<p>Comentarios: " + child.get('comentarios') + "</p>\n"
    html_file.write(nombre)
    html_file.write(apellidos)
    html_file.write(fechaNacimiento)
    html_file.write(lugarNacimiento)
    html_file.write(residencia)
    html_file.write(comentarios)

def addCoordenadaToHTML(child, html_file, i):
    sep = lambda x: x * '\t'
    tipo = sep(i) + "<p>Tipo: " + child.get('tipo') + "</p>\n"
    latitud = sep(i) + "<p>Latitud: " + child.get('latitud') + "</p>\n"
    longitud = sep(i) + "<p>Longitud: " + child.get('longitud') + "</p>\n"
    altitud = sep(i) + "<p>Altitud: " + child.get('altitud') + "</p>\n"
    html_file.write(tipo)
    html_file.write(latitud)
    html_file.write(longitud)
    html_file.write(altitud)

def addFotografiaToHTML(child, html_file, i):
    sep = lambda x: x * '\t'
    url = sep(i) + "<img src= " + child.get('url') + ' alt="imagen"></img>\n'
    html_file.write(url)


def addPersonToHTML(child, html_file, i):
    html_file.write(i * '\t' + '<li>\n')
    if child.tag == 'datos':
        addDatosToHTML(child, html_file, i)
    elif child.tag == 'coordenada':
        addCoordenadaToHTML(child, html_file, i)
    elif child.tag == 'fotografia':
        addFotografiaToHTML(child, html_file, i)
    html_file.write(i * '\t' + '</li>\n')

def getPersonaRecursivo(persona, html_file, i=0):
    if persona is not None:
        for child in persona:
            if child.tag == 'persona':
                html_file.write(i * '\t' + '<ul>\n')
                getPersonaRecursivo(child, html_file, i+1)
                html_file.write(i * '\t' + '</ul>\n')
            else:
                addPersonToHTML(child, html_file, i)
                

def getAllPersonas(root, html_file):
    personaPrincipal = root.find('persona')
    getPersonaRecursivo(personaPrincipal, html_file)

def createHTML(html_file):
    html_file.write('''<!DOCTYPE html>
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
                            <ul>''')

def closeHTML(html_file):
    html_file.write('''</ul>
                </body>
                </html>''')

def toHtml(xml_file, html_file):
    try:
        with open(xml_file, 'rb', encoding='utf-7') as xml_file:
            tree = ET.parse(xml_file)
        root = tree.getroot()
        html_file = open('redSocial.html', 'w')
        createHTML(html_file)
        getAllPersonas(root, html_file)
        closeHTML(html_file)

    except IOError:
        print('XML not found')
        exit()
    except ET.ParseError:
        print('Error parsing the XML file')
        exit()


def main():
    xml_file = 'redSocial.xml'
    html_file = 'redSocial.html'

    toHtml(xml_file, html_file)


if __name__ == '__main__':
    main()
