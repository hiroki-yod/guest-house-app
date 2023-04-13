# アプリケーション名
**Guest House App (仮称)**
<br>
<br>

# 概要紹介
このWebアプリは、大学の最後の春休みに制作されました。
その目的は、ゲストハウスでの滞在を通じて、ゲストと地域のつながりを深めることです。
主な機能として、宿泊予約時に近くのイベント情報を提供します。
また、リピート利用を促すために、次回の宿泊で使えるクーポンを発行する機能もあります。
<br>
<br>
![image](https://user-images.githubusercontent.com/77391181/231731317-e1b85e89-c76b-46d5-9f22-5c13bd7ee051.png)

# 機能一覧
## 認証
### Host / Guest のマルチログイン
HostとGuestを区別し、それぞれのサインアップ画面を用意しました。
同一のページからログインしても異なるページにリダイレクトされます。
実際に運用する際は、Hostのサインアップに対して審査を導入する予定です。
<br>
<br>
![image](https://user-images.githubusercontent.com/77391181/231731639-aa3d17e5-c9b1-4837-b2ce-f6698bef1ce8.png)

## 基本機能
### Host側
Hostの管理画面からはFacilityとRoomを登録することができます。
Roomが登録されると自動的に予約枠が生成されます。
<br>
<br>
![image](https://user-images.githubusercontent.com/77391181/231734236-e9dce80c-c5e1-4866-ab5e-bea6ad38c9cd.png)
#### Guest側
Guestの検索ページではゲストハウスの一覧が表示されます。
そこから1つを選び、予約手続に進むことができます。
<br>
<br>
![image](https://user-images.githubusercontent.com/77391181/231733647-12a7b586-9330-4d07-81da-c88150191dad.png)
## イベント
### Host側
Hostはゲストハウスに紐づいたイベントと参加特典を登録することができます。
<br>
<br>
![image](https://user-images.githubusercontent.com/77391181/231735380-f45a9498-734d-4a4a-9d90-d6774dcfd342.png)

### Guest側
Guestは宿泊予約時にイベント参加申込ができ、マイページで予約と参加特典を確認することができます。
![image](https://user-images.githubusercontent.com/77391181/231735262-a32a8f76-9464-4b88-9f43-132351e04f74.png)
