from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from agent.templates.android_template import AndroidProjectSpec


class AndroidProjectGenerationError(ValueError):
    """Raised when an Android project cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedAndroidProject:
    root: Path
    files: tuple[str, ...]


class AndroidProjectGenerator:
    """Generates a deterministic, dependency-light Android starter project.

    This is a real project skeleton, not a claim that arbitrary natural-language
    requirements have already been implemented. Feature generation can build on
    this verified baseline in later stages.
    """

    def generate(self, output_root: str | Path, spec: AndroidProjectSpec) -> GeneratedAndroidProject:
        if not isinstance(spec, AndroidProjectSpec):
            raise TypeError("spec must be an AndroidProjectSpec")

        root = Path(output_root).resolve()
        if root.exists() and any(root.iterdir()):
            raise AndroidProjectGenerationError("output_root must be empty when generating a new project")
        root.mkdir(parents=True, exist_ok=True)

        package_path = Path(*spec.package_name.split("."))
        app_id = spec.package_name
        files: dict[str, str] = {
            "settings.gradle": self._settings(spec.project_name),
            "build.gradle": self._root_build_gradle(),
            "gradle.properties": "org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\n",
            "app/build.gradle": self._app_build_gradle(app_id, spec.min_sdk, spec.target_sdk),
            "app/src/main/AndroidManifest.xml": self._manifest(app_id, spec.mode),
            f"app/src/main/java/{package_path}/MainActivity.java": self._activity(spec),
            "app/src/main/res/values/strings.xml": self._strings(spec.project_name),
            "app/src/main/res/values/colors.xml": self._colors(),
            "app/src/main/res/values/themes.xml": self._themes(),
            "app/src/main/res/values/styles.xml": self._styles(),
            "README.generated.md": self._generated_readme(spec),
        }

        for relative, content in files.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        return GeneratedAndroidProject(root=root, files=tuple(files))

    @staticmethod
    def _settings(name: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", name.strip())
        return f'pluginManagement {{ repositories {{ google(); mavenCentral(); gradlePluginPortal() }} }}\ndependencyResolutionManagement {{ repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories {{ google(); mavenCentral() }} }}\nrootProject.name = "{safe}"\ninclude(":app")\n'

    @staticmethod
    def _root_build_gradle() -> str:
        return 'plugins {\n    id "com.android.application" version "8.7.3" apply false\n}\n'

    @staticmethod
    def _app_build_gradle(package_name: str, min_sdk: int, target_sdk: int) -> str:
        return f'''plugins {{\n    id "com.android.application"\n}}\n\nandroid {{\n    namespace "{package_name}"\n    compileSdk 35\n\n    defaultConfig {{\n        applicationId "{package_name}"\n        minSdk {min_sdk}\n        targetSdk {target_sdk}\n        versionCode 1\n        versionName "1.0"\n    }}\n}}\n'''

    @staticmethod
    def _manifest(package_name: str, mode: str) -> str:
        permission = '    <uses-permission android:name="android.permission.INTERNET" />\n' if mode in {"online", "hybrid"} else ""
        return f'''<?xml version="1.0" encoding="utf-8"?>\n<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n{permission}    <application\n        android:allowBackup="false"\n        android:label="@string/app_name"\n        android:supportsRtl="true"\n        android:theme="@style/AppTheme">\n        <activity android:name=".MainActivity" android:exported="true">\n            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>\n'''

    @staticmethod
    def _activity(spec: AndroidProjectSpec) -> str:
        title = spec.project_name.replace('"', '\\"')
        return f'''package {spec.package_name};\n\nimport android.app.Activity;\nimport android.os.Bundle;\nimport android.view.ViewGroup;\nimport android.widget.Button;\nimport android.widget.LinearLayout;\nimport android.widget.TextView;\n\npublic final class MainActivity extends Activity {{\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {{\n        super.onCreate(savedInstanceState);\n\n        LinearLayout root = new LinearLayout(this);\n        root.setOrientation(LinearLayout.VERTICAL);\n        root.setPadding(32, 32, 32, 32);\n\n        TextView title = new TextView(this);\n        title.setText("{title}");\n        title.setTextSize(24);\n        title.setContentDescription("{title}");\n        root.addView(title, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));\n\n        Button action = new Button(this);\n        action.setText("Continue");\n        action.setContentDescription("Continue");\n        action.setOnClickListener(v -> title.setText("Ready for feature implementation"));\n        root.addView(action, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));\n\n        setContentView(root);\n    }}\n}}\n'''

    @staticmethod
    def _strings(name: str) -> str:
        safe = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;').replace("'", "\\'")
        return f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <string name="app_name">{safe}</string>\n</resources>\n'

    @staticmethod
    def _colors() -> str:
        return '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="primary">#3F51B5</color>\n</resources>\n'

    @staticmethod
    def _themes() -> str:
        return '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <style name="AppTheme" parent="android:style/Theme.Material.Light.NoActionBar">\n        <item name="android:fontFamily">sans</item>\n        <item name="android:windowActionModeOverlay">true</item>\n    </style>\n</resources>\n'

    @staticmethod
    def _styles() -> str:
        return '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <style name="AppTheme.NoActionBar" parent="android:style/Theme.Material.Light.NoActionBar" />\n</resources>\n'

    @staticmethod
    def _generated_readme(spec: AndroidProjectSpec) -> str:
        return f'''# Generated Android project\n\nProject: {spec.project_name}\nPackage: {spec.package_name}\nMode: {spec.mode}\nMinimum SDK: {spec.min_sdk}\nTarget SDK: {spec.target_sdk}\nAccessibility required: {spec.accessibility_required}\n\nThis project is a verified starter baseline. It must not be marked complete until the requested features, build, tests, and verification have all succeeded.\n'''
