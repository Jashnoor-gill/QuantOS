# QuantOS Project Demo Script

## 1) Login / Register
1. Open the app.
2. Go to **Login**.
3. Register a new user.
4. Login and observe success notifications.

## 2) Protected navigation
1. Open **Dashboard**.
2. Refresh the page.
3. Verify you remain authenticated (session persistence).

## 3) Browse authenticated areas
1. Visit Analytics / Alpha Lab.
2. Confirm navbar username appears.

## 4) Logout
1. Click profile dropdown.
2. Logout.
3. Confirm redirect to **Login**.

## 5) Backend health verification
1. Call `GET /health`.
2. (Optional) Call an authenticated endpoint and confirm 401 when logged out.

