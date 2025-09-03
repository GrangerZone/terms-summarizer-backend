import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'services/api_service.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String extractedText = '';

  void pickPdf() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null && result.files.single.path != null) {
      File file = File(result.files.single.path!);
      String text = await ApiService().extractTextFromPdf(file);
      setState(() {
        extractedText = text;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('PDF Text Extractor')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(child: Text(extractedText)),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: pickPdf,
        child: Icon(Icons.upload_file),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(home: HomePage()));
}

