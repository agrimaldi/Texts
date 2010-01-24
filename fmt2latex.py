#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import optparse

class TextChunk(object):

    def __init__(self, text):
        self._text = text
        self.sanitizeAccents()

    def __str__(self):
        return self._text

    def sanitizeAccents(self):
        oc = ('\\\'{e}', '\\`{e}', '\\^{e}', '\\"{e}',
              '\\\'{a}', '\\`{a}', '\\^{a}', '\\"{a}',
              '\\\'{o}', '\\`{o}', '\\^{o}', '\\"{o}',
              '\\\'{i}', '\\`{i}', '\\^{i}', '\\"{i}',
              '\\\'{u}', '\\`{u}', '\\^{u}', '\\"{o}',
              '\\c{c}')
        for i, ic in enumerate(u'éèêëáàâäóòôöíìîïúùûüç'):
            self._text = self._text.replace(ic, oc[i])


class TexWrapper(object):
    def __init__(self, template='memoir', text='', title='', author=''):
        self._rendered = u''
        self._author = author
        self._title = title
        self._text = text
        self.template = template

    def prints(self, ofile):
        #sys.stdout.write( self._rendered + '\n')
        print self._rendered
        
    @property
    def template(self):
        return self._template
    @template.setter
    def template(self, value):
        if value in ['memoir']:
            self._template = value
            if value == 'memoir':
                self._rendered = '''%! program = pdflatex

%\\documentclass[12pt,a4paper]{memoir} % for a long document
\\documentclass[12pt,a4paper,article]{memoir} % for a short document

% See the ``Memoir customise'' template for some common customisations
% Don't forget to read the Memoir manual: memman.pdf

\\title{''' + self._title + '''}
\\author{''' + self._author + '''}
\\date{} % Delete this line to display the current date

%%% BEGIN DOCUMENT
\\begin{document}

\\maketitle
%\\tableofcontents* % the asterisk means that the contents itself isn't put into the ToC

%\\chapter{}
%\\section{}
%\\subsection{}
''' + unicode(self._text) + '''

\\end{document}'''

if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option( '-i', '--input_txt_file',
                       dest='ifname',
                       help='Text file to convert to tex.',
                       metavar='FILE' )

    parser.add_option( '-o', '--output_tex_file',
                       dest='ofname',
                       help='Output tex file',
                       metavar='FILE' )

    parser.add_option( '-t', '--title',
                       dest='title',
                       help='Title of the text.',
                       metavar='STRING' )
    
    parser.add_option( '-T', '--template',
                       dest='template',
                       help='Template to use. [memoir]',
                       metavar='TEMPLATE' )
    
    parser.add_option( '-a', '--author',
                       dest='author',
                       help='Author of the text.',
                       metavar='STRING' )
    
    parser.set_defaults(template = 'memoir',
                        author = '',
                        title = '',
                        ifname = '',
                        ofname = '')

    (options, args) = parser.parse_args()

    if not options.ifname:
        parser.error('You must provide an input file name in text format.')

    if not options.ofname:
        ofile = sys.stdout
    else:
        ofile = codecs.open(options.ofname, 'w', 'utf-8')

    with codecs.open(options.ifname, 'r', 'utf-8') as iff:
        text = TextChunk(iff.read())

    texo = TexWrapper(template=options.template,
                      text=text,
                      title=options.title,
                      author=options.author)

    texo.prints(ofile)

    ofile.close()


