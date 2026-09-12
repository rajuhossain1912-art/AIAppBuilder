from __future__ import annotations


class ImageEditorGenerator:
    """Augment an Android activity with a small real bitmap editor."""

    def augment(self, source: str) -> str:
        source = self._add_imports(source)
        source = self._insert_ui(source)
        source = self._insert_state_and_methods(source)
        source = self._merge_activity_callback(source)
        return source

    @staticmethod
    def _add_imports(source: str) -> str:
        imports = [
            "import android.graphics.Bitmap;",
            "import android.graphics.BitmapFactory;",
            "import android.graphics.ColorMatrix;",
            "import android.graphics.ColorMatrixColorFilter;",
            "import android.graphics.Matrix;",
        ]
        for line in imports:
            if line not in source:
                source = source.replace("import android.app.Activity;", "import android.app.Activity;\n" + line, 1)
        return source

    @staticmethod
    def _insert_ui(source: str) -> str:
        marker = "        setContentView(root);"
        block = '''        Button pickImageEditor = button("Choose image for editing");
        pickImageEditor.setOnClickListener(v -> startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).setType("image/*").addCategory(Intent.CATEGORY_OPENABLE), 102));
        root.addView(pickImageEditor);
        Button rotateImage = button("Rotate image 90 degrees");
        rotateImage.setOnClickListener(v -> rotateSelectedImage());
        root.addView(rotateImage);
        Button grayscaleImage = button("Convert image to grayscale");
        grayscaleImage.setOnClickListener(v -> grayscaleSelectedImage());
        root.addView(grayscaleImage);
        Button exportImage = button("Export edited image");
        exportImage.setOnClickListener(v -> exportEditedImage());
        root.addView(exportImage);'''
        if block not in source:
            source = source.replace(marker, block + "\n" + marker, 1)
        return source

    @staticmethod
    def _insert_state_and_methods(source: str) -> str:
        state_marker = "    private TextView status;\n"
        state = "    private Uri selectedImageEditorUri;\n    private Bitmap editedImage;\n"
        if state not in source:
            source = source.replace(state_marker, state_marker + state, 1)

        methods = '''    private void loadSelectedImage() {
        try {
            if (selectedImageEditorUri == null) { status.setText("Choose an image first"); return; }
            try (java.io.InputStream input = getContentResolver().openInputStream(selectedImageEditorUri)) {
                editedImage = BitmapFactory.decodeStream(input);
            }
            if (editedImage == null) { status.setText("Unable to read image"); return; }
            status.setText("Image loaded for editing");
        } catch (Exception error) {
            status.setText("Image load failed");
        }
    }

    private void rotateSelectedImage() {
        if (editedImage == null) { loadSelectedImage(); }
        if (editedImage == null) return;
        Matrix matrix = new Matrix();
        matrix.postRotate(90.0f);
        Bitmap rotated = Bitmap.createBitmap(editedImage, 0, 0, editedImage.getWidth(), editedImage.getHeight(), matrix, true);
        if (rotated != editedImage) editedImage.recycle();
        editedImage = rotated;
        status.setText("Image rotated 90 degrees");
    }

    private void grayscaleSelectedImage() {
        if (editedImage == null) { loadSelectedImage(); }
        if (editedImage == null) return;
        Bitmap grayscale = Bitmap.createBitmap(editedImage.getWidth(), editedImage.getHeight(), Bitmap.Config.ARGB_8888);
        android.graphics.Canvas canvas = new android.graphics.Canvas(grayscale);
        android.graphics.Paint paint = new android.graphics.Paint();
        ColorMatrix matrix = new ColorMatrix();
        matrix.setSaturation(0.0f);
        paint.setColorFilter(new ColorMatrixColorFilter(matrix));
        canvas.drawBitmap(editedImage, 0, 0, paint);
        editedImage.recycle();
        editedImage = grayscale;
        status.setText("Image converted to grayscale");
    }

    private void exportEditedImage() {
        if (editedImage == null) { status.setText("Edit an image before export"); return; }
        java.io.File output = new java.io.File(getCacheDir(), "aiappbuilder-edited-image.png");
        try (java.io.FileOutputStream stream = new java.io.FileOutputStream(output)) {
            editedImage.compress(Bitmap.CompressFormat.PNG, 100, stream);
            stream.flush();
            status.setText("Edited image exported to app storage");
        } catch (Exception error) {
            status.setText("Image export failed");
        }
    }

'''
        marker = "    private LinearLayout base(String title) {"
        if "private void rotateSelectedImage()" not in source:
            source = source.replace(marker, methods + marker, 1)
        return source

    @staticmethod
    def _merge_activity_callback(source: str) -> str:
        handler = '''    private void handleImageEditorActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 102 && resultCode == RESULT_OK && data != null) {
            selectedImageEditorUri = data.getData();
            loadSelectedImage();
        }
    }

'''
        if "handleImageEditorActivityResult" not in source:
            source = source.replace("    private LinearLayout base(String title) {", handler + "    private LinearLayout base(String title) {", 1)

        signature = "    protected void onActivityResult(int requestCode, int resultCode, Intent data) {"
        callback_call = "        handleImageEditorActivityResult(requestCode, resultCode, data);"
        if signature in source:
            callback_marker = "        super.onActivityResult(requestCode, resultCode, data);"
            if callback_call not in source:
                source = source.replace(callback_marker, callback_marker + "\n" + callback_call, 1)
        else:
            callback = '''    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        handleImageEditorActivityResult(requestCode, resultCode, data);
    }

'''
            source = source.replace("    private LinearLayout base(String title) {", callback + "    private LinearLayout base(String title) {", 1)
        return source
