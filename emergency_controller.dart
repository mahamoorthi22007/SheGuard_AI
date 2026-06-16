import 'services/location_service.dart';
import 'services/siren_service.dart';
import 'services/sms_service.dart';
import 'services/call_service.dart';
import 'services/recording_service.dart';

class EmergencyController {

  final siren = SirenService();
  final location = LocationService();
  final sms = SmsService();
  final call = CallService();
  final recording = RecordingService();

  Future<void> activateEmergencyMode(double threatScore) async {
    try {
      print("Starting siren");
      await siren.startSiren();

      print("Getting location");
      final pos = await location.getLocation();

      print("Location: ${pos.latitude}, ${pos.longitude}");

      String mapLink =
          "https://www.google.com/maps/search/?api=1&query=${pos.latitude},${pos.longitude}";

      print("Sending SMS");
      await sms.sendEmergencySMS(mapLink);

      print("Starting recording");
      await recording.startRecording();

      print("Calling parent");
      await call.callParent();

      print("Emergency flow completed");
    } catch (e) {
      print("EMERGENCY ERROR: $e");
    }
  }
}
