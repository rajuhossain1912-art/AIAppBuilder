from pathlib import Path
import tempfile

from agent.android import AndroidProjectGenerator
from agent.templates.android_template import AndroidProjectSpec


def test_generates_real_android_project_files() -> None:
    with tempfile.TemporaryDirectory() as temp:
        spec = AndroidProjectSpec(
            project_name="Accessible Demo",
            package_name="com.example.accessibledemo",
            mode="hybrid",
        )
        result = AndroidProjectGenerator().generate(Path(temp) / "project", spec)
        assert "settings.gradle" in result.files
        assert "app/build.gradle" in result.files
        assert "app/src/main/AndroidManifest.xml" in result.files
        activity = Path(temp) / "project/app/src/main/java/com/example/accessibledemo/MainActivity.java"
        assert activity.is_file()
        text = activity.read_text(encoding="utf-8")
        assert "setContentDescription" in text


def test_refuses_non_empty_destination() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / "project"
        root.mkdir()
        (root / "existing.txt").write_text("keep", encoding="utf-8")
        spec = AndroidProjectSpec("Demo App", "com.example.demo")
        try:
            AndroidProjectGenerator().generate(root, spec)
        except ValueError as exc:
            assert "empty" in str(exc)
        else:
            raise AssertionError("generator must refuse a non-empty destination")
