import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:pdf_render/pdf_render.dart';

class ApiService {
  // Pick a PDF file
  Future<File?> pickPdfFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null && result.files.single.path != null) {
      return File(result.files.single.path!);
    }
    return null;
  }

  // Extract text from PDF
  Future<String> extractText(File pdfFile) async {
    final doc = await PdfDocument.openFile(pdfFile.path);
    String fullText = '';
    for (int i = 1; i <= doc.pageCount; i++) {
      final page = await doc.getPage(i);
      fullText += await page.text;
      await page.close();
    }
    await doc.close();
    return fullText;
  }
}
