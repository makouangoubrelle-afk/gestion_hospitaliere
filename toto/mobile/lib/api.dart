import 'dart:convert';
import 'package:http/http.dart' as http;

const String baseUrl = 'http://10.0.2.2:8000/api/v1';

class ApiClient {
  final String? accessToken;

  ApiClient({this.accessToken});

  Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (accessToken != null) 'Authorization': 'Bearer $accessToken',
      };

  Future<Map<String, dynamic>?> login(String username, String password) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: headers,
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    return null;
  }

  Future<List<dynamic>> getConsultations() async {
    final resp = await http.get(Uri.parse('$baseUrl/consultations/'), headers: headers);
    if (resp.statusCode != 200) return [];
    final data = jsonDecode(resp.body);
    if (data is Map && data.containsKey('items')) return data['items'] as List<dynamic>;
    return data as List<dynamic>;
  }

  Future<List<dynamic>> getRendezVous() async {
    final resp = await http.get(Uri.parse('$baseUrl/pharmacie/rendez-vous'), headers: headers);
    if (resp.statusCode != 200) return [];
    final data = jsonDecode(resp.body);
    if (data is Map && data.containsKey('items')) return data['items'] as List<dynamic>;
    return data as List<dynamic>;
  }

  Future<Map<String, dynamic>?> getSante() async {
    final resp = await http.get(Uri.parse('$baseUrl/sante/'));
    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    return null;
  }
}
