import 'package:flutter/material.dart';
import 'api.dart';

class HomePage extends StatefulWidget {
  final String accessToken;
  const HomePage({super.key, required this.accessToken});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late final ApiClient _client;
  List<dynamic> _consultations = [];
  List<dynamic> _rendezVous = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _client = ApiClient(accessToken: widget.accessToken);
    _loadData();
  }

  Future<void> _loadData() async {
    final consultations = await _client.getConsultations();
    final rdv = await _client.getRendezVous();
    setState(() {
      _consultations = consultations;
      _rendezVous = rdv;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Espace Patient SGHL'),
          bottom: const TabBar(tabs: [
            Tab(text: 'Historique'),
            Tab(text: 'Rendez-vous'),
            Tab(text: 'Observance'),
          ]),
        ),
        body: _loading
            ? const Center(child: CircularProgressIndicator())
            : TabBarView(
                children: [
                  _buildList(
                    _consultations,
                    'Aucune consultation',
                    (item) => ListTile(
                      title: Text(item['chief_complaint']?.toString() ?? 'Consultation'),
                      subtitle: Text('Statut: ${item['status']}'),
                    ),
                  ),
                  _buildList(
                    _rendezVous,
                    'Aucun rendez-vous',
                    (item) => ListTile(
                      title: Text(item['medecin']?.toString() ?? 'Médecin'),
                      subtitle: Text('${item['date_rdv']} — ${item['statut']}'),
                    ),
                  ),
                  const Center(
                    child: Padding(
                      padding: EdgeInsets.all(24),
                      child: Text(
                        'Rappels médicamenteux et suivi post-opératoire\n(notifications push à configurer)',
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _buildList(List<dynamic> items, String empty, Widget Function(dynamic) builder) {
    if (items.isEmpty) {
      return Center(child: Text(empty));
    }
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (_, i) => builder(items[i]),
    );
  }
}
