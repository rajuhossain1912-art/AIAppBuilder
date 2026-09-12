from __future__ import annotations

from dataclasses import dataclass

from agent.android.app_spec_builder import AndroidBuildIntent


@dataclass(frozen=True)
class ComposedAndroidScreen:
    """Java source assembled from all requested capabilities, not one family."""

    source: str
    capabilities: tuple[str, ...]


class AndroidCapabilityComposer:
    """Compose a deterministic Android activity from a capability set."""

    def compose(self, intent: AndroidBuildIntent) -> ComposedAndroidScreen:
        capabilities = tuple(intent.capabilities) or ("general",)
        sections: list[str] = []
        imports = {
            "import android.app.Activity;",
            "import android.os.Bundle;",
            "import android.speech.tts.TextToSpeech;",
            "import android.view.ViewGroup;",
            "import android.widget.Button;",
            "import android.widget.EditText;",
            "import android.widget.LinearLayout;",
            "import android.widget.TextView;",
            "import java.util.Locale;",
        }
        state: list[str] = []
        methods: list[str] = []

        for capability in capabilities:
            block, extra_imports, extra_state, extra_methods = self._section(capability)
            sections.append(block)
            imports.update(extra_imports)
            state.extend(extra_state)
            methods.extend(extra_methods)

        package = intent.spec.package_name
        title = _java(intent.spec.project_name)
        source = f"package {package};\n\n" + "\n".join(sorted(imports)) + "\n\n"
        source += "public final class MainActivity extends Activity {\n"
        source += "    private LinearLayout root;\n"
        source += "    private TextView status;\n"
        for line in state:
            source += f"    {line}\n"
        source += "\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n"
        source += "        super.onCreate(savedInstanceState);\n"
        source += f'        root = base("{title}");\n        status = label("Ready");\n        root.addView(status);\n'
        source += "\n".join(f"        {line}" for line in sections) + "\n"
        source += "        setContentView(root);\n    }\n\n"
        source += """    private LinearLayout base(String title) {
        LinearLayout view = new LinearLayout(this);
        view.setOrientation(LinearLayout.VERTICAL);
        view.setPadding(32, 32, 32, 32);
        TextView heading = label(title);
        heading.setTextSize(24);
        view.addView(heading);
        return view;
    }

    private TextView label(String text) {
        TextView view = new TextView(this);
        view.setText(text);
        view.setContentDescription(text);
        view.setTextSize(18);
        view.setPadding(0, 16, 0, 16);
        return view;
    }

    private EditText input(String hint) {
        EditText field = new EditText(this);
        field.setHint(hint);
        field.setContentDescription(hint);
        field.setSingleLine(true);
        field.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        return field;
    }

    private Button button(String text) {
        Button action = new Button(this);
        action.setText(text);
        action.setContentDescription(text);
        action.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        return action;
    }

"""
        source += "\n".join(methods)
        source += "\n}\n"
        return ComposedAndroidScreen(source=source, capabilities=capabilities)

    @staticmethod
    def _section(capability: str) -> tuple[str, set[str], list[str], list[str]]:
        if capability == "calculator":
            return (
                """EditText first = input("First number");
        EditText second = input("Second number");
        root.addView(first);
        root.addView(second);
        Button calculate = button("Calculate");
        calculate.setOnClickListener(v -> {
            try {
                double a = Double.parseDouble(first.getText().toString().trim());
                double b = Double.parseDouble(second.getText().toString().trim());
                status.setText("Result: " + (a + b));
            } catch (NumberFormatException error) {
                status.setText("Please enter valid numbers");
            }
        });
        root.addView(calculate);""",
                set(), [], [],
            )
        if capability in {"audio", "video", "image", "news", "education", "sports", "profile", "business", "text_content", "forms_data", "online_service", "calendar", "general"}:
            labels = {
                "audio": "Audio and voice capability",
                "video": "Video capability",
                "image": "Image capability",
                "news": "News and newspaper capability",
                "education": "Education and scholarship capability",
                "sports": "Sports capability",
                "profile": "Profile and portfolio capability",
                "business": "Business and merchant capability",
                "text_content": "Text and content capability",
                "forms_data": "Forms and data capability",
                "online_service": "Online service capability",
                "calendar": "Calendar capability",
                "general": "General application capability",
            }
            block = f'''TextView {capability.replace("-", "_")} = label("{labels[capability]} is included in this composed app.");
        root.addView({capability.replace("-", "_")});'''
            if capability == "audio":
                block += '''
        EditText voiceText = input("Text to speak");
        root.addView(voiceText);
        Button speak = button("Speak");
        speak.setOnClickListener(v -> speakText(voiceText.getText().toString()));
        root.addView(speak);'''
                return block, set(), ["private TextToSpeech tts;"], ["""    private void speakText(String text) {
        if (tts == null) {
            status.setText("Text to speech is not ready");
            return;
        }
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "aiappbuilder");
        status.setText("Speaking");
    }
"""]
            if capability == "calendar":
                block += '''
        Button today = button("Show today's date");
        today.setOnClickListener(v -> status.setText(java.time.LocalDate.now().toString()));
        root.addView(today);'''
            return block, set(), [], []
        return AndroidCapabilityComposer._section("general")


def _java(value: str) -> str:
    return (value or "AI App").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
