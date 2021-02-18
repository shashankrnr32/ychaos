from unittest import TestCase
from vzmi.ychaos.utils.dependency import DependencyUtils


class TestDependencyUtils(TestCase):
    def test_import_valid_module(self):
        module = DependencyUtils.import_module(
            "vzmi.ychaos.utils.dependency", raise_error=False
        )
        self.assertIsNotNone(module)

    def test_import_invalid_module(self):
        module = DependencyUtils.import_module(
            "vzmi.ychaos.some_unknown_module",
            message="mock warning message",
            raise_error=False,
        )
        self.assertIsNone(module)

    def test_import_invalid_module_raises_error(self):
        with self.assertRaises(ImportError):
            DependencyUtils.import_module(
                "vzmi.ychaos.some_unknown_module", raise_error=True
            )

    def test_import_valid_attr_from_valid_module(self):
        import_attrs = DependencyUtils.import_from(
            "vzmi.ychaos.utils.dependency", ("DependencyUtils",), raise_error=False
        )
        self.assertIsInstance(import_attrs, tuple)
        for attr in import_attrs:
            self.assertIsNotNone(attr)

    def test_import_invalid_attr_from_valid_module(self):
        handler_class = DependencyUtils.import_from(
            "vzmi.ychaos.utils.dependency", ("SomeUnknownAttribute",), raise_error=False
        )
        self.assertTupleEqual((None,), handler_class)

    def test_import_invalid_attr_from_valid_module_with_custom_message(self):
        handler_class = DependencyUtils.import_from(
            "vzmi.ychaos.utils.dependency",
            ("SomeUnknownAttribute",),
            message="mock import warning",
            raise_error=False,
        )
        self.assertTupleEqual((None,), handler_class)

    def test_import_invalid_attr_from_valid_module_raises_error(self):
        with self.assertRaises(ImportError):
            DependencyUtils.import_from(
                "vzmi.ychaos.utils.dependency",
                ("SomeUnknownAttribute",),
                raise_error=True,
            )

    def test_import_attr_from_invalid_module(self):
        handler_class = DependencyUtils.import_from(
            "vzmi.ychaos.some_unknown_module",
            ("SomeUnknownAttribute",),
            raise_error=False,
        )
        self.assertTupleEqual((None,), handler_class)
