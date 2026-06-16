import 'package:record/record.dart';

class RecordingService {

  final recorder = AudioRecorder();

  Future<void> startRecording() async {

    await recorder.start(
      const RecordConfig(),
      path: 'emergency_audio.m4a',
    );
  }
}