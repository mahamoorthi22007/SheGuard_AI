import 'package:geolocator/geolocator.dart';

class LocationService {

  Future<Position> getLocation() async {

    bool serviceEnabled =
        await Geolocator.isLocationServiceEnabled();

    if (!serviceEnabled) {
      throw Exception("Location disabled");
    }

    LocationPermission permission =
        await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission =
          await Geolocator.requestPermission();
    }

    return await Geolocator.getCurrentPosition();
  }
}