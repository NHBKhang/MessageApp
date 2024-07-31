# Django Message App

Ứng dụng nhắn tin Django tập trung vào mã hóa và giải mã thông tin phục vụ cho môn An toàn hệ thống thông tin. Ứng dụng là phiên bản cải tiến so với phiên bản đã sử dụng cho bài tập lớn.

* Các thuật toán được sử dụng
    - Phiên bản cũ: XOR bytes (mã hóa tin nhắn trên đường truyền), Vigenere (mã hóa tin nhắn trong SQLite)
    - Phiên bản mới: RSA (mã hóa tin nhắn trên đường truyền), AES (mã hóa private key của RSA), ChaCha20 (mã hóa tin nhắn trong SQLite) và chức năng thông báo lỗi cặp khóa của RSA để tạo lại cặp khóa khi cần
      
* Account (username/ password):
    - admin / 123456 (admin)
 
* Phiên bản cũ: https://github.com/dochihung2909/ATTT_ChatServer/tree/new
