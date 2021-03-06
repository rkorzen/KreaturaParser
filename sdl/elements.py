# coding: utf-8
import datetime
import re
from string import ascii_uppercase



from lxml import etree
from sdl.tools import build_precode, find_parent, clean_labels, wersjonowanie_plci
from sdl.tools import find_parent, filter_parser, make_caf_to_dim, unix_time, unix_creation_time, find_by_id
from sdl.spss import baskets_syntax, multi_syntax, var_lab, val_lab


WERSJONOWANIE = True



class SurveyElements:
    """Base of survey structures/elements"""

    def __init__(self, id_):
        self.id = id_
        # self.precode = ''
        self.precode = False
        # self.postcode = ''
        self.postcode = False
        self.rotation = False
        self.random = False
        self.hide = False
        self.childs = []
        self.parent_id = False
        self.typ = False
        self.cafeteria = []
        self.statements = []
        self.categories = []
        self.size = []
        self.content = False
        self.dontknow = None
        self.xml = None
        self.warnings = []
        self.dim_out = ""
        self.web_out = ""
        self.spss_out = ""
        self.kwargs = {}

    def __eq__(self, other):
        return (self.id == other.id and
                self.parent_id == other.parent_id and
                self.precode == other.precode and
                self.postcode == other.postcode and
                self.rotation == other.rotation and
                self.random == other.random and
                self.hide == other.hide and
                self.childs == other.childs and
                self.typ == other.typ and
                self.cafeteria == other.cafeteria and
                self.statements == other.statements and
                self.size == other.size and
                self.content == other.content and
                self.dontknow == other.dontknow

                )

    def set_precode(self):
        """Set precode of element"""
        if self.precode:  # jeśli element ma precode
            try:
                prec = build_precode(self.precode, 'precode')
                self.xml.append(prec)

            except ValueError as e:
                raise ValueError("Błąd w precode elementu {0}, {1}".format(self.id, e))

    def set_postcode(self):
        """Set precode of element"""
        if self.postcode:  # jeśli element ma precode
            try:
                prec = build_precode(self.postcode, 'postcode')
                self.xml.append(prec)

            except ValueError as e:
                raise ValueError("Błąd w postcode elementu {0}, {1}".format(self.id, e))

    def to_dim(self):
        for child in self.childs:
            child.to_dim()
            self.dim_out += child.dim_out

    def to_web(self):
        for child in self.childs:
            child.to_web()
            self.web_out += child.web_out

    def to_spss(self):
        for child in self.childs:
            child.to_spss()
            self.spss_out += child.spss_out


class Survey:
    """
    Survey contain childs
    Survey have s method to add a block element to his parent
    """

    def __init__(self):
        self.warnings = []
        self.childs = []
        self.id = ""   # just for a case... and for find_by_id function
        self.createtime = unix_creation_time(datetime.datetime.now())
        self.xml = False
        self.dim_out = ""
        self.web_out = ""
        self.spss_out = ""
        # self.wersjonowanie = True

    def __eq__(self, other):
        return self.childs == other.childs and self.id == other.id

    def __repr__(self):
        return "survey: " + self.id

    def append(self, block):
        """Add child to self.childs list"""
        self.childs.append(block)

    def add_to_parent(self, block):
        """
        Add child to his parent. Parent is nested somewhere in survey childs
        If there is not element with parent_id Exception is thrown.
        """
        #parent_id = find_parent(self, block.parent_id)
        parent = find_by_id(self, block.parent_id)
        if parent:
            parent.childs.append(block)
        else:
            # TODO: some other exception type?
            raise Exception("Wrong parent id", block.parent_id)

    def to_xml(self):
        """survey xml"""
        # TODO: opcjonalnie - procedury, zmienne
        self.xml = etree.Element('survey')
        self.xml.set('createtime', str(self.createtime))
        self.xml.set('creator', "CHANGEIT")
        self.xml.set('exitpage', "")
        self.xml.set('layoutid', "ShadesOfGray")
        self.xml.set('localeCode', "pl")
        self.xml.set('name', "CHANGEIT")
        self.xml.set('sensitive', "false")
        self.xml.set('showbar', "false")
        self.xml.set('time', "60000")
        self.xml.set('SMSComp', "false")
        for child in self.childs:
            child.warnings = self.warnings
            child.to_xml()
            self.warnings = child.warnings
            self.xml.append(child.xml)

        vars_ = etree.Element('vars')
        self.xml.append(vars_)

        procedures = etree.Element('procedures')
        procedure = etree.Element('procedure')
        procedure.set('id', 'PROC')
        procedure.set('shortdesc', '')
        procedures.append(procedure)

        self.xml.append(procedures)

    def to_dim(self):
        for child in self.childs:
            child.to_dim()
            self.dim_out += child.dim_out
            self.dim_out = wersjonowanie_plci(self.dim_out, "dim")

    def to_web(self):
        for child in self.childs:
            child.to_web()
            self.web_out += child.web_out

    def to_spss(self):
        for child in self.childs:
            child.to_spss()
            self.spss_out += child.spss_out


class Block(SurveyElements):
    """Block element."""

    def __init__(self, id_):
        SurveyElements.__init__(self, id_)
        self.quoted = False

    def __repr__(self):
        return "Block: " + self.id


    def to_xml(self):
        """xml representation of Block element"""
        self.xml = etree.Element('block')
        self.xml.set('id', self.id)
        self.xml.set('name', '')
        self.xml.set('quoted', 'false')
        self.xml.set('random', 'false')
        self.xml.set('rotation', 'false')

        if self.quoted:
            self.xml.set('quoted', 'true')

        if self.random:
            self.xml.set('random', 'true')

        if self.rotation:
            self.xml.set('rotation', 'true')

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            child.warnings = self.warnings
            child.to_xml()
            self.warnings = child.warnings
            self.xml.append(child.xml)

        self.set_postcode()


class Page(SurveyElements):
    """Page element."""

    def __init__(self, id_):
        SurveyElements.__init__(self, id_)
        self.hideBackButton = False
        # self.postcode = ""

    def __str__(self):
        return self.id

    def __repr__(self):
        return "Page " + self.id

    def to_xml(self):
        """xml representation of Page element"""
        # self.postcode = ""
        self.xml = etree.Element('page')
        self.xml.set('id', self.id)
        self.xml.set('hideBackButton', 'false')
        self.xml.set('name', '')
        # print(self.precode)
        if self.hideBackButton:
            self.xml.set('hideBackButton', 'true')

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            # ustawiam postcode dziecka na to co mamy
            child.postocde = self.postcode

            # przekazuje warningi
            child.warnings = self.warnings
            # metoda xml tworzy atrybut xml z odpowiednią zawartoscia
            # jej wywołanie wpływa jednak także na .postcode
            # przekazywany jest on aż do poziomu kafeterii i potem idzie w góre
            child.to_xml()

            # aktualizuję postcode strony tym  co zebrane w głębi
            if child.postcode:
                if not self.postcode:
                    self.postcode = ""
                self.postcode += child.postcode
            self.warnings = child.warnings

            # w gridzie to_xml dla question zwraca element page wraz z dziećmi.. trzeba to podmienić,
            # by nie było strony w stronie
            if child.xml.tag == 'page':
                self.xml = child.xml
            else:
                self.xml.append(child.xml)

        # print("jestem tu: ". self.postcode)
        self.set_postcode()
        # if self.postcode:
        #     # drukowanie postcodu do xmla ma sens tylko w przypadku stron i bloków
        #     # w tym przypadku chodzi o postcode strony tworzony na podstawie
        #     # jego dzieci
        #     postcode = etree.Element('postcode')
        #     postcode.text = etree.CDATA(self.postcode)
        #    self.xml.append(postcode)

    def to_web(self):
        if self.precode:
            self.childs[0].precode = self.precode
        if self.postcode:
            self.childs[0].postcode = self.postcode

        for child in self.childs:
            child.to_web()
            self.web_out += child.web_out


class Question(SurveyElements):
    """Question"""

    def __repr__(self):
        return "question: {} {} ".format(self.id, self.typ)

    def caf_to_dim(self, tabs=0, use=False, statements=False, **kwargs) :
        """:returns string
        :param cafeteria: cafeteria or statements list
        :param tabs: level of indent
        """

        prov_letter = kwargs.get('prov_letter', '_')
        images = kwargs.get('images')
        leadzero = kwargs.get('leadzero', 0)
        big_letters = kwargs.get("big-letters", False)
        int_implicite = kwargs.get("int-implicite", False)
        raw_id = kwargs.get("raw-id", False)
        first_id = kwargs.get("first-id", False)

        tmp_caf_id = []

        if use:
            out = "        use {} -".format(use)
        else:
            if statements:
                cafeteria = self.statements
            else:
                cafeteria = self.cafeteria
            out = ""
            ile = len(cafeteria)
            for caf in cafeteria:
                ref, na, dk = False, False, False
                if leadzero:
                    caf.id = "0"*(leadzero - len(caf.id)) + caf.id
                elif big_letters:
                    prov_letter = ""
                    caf.id = ascii_uppercase[int(caf.id)-1]
                elif int_implicite:
                    #print(caf.content)
                    caf.content = caf.id + " " + caf.content
                    #print(caf.content)
                    caf.id = str(cafeteria.index(caf) + 1)
                elif raw_id:
                    prov_letter = ""
                    caf.id = re.sub("\s", "_", caf.content)

                elif first_id:
                    prov_letter = ""
                    caf.id = caf.content.strip().split()[0]
                    caf.content = caf.content.replace(caf.id, "", 1).strip()

                if '--i' in caf.content:
                    caf.content = caf.content.replace('--i', "")
                    caf.content = '<i>' + caf.content.strip() + '</i>'

                if '--b' in caf.content:
                    caf.content = caf.content.replace('--b', "")
                    caf.content = '<b>' + caf.content.strip() + '</b>'

                if '|' in caf.content:
                    caf.content = caf.content.split('|')
                    caf.img = caf.content[1]
                    caf.content = caf.content[0]

                if '--@' in caf.content:
                    caf.content = caf.content.replace("--@", "").strip()
                    caf.id = caf.id + "@"

                if "--fix" in caf.content:
                    caf.fixposition = True
                    caf.content = caf.content.replace("--fix", "").strip()

                if "--ref"  in caf.content:
                    caf.content = caf.content.replace("--ref", "").strip()
                    ref = True

                if "--na" in caf.content:
                    caf.content = caf.content.replace("--na", "").strip()
                    na = True

                if "--dk" in caf.content:
                    caf.content = caf.content.replace("--dk", "").strip()
                    dk = True


                if "--use:" in caf.content:
                    list_ = caf.content.split('--use:')[1]
                    out += "    " * tabs + r"use {} -".format(list_)

                elif caf.deactivate or dk:
                    out += '    ' * tabs + '- "{}" DK'.format(caf.content)

                elif ref:
                    out += '    ' * tabs + '- "{}" REF'.format(caf.content)

                elif na:
                    out += '    ' * tabs + '- "{}" NA'.format(caf.content)


                elif caf.fixposition:
                    out += '    ' * tabs + prov_letter + caf.id + ' "' + caf.content + '" fix'
                else:
                    out += '    ' * tabs + prov_letter + caf.id + ' "' + caf.content + '"'


                if caf.other:
                    out += ' other'

                if caf.img:
                    out += r'''
            labelstyle(
                Image = "images\{0}",
                ImagePosition = "ImageOnly"
            )'''.format(caf.img)

                if images:
                    if isinstance(images, bool):
                        img = caf.id + '.jpg'
                    else:
                        img = images[0] + "\\" + caf.id + '.jpg'


                    out += r'''
            labelstyle(
                Image = "images\{0}",
                ImagePosition = "ImageOnly"
            )'''.format(img)

                if cafeteria.index(caf) == ile - 1:
                    out += '\n'
                else:
                    out += ",\n"

                # validation

                if caf.id in tmp_caf_id:
                    raise ValueError("Two positions can't have same id. Error in: " + self.id + ". Cafeteria id: " + caf.id )
                else:
                    tmp_caf_id.append(caf.id)


        return out

    # def statements_to_dim(self, tabs=0, use=None, prov_letter='_'):
    #     """:returns string
    #     :param cafeteria: cafeteria or statements list
    #     :param tabs: level of indent
    #     """
    #
    #     if use:
    #         out = "        use {} -".format(use)
    #     else:
    #         cafeteria = self.statements
    #         out = ""
    #         ile = len(cafeteria)
    #         for caf in cafeteria:
    #
    #             if '--i' in caf.content:
    #                 caf.content = caf.content.replace('--i', "")
    #                 caf.content = '<i>' + caf.content.strip() + '</i>'
    #
    #             if '--b' in caf.content:
    #                 caf.content = caf.content.replace('--b', "")
    #                 caf.content = '<b>' + caf.content + '</b>'
    #
    #             if '|' in caf.content:
    #                 caf.content = caf.content.split('|')
    #                 caf.img = caf.content[1]
    #                 caf.content = caf.content[0]
    #
    #             if "--use:" in caf.content:
    #                 list_ = caf.content.split('--use:')[1]
    #                 out += "    " * tabs + r"use {} -".format(list_)
    #             elif caf.deactivate:
    #                 out += '    ' * tabs + '- "{}" DK'.format(caf.content)
    #             else:
    #                 out += '    ' * tabs + prov_letter + caf.id + ' "' + caf.content + '"'
    #
    #             if caf.other:
    #                 out += ' other'
    #
    #             if caf.img:
    #                 out += r'''
    #         labelstyle(
    #             Image = "images\{0}",
    #             ImagePosition = "ImageOnly"
    #         )'''.format(caf.img)
    #
    #             if cafeteria.index(caf) == ile - 1:
    #                 out += '\n'
    #             else:
    #                 out += ",\n"
    #
    #     return out

    def meta_info(self):

        if self.typ == "B":

            metainfo = """
    [
        flametatype = "mbdragndrop"
        , toolPath = "[%ImageCacheBase%]/images/mbtools/"
        , rowBtnType = "Image"
        , dropType = "buckets"
        ' Optional settings:
        ', rowBtnUseZoom = True     ' Setting to true enables a zoom icon on each of the row images that allows the respondents to view a larger version on screen.
    ]
"""

    def special_markers(self):
        """Find special markers in content

        special markers:
        IBIS
        --multi                 : multianswer in grids, tables
        --images                : image cafeteria
        --listcolumn            : cafeteria in columns
        --dezaktywacja          :
        --minchoose:x           : multi min choose
        --maxchoose:x           : multi max choose
        --nr                    : not require
        --custom_css            : add custom css to page

        Dimensions
        --list:name             : define and use cafeteria object
        --use:name              : use cafeteria object


        """

        markers = {}
        # multi - np do gridów, tabel
        if '--multi' in self.content:
            markers['multi'] = True
            self.content = self.content.replace('--multi', '')

        # obrazki zamiast kafeterii
        if '--images' in self.content:
            pattern = re.compile(r"--images:([\w\d_\\]+)")
            path = pattern.search(self.content)
            try:
                markers['images'] = path.groups(1)
                text_to_replace = path.group(0)
            except AttributeError:
                markers['images'] = True
                text_to_replace = '--images'

            self.content = self.content.replace(text_to_replace, '')

        if '--listcolumn' in self.content:
            pattern = re.compile('--listcolumn:(\d+)')

            try:
                s = pattern.search(self.content)
                text_to_replace = s.group(0)
                list_column = s.group(1)

            except AttributeError:
                list_column = '2'
                text_to_replace = "--listcolumn"

            markers['listcolumn'] = list_column
            self.content = self.content.replace(text_to_replace, '')

        if '--dezaktywacja' in self.content:
            markers["dezaktywacja"] = True
            self.content = self.content.replace('--dezaktywacja', '')

        if '--minchoose:' in self.content:
            pattern = re.compile('--minchoose:(\d+)')
            try:
                s = pattern.search(self.content)
                text_to_replace = s.group(0)
                #print(text_to_replace)
                minchoose = s.group(1)
            except AttributeError:
                raise ValueError("minchoose to powinna być liczba. prawidłowe użycie to --minchoose:x, błąd w ", self.content)

            markers['minchoose'] = minchoose
            self.content = self.content.replace(text_to_replace, '')

        if '--maxchoose:' in self.content:
            pattern = re.compile('--maxchoose:(\d+)')
            try:
                s = pattern.search(self.content)
                text_to_replace = s.group(0)
                maxchoose = s.group(1)
            except AttributeError:
                raise ValueError("maxchoose to powinna być liczba. prawidłowe użycie to --minchoose:x, błąd w ",
                                 self.content)

            markers['maxchoose'] = maxchoose
            self.content = self.content.replace(text_to_replace, '')

        # --nr czyli not require. Przydatne np przy liście openów nie wymaganych
        if '--nr' in self.content:
            self.content = self.content.replace('--nr', '')
            markers['not_require'] = True

        if '--statements-ran' in self.content:
            self.content = self.content.replace('--statements-ran', '')
            markers['ran_stmt'] = True

        if '--ran' in self.content or self.random:
            self.content = self.content.replace('--ran', '')
            markers['ran'] = True

        if '--statements-rot' in self.content:
            self.content = self.content.replace('--statements-rot', '')
            markers['rot_stmt'] = True

        if '--rot' in self.content or self.rotation:
            self.content = self.content.replace('--rot', '')
            markers['rot'] = True

        if '--custom_css' in self.content:
            self.content = self.content.replace('--custom_css', '')
            markers['custom_css'] = True

        if '--use:' in self.content and '--list:' in self.content:  # this should be before --list and --use
            raise ValueError("You should'nt use '--use:' and '--list:' at the same time")

        if '--list:' in self.content:
            pattern = re.compile('--list:([\d\w]+)')
            try:
                s = pattern.search(self.content)
                list_ = s.group(1)
                text_to_replace = s.group(0)
            except AttributeError:
                raise ValueError("Nazwa listy ma zły format: ",
                                 self.content,
                                 "prawidłowy format to '--list:xxxx', gdzie xxxx to znaki  z zakresu: 'a-z0-9_'")
            markers['list'] = list_
            self.content = self.content.replace(text_to_replace, '')

        if '--use:' in self.content:
            pattern = re.compile('--use:([\d\w]+)')
            try:
                s = pattern.search(self.content)
                use = s.group(1)
                text_to_replace = s.group(0)
            except AttributeError:
                raise ValueError("Nazwa listy ma zły format: ",
                                 self.content,
                                 "prawidłowy format to '--list:xxxx', gdzie xxxx to znaki  z zakresu: 'a-z0-9_'")
            markers['use'] = use
            self.content = self.content.replace(text_to_replace, '')

        if '--gray'in self.content:
            markers['gray'] = True
            self.content = self.content.replace('--gray', '')

        if '--lz:' in self.content:
            pattern = re.compile('--lz:(\d+)')
            try:
                s = pattern.search(self.content)
                leadzero = int(s.group(1))
                text_to_replace = s.group(0)
            except AttributeError:
                raise ValueError("Nazwa listy ma zły format, ",
                                 self.content,
                                 "prawidłowy format to '--lz:xx', gdzie xxxx to liczba")
            markers['leadzero'] = leadzero
            self.content = self.content.replace(text_to_replace, '')

        if '--big-letters' in self.content:
            markers["big-letters"] = True
            self.content = self.content.replace("--big-letters", "")

        if '--int-implicite' in self.content:
            markers["int-implicite"] = True
            self.content = self.content.replace("--int-implicite", "")

        if "--sort-by-id" in self.content:
            markers["sort_by_id"] = True
            self.content = self.content.replace("--sort-by-id", "")

        if "--sort" in self.content:
            markers["sort"] = True
            self.content = self.content.replace("--sort", "")

        if "--raw-id" in self.content:
            markers['raw-id'] = True
            self.content = self.content.replace("--raw-id", "")

        if "--first-id" in self.content:
            markers['first-id'] = True
            self.content = self.content.replace("--first-id", "")



        return markers

    def to_xml(self):
        """xml representation of Question element

        Tu najwięcej się dzieje
        """

        # region sprawdzamy id stwierdzen i kafeterii
        temp_ids = []
        # print(self.cafeteria)
        for caf in self.cafeteria:
            if caf.id in temp_ids:
                raise ValueError('Przynajmniej dwie odpowiedzi mają to samo id w pytaniu', self.id)
            else:
                temp_ids.append(caf.id)
        # endregion

        special_markers = self.special_markers()

        # minchoice itd
        # to co do atrybutow tagow musi byc ustawione przed to_xml
        minchoose = special_markers.get('minchoose')
        maxchoose = special_markers.get('maxchoose')
        listcolumn = special_markers.get("listcolumn")
        images = special_markers.get("images")

        # TODO: tutaj duużo do zrobienia - wszystkie typy
        # region begin
        if self.typ in ('G', 'SDG', 'R'):
            # w tym przypadku niestety question w to_xml musi zwrócić page

            self.xml = etree.Element('page')
            self.xml.set('id', self.id + '_p')

            if self.typ is not 'R':
                self.xml.set('hideBackButton', 'false')

            # question z instrukcją
            instr = etree.Element('question')
            instr.set('id', self.id + 'instr')

            layout = ControlLayout(self.id + '_lab_instr')

            if WERSJONOWANIE:
                tresc =  wersjonowanie_plci(self.content)
            else:
                tresc = self.content

            if self.typ is "R":
                layout.content = '<div class="ranking_instrukcja">' + tresc + "</div>"
            else:
                layout.content = '<div class="grid_instrukcja">' + tresc + "</div>"
            layout.to_xml()

            instr.append(layout.xml)
            self.xml.append(instr)

        elif self.typ in ('B', 'LHS'):
            self.xml = etree.Element('question')
            self.xml.set('id', self.id)
            self.xml.set('name', '')

            if WERSJONOWANIE:
                tresc =  wersjonowanie_plci(self.content)
            else:
                tresc = self.content

            layout = ControlLayout(self.id + '.labelka')
            layout.content = '<div class="basket_instrukcja">' + tresc + '</div>'
            layout.to_xml()
            self.xml.append(layout.xml)

        else:
            self.xml = etree.Element('question')
            self.xml.set('id', self.id)
            self.xml.set('name', '')

            layout = ControlLayout(self.id + '.labelka')

            if WERSJONOWANIE:
                tresc =  wersjonowanie_plci(self.content)
            else:
                tresc = self.content

            layout.content = tresc
            layout.to_xml()
            self.xml.append(layout.xml)
        # endregion

        # region control_layout
        if self.typ is "L":

            if self.cafeteria:
                for nr, caf in enumerate(self.cafeteria):
                    if not caf.id:
                        id_suf = '_' + str(nr+1)
                    else:
                        id_suf = '_' + str(caf.id)
                    layout_ = ControlLayout(self.id + id_suf + '_txt')
                    if WERSJONOWANIE:
                        tresc =  wersjonowanie_plci(caf.content)
                    else:
                        tresc = self.content

                    layout_.content = tresc
                    layout_.to_xml()
                    self.xml.append(layout_.xml)

        # endregion

        # region control_open
        if self.typ is "O":
            # dodaję kontrolkę/kontrolki open
            if self.cafeteria:
                for nr, caf in enumerate(self.cafeteria):
                    id_suf = '_' + str(caf.id)
                    # if not caf.id:
                    #     id_suf = '_' + str(nr+1)
                    # else:
                    #     id_suf = '_' + str(caf.id)

                    open_ = ControlOpen(self.id + id_suf)
                    open_.name = self.id + id_suf + ' | ' + clean_labels(caf.content)
                    if special_markers.get('not_require'):
                        open_.require = 'false'
                    # if self.size:
                    #     open_.size = self.size
                    open_.to_xml()
                    self.xml.append(open_.xml)
            else:
                open_ = ControlOpen(self.id+"_OPEN")
                open_.name = self.id + ' | ' + clean_labels(self.content)
                if special_markers.get('not_require'):
                    open_.require = 'false'

                if self.size:
                    open_.size = self.size
                open_.to_xml()

                self.xml.append(open_.xml)

                if self.dontknow:
                    script_call = ScriptsCalls(self.id+"_OPEN")
                    script_call.dezaktywacja_opena(self.dontknow)
                    self.xml.append(script_call.to_xml())

        # endregion

        # region control_single/multi
        if self.typ == "S" or self.typ == "M":
            if not self.cafeteria:  # []
                raise ValueError("Brak kafeterii w pytaniu ", self.id)

            if self.typ == "S":
                control = ControlSingle(self.id)
            else:
                control = ControlMulti(self.id)

            if self.random:
                control.random = 'true'
            if self.rotation:
                control.rotation = 'true'

            control.cafeteria = self.cafeteria
            control.name = self.id + ' | ' + clean_labels(self.content)
            control.postcode = self.postcode

            if minchoose:
                control.minchoose = minchoose
            if maxchoose:
                control.maxchoose = maxchoose

            control.to_xml()
            self.postcode = control.postcode
            self.xml.append(control.xml)

            for caf in self.cafeteria:
                if caf.other:
                    open_id = self.id + '_' + caf.id + 'T'
                    open_ = ControlOpen(open_id)
                    open_.name = open_id + ' | ' + caf.content
                    open_.to_xml()
                    self.xml.append(open_.xml)

            # obrazki zamiast kafeterii
            if images:
                script_call = ScriptsCalls(self.id)
                script_call.obrazki_zamiast_kafeterii()
                self.xml.append(script_call.to_xml())

            # listcolumn
            if listcolumn:
                print(listcolumn)
                # jeśli mamy podejrzanie dużo kolumn to warto o tym poinformować
                if int(listcolumn) > 3:
                    self.warnings.append("W pytaniu " + self.id + " wskazana liczba kolumn ma być większa niż 3."
                                                                  " Nie za szeroko?")

                script_call = ScriptsCalls(self.id, **{'columns': listcolumn})
                script_call.list_column()

                self.xml.append(script_call.to_xml())

        # endregion

        # region control_number
        if self.typ == "N":
            if self.cafeteria:
                for nr, caf in enumerate(self.cafeteria):
                    if not caf.id:
                        id_suf = '_' + str(nr+1)
                    else:
                        id_suf = '_' + str(caf.id)

                    open_ = ControlNumber(self.id + id_suf)
                    open_.name = self.id + id_suf + ' | ' + clean_labels(caf.content)
                    if self.size:
                        open_.size = self.size
                    open_.to_xml()
                    self.xml.append(open_.xml)
            else:
                open_ = ControlNumber(self.id)
                open_.name = self.id + ' | ' + clean_labels(self.content)
                if self.size:
                    open_.size = self.size
                open_.to_xml()
                self.xml.append(open_.xml)
        # endregion

        # region js tables
        if self.typ == "T":
            if not self.statements:  # []
                raise ValueError("Brak stwierdzen w pytaniu ", self.id, "Być może zapomniałeś o _, "
                                                                        "albo chciales zastosowac inny typ pytania")
            hide_stw_pattern = None
            for stwierdzenie in self.statements:

                el_id = self.id + '_' + stwierdzenie.id

                layout = ControlLayout(el_id + '_txt')
                layout.content = stwierdzenie.content
                if stwierdzenie.hide:
                    hide_stw_pattern = stwierdzenie.hide

                if hide_stw_pattern and hide_stw_pattern not in ['"0"', '&quot;0&quot;']:
                    layout.hide = hide_stw_pattern.format(stwierdzenie.id)

                layout.to_xml()
                self.xml.append(layout.xml)

                if 'multi' in special_markers:
                    control = ControlMulti(el_id)
                else:
                    control = ControlSingle(el_id)

                control.cafeteria = self.cafeteria
                control.name = el_id + ' | ' + clean_labels(stwierdzenie.content)

                if hide_stw_pattern and hide_stw_pattern not in ['"0"', '&quot;0&quot;']:
                    control.hide = hide_stw_pattern.format(stwierdzenie.id)

                # nie wiem na razie jak tu powinno być z postcodem
                control.postcode = self.postcode

                control.to_xml()
                self.xml.append(control.xml)

            script_call = ScriptsCalls(self.id)
            script_call.js_table()
            # script_call = script_call.to_xml()
            self.xml.append(script_call.to_xml())
        # endregion

        # region dinamic grid
        if self.typ in ('G', 'SDG'):
            hide_ptrn = ""
            for stwierdzenie in self.statements:

                el_id = self.id + '_' + stwierdzenie.id
                question = etree.Element('question')
                question.set('id', el_id)

                if stwierdzenie.hide:
                    hide_ptrn = stwierdzenie.hide

                if hide_ptrn:
                    try:
                        hide_q = hide_ptrn.format(stwierdzenie.id)
                    except ValueError as e:
                        raise ValueError(e, self.id)
                    hide = etree.Element('hide')
                    hide.text = etree.CDATA(hide_q)
                    question.append(hide)

                lay = ControlLayout(el_id + '_txt')

                if '--multi' in stwierdzenie.content:
                    control = ControlMulti(el_id)
                    stwierdzenie.content = stwierdzenie.content.replace('--multi', '')
                else:
                    control = ControlSingle(el_id)

                # rotation
                if '--rot' in stwierdzenie.content:
                    stwierdzenie.content = stwierdzenie.content.replace('--rot', '')
                    control.rotation = 'true'

                # random
                if '--ran' in stwierdzenie.content:
                    stwierdzenie.content = stwierdzenie.content.replace('--ran', '')
                    control.random = 'true'

                lay.content = stwierdzenie.content
                # print(lay.content)
                control.cafeteria = self.cafeteria
                # print(control.cafeteria)
                lay.to_xml()

                if minchoose:
                    control.minchoose = minchoose
                if maxchoose:
                    control.maxchoose = maxchoose

                control.name = el_id + ' | ' + clean_labels(stwierdzenie.content)
                control.to_xml()

                question.append(lay.xml)
                question.append(control.xml)

                for caf in self.cafeteria:
                    if caf.other:
                        open_id = el_id + '_' + caf.id + 'T'
                        open_ = ControlOpen(open_id)
                        open_.name = open_id + ' | ' + caf.content
                        open_.to_xml()
                        question.append(open_.xml)

                self.xml.append(question)

            question_sc = etree.Element('question')
            question_sc.set('id', self.id + 'script_calls')

            script_call = ScriptsCalls(self.id)
            script_call.dinamic_grid()

            question_sc.append(script_call.to_xml())
            self.xml.append(question_sc)
        # endregion

        # region slider
        if self.typ == 'SLIDER':
            # TODO: dodatkowe atrybuty? value min max step - można to też odpuścić

            left, right = None, None

            num = ControlNumber(self.id)

            # jeśłi jest kafeteria - to powinny być poadane oba końce skali
            if self.cafeteria:
                try:
                    left = self.cafeteria[0].content
                    right = self.cafeteria[1].content
                except IndexError as e:
                    raise ValueError('W pytaniu ' + self.id + ' powinny być podane oba końce skali - '
                                                              'czyli dwa elementy kafeterii', e)

            if not left:
                num.name = self.id + ' ' + clean_labels(self.content)
                num.to_xml()

                self.xml.append(num.xml)
            else:
                num.name = "{0} | {1} - {2} | {3} ".format(self.id, clean_labels(left), clean_labels(right),
                                                           clean_labels(self.content))
                table = ControlTable(self.id+'_table')
                row = Row()

                l_cell = Cell()
                l_cell.add_control(ControlLayout(self.id + 'left', **{'content': left}))

                n_cell = Cell()
                n_cell.add_control(num)

                r_cell = Cell()
                r_cell.add_control(ControlLayout(self.id + 'right', **{'content': right}))

                row.add_cell(l_cell)
                row.add_cell(n_cell)
                row.add_cell(r_cell)

                table.add_row(row)
                table.to_xml()

                self.xml.append(table.xml)

            script_call = ScriptsCalls(self.id)
            script_call.slider()

            self.xml.append(script_call.to_xml())

        # endregion

        # region sliders
        if self.typ == "SLIDERS":

            # ustawienia:
            if self.cafeteria:
                try:
                    left = self.cafeteria[0].content
                except IndexError as e:
                    left = "Lewy koniec skali"

                try:
                    right = self.cafeteria[1].content
                except IndexError as e:
                    right = "Prawy koniec skali"

            min, max = 1, 10  # domyślne ustawienia dla sliderOpts.min i sliderOpts.max

            for marker in special_markers:
                if marker.startswith("minchoose"):
                    min = marker.split(':')[1]
                if marker.startswith("maxchoose"):
                    max = marker.split(':')[1]

            # tabelka
            hide_ptrn = ""
            for stmnt in self.statements:
                table = ControlTable("{}_{}_table".format(self.id, stmnt.id))
                if stmnt.hide:
                    hide_ptrn = stmnt.hide

                if hide_ptrn:
                    table.hide = hide_ptrn.format(stmnt.id)
                row = Row()

                statement_tekst = ControlLayout("{}_{}_table_stmnt".format(self.id, stmnt.id))
                statement_tekst.content = stmnt.content

                lewy_tekst = ControlLayout("{}_{}_table_left".format(self.id, stmnt.id))
                lewy_tekst.content = left

                prawy_tekst = ControlLayout("{}_{}_table_right".format(self.id, stmnt.id))
                prawy_tekst.content = right

                numeric = ControlNumber("{}_{}".format(self.id, stmnt.id))
                numeric.name = "{}_{} | {}".format(self.id, stmnt.id, self.content)

                cell_statement, cell_left, cell_middle, cell_right = Cell(), Cell(), Cell(), Cell()

                cell_statement.add_control(statement_tekst)
                cell_left.add_control(lewy_tekst)
                cell_middle.add_control(numeric)
                cell_right.add_control(prawy_tekst)

                row.add_cell(cell_statement)
                row.add_cell(cell_left)
                row.add_cell(cell_middle)
                row.add_cell(cell_right)

                table.add_row(row)
                table.to_xml()

                self.xml.append(table.xml)


            # dodajemy skrypt js
            script_call = ScriptsCalls(self.id, **{'statements':self.statements,
                                                   'cafeteria':self.cafeteria,
                                                   'min':min,
                                                   'max':max,
                                                   'random': self.random})

            script_call.sliders()
            self.xml.append(script_call.to_xml())
        # endregion

        # region highlighter
        if self.typ == "H":
            script_call = ScriptsCalls(self.id)
            script_call.highlighter()
            self.xml.append(script_call.to_xml())

            img = ControlLayout(self.id + '.img')
            try:
                img.content = '<img src="{0}">'.format(self.cafeteria[0].content)
            except IndexError:
                raise ValueError('Highlighter wymaga podania obrazka, lokalizacje obrazka bez znaczników'
                                 'html umiesc  jako pierwszy element kafeterii', self.id)
            img.to_xml()
            self.xml.append(img.xml)

            open_ = ControlOpen(self.id + '.input')
            open_.to_xml()
            self.xml.append(open_.xml)

        # endregion

        # region baskets
        if self.typ in ('B', 'LHS'):
            if not self.cafeteria:
                raise ValueError('W pytaniu {} brak kafeterii.'.format(self.id))

            if not self.statements:
                raise ValueError('W pytaniu {} brak stwierdzeń. Być może zapomniałeś o _'.format(self.id))

            # prepare images in cafeteria

            # print(self.cafeteria)
            for c, caf in enumerate(self.cafeteria):
                self.cafeteria[c].content = '<img src="public/{0}/{1}.jpg" alt = "{2}">'.format(self.id, caf.id,
                                                                                                caf.content)
            source = ControlSingle(self.id)
            source.require = 'false'
            source.cafeteria = self.cafeteria
            if self.rotation:
                source.rotation = 'true'
            if self.random:
                source.random = "true"

            source.name = self.content
            source.to_xml()

            self.xml.append(source.xml)

            basket_calls = ""
            baskets_count = len(self.statements)
            for count, statement in enumerate(self.statements):
                basket = ControlMulti(self.id + 'x' + str(count+1))
                basket.cafeteria = self.cafeteria
                basket.name = self.id + 'x' + str(count+1) + " | " + statement.content
                basket.require = 'false'
                basket.to_xml()
                self.xml.append(basket.xml)

                basket_calls += '''bm.createBasket("{id}", {{
    label: "{label}",
    min: 0,
    max: {max},
    maxreplace: true
}});
'''.format(**{'id': basket.id, 'label': statement.content.strip(), 'max': baskets_count})

            script_call = ScriptsCalls(self.id)
            script_call.baskets(basket_calls)

            self.xml.append(script_call.to_xml())

        # endregion

        # region ranking
        if self.typ == "R":
            question = etree.Element('question')
            question.set('id', self.id)
            source = ControlSingle(self.id)
            source.cafeteria = self.cafeteria
            source.name = self.id + ' | ' + self.content
            source.require = 'false'
            source.to_xml()

            question.append(source.xml)

            for caf in self.cafeteria:
                if caf.id.startswith('0'):
                    raise ValueError('W rankingu {0} w kafeterii nie może być zer wiodących'.format(self.id))

                number = ControlNumber(self.id + '.number' + caf.id)
                number.name = "Pozycja Odp" + caf.id
                # if caf.hide:
                #     pass

                number.to_xml()
                question.append(number.xml)

            script_call = ScriptsCalls(self.id)
            script_call.ranking()
            question.append(script_call.to_xml())
            self.xml.append(question)

        # endregion

        # region ConceptSelect
        if self.typ == "CS":
            if not self.cafeteria:
                raise ValueError('W pytaniu {} brak tekstu do ConceptSelecta. '
                                 'Powinien to być 1 element'.format(self.id))

            cs_tekst = " | ".join(self.cafeteria[0].content.split())
            id_c_tresc = self.id + '_tresc'
            control_tresc = ControlLayout(id_c_tresc)
            control_tresc.content = cs_tekst
            control_tresc.to_xml()
            self.xml.append(control_tresc.xml)

            id_c_data = self.id + '_data'
            control_data = ControlOpen(id_c_data)
            control_data.style = "display:none;"
            control_data.name = self.id + '_data | ConceptSelect'
            control_data.to_xml()
            self.xml.append(control_data.xml)

            control_disabler = ControlMulti(self.id + '_dis')
            if not self.statements:
                caf = Cafeteria(**{'id': '98', 'content': 'Nic nie zwróciło mojej uwagi'})
                control_disabler.cafeteria.append(caf)
            else:
                for el in self.statements:
                    caf = Cafeteria(**{'id': el.id, 'content': el.content})
                    caf.deactivate = 'true'
                    control_disabler.cafeteria.append(caf)

            control_disabler.require = 'false'
            control_disabler.name = self.id + '_dis'
            control_disabler.to_xml()

            self.xml.append(control_disabler.xml)

            script_call = ScriptsCalls(self.id)

            if not self.statements:
                id_disablera = self.id + '_dis.98'
                script_call.ibis_disabler(id_disablera, id_c_tresc)
                script_call.ibis_disabler(id_disablera, id_c_data, '98')
            else:
                for el in self.statements:
                    id_disablera = self.id + '_dis.' + el.id
                    script_call.ibis_disabler(id_disablera, id_c_tresc)
                    script_call.ibis_disabler(id_disablera, id_c_data, el.id)

            script_call.concept_select(id_c_tresc, id_c_data)

            self.xml.append(script_call.to_xml())
        # endregion

        if 'custom_css' in special_markers:
            css_lay = ControlLayout(self.id + '_css')
            css_lay.content = '<link rel="stylesheet" href="public/custom.css" type="text/css">'
            css_lay.to_xml()
            self.xml.append(css_lay.xml)

        if self.hide:
            hide = etree.Element('hide')
            hide.text = etree.CDATA(self.hide.format(self.id))
            self.xml.append(hide)

    @staticmethod
    def min_max_choice(special_markers, control):
        self = control
        for el in special_markers:
            if el.startswith('minchoose:'):
                try:
                    # print('BBB')
                    minchoose = el.split(':')
                    control.minchoose = minchoose[1]
                    # print(control.minchoice)
                except:
                    raise ValueError("W pytaniu: ", self.id, "zadeklarowano minchoice, ale nie podano wartości",
                                     'być może  po --min: jest spacja. Format to --min:x')

            if el.startswith('maxchoose:'):
                try:
                    # print('BBB')
                    maxchoose = el.split(':')
                    control.maxchoose = maxchoose[1]
                    # print(control.minchoice)
                except:
                    raise ValueError("W pytaniu: ", self.id, "zadeklarowano minchoice, ale nie podano wartości",
                                     'być może  po --min: jest spacja. Format to --min:x')

    def to_dim(self):
        """Generate Dimension metadata"""

        options = self.special_markers()
        #print(options)
        defined_list = options.get("use")
        create_list = options.get("list")
        minchoose = options.get("minchoose")
        maxchoose = options.get("maxchoose")
        images = options.get("images")
        sort_ = options.get("sort")
        sort_by_id = options.get("sort_by_id")
        ran = options.get("ran")
        ran_stmt = options.get("ran_stmt")
        rot = options.get("rot")
        rot_stmt = options.get("rot_stmt")

        print(ran, ran_stmt)
        ran_rot, ran_rot_stmt = "", ""

        if ran:
            ran_rot = " ran "
        if rot:
            ran_rot = " rot "

        if ran_stmt:
            ran_rot_stmt = " ran "
        if rot_stmt:
            ran_rot_stmt = " rot "



        if sort_ and self.cafeteria:
            self.cafeteria = sorted(self.cafeteria, key=lambda x: x.content)

        if sort_by_id and self.cafeteria:
            self.cafeteria = sorted(self.cafeteria, key=lambda x: x.id)

        if not minchoose:
            minchoose = "1"

        if not maxchoose:
            if self.typ == "S":
                maxchoose = "1"
            else:
                maxchoose = ""

        use = None

        self.kwargs = options
        # if options.get("int-implicite", False):
        #     self.kwargs["int-implicite"] = True
        #
        if images:
            self.kwargs['images'] = images

        self.kwargs['leadzero'] = options.get('leadzero', 0)

        if self.typ == "DEF":
            if options.get("big-letters", False):
                self.kwargs["big-letters"] = True
            caf = self.caf_to_dim(2, use, **self.kwargs)

            self.dim_out += """
    {0} - define
    {{
{1}
    }};
""".format(self.id, caf)

        elif self.typ in ["S", "M"]:
            if create_list:
                self.dim_out += self.dim_create_list(create_list)
                use = create_list

            if defined_list:
                use = defined_list

            self.dim_out += '\n    ' + self.id + ' "{0}"'.format(self.content)

            if images:
                self.dim_out += """
        [
            flametatype = "mbclickableimages"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"

        ]"""

            self.dim_out += """
    Categorical [{1}..{2}]
    {{
{0}
    }}{3};
""".format(self.caf_to_dim(2, use,  **self.kwargs), minchoose, maxchoose, ran_rot)

        elif self.typ == "L":
            self.dim_out += "    " + self.id + ' "' + self.content + '" info;\n\n'

        elif self.typ in ["G", "SDG"] and not self.categories:
            if '--byslice' in self.content:
                content = self.content.replace('--byslice', '')
                out = """
    {id} ""
        [
            flametatype = "mbdynamicgrid"
             , toolPath = "[%ImageCacheBase%]/images/mbtools/"
        ]
    loop
    {{
{stw}
    }}{ran_rot_stmt}fields -
    (
        slice "{content}

        <b>{{@}}</b>
        {{obraz}}
        "
        categorical [1..1]
        {{
{caf}
        }}{ran};
    ) expand grid;
""".format(**{'id': self.id,
                          'content': content,
                          'stw': make_caf_to_dim(self.statements, 2),
                          'caf': make_caf_to_dim(self.cafeteria, 3),
                          'ran_rot_stmt': ran_rot_stmt,
                          'ran_rot': ran_rot
                          })
            else:
                out = """
    {id} "{content}"
        [
            flametatype = "mbdynamicgrid"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
        ]
    loop
    {{
{caf}
    }}{ran_rot_stmt} fields -
    (
        slice ""
        categorical [1..1]
        {{
{stw}
        }}{ran_rot};
    ) expand grid;
""".format(**{'id': self.id,
              'content': self.content,
              'stw': self.caf_to_dim(3),
              'caf': self.caf_to_dim(2, statements=True),
              'ran_rot_stmt': ran_rot_stmt,
              'ran_rot': ran_rot
              })

            self.dim_out += out

        elif self.typ in ["G", "SDG"] and self.categories:
            if '--byslice' in self.content:
                out = """
                    {id} - loop
                    {{
                {cat}
                    }} ran fields -
                    (
                        LR " {content}" loop
                        {{
                {stw}
                        }} fields -
                        (
                            slice ""
                            categorical [1..1]
                            {{
                {caf}
                            }};
                        ) expand grid;
                    ) expand;
                """.format(**{'id': self.id,
                              'content': self.content,
                              'cat': make_caf_to_dim(self.categories, 2, 'c'),
                              'stw': make_caf_to_dim(self.statements, 3, 'l'),
                              'caf': make_caf_to_dim(self.cafeteria, 4)
                              })
            else:
                out = """
    {id} - loop
    {{
{cat}
    }} ran fields -
    (
        LR " {content}" loop
        {{
{stw}
        }} fields -
        (
            slice ""
            categorical [1..1]
            {{
{caf}
            }};
        ) expand grid;
    ) expand;
""".format(**{'id': self.id,
              'content': self.content,
              'cat': make_caf_to_dim(self.categories, 2, 'c'),
              'stw': make_caf_to_dim(self.statements, 3, 'l'),
              'caf': make_caf_to_dim(self.cafeteria, 4)
              })

            self.dim_out += out

        elif self.typ == "O":
            self.dim_out += '''    {0} "{1}" text;\n\n'''.format(self.id, self.content)

        elif self.typ == "N":
            numeric = ControlNumber(self.id)
            numeric.content = self.content
            numeric.to_dim()
            self.dim_out += numeric.dim_out

        elif self.typ in ["B", "LHS"]:

            if images:
                row_btn_type = "Image"
                rowBtnUseZoom = "\n            ' , rowBtnUseZoom = True             ' Setting to true enables a zoom icon on each of the row images that allows the respondents to view a larger version on screen."
                rowBtnWidth = ""
            else:
                row_btn_type = "Text"
                rowBtnUseZoom = ""
                rowBtnWidth = "\n            ' , rowBtnWidth = 200                 ' width should be any integer > 10"

            if self.typ in ["B"]:
                dropType = "buckets"
                colImgType = ""

            elif self.typ in ["LHS"]:
                dropType = "scale"
                colImgType = '''\n            , colImgType = "LoveHate"            ' RedBlack, Grey"'''


            out = """
    {id} "{content}"
        [
            flametatype = "mbdragndrop"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
            , rowBtnType = "{rowBtnType}"{rowBtnWidth}{rowBtnUseZoom}{colImgType}
            , dropType = "{dropType}"
        ]
    loop
    {{
{stw}
    }}{ran_rot_stmt} fields -
    (
        slice ""
        categorical [{minchoose}..{maxchoose}]
        {{
{caf}
        }}{ran_rot};
    ) expand grid;
""".format(**{'id': self.id,
              'content': self.content,
              'stw': self.caf_to_dim(2, statements=True),
              'caf': self.caf_to_dim(3),
              'minchoose': minchoose,
              'maxchoose': maxchoose,
              'rowBtnType': row_btn_type,
              'rowBtnUseZoom': rowBtnUseZoom,
              'rowBtnWidth': rowBtnWidth,
              "dropType": dropType,
              "colImgType": colImgType,
              'ran_rot_stmt': ran_rot_stmt,
              'ran_rot': ran_rot
              })

            self.dim_out += out

        elif self.typ  == "H":
            pass

        else:
            stat, caf = None, None
            if self.statements:
                stat = make_caf_to_dim(self.statements, 2)
            if self.cafeteria:
                caf = make_caf_to_dim(self.cafeteria, 3)

            self.dim_out += '''   {0} "" loop
    {{
{2}
    }} fields -
    (
        slice "{1}"
        Categorical [1..]
        {{
{3}
        }};

    ) expand grid;'

'''.format(self.id, self.content, stat, caf)

    def to_web(self):

        if self.precode:
            filter = filter_parser(self.precode)

            if filter.strip().startswith("'"):
                self.web_out += filter + '\n'

            elif filter:
                try:
                    self.web_out += filter.format(self.id)
                except:
                    raise(Exception("OJ"))

        if '--byslice' in self.content:
            self.web_out += """
    Dim {0}_iter
    For Each {0}_iter in {0}.Categories
        {0}[{0}_iter].slice.Label.Style.ImagePosition=imagepositions.ipImageOnly
        {0}[{0}_iter].slice.Label.Inserts["obraz"]= "<div align='center'><mrRef RefType='img' src='" + {0}_iter.Label.Style.Image + "' alt='image'/></div>"
        {0}[{0}_iter].Ask()
    next             
""".format(self.id)

        else:
            self.web_out += "    " + self.id + '.Ask()\n'

        if self.typ in ["S", "M"]:
            for caf in self.cafeteria:
                if caf.screenout:
                    self.web_out += '    if {0}.ContainsAny("x{1}") then IOM.SbScreenOut()\n\n'.format(self.id, caf.id)

        if self.postcode:

            filter = filter_parser(self.postcode)

            if filter.strip().startswith("'"):
                self.web_out += filter + '\n'

    def to_spss(self):
        if self.typ in ["LHS", "B"]:
            self.spss_out = baskets_syntax(self)


        if self.typ == "M":
            self.spss_out =  multi_syntax(self)
            lista = None
            if "--use:" in self.cafeteria[0].content:
                l_name = self.cafeteria[0].content.replace("--use:", "").strip()
                #print(self.parent_id)
                #lista = find_by_id(l_name)

            self.spss_out += var_lab(self, lista)



    def dim_create_list(self, create_list):

        caf = self.caf_to_dim(2, **self.kwargs)

        return """
    {0} - define
    {{
{1}
    }};
""".format(create_list, caf)


class Control:
    def __init__(self, id_, **kwargs):
        self.id = id_
        self.xml = False
        self.tag = None
        self.layout = False
        self.style = ""
        self.require = "true"
        self.hide = False
        self.rotation = 'false'
        self.random = 'false'
        self.name = None
        self.results = 'true'
        self.cafeteria = []
        self.statements = []
        self.xml = ""
        self.postcode = False
        self.dim_out = None
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def to_xml(self):
        self.xml = etree.Element(self.tag)
        self.xml.attrib['id'] = self.id

        if self.layout:
            self.xml.attrib['layout'] = self.layout
            self.xml.set('layout', self.layout)
        else:
            self.xml.set('layout', 'default')
        if self.style:
            self.xml.set('style', self.style)
        else:
            self.xml.set('style', '')

        if self.hide:
            hide = etree.Element('hide')
            hide.text = etree.CDATA(self.hide)
            self.xml.append(hide)


class ControlLayout(Control):
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.tag = 'control_layout'
        if 'content' in kwargs:
            self.content = kwargs['content']
        else:
            self.content = False

    def to_xml(self):
        Control.to_xml(self)
        content = etree.Element('content')
        if self.content:
            content.text = self.content
        self.xml.append(content)


class ControlOpen(Control):
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.tag = 'control_open'

        # default values:
        self.content = False
        self.require = 'true'
        self.size = ['25', '1']
        self.mask = '.*'
        self.results = 'true'
        self.style = ''
        self.name = self.id

        # wartości nadpisane
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def to_xml(self):
        # example: <control_open id="Q1" length="25" line="1" mask=".*" require="true" results="true" rotation="false"
        # style="" name="Q1 COS"/>
        # print(self.require)

        self.xml = etree.Element(self.tag)
        self.xml.set('id', self.id)
        self.xml.set('length', self.size[0])
        self.xml.set('lines', self.size[1])
        self.xml.set('mask', self.mask)

        self.xml.set('name', self.name)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        self.xml.set('style', self.style)

        content = etree.Element('content')
        if self.content:
            content.text = self.content
        self.xml.append(content)

    def to_dim(self):
        self.dim_out += '\n    ' + self.id + ' "' + self.content + '"\n'
        self.dim_out += '''
    'style(
    '    Width = "3em";
    ')
    text;
'''


class ControlSingle(Control):
    """Categorical with single response class"""
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.tag = 'control_single'
        if not self.layout:
            self.layout = 'vertical'
        self.itemlimit = "0"

        self.minchoose = None
        self.maxchoose = None

        # wartości nadpisane
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])
        self.dim_out = ""

    def to_xml(self):
        Control.to_xml(self)
        # self.xml = etree.Element(self.tag)
        # self.xml.set('id', self.id)
        self.xml.set('itemlimit', self.itemlimit)
        self.xml.set('layout', self.layout)

        # self.name powinno być ustawione w question przed wywołaniem metody to_xml()
        self.xml.set('name', self.name)
        self.xml.set('random', self.random)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        self.xml.set('rotation', self.rotation)
        self.xml.set('style', self.style)

        if self.minchoose:
            self.xml.set('minchoose', self.minchoose)

        if self.maxchoose:
            self.xml.set('maxchoose', self.maxchoose)

        """Sprawdzenie, czy ma kafeterię zostawiam tutaj. Nie chcę tego robić w init
        ponieważ dopuszczam różne możliwości ustawiania atrybutu:
          + poprzez kwargs
          + poprzez bezpośrednie odwołania
        """
        if self.cafeteria:

            caf_hide_pattern = ""  # na poczatek pusty hide pattern
            for caf in self.cafeteria:
                list_item = Cafeteria()
                list_item.id = caf.id

                if '--i' in caf.content:
                    caf.content = '<i>'+caf.content.replace('--i', '')+'</i>'

                if '--b' in caf.content:
                    caf.content = '<b>'+caf.content.replace('--b', '')+'</b>'


                list_item.content = caf.content

                # hide pattern ustawiony dla jednego elementu kafeterii
                # obowiazuje tez dla kolejnych
                # chyba, ze zostanie zmieniony
                # stąd sprawdzam czy jest caf.hide
                # i jesli jest to aktualizuje caf_hide_pattern

                if caf.hide:
                    caf_hide_pattern = caf.hide

                if caf_hide_pattern:
                    list_item.hide = caf_hide_pattern

                if caf.deactivate:
                    list_item.deactivate = True

                if caf.other:
                    list_item.connected = self.id + '_' + caf.id + 'T'

                list_item.to_xml()

                self.xml.append(list_item.xml)

                if caf.screenout:
                    if not self.postcode:
                        self.postcode = ""

                    self.postcode += """;;if (${0}:{1} == "1");#OUT = "1";goto KONKURS;else;endif;;""".format(self.id,
                                                                                                              caf.id)
        else:
            raise ValueError("Brak kafeterii w pytaniu: ", self.id)


class ControlMulti(ControlSingle):
    # example: <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 Kryss av:" random="false"
    # require="true" results="true" rotation="false" style="">
    def __init__(self, id_, **kwargs):
        ControlSingle.__init__(self, id_, **kwargs)
        self.tag = 'control_multi'


class ControlNumber(Control):
    # example min: <control_number float="false" id="Q2" mask=".*" name="" require="true" results="true" style="">
    # example max: <control_number float="true" id="Q2" mask=".*" max="99.0" maxsize="2" min="1.0" name=""
    # require="true" results="true" style="">

    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.float = "false"
        self.mask = ".*"
        # self.content = ""
        # self.require = 'true'
        # self.results = 'true'
        # self.style = ""

        self.max = None
        self.maxsize = None
        self.min = None

    def to_xml(self):
        # self.name = self.id + ' | ' + self.content
        self.xml = etree.Element('control_number')
        self.xml.set('id', self.id)
        self.xml.set('float', self.float)
        self.xml.set('mask', self.mask)
        self.xml.set('name', self.name)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        self.xml.set('style', self.style)

        if self.max:
            self.xml.set('max', self.max)
        if self.min:
            self.xml.set('min', self.min)
        if self.maxsize:
            self.xml.set('maxsize', self.maxsize)

        # w sumie chyna nigdy nie użyłem wartości wpisanej domyślnie w control_number
        # gdyby była taka potrzeba.. to coś tu trzeba będzie zmienic
        content = etree.SubElement(self.xml, 'content')

    def to_dim(self):
        self.dim_out = """
    {} "{}"
    ' style( Width = "3em" )
    long;
""".format(self.id, self.content)

class Cafeteria:
    """List element - to np cafeteria, statements"""

    def __init__(self, **kwargs):
        self.tag = 'list_item'
        self.id = None
        self.content = ""
        self.hide = None
        self.deactivate = False
        self.other = False
        self.screenout = False
        self.gotonext = False
        self.goto = None
        self.xml = None
        self.connected = False
        self.img = None
        self.fixposition = False
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def __eq__(self, other):
        return(self.id == other.id and
               self.content == other.content and
               self.hide == other.hide and
               self.deactivate == other.deactivate and
               self.other == other.other and
               self.screenout == other.screenout and
               self.gotonext == other.gotonext and
               self.goto == other.goto
               )

    def __repr__(self):
        return str(self.id) + ',' + self.content

    def to_xml(self):
        self.xml = etree.Element('list_item')
        self.xml.set('id', self.id)
        self.xml.set('name', "")
        self.xml.set('style', "")
        content = etree.Element('content')
        if WERSJONOWANIE:
            content.text = wersjonowanie_plci(self.content)
        else:
            content.text = self.content
        self.xml.append(content)

        if self.deactivate:
            self.xml.set('disablerest', 'true')

        if self.hide:
            hide = etree.Element('hide')
            hide.text = etree.CDATA(self.hide.format(self.id))
            self.xml.append(hide)

        if self.connected:
            # print(self.connected)
            self.xml.set('connected', self.connected)


class ScriptsCalls:
    def __init__(self, id_, **kwargs):
        self.id = id_
        # self.typ = typ_

        self.control = etree.Element('control_layout')
        self.control.set('id', id_+'.js')
        self.control.set('layout', 'default')
        self.control.set('style', "")

        self.content = etree.SubElement(self.control, 'content')
        self.content.text = ""
        self.random = False
        self.columns = ''
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def js_table(self):
        """Xml kontrolki z wywołaniem skryptów tabelki js"""
        self.content.text += '''
<!-- tabela js -->
<link rel="stylesheet" href="public/tables.css" type="text/css">
<script type='text/javascript' src='public/tables.js'></script>
<script type='text/javascript'>

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table("{0}_");

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
</script>

<!-- custom css -->
<link rel="stylesheet" href="public/custom.css" type="text/css">
'''.format(self.id)

    def obrazki_zamiast_kafeterii(self):
        self.content.text += '''
<!-- Obrazki zamiast kafeterii -->
<script type='text/javascript'>
var multiImageControlId = '{0}';
</script>
'''.format(self.id)

    def list_column(self, example=False):

        if example:
            self.content.text += '''
<!-- list column -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
  // new IbisListColumn("{0}",{1});
</script>
'''.format(self.id, self.columns)

        else:
            self.content.text += '''
<!-- list column -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
new IbisListColumn("{0}",{1});
</script>
'''.format(self.id, self.columns)

    def dezaktywacja_opena(self, dk="Nie wiem / trudno powiedzieć"):

        self.content.text = '''
<!-- dezaktywacja opena -->
<script type='text/javascript'>
    var opendisDest = "{0}";
    var opendisText = "{1}";
    var opendisValue = "98";
</script>
<script type='text/javascript' src='opendis/opendis.js'></script>
'''.format(self.id, dk)

    def superimages(self, example=False):

        if example:
            self.content.text += '''
<!-- super images -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  // s{0} = new SuperImages("{0}", {{zoom: false}});
</script>
'''.format(self.id)
        else:
            self.content.text += '''
<!-- super images -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  s{0} = new SuperImages("{0}", {{zoom: false}});
</script>
'''.format(self.id)

    def slider(self):
        self.content.text += '''
<!-- Script name/version: slider/1.0 -->
<link rel="stylesheet" href="public/slider3/css/ui-lightness/jquery-ui-1.8.9.custom.css" type="text/css">
<script type='text/javascript' src='public/slider3/js/jquery-ui-1.8.9.custom.min.js'></script>
<link rel="stylesheet" href="public/slider3/slider_sog.css" type="text/css">
<script type='text/javascript' src='public/slider3/slider_sog.js'></script>
<script type='text/javascript'>
     sliderOpts = {{
          value: 1,
          min: 1,
          max: 10,
          step: 1,
          animate:"slow",
          orientation: 'horizontal'
     }};

new IbisSlider("{0}", sliderOpts);
</script>
<!-- ControlScript ENDS HERE: slider -->
'''.format(self.id)

    def sliders(self):

        call_slider = ""
        for el in self.statements:
            call_slider += 'new IbisSlider("{0}", sliderOpts);\n'.format(self.id+'_'+el.id)

        self.content.text += '''
<link rel="stylesheet" href="public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css" type="text/css">
<link rel="stylesheet" href="public/slider/slider.css" type="text/css">
<link rel="stylesheet" href="public/custom.css" type="text/css">

<script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'></script>

<script type='text/javascript' src='public/slider/slider.js'></script>
<script type='text/javascript'>
     sliderOpts = {{
          value: 0,
          min: {2},
          max: {3},
          step: 1,
          animate:"slow",
          orientation: 'horizontal'
     }};
{1}
</script>
'''.format(self.id, call_slider, self.min, self.max)
        if self.random:
             self.content.text += '''
<script type='text/javascript' src='public/rotate_tables.js'></script>
<!-- get the file from https://github.com/rkorzen/ibisjs
     optionally uncomment the line bellow (only for tests - never for production!!)
-->
<!--
<script type='text/javascript' src='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.js'></script>
<link rel='stylesheet' href='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.css' type='text/css'>
-->
'''



    def dinamic_grid(self):
        self.content.text += '''<!-- Script: listcolumn -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
  // przykład dla list kolumn
  // użyj, gdy listy mają być podzielone na kolumny - np gdy bardzo długa lista
  // new IbisListColumn("{0}_1",2);
</script>
<!-- end: listcolumn -->

<!-- Script: SuperImages -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  // przykład dla SuperImages
  // użyj jeśli mają być w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("{0}_1", {{zoom: false}});
</script>
<!-- end: SuperImages -->

<!-- Script: MerryGoRound -->
<link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/>
<script type='text/javascript' src='public/merryGoRound.js'></script>
<script type='text/javascript'>
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
</script>
<!-- end: MerryGoRound -->

<link rel="stylesheet" href="public/custom.css" type="text/css">
'''.format(self.id)

    def highlighter(self):
        self.content.text += '''<script type='text/javascript' src='public/highlighter/highlighter.js'></script>
<link rel='stylesheet' type='text/css' href='public/highlighter/highlighter.css'/>
<script type='text/javascript'>
hl = new IbisHighlighter('{0}.img','{0}.input', {{ hlClass: 'hl-active-green', debug: false }})
</script>'''.format(self.id)

    def baskets(self, calls):
        self.content.text += '''<!-- Baskets -->
<script type="text/javascript" src="public/baskets/jquery-ui/js/jquery-ui-1.8.18.custom.min.js"></script>
<link rel="stylesheet" href="public/baskets/jquery-ui/css/ui-lightness/jquery-ui-1.8.18.custom.css" type="text/css">
<script type="text/javascript" src="public/baskets/baskets.js"></script>
<link rel="stylesheet" href="public/baskets/baskets.css" type="text/css">
<script type="text/javascript">
var bm = new BasketManager({{className: "multi", dest: "{0}"}});
bm.createBasket("{0}", {{
    source: true,
    max: 0
}});
{1}
</script>
<link rel="stylesheet" href="public/custom.css" type="text/css">'''.format(self.id, calls)

    def ranking(self):
        self.content.text += '''<!-- Script Ranking -->
<link rel=stylesheet type=text/css href="public/ranking.css">
<script type='text/javascript' src='public/jquery-ui-1.7.2.custom.min.js'></script>
<script type='text/javascript' src='public/ranking.js'></script>
<script type='text/javascript'>addRanking("{}");</script>
<!-- end Script Ranking -->

<link rel=stylesheet type=text/css href="public/custom.css">'''.format(self.id)

    def ibis_disabler(self, id_disablera, id_disablowane, wartosc=""):
        if "<script type='text/javascript' src='public/ibisDisabler.js'></script>" not in self.content.text:
            self.content.text += "<script type='text/javascript' src='public/ibisDisabler.js'></script>"

        if wartosc:
            self.content.text += '''
<!-- Disabler  -->
<script type='text/javascript'>
setIbisDisabler('{0}','{1}',{2});
</script>
<!-- End Disabler  -->
'''.format(id_disablera, id_disablowane, wartosc)

        else:
            self.content.text += '''
<!-- Disabler  -->
<script type='text/javascript'>
setIbisDisabler('{0}','{1}');
</script>
<!-- End Disabler  -->
'''.format(id_disablera, id_disablowane)

    def concept_select(self, id_tresc, id_data):
        self.content.text += '''
<!-- Concept Select  -->
<link rel="stylesheet" href="public/Selection_sog.css" type="text/css">
<script type='text/javascript' src='public/Selection_sog.js'></script>
<script type='text/javascript'>
var sel = new Selection({{
textContainerId: "{0}",
openContainerId: "{1}",
delimiter: "|"
}});
</script>
<!-- End ConceptSelect -->
'''.format(id_tresc, id_data)

    def to_xml(self):
        return self.control


class Row:
    def __init__(self):
        self.forcestable = 'true'
        self.style = ""
        self.cells = []
        self.xml = None

    def add_cell(self, cell):

        if isinstance(cell, Cell):
            self.cells.append(cell)
        else:
            raise TypeError("Próbujesz dodać do wiersza coś co nie jest komórką")

    def to_xml(self):
        self.xml = etree.Element('row')
        self.xml.set('forcestable', self.forcestable)
        self.xml.set('style', self.style)

        if not self.cells:
            raise ValueError('Wiersz nie ma żadnej komórki')

        for cell in self.cells:
            cell.to_xml()
            self.xml.append(cell.xml)


class Cell:
    def __init__(self):
        self.colspan = '1'
        self.forcestable = 'false'
        self.rowspan = '1'
        self.style = ''
        self.xml = None
        self.control = None

    def add_control(self, control):
        self.control = control

    def to_xml(self):
        self.xml = etree.Element('cell')
        self.xml.set('colspan', self.colspan)
        self.xml.set('forcestable', self.forcestable)
        self.xml.set('rowspan', self.rowspan)
        self.xml.set('style', self.style)

        if self.control:
            control = self.control.to_xml()
            self.xml.append(self.control.xml)
        else:
            raise ValueError('W komórce tabeli powinna być kontrolka')


class ControlTable:
    def __init__(self, id_):
        self.id = id_
        self.rows = []
        self.random = 'false'
        self.rotation = 'false'
        self.rrdest = 'row'
        self.style = ''
        self.xml = None
        self.hide = False
    def add_row(self, row):
        if isinstance(row, Row):
            self.rows.append(row)
        else:
            raise TypeError('Chcesz dodać do tabeli element inny niż typ row... może dodajesz cell?')

    def to_xml(self):
        self.xml = etree.Element('control_table')
        self.xml.set('id', self.id)
        self.xml.set('random', self.random)
        self.xml.set('rotation', self.rotation)
        self.xml.set('rrdest', self.rrdest)
        self.xml.set('style', self.style)

        if not self.rows:
            raise ValueError('Tabela', self.id, 'nie ma wierszy, a powinna mieć przynajmniej jeden')

        try:
            for row in self.rows:
                row.to_xml()
                self.xml.append(row.xml)


        except ValueError as e:
            # print(str(e))
            raise ValueError("W tabeli " + self.id, e)

        if self.hide:
            hide = etree.Element('hide')
            hide.text = etree.CDATA(self.hide)
            self.xml.append(hide)
