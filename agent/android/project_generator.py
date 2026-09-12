from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import xml.sax.saxutils as xml_utils

from agent.templates.android_template import AndroidProjectSpec


class AndroidProjectGenerationError(ValueError):
    """Raised when an Android project cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedAndroidProject:
    root: Path
    files: tuple[str, ...]


class AndroidProjectGenerator:
    """Generates a deterministic, dependency-light Android starter project."""

    def generate(self, output_root: str | Path, spec: AndroidProjectSpec) -> GeneratedAndroidProject:
        if not isinstance(spec, AndroidProjectSpec):
            raise TypeError("spec must be an AndroidProjectSpec")

        root = Path(output_root).resolve()
        if root.exists() and any(root.iterdir()):
            raise AndroidProjectGenerationError("output_root must be empty when generating a new project")
        root.mkdir(parents=True, exist_ok=True)

        package_path = Path(*spec.package_name.split("."))
        files: dict[str, str] = {
            "settings.gradle": self._settings(spec.project_name),
            "build.gradle": self._root_build_gradle(),
            "gradle.properties": "org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\n",
            "app/build.gradle": self._app_build_gradle(spec.package_name, spec.min_sdk, spec.target_sdk),
            "app/src/main/AndroidManifest.xml": self._manifest(spec.package_name, spec.mode),
            f"app/src/main/java/{package_path}/MainActivity.java": self._activity(spec),
            "app/src/main/res/values/strings.xml": self._strings(spec.project_name),
            "app/src/main/res/values/colors.xml": self._colors(),
            "app/src/main/res/values/themes.xml": self._themes(),
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
        return (
            "import org.gradle.api.initialization.resolve.RepositoriesMode\n\n"
            "pluginManagement {\n"
            "    repositories { google(); mavenCentral(); gradlePluginPortal() }\n"
            "}\n"
            "dependencyResolutionManagement {\n"
            "    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)\n"
            "    repositories { google(); mavenCentral() }\n"
            "}\n"
            f'rootProject.name = "{safe}"\n'
            'include(":app")\n'
        )

    @staticmethod
    def _root_build_gradle() -> str:
        return 'plugins {\n    id "com.android.application" version "8.7.3" apply false\n}\n'

    @staticmethod
    def _app_build_gradle(package_name: str, min_sdk: int, target_sdk: int) -> str:
        return f'''plugins {{
    id "com.android.application"
}}

android {{
    namespace "{package_name}"
    compileSdk {target_sdk}

    defaultConfig {{
        applicationId "{package_name}"
        minSdk {min_sdk}
        targetSdk {target_sdk}
        versionCode 1
        versionName "1.0"
    }}
}}
'''

    @staticmethod
    def _manifest(package_name: str, mode: str) -> str:
        permission = '    <uses-permission android:name="android.permission.INTERNET" />\n' if mode in {"online", "hybrid"} else ""
        return f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
{permission}    <application
        android:allowBackup="false"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
'''

    @staticmethod
    def _activity(spec: AndroidProjectSpec) -> str:
        title = spec.project_name.replace('\\', '\\\\').replace('"', '\\"')
        return f'''package {spec.package_name};

import android.app.Activity;
import android.os.Bundle;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public final class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(32, 32, 32, 32);

        TextView title = new TextView(this);
        title.setText("{title}");
        title.setTextSize(24);
        title.setContentDescription("{title}");
        root.addView(title, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        Button action = new Button(this);
        action.setText("Continue");
        action.setContentDescription("Continue");
        action.setOnClickListener(v -> title.setText("Ready for feature implementation"));
        root.addView(action, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        setContentView(root);
    }}
}}
'''

    @staticmethod
    def _strings(name: str) -> str:
        safe = xml_utils.escape(name, {'"': '&quot;'})
        return f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{safe}</string>
</resources>
'''

    @staticmethod
    def _colors() -> str:
        return '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="primary">#3F51B5</color>\n</resources>\n'

    @staticmethod
    def _themes() -> str:
        return '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <style name="AppTheme" parent="android:style/Theme.Material.Light.NoActionBar">\n        <item name="android:fontFamily">sans</item>\n        <item name="android:windowActionModeOverlay">true</item>\n    </style>\n</resources>\n'

    @staticmethod
    def _generated_readme(spec: AndroidProjectSpec) -> str:
        return f'''# Generated Android project

Project: {spec.project_name}
Package: {spec.package_name}
Mode: {spec.mode}
Minimum SDK: {spec.min_sdk}
Target SDK: {spec.target_sdk}
Accessibility required: {spec.accessibility_required}

This project is a verified starter baseline. It must not be marked complete until the requested features, build, tests, and verification have all succeeded.
'''
