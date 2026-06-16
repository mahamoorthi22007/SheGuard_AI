import 'package:audioplayers/audioplayers.dart';

class SirenService {
  final AudioPlayer _player = AudioPlayer();

  Future<void> startSiren() async {
    // Configure the player to stay active during calls
    await _player.setAudioContext(AudioContext(
      android: AudioContextAndroid(
        isSpeakerphoneOn: true,
        stayAwake: true,
        contentType: AndroidContentType.sonification,
        usageType: AndroidUsageType.alarm, // CRITICAL: Tells OS this is an alarm
      ),
    ));

    await _player.setReleaseMode(ReleaseMode.loop);
    await _player.play(AssetSource('audio/siren.mp3'));
  }

  Future<void> stopSiren() async {
    await _player.stop();
  }
}