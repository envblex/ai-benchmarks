import unittest
import subprocess
import shutil

class TestAgyEngine(unittest.TestCase):
    def test_agy_cli_installed(self):
        agy_path = shutil.which("agy") or "/home/takayoshi/.local/bin/agy"
        res = subprocess.run(["which", agy_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("agy", res.stdout)

    def test_agy_gpt_oss_smoke(self):
        agy_path = shutil.which("agy") or "/home/takayoshi/.local/bin/agy"
        cmd = [agy_path, "--model", "gpt-oss-120b-medium", "--dangerously-skip-permissions", "-p", "Respond only with: READY"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        self.assertEqual(res.returncode, 0)
        self.assertIn("READY", res.stdout)

if __name__ == "__main__":
    unittest.main()
