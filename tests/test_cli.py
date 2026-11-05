import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_quotes(self):
        for zone, options, expected in (
            ("local", [], "$8.00"),
            ("regional", [], "$11.00"),
            ("local", ["--service", "standard"], "$8.00"),
            ("regional", ["--service", "standard"], "$11.00"),
            ("local", ["--service", "express"], "$15.00"),
            ("regional", ["--service", "express"], "$18.00"),
        ):
            with self.subTest(zone=zone, options=options):
                result = subprocess.run(
                    [sys.executable, "-m", "warehouse.cli", "2", zone, *options],
                    capture_output=True, text=True, check=True,
                )
                self.assertEqual(result.stdout.strip(), expected)

    def test_unknown_service(self):
        result = subprocess.run(
            [sys.executable, "-m", "warehouse.cli", "2", "local",
             "--service", "overnight"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)
        self.assertEqual(result.stdout, "")
