from __future__ import annotations

from dataclasses import dataclass

from agent.android.app_spec_builder import AndroidBuildIntent


@dataclass(frozen=True)
class ComposedAndroidScreen:
    """Java source assembled from all requested capabilities, not one family."""

    source: str
    capabilities: tuple[str, ...]
    implemented_capabilities: tuple[str, ...] = ()
    unsupported_capabilities: tuple[str, ...] = ()


class AndroidCapabilityComposer:
    """Compose a dependency-light Android activity from a capability set.

    A capability is marked implemented only when generated code contains a
    usable local Android implementation. Labels alone never count as a feature.
    """

    IMPLEMENTED_CAPABILITIES = frozenset({
        "calculator", "audio", "forms_data", "calendar", "general",
        "text_content", "profile", "business", "education", "sports",
        "news", "online_service", "image", "video", "music", "instrument",
        "typing_keyboard",
    })

    def compose(self, intent: AndroidBuildIntent) -> ComposedAndroidScreen:
        # A planner may contribute the same capability more than once. Generate
        # each capability section once so Java local variables never collide.
        capabilities = tuple(dict.fromkeys(intent.capabilities)) or ("general",)
        sections: list[str] = []
        imports = {
            "import android.app.Activity;",
            "import android.content.Intent;",
            "import android.net.Uri;",
            "import android.os.Bundle;",
            "import android.view.ViewGroup;",
            "import android.widget.Button;",
            "import android.widget.EditText;",
            "import android.widget.LinearLayout;",
            "import android.widget.TextView;",
        }
        state: list[str] = []
        methods: list[str] = []

        for capability in capabilities:
            block, extra_imports, extra_state, extra_methods = self._section(capability)
            sections.append(block)
            imports.update(extra_imports)
            state.extend(extra_state)
            methods.extend(extra_methods)

        if "audio" in capabilities:
            imports.add("import android.speech.tts.TextToSpeech;")
        if "music" in capabilities or "instrument" in capabilities:
            imports.add("import android.media.AudioFormat;")
            imports.add("import android.media.AudioManager;")
            imports.add("import android.media.AudioTrack;")

        implemented = tuple(capability for capability in capabilities if capability in self.IMPLEMENTED_CAPABILITIES)
        unsupported = tuple(capability for capability in capabilities if capability not in self.IMPLEMENTED_CAPABILITIES)

        package = intent.spec.package_name
        title = _java(intent.spec.project_name)
        source = f"package {package};\n\n" + "\n".join(sorted(imports)) + "\n\n"
        source += "public final class MainActivity extends Activity {\n"
        source += "    private LinearLayout root;\n    private TextView status;\n"
        for line in dict.fromkeys(state):
            source += f"    {line}\n"
        source += "\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n"
        source += "        super.onCreate(savedInstanceState);\n"
        source += f'        root = base("{title}");\n        status = label("Ready");\n        root.addView(status);\n'
        if "audio" in capabilities:
            source += '        tts = new TextToSpeech(this, result -> { if (result == TextToSpeech.SUCCESS) tts.setLanguage(java.util.Locale.getDefault()); });\n'
        source += "\n".join(f"        {line}" for line in sections) + "\n"
        source += "        setContentView(root);\n    }\n\n"
        if "audio" in capabilities:
            source += """    @Override
    protected void onDestroy() {
        if (tts != null) tts.shutdown();
        super.onDestroy();
    }

"""
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

    private Button keyButton(String label, EditText target) {
        Button key = button(label);
        key.setOnClickListener(v -> {
            int start = Math.max(0, target.getSelectionStart());
            int end = Math.max(start, target.getSelectionEnd());
            target.getText().replace(start, end, label);
            target.requestFocus();
            status.setText("Inserted " + label);
        });
        return key;
    }

"""
        source += "\n".join(dict.fromkeys(methods))
        source += "\n}\n"
        return ComposedAndroidScreen(source, capabilities, implemented, unsupported)

    @staticmethod
    def _section(capability: str) -> tuple[str, set[str], list[str], list[str]]:
        if capability == "calculator":
            return ("""EditText first = input("First number");
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
        root.addView(calculate);""", set(), [], [])

        labels = {
            "audio": "Audio and voice", "video": "Video", "image": "Image",
            "news": "News and newspaper", "education": "Education and scholarship",
            "sports": "Sports", "profile": "Profile and portfolio",
            "business": "Business and merchant", "text_content": "Text and content",
            "forms_data": "Forms and data", "online_service": "Online service",
            "calendar": "Calendar", "music": "Music and composition",
            "instrument": "Virtual musical instrument", "typing_keyboard": "Typing keyboard",
            "general": "General application",
        }
        name = capability if capability in labels else "general"
        # Use the actual capability key for the Java local name. This prevents
        # unknown capabilities (which fall back to the General label) from
        # colliding with an explicit general capability.
        variable = "section_" + "".join(character if character.isalnum() else "_" for character in capability)
        block = f'''TextView {variable} = label("{labels[name]}");
        root.addView({variable});'''

        if capability == "audio":
            block += '''
        EditText voiceText = input("Text to speak");
        root.addView(voiceText);
        Button speak = button("Speak");
        speak.setOnClickListener(v -> speakText(voiceText.getText().toString()));
        root.addView(speak);'''
            return block, set(), ["private TextToSpeech tts;"], ["""    private void speakText(String text) {
        if (tts == null) { status.setText("Text to speech is not ready"); return; }
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "aiappbuilder");
        status.setText("Speaking");
    }
"""]

        if capability == "forms_data":
            block += '''
        EditText formName = input("Name");
        root.addView(formName);
        Button submit = button("Submit");
        submit.setOnClickListener(v -> {
            String value = formName.getText().toString().trim();
            if (value.isEmpty()) { status.setText("Name is required"); formName.requestFocus(); return; }
            status.setText("Saved: " + value);
        });
        root.addView(submit);'''

        if capability == "calendar":
            block += '''
        Button today = button("Show today's date");
        today.setOnClickListener(v -> status.setText(java.time.LocalDate.now().toString()));
        root.addView(today);'''

        if capability in {"text_content", "profile", "business", "education", "sports"}:
            suffix = capability.replace("_", "")
            block += f'''
        EditText {suffix}Content = input("Write content");
        {suffix}Content.setSingleLine(false);
        root.addView({suffix}Content);
        Button {suffix}Save = button("Save content");
        {suffix}Save.setOnClickListener(v -> status.setText("Content saved in this session"));
        root.addView({suffix}Save);'''

        if capability in {"news", "online_service"}:
            suffix = capability.replace("_", "")
            block += f'''
        EditText {suffix}Address = input("Web address");
        root.addView({suffix}Address);
        Button {suffix}Open = button("Open online service");
        {suffix}Open.setOnClickListener(v -> {{
            String value = {suffix}Address.getText().toString().trim();
            if (!value.startsWith("https://") && !value.startsWith("http://")) {{
                status.setText("Enter a valid web address");
                return;
            }}
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(value)));
        }});
        root.addView({suffix}Open);'''

        if capability == "image":
            block += '''
        Button pickImage = button("Choose image");
        pickImage.setOnClickListener(v -> startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("image/*").addCategory(Intent.CATEGORY_OPENABLE), 100));
        root.addView(pickImage);'''

        if capability == "video":
            block += '''
        Button pickVideo = button("Choose video");
        pickVideo.setOnClickListener(v -> startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("video/*").addCategory(Intent.CATEGORY_OPENABLE), 101));
        root.addView(pickVideo);'''

        if capability == "typing_keyboard":
            block += '''
        EditText typingTarget = input("Type here");
        typingTarget.setSingleLine(false);
        root.addView(typingTarget);
        LinearLayout englishKeys = new LinearLayout(this);
        englishKeys.setOrientation(LinearLayout.VERTICAL);
        String[] englishRows = {"Q W E R T Y U I O P", "A S D F G H J K L", "Z X C V B N M"};
        for (String rowText : englishRows) {
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            for (String keyLabel : rowText.split(" ")) {
                row.addView(keyButton(keyLabel, typingTarget));
            }
            englishKeys.addView(row);
        }
        root.addView(englishKeys);
        LinearLayout banglaKeys = new LinearLayout(this);
        banglaKeys.setOrientation(LinearLayout.HORIZONTAL);
        String[] banglaLabels = {"অ", "আ", "ই", "উ", "এ", "ও", "ক", "খ", "গ", "ম", "য", "র"};
        for (String keyLabel : banglaLabels) {
            banglaKeys.addView(keyButton(keyLabel, typingTarget));
        }
        root.addView(banglaKeys);
        Button spaceKey = keyButton(" ", typingTarget);
        spaceKey.setContentDescription("Space");
        root.addView(spaceKey);
        Button backspaceKey = button("Backspace");
        backspaceKey.setOnClickListener(v -> {
            int start = typingTarget.getSelectionStart();
            int end = typingTarget.getSelectionEnd();
            if (start > 0 && start == end) {
                typingTarget.getText().delete(start - 1, start);
            } else if (start != end) {
                typingTarget.getText().delete(Math.min(start, end), Math.max(start, end));
            }
            typingTarget.requestFocus();
            status.setText("Backspace");
        });
        root.addView(backspaceKey);'''

        if capability in {"music", "instrument"}:
            suffix = capability.replace("_", "")
            block += f'''
        TextView {suffix}NoteHelp = label("Playable tone instrument. Each button produces a synthesized note.");
        root.addView({suffix}NoteHelp);
        LinearLayout {suffix}Notes = new LinearLayout(this);
        {suffix}Notes.setOrientation(LinearLayout.VERTICAL);
        String[] {suffix}Names = {{"C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"}};
        double[] {suffix}Frequencies = {{261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25}};
        for (int i = 0; i < {suffix}Names.length; i++) {{
            final double frequency = {suffix}Frequencies[i];
            Button {suffix}Note = button({suffix}Names[i]);
            {suffix}Note.setOnClickListener(v -> playTone(frequency, 260));
            {suffix}Notes.addView({suffix}Note);
        }}
        root.addView({suffix}Notes);'''
            return block, set(), [], ["""    private void playTone(double frequency, int durationMs) {
        final int sampleRate = 44100;
        final int sampleCount = (int) (sampleRate * durationMs / 1000.0);
        final short[] samples = new short[sampleCount];
        for (int i = 0; i < sampleCount; i++) {
            double envelope = Math.min(1.0, Math.min(i / 500.0, (sampleCount - i) / 500.0));
            samples[i] = (short) (Math.sin(2.0 * Math.PI * frequency * i / sampleRate) * 12000 * envelope);
        }
        AudioTrack track = new AudioTrack(AudioManager.STREAM_MUSIC, sampleRate,
                AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT,
                samples.length * 2, AudioTrack.MODE_STATIC);
        track.write(samples, 0, samples.length);
        track.setNotificationMarkerPosition(sampleCount);
        track.setPlaybackPositionUpdateListener(new AudioTrack.OnPlaybackPositionUpdateListener() {
            @Override public void onMarkerReached(AudioTrack audioTrack) { audioTrack.release(); }
            @Override public void onPeriodicNotification(AudioTrack audioTrack) { }
        });
        track.play();
        status.setText("Playing tone " + frequency + " Hz");
    }
"""]

        return block, set(), [], []


def _java(value: str) -> str:
    return (value or "AI App").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
