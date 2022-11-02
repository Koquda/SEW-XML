import xml.etree.ElementTree as ET


#----------------------------------------------
# Parser
#----------------------------------------------

class XMLParser:
    
    NAMESPACE = '{https://www.uniovi.es}'

    def __init__(self, pathToFile):
        with open(pathToFile, 'rb') as xml_file:
            tree = ET.parse(xml_file)
        self.root = tree.getroot()
        child = self.root.find(self.NAMESPACE + 'persona')
        self.root_node = self.parse_person(child)
        self.create_person(self.root_node, child)

    class Persona:

        def __init__(self):
            self.data = []
            self.coordinates = []
            self.photos = []

            self.parent = None

        def add_parent(self, parent):
            if not self.parent:
                self.parent = parent

    
    class Datos:
        
        def __init__(self, name, surnames, dateOfBirth, placeOfBirth, placeOfResidence, comments):
            self.name = name
            self.surnames = surnames
            self.dateOfBirth = dateOfBirth
            self.placeOfBirth = placeOfBirth
            self.placeOfResidence = placeOfResidence
            self.comments = comments

    class Coordenadas:
        
        def __init__(self, type, latitude, longitude, altitude):
            self.type = type
            self.latitude = latitude
            self.longitude = longitude
            self.altitude = altitude

    class Fotos:

        def __init__(self, path):
            self.path = path


    def parse_person(self, child):
        return self.Persona()

    def parse_datos(self, child):
        name = child.get('nombre')
        surnames = child.get('apellidos')
        dateOfBirth = child.get('fechaNacimiento')
        placeOfBirth = child.get('lugarNacimiento')
        placeOfResidence = child.get('residencia')
        comments = child.get('comentarios')

        return self.Datos(name, surnames, dateOfBirth, placeOfBirth, placeOfResidence, comments)

    def parse_coordenadas(self, child):
        type = child.get('tipo')
        latitude = child.get('latitud')
        longitude = child.get('longitud')
        altitude = child.get('altitud')

        return self.Coordenadas(type, latitude, longitude, altitude)

    def parse_fotos(self, child):
        path = child.get('ruta')

        return self.Fotos(path)

    def create_person(self, p, node):
        if not node:
            return # STOP rec
        else:
            # We add the parents...
            for e in node.findall(self.NAMESPACE + 'persona'):
                person = self.parse_person(e)
                p.add_parent(person)
                self.create_person(person, e)

            # We add the data...
            for e in node.findall(self.NAMESPACE + 'datos'):
                p.data.append(self.parse_datos(e))

            # We add the coordinates...
            for e in node.findall(self.NAMESPACE + 'coordenadas'):
                p.coordinates.append(self.parse_coordenadas(e))

            # We add the photos...
            for e in node.findall(self.NAMESPACE + 'fotos'):
                p.photos.append(self.parse_fotos(e))


#----------------------------------------------
# De XML a HTML
#----------------------------------------------

class XMLtoHTML:
    STARTING_TAB = 3
    sep = lambda self, x: '\n' + x * '\t'

    html = '''<!DOCTYPE html>
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
                        <ul> %s
                        </ul>
                    </body>
                </html>'''


    def __init__(self, xml_file, html_file):
        self.xml_parser = XMLParser(xml_file)
        self.html = self.html % self.rec(self.xml_parser.root_node, self.STARTING_TAB)
        open(html_file, 'w', encoding='utf-8').write(self.html)

    def personToHtml(self, p, i, aux=''):
        for img in p.photos:
            aux += self.sep(i) + '<img src="%s" alt="Foto de %s" />' % (img.path, dato.name)

        for dato in p.data:
            aux += self.sep(i) + '<p> Nombre: %s </p>' % dato.name
            aux += self.sep(i) + '<p> Apellidos: %s </p>' % dato.surnames
            aux += self.sep(i) + '<p> Fecha de nacimiento: %s </p>' % dato.dateOfBirth
            aux += self.sep(i) + '<p> Lugar de nacimiento: %s </p>' % dato.placeOfBirth
            aux += self.sep(i) + '<p> Residencia: %s </p>' % dato.placeOfResidence
            aux += self.sep(i) + '<p> Comentarios: %s </p>' % dato.comments

        for e in p.coordinates:
            aux += self.sep(i) + '<p> Tipo: %s </p>' % e.type
            aux += self.sep(i) + '<p> Latitud: %s </p>' % e.latitude
            aux += self.sep(i) + '<p> Longitud: %s </p>' % e.longitude
            aux += self.sep(i) + '<p> Altitud: %s </p>' % e.altitude

        
        return aux

    def rec(self, p, i, ans=''):
        if not p:
            return ans

        start_li = self.sep(i) + '<li>'
        end_li = self.sep(i) + '</li>'

        i += 1

        start_ul = self.sep(i) + '<ul>'
        end_ul = self.sep(i) + '</ul>'

        ans += start_li + self.personToHtml(p, i)

        if p.parent:
            ans += start_ul
            ans += self.rec(p.parent, i)
            ans += end_ul   
        
        ans += end_li

        return ans


#----------------------------------------------
# Main
#----------------------------------------------


def main():
    xml_file = input('Introduce el nombre del fichero XML: ')
    html_file = input('Introduce el nombre del fichero HTML generado: ')

    try:
        XMLtoHTML(xml_file, html_file)
    except FileNotFoundError:
        print('El fichero no existe, intentemoslo de nuevo...')
        main()


if __name__ == '__main__':
    main()




