import 'dart:convert';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;

/// URL de l'API :
/// - Web (servi sous /mobile/) : même origine → /api/v1
/// - Android émulateur : 10.0.2.2
/// - Override possible : --dart-define=API_BASE=https://xxx.onrender.com/api/v1
String get apiBaseUrl {
  const fromEnv = String.fromEnvironment('API_BASE');
  if (fromEnv.isNotEmpty) return fromEnv.replaceAll(RegExp(r'/+$'), '');
  if (kIsWeb) {
    final origin = Uri.base.origin;
    return '$origin/api/v1';
  }
  return 'http://10.0.2.2:8000/api/v1';
}

class ApiClient {
  final String? accessToken;

  ApiClient({this.accessToken});

  Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (accessToken != null) 'Authorization': 'Bearer $accessToken',
      };

  Future<Map<String, dynamic>?> login(String username, String password) async {
    final resp = await http.post(
      Uri.parse('$apiBaseUrl/auth/login'),
      headers: headers,
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    return null;
  }

  Future<Map<String, dynamic>?> me() async {
    final resp = await http.get(Uri.parse('$apiBaseUrl/auth/me'), headers: headers);
    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    return null;
  }

  Future<List<dynamic>> getConsultations() async {
    final resp = await http.get(Uri.parse('$apiBaseUrl/consultations/'), headers: headers);
    if (resp.statusCode != 200) return [];
    final data = jsonDecode(resp.body);
    if (data is Map && data.containsKey('items')) return data['items'] as List<dynamic>;
    if (data is List) return data;
    return [];
  }

  Future<List<dynamic>> getRendezVous() async {
    final resp = await http.get(Uri.parse('$apiBaseUrl/pharmacie/rendez-vous'), headers: headers);
    if (resp.statusCode != 200) return [];
    final data = jsonDecode(resp.body);
    if (data is Map && data.containsKey('items')) return data['items'] as List<dynamic>;
    if (data is List) return data;
    return [];
  }

  Future<Map<String, dynamic>?> getSante() async {
    final resp = await http.get(Uri.parse('$apiBaseUrl/sante/'));
    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    return null;
  }
}
