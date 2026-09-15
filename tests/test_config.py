import unittest
import tempfile
import os
from stackforge.core.config import StackConfig
from stackforge.core.validator import ConfigValidator

class TestConfig(unittest.TestCase):
    def test_save_and_load_config(self):
        config = StackConfig(
            project_name="custom-stack",
            backend="rust_axum",
            frontend="vue_vite",
            database="redis",
            pipeline="azure_devops",
            docker=True,
            k8s=False
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = os.path.join(tmpdir, "stackforge.json")
            config.save_to_file(cfg_path)
            self.assertTrue(os.path.exists(cfg_path))

            loaded = StackConfig.load_from_file(cfg_path)
            self.assertEqual(loaded.project_name, "custom-stack")
            self.assertEqual(loaded.backend, "rust_axum")
            self.assertEqual(loaded.frontend, "vue_vite")
            self.assertEqual(loaded.database, "redis")
            self.assertEqual(loaded.pipeline, "azure_devops")
            self.assertFalse(loaded.k8s)

    def test_validator_detects_invalid_names(self):
        invalid_config = StackConfig(project_name="invalid name with spaces!")
        errors, _ = ConfigValidator.validate(invalid_config)
        self.assertGreater(len(errors), 0)

if __name__ == "__main__":
    unittest.main()
