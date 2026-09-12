from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioEditorGenerationResult:
    source: str
    operations: tuple[str, ...]


class AudioEditorGenerator:
    """Adds a real, dependency-free Android audio trim/split/export surface."""

    OPERATIONS = ("pick_audio", "preview", "trim", "split", "export")

    def augment(self, source: str) -> AudioEditorGenerationResult:
        if "class MainActivity" not in source:
            raise ValueError("MainActivity source is required")
        imports = """import android.media.MediaCodec;
import android.media.MediaExtractor;
import android.media.MediaFormat;
import android.media.MediaMuxer;
import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
"""
        source = self._add_imports(source, imports)
        marker = "        setContentView(root);"
        section = """        EditText audioStartMs = input("Start milliseconds");
        EditText audioEndMs = input("End milliseconds");
        root.addView(audioStartMs);
        root.addView(audioEndMs);
        Button pickAudioEditor = button("Choose audio");
        pickAudioEditor.setOnClickListener(v -> pickAudioForEditor());
        root.addView(pickAudioEditor);
        Button previewAudioEditor = button("Preview audio");
        previewAudioEditor.setOnClickListener(v -> previewSelectedAudio());
        root.addView(previewAudioEditor);
        Button trimAudioEditor = button("Trim and export");
        trimAudioEditor.setOnClickListener(v -> {
            long start = parseEditorTime(audioStartMs, 0L);
            long end = parseEditorTime(audioEndMs, -1L);
            if (end <= start) { status.setText("End time must be greater than start time"); return; }
            exportAudioRange(start, end, "trimmed_audio.m4a");
        });
        root.addView(trimAudioEditor);
        Button splitAudioEditor = button("Split at end time");
        splitAudioEditor.setOnClickListener(v -> {
            long split = parseEditorTime(audioEndMs, -1L);
            if (split <= 0) { status.setText("Enter a valid split time"); return; }
            exportAudioRange(0L, split, "audio_part_1.m4a");
            if (selectedAudioUri != null) exportAudioRange(split, Long.MAX_VALUE, "audio_part_2.m4a");
        });
        root.addView(splitAudioEditor);
"""
        source = source.replace(marker, section + marker, 1)
        methods = """    private android.net.Uri selectedAudioUri;
    private android.media.MediaPlayer editorPlayer;

    private void pickAudioForEditor() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("audio/*");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(intent, 7001);
        status.setText("Choose an audio file");
    }

    private void handleAudioActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 7001 && resultCode == RESULT_OK && data != null && data.getData() != null) {
            selectedAudioUri = data.getData();
            try { getContentResolver().takePersistableUriPermission(selectedAudioUri, Intent.FLAG_GRANT_READ_URI_PERMISSION); } catch (SecurityException ignored) { }
            status.setText("Audio selected");
        }
    }

    private void previewSelectedAudio() {
        if (selectedAudioUri == null) { status.setText("Choose an audio file first"); return; }
        try {
            if (editorPlayer != null) editorPlayer.release();
            editorPlayer = android.media.MediaPlayer.create(this, selectedAudioUri);
            if (editorPlayer == null) { status.setText("This audio format cannot be previewed"); return; }
            editorPlayer.setOnCompletionListener(player -> status.setText("Preview finished"));
            editorPlayer.start();
            status.setText("Playing audio preview");
        } catch (Exception error) { status.setText("Unable to preview audio"); }
    }

    private long parseEditorTime(EditText field, long fallback) {
        try { return Long.parseLong(field.getText().toString().trim()); }
        catch (NumberFormatException error) { return fallback; }
    }

    private void exportAudioRange(long startMs, long endMs, String name) {
        if (selectedAudioUri == null) { status.setText("Choose an audio file first"); return; }
        try {
            MediaExtractor extractor = new MediaExtractor();
            android.os.ParcelFileDescriptor descriptor = getContentResolver().openFileDescriptor(selectedAudioUri, "r");
            if (descriptor == null) throw new IOException("Unable to open audio");
            extractor.setDataSource(descriptor.getFileDescriptor());
            int audioTrack = -1;
            for (int i = 0; i < extractor.getTrackCount(); i++) {
                MediaFormat format = extractor.getTrackFormat(i);
                String mime = format.getString(MediaFormat.KEY_MIME);
                if (mime != null && mime.startsWith("audio/")) { audioTrack = i; break; }
            }
            if (audioTrack < 0) throw new IOException("No audio track");
            extractor.selectTrack(audioTrack);
            MediaFormat format = extractor.getTrackFormat(audioTrack);
            File output = new File(getExternalFilesDir(null), name);
            MediaMuxer muxer = new MediaMuxer(output.getAbsolutePath(), MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
            int muxTrack = muxer.addTrack(format);
            muxer.start();
            long startUs = Math.max(0L, startMs) * 1000L;
            long endUs = endMs == Long.MAX_VALUE ? Long.MAX_VALUE : Math.max(0L, endMs) * 1000L;
            extractor.seekTo(startUs, MediaExtractor.SEEK_TO_CLOSEST_SYNC);
            ByteBuffer buffer = ByteBuffer.allocateDirect(1024 * 1024);
            MediaCodec.BufferInfo info = new MediaCodec.BufferInfo();
            for (int sampleIndex = 0; sampleIndex < 1000000; sampleIndex++) {
                int size = extractor.readSampleData(buffer, 0);
                if (size < 0) break;
                long timeUs = extractor.getSampleTime();
                if (timeUs < 0 || timeUs > endUs) break;
                if (timeUs >= startUs) {
                    info.offset = 0;
                    info.size = size;
                    info.presentationTimeUs = timeUs - startUs;
                    info.flags = extractor.getSampleFlags();
                    muxer.writeSampleData(muxTrack, buffer, info);
                }
                extractor.advance();
                buffer.clear();
            }
            muxer.stop();
            muxer.release();
            descriptor.close();
            extractor.release();
            status.setText("Exported: " + output.getName());
        } catch (Exception error) {
            status.setText("Audio export failed: " + error.getClass().getSimpleName());
        }
    }

"""
        source = self._insert_before_class_close(source, methods)
        callback = "        handleAudioActivityResult(requestCode, resultCode, data);\n"
        if "protected void onActivityResult(int requestCode, int resultCode, Intent data)" in source:
            source = source.replace("        super.onActivityResult(requestCode, resultCode, data);", "        super.onActivityResult(requestCode, resultCode, data);\n" + callback, 1)
        else:
            activity_result = """    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        handleAudioActivityResult(requestCode, resultCode, data);
    }

"""
            source = self._insert_before_class_close(source, activity_result)
        return AudioEditorGenerationResult(source=source, operations=self.OPERATIONS)

    @staticmethod
    def _insert_before_class_close(source: str, text: str) -> str:
        close = source.rfind("}\n")
        if close < 0:
            raise ValueError("MainActivity closing brace is missing")
        return source[:close] + text + source[close:]

    @staticmethod
    def _add_imports(source: str, imports: str) -> str:
        package_end = source.find("\n\n", source.find("package "))
        if package_end < 0:
            raise ValueError("Invalid Java source package header")
        return source[:package_end] + "\n\n" + imports.rstrip() + source[package_end:]
