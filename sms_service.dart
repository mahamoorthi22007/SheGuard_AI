import 'package:flutter_sms/flutter_sms.dart';

class SmsService {
  Future<void> sendEmergencySMS(String locationLink) async {
    try {
      await sendSMS(
        message: "EMERGENCY: I am in danger! My location is: $locationLink",
        recipients: ["+918760550355"],
       );
      print("Emergency SMS sent successfully");
    } catch (e) {
      print("Error sending SMS: $e");
    }
  }
}