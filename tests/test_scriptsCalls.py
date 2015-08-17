# encoding: utf-8
from tests.testing_tools import KreaturaTestCase
from elements import ScriptsCalls
from lxml import etree


class TestScriptsCalls(KreaturaTestCase):
    def setUp(self):
        self.sc = ScriptsCalls('Q1')
        self.want = etree.Element('control_layout')
        self.want.set('id', self.sc.id+'.js')
        self.want.set('layout', 'default')
        self.want.set('style', "")
        self.content = etree.SubElement(self.want, 'content')

    def test_js_table(self):
        # print(self.sc.id)
        # content.text = 'A'

        self.content.text = '''
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
'''.format(self.sc.id)

        self.sc.js_table()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_obrazki_zamiast_kafeterii(self):
        self.content.text = '''
<!-- Obrazki zamiast kafeterii -->
<script type='text/javascript'>
var multiImageControlId = '{0}';
</script>
'''.format(self.sc.id)
        self.sc.obrazki_zamiast_kafeterii()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_list_column(self):
        self.sc.columns = 2

        self.content.text = '''
<!-- list column -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
new IbisListColumn("{0}",{1});
</script>
'''.format(self.sc.id, 2)

        self.sc.list_column()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_list_column_example(self):
        self.sc.columns = 2

        self.content.text = '''
<!-- list column -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
  // new IbisListColumn("{0}",{1});
</script>
'''.format(self.sc.id, 2)

        self.sc.list_column(example=True)
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_dezaktywacja_opena(self):
        self.content.text = '''
<!-- dezaktywacja opena -->
<script type='text/javascript'>
    var opendisDest = "{0}";
    var opendisText = "Nie wiem / trudno powiedzieć";
    var opendisValue = "98";
</script>
<script type='text/javascript' src='opendis/opendis.js'></script>
'''.format(self.sc.id)

        self.sc.dezaktywacja_opena()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_superimages(self):
        self.content.text = '''<!-- super images -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  s{0} = new SuperImages("{0}", {{zoom: false}});
</script>
'''.format(self.sc.id)

        self.sc.superimages()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_superimages_example(self):
        self.content.text = '''<!-- super images -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  // s{0} = new SuperImages("{0}", {{zoom: false}});
</script>
'''.format(self.sc.id)

        self.sc.superimages(example=True)
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))
