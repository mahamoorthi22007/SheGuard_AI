class EmergencyData {
  final double threatScore;
  final double latitude;
  final double longitude;
  final DateTime timestamp;

  EmergencyData({
    required this.threatScore,
    required this.latitude,
    required this.longitude,
    required this.timestamp,
  });
}