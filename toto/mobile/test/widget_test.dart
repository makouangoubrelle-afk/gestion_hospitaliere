import 'package:flutter_test/flutter_test.dart';
import 'package:gestion_hospitaliere_mobile/main.dart';

void main() {
  testWidgets('Login page renders', (WidgetTester tester) async {
    await tester.pumpWidget(const SghlMobileApp());
    expect(find.text('SGHL Patient'), findsOneWidget);
    expect(find.text('Se connecter'), findsOneWidget);
  });
}
