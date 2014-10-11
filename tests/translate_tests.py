from . import BaseTestCase
from hackzurich.translate import translate


class TranslateTestCase(BaseTestCase):

    def test_translate(self):
        """
            Ensure that basic translation works
        """
        translation = translate("Geschaelte Tomaten")
        assert translation == "Peeled tomatoes"
