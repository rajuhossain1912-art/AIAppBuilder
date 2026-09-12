from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.android.app_spec_builder import AndroidBuildIntent


class AndroidFeatureGenerationError(ValueError):
    """Raised when a feature cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedAndroidFeatures:
    files: tuple[str, ...]
    family: str


class AndroidFeatureGenerator:
    """Generate dependency-light, deterministic first-class Android features."""

    def generate(self, project_root: str | Path, intent: AndroidBuildIntent) -> GeneratedAndroidFeatures:
        if not isinstance(intent, AndroidBuildIntent):
            raise TypeError("intent must be an AndroidBuildIntent")
        root = Path(project_root).resolve()
        if not root.is_dir():
            raise AndroidFeatureGenerationError("project_root must be an existing directory")

        package_path = Path(*intent.spec.package_name.split("."))
        activity = root / "app" / "src" / "main" / "java" / package_path / "MainActivity.java"
        if not activity.is_file():
            raise AndroidFeatureGenerationError("generated Android project is missing MainActivity.java")

        content = self._activity(intent)
        activity.write_text(content, encoding="utf-8")
        return GeneratedAndroidFeatures(
            files=(str(activity.relative_to(root)),),
            family=intent.family,
        )

    @staticmethod
    def _activity(intent: AndroidBuildIntent) -> str:
        package = intent.spec.package_name
        title = _java(intent.spec.project_name)
        if intent.family == "utility":
            body = _calculator_body(title)
        elif intent.family == "form":
            body = _form_body(title)
        elif intent.family == "database":
            body = _record_body(title)
        elif intent.family == "content":
            body = _content_body(title)
        elif intent.family == "api_client":
            body = _api_body(title)
        else:
            body = _general_body(title)
        return f"package {package};\n\n{body}\n"


def _java(value: str) -> str:
    return (value or "AI App").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def _common_imports() -> str:
    return """import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
"""


def _calculator_body(title: str) -> str:
    return _common_imports() + f"""
public final class MainActivity extends Activity {{
    private TextView result;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout root = base("{title}");
        EditText first = input("First number");
        EditText second = input("Second number");
        root.addView(first);
        root.addView(second);
        result = label("Result: ");
        root.addView(result);
        Button add = button("Add");
        add.setOnClickListener(v -> calculate(first, second));
        root.addView(add);
        setContentView(root);
    }}

    private void calculate(EditText first, EditText second) {{
        try {{
            double a = Double.parseDouble(first.getText().toString().trim());
            double b = Double.parseDouble(second.getText().toString().trim());
            result.setText("Result: " + (a + b));
        }} catch (NumberFormatException error) {{
            result.setText("Please enter valid numbers");
        }}
    }}

{_helpers()}
}}
"""


def _form_body(title: str) -> str:
    return _common_imports() + f"""
public final class MainActivity extends Activity {{
    private TextView status;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout root = base("{title}");
        EditText name = input("Name");
        EditText details = input("Details");
        root.addView(name);
        root.addView(details);
        status = label("Ready");
        root.addView(status);
        Button submit = button("Submit");
        submit.setOnClickListener(v -> {{
            if (name.getText().toString().trim().isEmpty()) {{
                status.setText("Name is required");
                name.requestFocus();
                return;
            }}
            status.setText("Saved: " + name.getText().toString().trim());
        }});
        root.addView(submit);
        setContentView(root);
    }}

{_helpers()}
}}
"""


def _record_body(title: str) -> str:
    return _common_imports() + f"""
public final class MainActivity extends Activity {{
    private final java.util.ArrayList<String> records = new java.util.ArrayList<>();
    private TextView list;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout root = base("{title}");
        EditText value = input("Record");
        root.addView(value);
        list = label("No records yet");
        root.addView(list);
        Button add = button("Add record");
        add.setOnClickListener(v -> {{
            String item = value.getText().toString().trim();
            if (!item.isEmpty()) {{
                records.add(item);
                value.setText("");
                refresh();
            }}
        }});
        root.addView(add);
        setContentView(root);
    }}

    private void refresh() {{
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < records.size(); i++) text.append(i + 1).append(". ").append(records.get(i)).append("\\n");
        list.setText(text.toString());
    }}

{_helpers()}
}}
"""


def _content_body(title: str) -> str:
    return _common_imports() + f"""
public final class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout root = base("{title}");
        TextView content = label("Welcome. This content screen is ready for verified project-specific content.");
        root.addView(content);
        Button more = button("Show more");
        more.setOnClickListener(v -> content.setText("Content loaded successfully."));
        root.addView(more);
        setContentView(root);
    }}

{_helpers()}
}}
"""


def _api_body(title: str) -> str:
    return _common_imports() + f"""
public final class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout root = base("{title}");
        TextView status = label("API mode is enabled. Network implementation requires an approved endpoint and response contract.");
        root.addView(status);
        Button check = button("Check configuration");
        check.setOnClickListener(v -> status.setText("Configuration check complete. No endpoint was invented."));
        root.addView(check);
        setContentView(root);
    }}

{_helpers()}
}}
"""


def _general_body(title: str) -> str:
    return _common_imports() + f"""
public final class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout root = base("{title}");
        TextView status = label("Project shell ready. Requested features must be specified before they are invented.");
        root.addView(status);
        Button action = button("Continue");
        action.setOnClickListener(v -> status.setText("Ready"));
        root.addView(action);
        setContentView(root);
    }}

{_helpers()}
}}
"""


def _helpers() -> str:
    return """    private LinearLayout base(String title) {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(32, 32, 32, 32);
        TextView heading = label(title);
        heading.setTextSize(24);
        root.addView(heading);
        return root;
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
        field.setInputType(1);
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
