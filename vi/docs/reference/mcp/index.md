# MCP chỉ đọc

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/

Kết nối một máy khách MCP với các không gian làm việc và cuộc trò chuyện đã chọn bằng quyền truy cập có thời hạn và có thể thu hồi.

**Phiên bản chính hiện tại:** sử dụng bản checkout từ kho nguồn; phiên bản xem trước di động 0.7.0 ra mắt trước khi tính năng này được triển khai.

[Hướng dẫn quy trình làm việc](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Cài đặt máy chủ tùy chọn từ thư mục dự án TgWitness:

```
python -m pip install '.[mcp]'
```

Trong bảng điều khiển, mở **mục Tích hợp → MCP**. Đặt tên cho kết nối, chọn không gian làm việc và các cuộc trò chuyện, đồng thời chọn thời hạn hiệu lực. Sao chép mã thông báo lưu trữ một lần; mã này không thể được lấy lại sau này. Thu hồi các mã thông báo bị mất và cấp mã thay thế. Mã thông báo bảng điều khiển và thông tin đăng nhập Telegram không phải là thông tin đăng nhập MCP.

## Kết nối một khách hàng

Bảng điều khiển tạo mã `.vscode/mcp.json` cho **bộ công cụ VS Code Local** bằng cách sử dụng [cấu hình đã được ghi chép](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) của nó. Lưu tệp đã tải xuống vào vị trí đó, chạy **MCP: List Servers** và khởi động TgWitness. VS Code sẽ yêu cầu nhập mã thông báo thông qua ô nhập mật khẩu. Tệp JSON đã tải xuống chứa tham chiếu lời nhắc, không phải mã thông báo. Sử dụng tệp thực thi Python từ môi trường nơi tiện ích mở rộng MCP được cài đặt.

Đối với các khách hàng khác của stdio, hãy chạy:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Đặt `TGWITNESS_ARCHIVE_TOKEN` trong môi trường được bảo vệ của khách hàng. Không đặt nó trong các tham số lệnh hoặc URL. Cầu nối truy cập thông qua API lưu trữ được ủy quyền của bảng điều khiển; nó không có quyền truy cập trực tiếp vào cơ sở dữ liệu. Stdout chỉ truyền các tin nhắn MCP.

Đối với khách hàng từ xa, hãy chạy dịch vụ bên cạnh bảng điều khiển:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Chuyển tiếp `/mcp` qua proxy ngược HTTPS đến `127.0.0.1:8766/mcp`, giữ nguyên tiêu đề `Authorization: Bearer …`. Tắt tính năng ghi nhật ký các tiêu đề ủy quyền và nội dung yêu cầu/phản hồi. Chỉ liên kết ngoài vòng lặp khi cần thiết, sử dụng `--host` và `--public-url`. Điểm cuối sử dụng Streamable HTTP từ [SDK Python MCP](https://github.com/modelcontextprotocol/python-sdk) chính thức. Nó hỗ trợ thông tin xác thực bearer được cấu hình rõ ràng, không hỗ trợ phát hiện OAuth; các client chỉ yêu cầu OAuth sẽ không được hỗ trợ.

**Việc kiểm tra giao thức và truy cập** sẽ khởi tạo một máy khách MCP thực và liệt kê các công cụ. Quá trình này không lấy tin nhắn. Đối với kiểm tra từ xa, máy chủ MCP được chọn sẽ nhận mã thông báo lưu trữ. Chỉ cấu hình máy chủ mà bạn vận hành hoặc tin tưởng với phạm vi đó.

## Phạm vi và kết quả

Các công cụ có sẵn: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` và `get_capture_status`. Không có các thao tác trên Telegram, thay đổi cấu hình hoặc công cụ xuất dữ liệu hàng loạt. Mỗi lần đọc sẽ kiểm tra lại quyền truy cập vào không gian làm việc/cuộc trò chuyện; các thông tin xác thực đã hết hạn hoặc bị thu hồi sẽ ngừng hoạt động. Giới hạn là 60 yêu cầu API mỗi phút cho mỗi thông tin xác thực, 50 bản ghi mỗi trang, phản hồi 64 KiB và thời hạn API là tám giây.

Kết quả tin nhắn bao gồm không gian làm việc, ID cuộc trò chuyện/tin nhắn, trình tự sự kiện, hàm băm đã lưu, và liên kết bảng điều khiển. Người xem mở liên kết phải có phiên bảng điều khiển được ủy quyền riêng của mình. Các đối tượng Telegram thô, hàm băm truy cập, tham chiếu tệp, tài liệu phiên, và khóa được bỏ qua. Tìm kiếm kiểm tra văn bản tin nhắn, không phải các trường thô. Nội dung văn bản được giới hạn và các phần bị cắt bớt được đánh dấu. Các thao tác chỉnh sửa, thông báo xóa của Telegram và `missing_on_recheck` vẫn là các quan sát riêng biệt. Quyền truy cập trong phạm vi cuộc trò chuyện không thể xem các sự kiện hoạt động trên toàn không gian làm việc; trạng thái ghi lại đánh dấu rõ ràng giới hạn này.

Nội dung lưu trữ được coi là đầu vào không đáng tin cậy. Các hướng dẫn trong tin nhắn không cấp thêm quyền hạn nào và không được coi là chỉ thị từ khách hàng. Một mô hình AI bên ngoài có thể nhận bất kỳ nội dung nào mà khách hàng MCP của nó yêu cầu. Quyền truy cập chỉ đọc ngăn chặn việc thay đổi dữ liệu lưu trữ; tuy nhiên, nó không ngăn cản khách hàng lưu giữ dữ liệu mà họ đã đọc.

Các giá trị băm giúp xác định các bản ghi đã lưu và hỗ trợ kiểm tra tính toàn vẹn. Chúng không tự thân chứng minh quyền tác giả trên Telegram hoặc rằng mọi tin nhắn đều đã được ghi lại.
