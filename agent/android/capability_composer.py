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
    })

    def compose(self, intent: AndroidBuildIntent) -> ComposedAndroidScreen:
        capabilities = tuple(intent.capabilities) or ("general",)
        sections: list[str] = []
        imports = {
            "import android.app.Activity;",
            "import android.content.Intent;",
            "import android.net.Uri;",
            "import android.os.Bundle;",
            "import android.view.ViewGroup;",
            "import android.widget.Button;",
            "import android.widget.EditText;",
            "import android.widget.ImageView;",
            "import android.widget.LinearLayout;",
            "import android.widget.TextView;",
            "import android.widget.VideoView;",
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
        variable = name.replace("-", "_")
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
        EditText name = input("Name");
        root.addView(name);
        Button submit = button("Submit");
        submit.setOnClickListener(v -> {
            String value = name.getText().toString().trim();
            if (value.isEmpty()) { status.setText("Name is required"); name.requestFocus(); return; }
            status.setText("Saved: " + value);
        });
        root.addView(submit);'''

        if capability == "calendar":
            block += '''
        Button today = button("Show today's date");
        today.setOnClickListener(v -> status.setText(java.time.LocalDate.now().toString()));
        root.addView(today);'''

        if capability in {"text_content", "profile", "business", "education", "sports"}:
            block += '''
        EditText content = input("Write content");
        content.setSingleLine(false);
        root.addView(content);
        Button save = button("Save content");
        save.setOnClickListener(v -> status.setText("Content saved in this session"));
        root.addView(save);'''

        if capability in {"news", "online_service"}:
            block += '''
        EditText address = input("Web address");
        root.addView(address);
        Button open = button("Open online service");
        open.setOnClickListener(v -> {
            String value = address.getText().toString().trim();
            if (!value.startsWith("https://") && !value.startsWith("http://")) {
                status.setText("Enter a valid web address");
                return;
            }
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(value)));
        });
        root.addView(open);'''

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

        if capability in {"music", "instrument"}:
            block += '''
        TextView noteHelp = label("Playable tone instrument. Each button produces a synthesized note.");
        root.addView(noteHelp);
        LinearLayout notes = new LinearLayout(this);
        notes.setOrientation(LinearLayout.VERTICAL);
        String[] names = {"C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"};
        double[] frequencies = {261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25};
        for (int i = 0; i < names.length; i++) {
            final double frequency = frequencies[i];
            Button note = button(names[i]);
            note.setOnClickListener(v -> playTone(frequency, 260));
            notes.addView(note);
        }
        root.addView(notes);'''
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
