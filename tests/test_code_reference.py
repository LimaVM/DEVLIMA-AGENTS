import ast
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/document_code.py"
SPEC = importlib.util.spec_from_file_location("code_reference", SCRIPT)
reference = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reference)
CATALOG = json.loads(reference.CATALOG.read_text())


# Documentação: Define o tipo CodeReferenceTests e reúne o estado/contrato descrito para este
# módulo.
class CodeReferenceTests(unittest.TestCase):
    # Documentação: Verifica o cenário test_python_comments_preserve_ast_decorators_and_literal;
    # as condições e resultados esperados aparecem nos asserts.
    def test_python_comments_preserve_ast_decorators_and_literal(self):
        source = '''"""Module docstring stays the first statement."""
class Example:
    @staticmethod
    def value():
        text = """def not_a_function():

return literal data"""
        return text
'''
        updated, count = reference.annotate_text("example.py", source, CATALOG)
        self.assertEqual(2, count)
        self.assertEqual(ast.dump(ast.parse(source)), ast.dump(ast.parse(updated)))
        self.assertEqual(
            "Module docstring stays the first statement.", ast.get_docstring(ast.parse(updated))
        )
        self.assertEqual((updated, 0), reference.annotate_text("example.py", updated, CATALOG))

    # Documentação: Verifica o cenário
    # test_kotlin_comments_preserve_tokens_and_do_not_annotate_raw_strings; as condições e
    # resultados esperados aparecem nos asserts.
    def test_kotlin_comments_preserve_tokens_and_do_not_annotate_raw_strings(self):
        source = '''package test
class Example {
    fun value() = """fun notAFunction() {
    }
    """
}
fun topLevel() = "https://example.invalid/a//b"
'''
        updated, count = reference.annotate_text("example.kt", source, CATALOG)
        self.assertEqual(3, count)
        self.assertEqual(reference.kotlin_mask(source)[1], reference.kotlin_mask(updated)[1])
        symbols = [name for _, name, _ in reference.kotlin_symbols(source)]
        self.assertEqual(["Example", "Example.value", "topLevel"], symbols)
        self.assertEqual((updated, 0), reference.annotate_text("example.kt", updated, CATALOG))

    # Documentação: Verifica o cenário
    # test_all_lines_including_blank_and_literal_have_a_description; as condições e resultados
    # esperados aparecem nos asserts.
    def test_all_lines_including_blank_and_literal_have_a_description(self):
        source = 'value = """one\n\n# literal, not a comment\n"""\n\nassert value\n'
        rows, _ = reference.python_rows("example.py", source, CATALOG)
        self.assertEqual(list(range(1, 7)), [number for number, _, _ in rows])
        self.assertTrue(all(explanation for _, _, explanation in rows))
        self.assertIn("literal", rows[1][2])
        self.assertIn("literal", rows[2][2])
        self.assertIn("em branco", rows[4][2])
        page = reference.reference_page("example.py", source, CATALOG)
        self.assertEqual(6, page.count('<a id="L'))

    # Documentação: Verifica o cenário test_code_is_escaped_and_rendering_is_deterministic; as
    # condições e resultados esperados aparecem nos asserts.
    def test_code_is_escaped_and_rendering_is_deterministic(self):
        source = 'assert "<a|b>" != "&"\n'
        first = reference.reference_page("example.py", source, CATALOG)
        self.assertEqual(first, reference.reference_page("example.py", source, CATALOG))
        self.assertIn("&lt;a&#124;b&gt;", first)
        self.assertIn("&amp;", first)

    # Documentação: Verifica o cenário
    # test_inventory_excludes_ignored_private_files_and_identifies_binary; as condições e
    # resultados esperados aparecem nos asserts.
    def test_inventory_excludes_ignored_private_files_and_identifies_binary(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", folder], check=True)
            (root / ".gitignore").write_text(".env\n")
            (root / ".env").write_text("PRIVATE_VALUE=only-a-test-placeholder\n")
            (root / "example.py").write_text("value = 1\n")
            (root / "asset.bin").write_bytes(b"\0binary")
            subprocess.run(
                ["git", "add", ".gitignore", "example.py", "asset.bin"], cwd=root, check=True
            )
            sources, binaries = reference.inventory(root)
            self.assertNotIn(".env", sources)
            self.assertEqual(["asset.bin"], [item["path"] for item in binaries])
            self.assertIn("example.py", sources)

    # Documentação: Verifica o cenário
    # test_similar_api_names_and_resource_settings_keep_their_meaning; as condições e resultados
    # esperados aparecem nos asserts.
    def test_similar_api_names_and_resource_settings_keep_their_meaning(self):
        rows, _ = reference.kotlin_rows(
            "example.kt",
            'ContextCompat.startForegroundService(context, intent)\nText("Hello")\n',
            CATALOG,
        )
        self.assertIn("Solicita início do serviço", rows[0][2])
        self.assertNotIn("promove o serviço", rows[0][2])
        self.assertIn("Renderiza texto", rows[1][2])
        config, _ = reference.configuration_rows(
            "infra/docker-compose.yml", "mem_limit: 768m\n", CATALOG
        )
        self.assertIn("Limita memória", config[0][2])

    # Documentação: Verifica o cenário test_check_detects_source_or_reference_drift; as condições
    # e resultados esperados aparecem nos asserts.
    def test_check_detects_source_or_reference_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rendered, manifest = reference.rendered_reference(
                {"example.py": "value = 1\n"}, [], CATALOG
            )
            self.assertEqual(1, manifest["physical_lines"])
            for path, text in rendered.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            self.assertEqual([], reference.differences(root, rendered))
            changed, _ = reference.rendered_reference({"example.py": "value = 2\n"}, [], CATALOG)
            self.assertIn("docs/code/example.py.md", reference.differences(root, changed))
            (root / "docs/code/example.py.md").write_text("outdated reference")
            self.assertIn("docs/code/example.py.md", reference.differences(root, rendered))

    # Documentação: Verifica o cenário test_environment_guide_is_not_hidden_by_private_file_rules;
    # as condições e resultados esperados aparecem nos asserts.
    def test_environment_guide_is_not_hidden_by_private_file_rules(self):
        self.assertEqual(
            "docs/code/environment-example.md", str(reference.reference_path(".env.example"))
        )
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", folder], check=True)
            (root / ".gitignore").write_text(".env\n.env.*\n!.env.example\n")
            path = str(reference.reference_path(".env.example"))
            result = subprocess.run(
                ["git", "check-ignore", "--no-index", path],
                cwd=root,
                stdout=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(1, result.returncode)
        rendered, _ = reference.rendered_reference(
            {".env.example": "JWT_SECRET=placeholder\n"}, [], CATALOG
        )
        self.assertIn("docs/code/environment-example.md", rendered)
        self.assertIn("environment-example.md)", rendered["docs/code/README.md"])


if __name__ == "__main__":
    unittest.main()
