import unittest
import tempfile
import shutil
import os
from stackforge.core.config import StackConfig
from stackforge.core.generator import ProjectGenerator

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_fastapi_github_blueprint(self):
        """Test blueprint generation for FastAPI + React + PostgreSQL + GitHub Actions."""
        config = StackConfig(
            project_name="demo-app",
            backend="fastapi",
            frontend="react_vite",
            database="postgresql",
            pipeline="github_actions",
            docker=True,
            k8s=True,
            helm=True,
            terraform=True,
            output_dir=os.path.join(self.temp_dir, "demo-app")
        )

        gen = ProjectGenerator(config)
        blueprint = gen.compile_blueprint()

        # Check key files exist in blueprint
        self.assertIn("README.md", blueprint)
        self.assertIn("Makefile", blueprint)
        self.assertIn("docker-compose.yml", blueprint)
        self.assertIn(".github/workflows/ci.yml", blueprint)
        self.assertIn(".github/workflows/cd.yml", blueprint)
        self.assertIn(".github/workflows/security.yml", blueprint)
        self.assertIn("backend/app/main.py", blueprint)
        self.assertIn("backend/requirements.txt", blueprint)
        self.assertIn("frontend/src/App.tsx", blueprint)
        self.assertIn("database/init.sql", blueprint)
        self.assertIn("k8s/backend-deployment.yaml", blueprint)
        self.assertIn("helm/Chart.yaml", blueprint)
        self.assertIn("terraform/main.tf", blueprint)

    def test_actual_file_writing(self):
        """Test writing files to disk in a temporary directory."""
        target_path = os.path.join(self.temp_dir, "generated-project")
        config = StackConfig(
            project_name="generated-project",
            backend="express_ts",
            frontend="nextjs",
            database="mongodb",
            pipeline="gitlab_ci",
            docker=True,
            k8s=False,
            helm=False,
            output_dir=target_path
        )

        gen = ProjectGenerator(config)
        created_files, blueprint = gen.generate(dry_run=False)

        self.assertGreater(len(created_files), 10)
        self.assertTrue(os.path.exists(os.path.join(target_path, "README.md")))
        self.assertTrue(os.path.exists(os.path.join(target_path, ".gitlab-ci.yml")))
        self.assertTrue(os.path.exists(os.path.join(target_path, "backend", "package.json")))
        self.assertTrue(os.path.exists(os.path.join(target_path, "frontend", "package.json")))
        self.assertTrue(os.path.exists(os.path.join(target_path, "docker-compose.yml")))

    def test_go_service_pipeline(self):
        """Test Go service with Jenkinsfile."""
        config = StackConfig(
            project_name="go-service",
            backend="go_gin",
            frontend="none",
            database="postgresql",
            pipeline="jenkins",
            docker=True,
            k8s=True,
            output_dir=os.path.join(self.temp_dir, "go-service")
        )

        gen = ProjectGenerator(config)
        blueprint = gen.compile_blueprint()

        self.assertIn("Jenkinsfile", blueprint)
        self.assertIn("backend/main.go", blueprint)
        self.assertIn("backend/go.mod", blueprint)
        # Should not contain frontend
        self.assertFalse(any(k.startswith("frontend/") for k in blueprint.keys()))

if __name__ == "__main__":
    unittest.main()
