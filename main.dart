import 'package:flutter/material.dart';
import 'emergency/emergency_controller.dart';
import 'package:percent_indicator/circular_percent_indicator.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: EmergencyScreen(),
    );
  }
}

class EmergencyScreen extends StatelessWidget {
  final EmergencyController controller = EmergencyController();

  EmergencyScreen({super.key});

  double threatScore = 0.92;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color.fromARGB(255, 81, 27, 78),
              Color.fromARGB(255, 213, 114, 213),
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              children: [
                _buildHeader(),
                const SizedBox(height: 40),
                _buildCircularMeter(),
                const SizedBox(height: 40),
                _buildDataRow(),
                const Spacer(),
                _buildSOSButton(context), // 👈 same function logic
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      children: [
        Text(
          "SHEGUARD",
          style: GoogleFonts.orbitron(
            fontSize: 26,
            color: Colors.white,
            letterSpacing: 4,
          ),
        ),
        const Text(
          "LIVE MONITORING ACTIVE",
          style: TextStyle(color: Colors.white54, fontSize: 12),
        ),
      ],
    );
  }

  Widget _buildCircularMeter() {
    return CircularPercentIndicator(
      radius: 120,
      lineWidth: 18,
      percent: threatScore,
      animation: true,
      center: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            "${(threatScore * 100).toInt()}%",
            style: GoogleFonts.exo2(
              fontSize: 48,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const Text(
            "THREAT LEVEL",
            style: TextStyle(color: Colors.white70),
          ),
        ],
      ),
      progressColor: threatScore > 0.8 ? Colors.red : Colors.green,
      backgroundColor: Colors.white10,
      circularStrokeCap: CircularStrokeCap.round,
    );
  }

  Widget _buildDataRow() {
    return Row(
      children: [
        _glassCard("Audio", "Normal", Icons.mic),
        const SizedBox(width: 16),
        _glassCard("Motion", "Stable", Icons.directions_run),
      ],
    );
  }

  Widget _glassCard(String title, String val, IconData icon) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.08),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.white12),
        ),
        child: Column(
          children: [
            Icon(icon, color: Colors.white70),
            const SizedBox(height: 8),
            Text(title, style: const TextStyle(color: Colors.white54)),
            Text(
              val,
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSOSButton(BuildContext context) {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(30),
        boxShadow: [
          BoxShadow(
            color: Colors.red.withOpacity(0.3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          )
        ],
      ),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.red,
          padding: const EdgeInsets.symmetric(vertical: 20),
        ),

        // 🔥 YOUR ORIGINAL FUNCTION (UNCHANGED)
        onPressed: () async {
          print("Button pressed");

          try {
            await controller.activateEmergencyMode(92);
            print("Emergency activated");

            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text("Emergency Activated!"),
                backgroundColor: Color.fromARGB(255, 50, 95, 0),
              ),
            );
          } catch (e) {
            print("ERROR: $e");
          }
        },

        child: Text(
          "TRIGGER EMERGENCY",
          style: GoogleFonts.montserrat(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
    );
  }
}