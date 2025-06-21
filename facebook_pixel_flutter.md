# Complete Guide to Integrating Facebook App Events (Pixel Alternative) in Flutter (Android & iOS)

## 🔍 Understanding Facebook Pixel vs. Facebook App Events

**Facebook Pixel** is a tool used for tracking user actions on **websites**, helping marketers measure the effectiveness of their advertising by understanding what people do on their site. It works by embedding a JavaScript code snippet (`fbq(...)`) into web pages.

### ❗ Important Clarification

You **cannot directly use the JavaScript-based Facebook Pixel in mobile apps or Flutter** because:

- Flutter is not a browser and doesn't run JavaScript in a webpage context.
- Facebook Pixel is meant for website tracking using browser cookies.

### ✅ What You Can Do in Mobile Apps (Android/iOS)

For **mobile apps**, Facebook provides **Facebook App Events** — a native SDK-based solution for tracking similar user actions like purchases, views, and installs.

These app events:

- Are sent via Facebook SDKs (or Flutter plugin `facebook_app_events`)
- Are visible in **Meta Events Manager**, often unified with website Pixel data
- Can be linked to your Facebook Pixel/Dataset for a consolidated view

> 📌 So, while you can’t use the raw `fbq(...)` Pixel code, you **can achieve the same goals** through Facebook App Events.

---

## ✅ Overview of What You’ll Do

1. Create a Facebook App through Meta Developer Portal.
2. Get your **App ID** and **Client Token**.
3. Add the `facebook_app_events` plugin to your Flutter project.
4. Configure your **Android** and **iOS** projects.
5. Log standard or custom app events.
6. Test your events in Meta Events Manager.

---

## 🌐 Step 1: Create a Facebook App

### Go to Meta Developers

Visit: [https://developers.facebook.com/apps](https://developers.facebook.com/apps)

### Create a New App

1. Click **Create App**.
2. Choose **"Business"** as the app type.
3. Fill in the app name and contact email.
4. Once the app is created, go to **Settings > Basic**.
5. Copy the **App ID** and **Client Token** from this page.

---

## 📊 Step 2: Add Dependency to Flutter

In your `pubspec.yaml`:

```yaml
dependencies:
  facebook_app_events: ^0.20.1
```

Then run:

```bash
flutter pub get
```

---

## 📱 Step 3: Android Setup

### 3.1 Add App Info to `strings.xml`

Open `android/app/src/main/res/values/strings.xml` and add:

```xml
<resources>
    <string name="facebook_app_id">[YOUR_APP_ID]</string>
    <string name="facebook_client_token">[YOUR_CLIENT_TOKEN]</string>
    <string name="fb_login_protocol_scheme">fb[YOUR_APP_ID]</string>
    <string name="app_name">[YOUR_APP_NAME]</string>
</resources>
```

> Replace placeholders like `[YOUR_APP_ID]`, `[YOUR_CLIENT_TOKEN]`, etc.

### 3.2 Modify `AndroidManifest.xml`

Inside the `<application>` tag in `android/app/src/main/AndroidManifest.xml`, add:

```xml
<meta-data android:name="com.facebook.sdk.ApplicationId" android:value="@string/facebook_app_id"/>
<meta-data android:name="com.facebook.sdk.ClientToken" android:value="@string/facebook_client_token"/>
```

---

## 🍏 Step 4: iOS Setup

### 4.1 Open `Info.plist`

Navigate to `ios/Runner/Info.plist` and open it as source code.

Add the following **before** the last `</dict>`:

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>fb[YOUR_APP_ID]</string>
    </array>
  </dict>
</array>
<key>FacebookAppID</key>
<string>[YOUR_APP_ID]</string>
<key>FacebookClientToken</key>
<string>[YOUR_CLIENT_TOKEN]</string>
<key>FacebookDisplayName</key>
<string>[YOUR_APP_NAME]</string>
```

> Again, replace the placeholders with your actual data.

---

## ⚡ Step 5: Initialize and Log Events

### 5.1 Import the Plugin

In your Dart code:

```dart
import 'package:facebook_app_events/facebook_app_events.dart';
```

### 5.2 Create an Instance

```dart
final facebookAppEvents = FacebookAppEvents();
```

### 5.3 Log Standard or Custom Events

### Example: Logging a purchase

```dart
facebookAppEvents.logEvent(
  name: 'purchase',
  parameters: {
    'currency': 'USD',
    'value': 99.99,
  },
);
```

#### Example: Custom event

```dart
facebookAppEvents.logEvent(
  name: 'my_custom_event',
  parameters: {
    'foo': 'bar',
  },
);
```

---

## 🧪 Step 6: Testing Events in Meta Events Manager

1. Go to: [https://www.facebook.com/events\_manager](https://www.facebook.com/events_manager)
2. Click on your App.
3. Go to **"Test Events"** tab.
4. Run your app and trigger the logged events.
5. You should see them appear in real-time.

---

## 🚧 Troubleshooting Tips

- If events don’t show:
  - Double-check App ID and Client Token.
  - Ensure strings.xml and Info.plist are properly configured.
  - Use real devices rather than emulators for better tracking.
- For iOS 14+, remember to handle ATT (App Tracking Transparency) permissions.

---

## 📖 Useful Resources

- Plugin: [https://pub.dev/packages/facebook\_app\_events](https://pub.dev/packages/facebook_app_events)
- Meta App Events Docs: [https://developers.facebook.com/docs/app-events/](https://developers.facebook.com/docs/app-events/)
- Events Manager: [https://www.facebook.com/events\_manager](https://www.facebook.com/events_manager)

---

---

## 📖 Facebook Pixel Resources

- Facebook Pixel integration overview: [Implement the Meta pixel and mobile SDK for automotive ads](https://www.facebook.com/business/help/1989760861301766?id=378777162599537)
- Facebook Pixel Detailed documentation: [Automotive Ads - Events](https://developers.facebook.com/docs/marketing-api/auto-ads/guides/events)

---

## 💪 Summary

With this setup, you can now track important actions that users take in your Flutter mobile app using **Facebook App Events**. These events will be visible inside your Meta Business Suite, often alongside web Pixel data, helping you understand user behavior, optimize ads, and make better decisions for your business.
