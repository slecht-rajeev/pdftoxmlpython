import os
import io
import xml.etree.ElementTree as xml

# from miner_text_generator import extract_text_by_page
from xml.dom import minidom
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO


def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


def export_as_xml(pdf_path, xml_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    root = xml.Element('{filename}'.format(filename=filename))
    pages = xml.Element('Pages')
    root.append(pages)

    counter = 1
    for page in extract_text_by_page(pdf_path):
        text = xml.SubElement(pages, 'Page_{}'.format(counter))
        text.text = page[0:100]
        counter += 1

    tree = xml.ElementTree(root)
    xml_string = xml.tostring(root, 'utf-8')
    parsed_string = minidom.parseString(xml_string)
    pretty_string = parsed_string.toprettyxml(indent='  ')

    with open(xml_path, 'w') as fh:
        fh.write(pretty_string)
    # tree.write(xml_path)


# if __name__ == '__main__':
pdf_path = 'D:/PycharmProjects/first/rajeev_ranjan_resume.pdf'
xml_path = 'D:/PycharmProjects/first/rajeev_ranjan_resume.xml'
export_as_xml(pdf_path, xml_path)