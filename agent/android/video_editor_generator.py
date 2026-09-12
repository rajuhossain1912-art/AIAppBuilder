from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VideoEditorGenerationResult:
    source: str
    operations: tuple[str, ...]


class VideoEditorGenerator:
    """Adds a dependency-free Android video trim/split/preview/export surface."""

    OPERATIONS = ("pick_video", "preview", "trim", "split", "export")

    def augment(self, source: str) -> VideoEditorGenerationResult:
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
        section = """        EditText videoStartMs = input("Start milliseconds");
        EditText videoEndMs = input("End milliseconds");
        root.addView(videoStartMs);
        root.addView(videoEndMs);
        Button pickVideoEditor = button("Choose video");
        pickVideoEditor.setOnClickListener(v -> pickVideoForEditor());
        root.addView(pickVideoEditor);
        Button previewVideoEditor = button("Preview video");
        previewVideoEditor.setOnClickListener(v -> previewSelectedVideo());
        root.addView(previewVideoEditor);
        Button trimVideoEditor = button("Trim and export video");
        trimVideoEditor.setOnClickListener(v -> {
            long start = parseVideoTime(videoStartMs, 0L);
            long end = parseVideoTime(videoEndMs, -1L);
            if (end <= start) { status.setText("End time must be greater than start time"); return; }
            exportVideoRange(start, end, "trimmed_video.mp4");
        });
        root.addView(trimVideoEditor);
        Button splitVideoEditor = button("Split at end time");
        splitVideoEditor.setOnClickListener(v -> {
            long split = parseVideoTime(videoEndMs, -1L);
            if (split <= 0) { status.setText("Enter a valid split time"); return; }
            exportVideoRange(0L, split, "video_part_1.mp4");
            if (selectedVideoUri != null) exportVideoRange(split, Long.MAX_VALUE, "video_part_2.mp4");
        });
        root.addView(splitVideoEditor);
"""
        source = source.replace(marker, section + marker, 1)
        methods = """    private android.net.Uri selectedVideoUri;
    private android.media.MediaPlayer videoEditorPlayer;

    private void pickVideoForEditor() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("video/*");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(intent, 7002);
        status.setText("Choose a video file");
    }

    private void handleVideoActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 7002 && resultCode == RESULT_OK && data != null && data.getData() != null) {
            selectedVideoUri = data.getData();
            try { getContentResolver().takePersistableUriPermission(selectedVideoUri, Intent.FLAG_GRANT_READ_URI_PERMISSION); } catch (SecurityException ignored) { }
            status.setText("Video selected");
        }
    }

    private void previewSelectedVideo() {
        if (selectedVideoUri == null) { status.setText("Choose a video file first"); return; }
        try {
            if (videoEditorPlayer != null) videoEditorPlayer.release();
            videoEditorPlayer = android.media.MediaPlayer.create(this, selectedVideoUri);
            if (videoEditorPlayer == null) { status.setText("This video format cannot be previewed"); return; }
            videoEditorPlayer.setOnCompletionListener(player -> status.setText("Preview finished"));
            videoEditorPlayer.start();
            status.setText("Playing video preview");
        } catch (Exception error) { status.setText("Unable to preview video"); }
    }

    private long parseVideoTime(EditText field, long fallback) {
        try { return Long.parseLong(field.getText().toString().trim()); }
        catch (NumberFormatException error) { return fallback; }
    }

    private void exportVideoRange(long startMs, long endMs, String name) {
        if (selectedVideoUri == null) { status.setText("Choose a video file first"); return; }
        try {
            MediaExtractor extractor = new MediaExtractor();
            android.os.ParcelFileDescriptor descriptor = getContentResolver().openFileDescriptor(selectedVideoUri, "r");
            if (descriptor == null) throw new IOException("Unable to open video");
            extractor.setDataSource(descriptor.getFileDescriptor());
            int videoTrack = -1;
            for (int i = 0; i < extractor.getTrackCount(); i++) {
                MediaFormat format = extractor.getTrackFormat(i);
                String mime = format.getString(MediaFormat.KEY_MIME);
                if (mime != null && mime.startsWith("video/")) { videoTrack = i; break; }
            }
            if (videoTrack < 0) throw new IOException("No video track");
            extractor.selectTrack(videoTrack);
            MediaFormat format = extractor.getTrackFormat(videoTrack);
            File output = new File(getExternalFilesDir(null), name);
            MediaMuxer muxer = new MediaMuxer(output.getAbsolutePath(), MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
            int muxTrack = muxer.addTrack(format);
            muxer.start();
            long startUs = Math.max(0L, startMs) * 1000L;
            long endUs = endMs == Long.MAX_VALUE ? Long.MAX_VALUE : Math.max(0L, endMs) * 1000L;
            extractor.seekTo(startUs, MediaExtractor.SEEK_TO_CLOSEST_SYNC);
            ByteBuffer buffer = ByteBuffer.allocateDirect(4 * 1024 * 1024);
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
                    int sampleFlags = extractor.getSampleFlags();
                    info.flags = (sampleFlags & MediaExtractor.SAMPLE_FLAG_SYNC) != 0
                            ? MediaCodec.BUFFER_FLAG_KEY_FRAME
                            : 0;
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
            status.setText("Video export failed: " + error.getClass().getSimpleName());
        }
    }

"""
        source = self._insert_before_class_close(source, methods)
        callback = "        handleVideoActivityResult(requestCode, resultCode, data);\n"
        signature = "    protected void onActivityResult(int requestCode, int resultCode, Intent data) {"
        if signature in source:
            source = source.replace("        super.onActivityResult(requestCode, resultCode, data);", "        super.onActivityResult(requestCode, resultCode, data);\n" + callback, 1)
        else:
            activity_result = """    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        handleVideoActivityResult(requestCode, resultCode, data);
    }

"""
            source = self._insert_before_class_close(source, activity_result)
        return VideoEditorGenerationResult(source=source, operations=self.OPERATIONS)

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
