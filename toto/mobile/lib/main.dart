import 'package:flutter/material.dart';

import 'login_page.dart';

void main() {
  runApp(const SghlMobileApp());
}

class SghlMobileApp extends StatelessWidget {
  const SghlMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    const teal = Color(0xFF0D9488);
    return MaterialApp(
      title: 'SGHL Patient',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: teal,
          primary: teal,
          secondary: const Color(0xFF2563EB),
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0F766E),
          foregroundColor: Colors.white,
          centerTitle: true,
        ),
        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: teal,
          foregroundColor: Colors.white,
        ),
      ),
      home: const LoginPage(),
    );
  }
}
