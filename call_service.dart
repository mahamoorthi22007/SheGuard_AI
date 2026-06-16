import 'package:flutter_phone_direct_caller/flutter_phone_direct_caller.dart';

class CallService {
  Future<void> callParent() async {
    // This will initiate the call immediately without opening the dialer UI
    await FlutterPhoneDirectCaller.callNumber("+918760550355");
  }
}