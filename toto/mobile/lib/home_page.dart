import 'package:flutter/material.dart';

import 'api.dart';
import 'login_page.dart';

class HomePage extends StatefulWidget {
  final String accessToken;
  const HomePage({super.key, required this.accessToken});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late final ApiClient _client;
  Map<String, dynamic>? _me;
  List<dynamic> _consultations = [];
  List<dynamic> _rendezVous = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _client = ApiClient(accessToken: widget.accessToken);
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final me = await _client.me();
      final consultations = await _client.getConsultations();
      final rdv = await _client.getRendezVous();
      if (!mounted) return;
      setState(() {
        _me = me;
        _consultations = consultations;
        _rendezVous = rdv;
        _loading = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _error = 'Impossible de charger les données';
      });
    }
  }

  void _logout() {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final username = _me?['username']?.toString() ?? 'Patient';
    final role = _me?['role']?.toString() ?? 'patient';

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Espace Patient'),
          actions: [
            IconButton(
              tooltip: 'Actualiser',
              onPressed: _loading ? null : _loadData,
              icon: const Icon(Icons.refresh),
            ),
            IconButton(
              tooltip: 'Déconnexion',
              onPressed: _logout,
              icon: const Icon(Icons.logout),
            ),
          ],
          bottom: const TabBar(
            indicatorColor: Colors.white,
            labelColor: Colors.white,
            unselectedLabelColor: Color(0xFFCCFBF1),
            tabs: [
              Tab(icon: Icon(Icons.history), text: 'Historique'),
              Tab(icon: Icon(Icons.event), text: 'RDV'),
              Tab(icon: Icon(Icons.medication), text: 'Suivi'),
            ],
          ),
        ),
        body: _loading
            ? const Center(child: CircularProgressIndicator())
            : Column(
                children: [
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
                    color: const Color(0xFFECFDF5),
                    child: Text(
                      'Bonjour $username · rôle $role',
                      style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        color: Color(0xFF0F766E),
                      ),
                    ),
                  ),
                  if (_error != null)
                    Padding(
                      padding: const EdgeInsets.all(12),
                      child: Text(_error!, style: const TextStyle(color: Colors.red)),
                    ),
                  Expanded(
                    child: TabBarView(
                      children: [
                        _buildConsultations(),
                        _buildRendezVous(),
                        _buildObservance(),
                      ],
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _empty(String message, IconData icon) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 48, color: const Color(0xFF94A3B8)),
            const SizedBox(height: 12),
            Text(message, textAlign: TextAlign.center, style: const TextStyle(color: Color(0xFF64748B))),
          ],
        ),
      ),
    );
  }

  Widget _buildConsultations() {
    if (_consultations.isEmpty) {
      return _empty('Aucune consultation pour le moment', Icons.medical_services_outlined);
    }
    return RefreshIndicator(
      onRefresh: _loadData,
      child: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: _consultations.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (_, i) {
          final item = _consultations[i] as Map<String, dynamic>;
          return Card(
            elevation: 0,
            color: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: Color(0xFFE2E8F0)),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              leading: CircleAvatar(
                backgroundColor: const Color(0xFFCCFBF1),
                child: const Icon(Icons.medical_services, color: Color(0xFF0F766E)),
              ),
              title: Text(
                item['chief_complaint']?.toString() ?? 'Consultation',
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              subtitle: Text(
                'Statut : ${item['status'] ?? '—'}'
                '${item['appointment_date'] != null ? '\n${item['appointment_date']}' : ''}',
              ),
              isThreeLine: item['appointment_date'] != null,
            ),
          );
        },
      ),
    );
  }

  Widget _buildRendezVous() {
    if (_rendezVous.isEmpty) {
      return _empty('Aucun rendez-vous planifié', Icons.event_busy);
    }
    return RefreshIndicator(
      onRefresh: _loadData,
      child: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: _rendezVous.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (_, i) {
          final item = _rendezVous[i] as Map<String, dynamic>;
          return Card(
            elevation: 0,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: Color(0xFFE2E8F0)),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              leading: const CircleAvatar(
                backgroundColor: Color(0xFFDBEAFE),
                child: Icon(Icons.event_available, color: Color(0xFF1D4ED8)),
              ),
              title: Text(
                item['medecin']?.toString() ?? 'Médecin',
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              subtitle: Text('${item['date_rdv'] ?? '—'}\nStatut : ${item['statut'] ?? '—'}'),
              isThreeLine: true,
            ),
          );
        },
      ),
    );
  }

  Widget _buildObservance() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFFE2E8F0)),
          ),
          child: const Padding(
            padding: EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Suivi & rappels', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                SizedBox(height: 8),
                Text(
                  'Rappels médicamenteux, suivi post-opératoire et notifications push '
                  'seront branchés ici. En attendant, consultez vos rendez-vous et votre historique.',
                  style: TextStyle(height: 1.45, color: Color(0xFF475569)),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 12),
        Card(
          color: const Color(0xFFECFDF5),
          elevation: 0,
          child: ListTile(
            leading: const Icon(Icons.check_circle, color: Color(0xFF059669)),
            title: const Text('API connectée'),
            subtitle: Text(apiBaseUrl, style: const TextStyle(fontSize: 12)),
          ),
        ),
      ],
    );
  }
}
