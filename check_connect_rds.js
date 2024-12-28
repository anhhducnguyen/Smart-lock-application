const mysql = require('mysql2');

// Thông tin kết nối RDS
const connection = mysql.createConnection({
  host: 'your-rds-endpoint',  
  user: 'nodeapp',      
  password: 'student12',  
  database: 'STUDENTS',  
  port: 3306                  // Cổng mặc định MySQL
});

// Kiểm tra kết nối
connection.connect(function(err) {
  if (err) {
    console.error('Lỗi kết nối: ' + err.stack);
    return;
  }
  console.log('Kết nối thành công với ID kết nối: ' + connection.threadId);
});

// Đóng kết nối sau khi kiểm tra
connection.end();
