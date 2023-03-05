from django.test import TestCase
from accounts.validators import cpf_validator as validate_cpf
from django.core.exceptions import ValidationError

class CPFValidatorTestCase(TestCase):
    def test_valid_cpf(self):
        self.assertEqual('12345678909', validate_cpf('123.456.789-09'))
        self.assertEqual('12345678909', validate_cpf('12345678909'))

    def test_invalid_cpf(self):
        cpf = '00000000000'
        with self.assertRaises(ValidationError) as context:
            validate_cpf(cpf)
        
        self.assertEqual(str(context.exception), "['Invalid CPF']")

    def test_invalid_cpf_format(self):
        cpf = '12345asd678910'
        with self.assertRaises(ValidationError) as context:
            validate_cpf(cpf)

        self.assertEqual(str(context.exception),  "['Wrong format']")