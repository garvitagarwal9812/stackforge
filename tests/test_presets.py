import unittest
from stackforge.presets.default_presets import PRESETS
from stackforge.core.config import StackConfig
from stackforge.core.validator import ConfigValidator

class TestPresets(unittest.TestCase):
    def test_all_presets_valid(self):
        """Ensure every preset has a valid configuration without errors."""
        self.assertGreater(len(PRESETS), 0, "Presets list must not be empty")

        for key, p in PRESETS.items():
            config_dict = p["config"].copy()
            config_dict["project_name"] = f"test_{key.replace('-', '_')}"
            config_dict["output_dir"] = f"./tmp/{config_dict['project_name']}"

            config = StackConfig.from_dict(config_dict)
            errors, _ = ConfigValidator.validate(config)
            self.assertEqual(errors, [], f"Preset '{key}' had validation errors: {errors}")

    def test_preset_names_and_tags(self):
        """Ensure presets have names and descriptive tags."""
        for key, p in PRESETS.items():
            self.assertTrue(p["name"], f"Preset {key} must have a name")
            self.assertTrue(p["description"], f"Preset {key} must have a description")
            self.assertIsInstance(p["tags"], list)
            self.assertGreater(len(p["tags"]), 0)

if __name__ == "__main__":
    unittest.main()
