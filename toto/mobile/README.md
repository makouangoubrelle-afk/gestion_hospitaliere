# Mobile client (Flutter)

This folder contains a minimal Flutter client that authenticates with the Django backend using token auth.

Quick start (requires Flutter SDK installed):

1. Open a terminal and go to `mobile/`:

```bash
cd mobile
```

2. Get packages:

```bash
flutter pub get
```

3. Run on Android emulator (ensure your Django server is running on the host at port 8000). On the Android emulator, `localhost` is `10.0.2.2`.

```bash
flutter run
```

4. By default the app points to `http://10.0.2.2:8000` (see `lib/api.dart`). Change `baseUrl` if your backend is remote.

Building an APK:

```bash
flutter build apk --release
```

Then install the APK on a device with `adb install build/app/outputs/flutter-apk/app-release.apk`.
