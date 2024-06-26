
import re
import xml.etree.ElementTree as et

alljobs = {
    "BookHeaders":          ("bkhdrs", ("Headers.para.style.enum",)),
    "BookTitles":           ("bktitles", ("Titles.para.style.enum",)),
    "BookIntroduction":     ("bkintro", ('Introductions.para.style.enum',)),
    "BookIntroductionEndTitles": ("bkintroend", ("Titles.para.style.enum",)),
    "ChapterContent":       ("chaptercontent", ),
    "ChapterStart":         ("chapter",),
    "ChapterEnd":           ("chapterend",),
    "Char":                 ("char", ("Char.char.style.enum", "+char.closed", "Attributes", "Break",
                                        "CharContent", "FullChar.char.style.enum", "FullCharExtra.char.style.enum")),
    "CharEmbed":            ("charembed", ("Char.char.style.enum", "+char.closed", "Attributes", "Break",
                                            "FullChar.char.style.enum", "FullCharExtra.char.style.enum")),
    "CrossReference":       ("crossref",),
    "CrossReferenceChar":   ("xchar",("CrossReferenceChar.char.style.enum", "+char.closed")),
    "Figure":               ("fig",("FigureTwo", "Attributes", "FigureThree")),
    "Footnote":             ("f", ("NoteCharEmbed", "Attributes"), ("category", )),
    "FootnoteChar":         ("fchar", ("FootnoteVerse", "FootnoteChars.char.style.enum", "char.closed")),
    "List":                 ("list", ("List.para.style.enum",)),
    "ListChar":             ("listchar", ("+char.closed", "ListChar.char.style.enum",)),
    "Milestone":            ("ms", ("Milestone.enum", "Attributes")),
    "Para":                 ("p", ("VersePara", "NonVersePara", "Para.para.style.enum", "Para.nonpara.style.enum", "Break")),
    "PeripheralDivision":   ("periph", ("Peripheral.FRT.periph.id.enum", "Peripheral.INT.periph.id.enum",
                                        "Peripheral.BAK.periph.id.enum", "Peripheral.OTH.periph.id.enum", "PeripheralContent")),
    "Reference":            ("ref",),
    "Scripture":            ("id", ("BookIdentification", "BookIdentification.book.code.enum", "ChapterContent")),
    "Sidebar":              ("esb",),
    "Table":                ("table", ("TableContent",)),
    "VerseStart":           ("verse",),
    "VerseEnd":             ("verseend",),
    "category":             ("cat",),
}

usxenums = {
    'hdr': 'Headers.para.style',
    'titles': 'Titles.para.style',
    'introduction': 'Introductions.para.style',
    'para': 'VerseParas.para.style',
    'section': 'SectionParas.para.style',
    'other': 'OtherParas.para.style',
    'list': 'List.para.style',
    'introchar': 'IntroChars.char.style',
    'char': 'Chars.char.style',
    'listchar': 'ListChars.char.style',
    'ms': 'Milestones',
    'footnotechar': 'FootnoteChars.char.style',
    'crossrefchar': 'CrossReferenceChars.char.style',
}

relaxns = "{http://relaxng.org/ns/structure/1.0}"

def addmarkers(rdoc, markers):
    for s in markers:
        t, r = s.split('=')
        mks = re.split(r'[,;\s]\s*', r)
        ty = t.strip()
        e = rdoc.find('./{0}define[@name="{1}.enum"]/{0}choice'.format(relaxns, usxenums.get(ty, None)))
        if e is None:
            print(f"Can't find an enum for {ty}.")
            continue
        for m in mks:
            v = et.Element(f'{relaxns}value')
            v.text = m.strip()
            e.insert(0, v)


