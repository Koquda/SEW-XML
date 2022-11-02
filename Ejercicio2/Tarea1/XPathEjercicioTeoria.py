import xml.etree.ElementTree as ET

def verXPath(archivoXML, expresionXPath):
    try:
        arbol = ET.parse(archivoXML)

    except IOError:
        print("Error: no se encuentra el archivo", archivoXML)
        exit()

    except Et.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
    

    raiz = arbol.getroot()

    for hijo in raiz.findall(expresionXPath):
        print("\nElemento: ", hijo.tag)
        if hijo.text != None:
            print("Contenido = ", hijo.text.strip('\n'))
        else:
            print("Contenido = ", hijo.text)
        print("Atributos = ", hijo.attrib)

def main():

    print(verXPath.__doc__)
    
    miArchivoXML = input('Introduce el nombre del archivo XML: ')

    miExpresionXPath = input('Introduce la expresión XPath: ')

    verXPath(miArchivoXML, miExpresionXPath)

if __name__ == "__main__":
    main()
