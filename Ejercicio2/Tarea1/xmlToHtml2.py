import xml.etree.ElementTree as ET


def addDatosToHTML(child, html_file):
    nombre = "<li>Nombre: " + child.get('nombre') + "</li>\n"
    apellidos = "<li>Apellidos: " + child.get('apellidos') + "</li>\n"
    fechaNacimiento = "<li>Fecha de nacimiento: " + child.get('fechaNacimiento') + "</li>\n"
    lugarNacimiento = "<li>Lugar de nacimiento: " + child.get('lugarNacimiento') + "</li>\n"
    residencia = "<li>Residencia: " + child.get('residencia') + "</li>\n"
    comentarios = "<li>Comentarios: " + child.get('comentarios') + "</li>\n"
    html_file.write(nombre)
    html_file.write(apellidos)
    html_file.write(fechaNacimiento)
    html_file.write(lugarNacimiento)
    html_file.write(residencia)
    html_file.write(comentarios)

def addCoordenadaToHTML(child, html_file):
    tipo = "<li>Tipo: " + child.get('tipo') + "</li>\n"
    latitud = "<li>Latitud: " + child.get('latitud') + "</li>\n"
    longitud = "<li>Longitud: " + child.get('longitud') + "</li>\n"
    altitud = "<li>Altitud: " + child.get('altitud') + "</li>\n"
    html_file.write(tipo)
    html_file.write(latitud)
    html_file.write(longitud)
    html_file.write(altitud)

def addFotografiaToHTML(child, html_file):
    url = "<li>URL: " + child.get('url') + "</li>\n"
    html_file.write(url)


def addPersonToHTML(child, html_file):
    if child.tag == 'datos':
        addDatosToHTML(child, html_file)
    elif child.tag == 'coordenada':
        addCoordenadaToHTML(child, html_file)
    elif child.tag == 'fotografia':
        addFotografiaToHTML(child, html_file)

def getPersonaRecursivo(persona, html_file):
    if persona is not None:
        for child in persona:
            if child.tag == 'persona':
                getPersonaRecursivo(child, html_file)
            else:
                addPersonToHTML(child, html_file)
                

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
                        <base href="media/" />
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
        with open(xml_file, 'rb') as xml_file:
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
