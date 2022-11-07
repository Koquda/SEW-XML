import xml.etree.ElementTree as ET

# Usar la funcion de crear la línea
# Que las corrdenadas muestren menos decimales

WIDTH = 2400
HEIGHT = 2400
Y_INC = 400

FONT_SIZE = 20



text = lambda x,y,z,a: '\n\t\t<text x="%d" y="%d" %s> %s </text>' % (x,y,z,a)

def addLinea(x1, y1, x2, y2, aux=''):
        aux += '\n\t<line x1="%d" y1="%d" x2="%d" y2="%d" />' % (x1, y1, x2, y2-FONT_SIZE)
        return aux

def addDatosToSVG(child, svg_file, x, y):
    y_calc = lambda x: y + x * FONT_SIZE + 1
    nombre = text(x,y_calc(1),'font-weight="bold"',(child.get('nombre') + " " + child.get('apellidos')))
    fechaNacimiento = text(x,y_calc(2),'', ('Fecha de nacimiento: ' + child.get('fechaNacimiento')))
    lugarNacimiento = text(x,y_calc(3),'', ('Lugar de nacimiento: ' + child.get('lugarNacimiento')))
    residencia = text(x,y_calc(4),'', ('Residencia: ' + child.get('residencia')))
    comentarios = text(x,y_calc(5),'', ('Comentarios: ' + child.get('comentarios')))
    svg_file.write('<g>\n')
    svg_file.write(nombre)
    svg_file.write(fechaNacimiento)
    svg_file.write(lugarNacimiento)
    svg_file.write(residencia)
    svg_file.write(comentarios)

def addCoordenadaToSVG(child, svg_file, x, y, iteration):
    y_calc = lambda x: y + x * FONT_SIZE + 1
    if iteration % 2 == 0:
        coordenadaTipo = text(x,y_calc(6),'font-weight="bold"',(child.get('tipo')))
        coordenadaValores = text(x,y_calc(7),'', (child.get('latitud') + " / " + child.get('longitud') + " / " + child.get('altitud')))
    else:
        coordenadaTipo = text(x,y_calc(8),'font-weight="bold"',(child.get('tipo')))
        coordenadaValores = text(x,y_calc(9),'', (child.get('latitud') + " / " + child.get('longitud') + " / " + child.get('altitud')))
    svg_file.write(coordenadaTipo)
    svg_file.write(coordenadaValores)

def addFotografiaToSVG(child, svg_file, x, y, iteration):
    y_calc = lambda x: y + x * FONT_SIZE + 1
    if iteration % 2 == 1:
        url = text(x,y_calc(8),'', ('Fotografia: ' + child.get('url')))
    else:
        url = text(x,y_calc(10),'', ('Fotografia: ' + child.get('url')))
    svg_file.write(url)
    svg_file.write('</g>\n')


def addPersonToSVG(child, svg_file, x, y, iteration):
    for subchild in child:
        if subchild.tag == 'datos':
            addDatosToSVG(subchild, svg_file, x, y)
        elif subchild.tag == 'coordenada':
            addCoordenadaToSVG(subchild, svg_file, x, y, iteration)
            iteration+=1
        elif subchild.tag == 'fotografia':
            addFotografiaToSVG(subchild, svg_file, x, y, iteration)

def getPersonaRecursivo(persona, svg_file, x, y, iteration, i=1):
    if len(persona.findall('persona')) > 0:
        yNueva = y + Y_INC
        getPersonaRecursivo(persona.findall('persona')[0], svg_file, x-HEIGHT/(3**i), yNueva, iteration, i+1)
        getPersonaRecursivo(persona.findall('persona')[1], svg_file, x, yNueva, iteration, i+1)
        getPersonaRecursivo(persona.findall('persona')[2], svg_file, x+HEIGHT/(3**i), yNueva, iteration, i+1)
    addPersonToSVG(persona, svg_file, x, y, iteration)
    
                

def getAllPersonas(root, svg_file, iteration):
    personaPrincipal = root.find('persona')
    addPersonToSVG(personaPrincipal, svg_file, WIDTH/2, FONT_SIZE, iteration)
    getPersonaRecursivo(personaPrincipal, svg_file, WIDTH/2, FONT_SIZE, iteration)

def createSVG(svg_file):
    svgHeader = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
    width="%dpx" height="%dpx" viewBox="0 0 %d %d">

    '''

    svg_file.write(svgHeader % (WIDTH, HEIGHT, WIDTH, HEIGHT))

def closeSVG(svg_file):
    svgFooter = '''<style><![CDATA[
    text{
        dominant-baseline: middle;
        text-anchor: middle;
        font: %s Verdana, Helvetica, Arial, sans-serif;
    }

    line {
        stroke:rgb(0,0,0);
        stroke-width:2;
    }
    ]]></style>
</svg>'''

    svg_file.write(svgFooter % FONT_SIZE)

def toHtml(xml_file, svg_file, iteration=0):
    try:
        with open(xml_file, 'rb') as xml_file:
            tree = ET.parse(xml_file)
        root = tree.getroot()
        svg_file = open(svg_file, 'w')
        createSVG(svg_file)
        getAllPersonas(root, svg_file, iteration)
        closeSVG(svg_file)

    except IOError:
        print('XML not found')
        exit()
    except ET.ParseError:
        print('Error parsing the XML file')
        exit()


def main():
    xml_file = 'redSocial.xml'
    svg_file = 'redSocial.svg'

    toHtml(xml_file, svg_file)


if __name__ == '__main__':
    main()