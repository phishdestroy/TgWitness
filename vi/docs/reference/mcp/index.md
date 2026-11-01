# MCP chỉ đọc

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/

Kết nối một máy khách MCP với các không gian làm việc và cuộc trò chuyện đã chọn bằng quyền truy cập có thời hạn và có thể thu hồi.

Kết nối một ứng dụng khách dành cho chuyên viên phân tích với các không gian làm việc và cuộc trò chuyện đã chọn. TgWitness phục vụ **Streamable HTTP tại `/mcp` trong tiến trình bảng điều khiển**. Mỗi kết nối có mã thông báo, thời hạn và các công cụ được phép riêng. MCP không thể gửi tin nhắn Telegram, thay đổi cài đặt hoặc sửa đổi nhật ký đã ký.

[Hướng dẫn quy trình làm việc](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Cài đặt và kiểm tra

Sử dụng môi trường Python chạy bảng điều khiển. Từ bản mã nguồn đã tải về:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Khởi động lại bảng điều khiển với thư mục dữ liệu và các đối số khởi chạy thông thường sau khi cài đặt. Trạng thái sẵn sàng sẽ bao gồm `[PASS] mcp: streamable-http available`. **Integrations → MCP** hiển thị trạng thái thời gian chạy và lệnh cài đặt sử dụng tệp thực thi Python thực tế của máy chủ đó. **Re-check** làm mới trạng thái này mà không cần tải lại trang; thao tác này không cài đặt các gói hoặc khởi động lại máy chủ.

Tiện ích MCP extra sử dụng [SDK Python chính thức của MCP](https://github.com/modelcontextprotocol/python-sdk). Tệp`deploy/constraints-mcp.txt` cố định phiên bản SDK và các phụ thuộc đã được kiểm thử.

## Cấp một kết nối

1. Nhập nhãn và chọn các không gian làm việc cũng như cuộc trò chuyện mà ứng dụng khách được phép đọc.
2. Chọn từng công cụ riêng lẻ hoặc sử dụng cấu hình đặt sẵn. Chỉ các công cụ đã được triển khai mới được cung cấp.
3. Chọn 1, 7, 30 hoặc 90 ngày, hoặc thời hạn tùy chỉnh từ một phút đến 90 ngày.
4. Nhấn **Create connection**. Mã thông báo sẽ xuất hiện một lần bên cạnh cấu hình ứng dụng khách.
5. Sao chép mã thông báo và cấu hình, sau đó chạy **Check connection**. Thao tác này sẽ khởi tạo MCP và liệt kê các công cụ được phép; **không có tin nhắn nào được đọc**. Kết quả hiển thị phiên bản giao thức, tên công cụ, số lượng và thời gian đã trôi qua.
6. Nhấn **Done** khi thông tin xác thực đã được lưu. Quá trình thăm dò sẽ giữ nguyên biểu mẫu và thẻ chỉ hiển thị một lần. Việc khóa bảng điều khiển sẽ xóa các thông tin bí mật đang hiển thị.

Danh sách hiển thị lần sử dụng gần đây, công cụ cuối cùng, địa chỉ và các yêu cầu trong phút vừa qua. **Revoke** chấm dứt quyền truy cập. **Rotate token** thu hồi thông tin xác thực cũ và cấp một mã thay thế có cùng phạm vi, công cụ và thời hạn; hãy sao chép mã thay thế hiển thị một lần này. Mã thông báo đăng nhập bảng điều khiển và thông tin xác thực Telegram không hoạt động như mã thông báo MCP.

## Kết nối ứng dụng khách của bạn

Chọn ứng dụng khách trong bảng điều khiển và sao chép cấu hình được tạo ra. Các cấu hình sử dụng tham chiếu bí mật hoặc trình giữ chỗ tường minh; mã thông báo được sao chép riêng.

| Ứng dụng khách | Cấu hình | Kết nối |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, tiêu đề bearer |
| Claude Desktop | `claude_desktop_config.json` | Cầu nối stdio cục bộ |
| Cursor | `.cursor/mcp.json` | HTTP với tiêu đề biến môi trường |
| VS Code Local | `.vscode/mcp.json` | HTTP với đầu vào mật khẩu `promptString` |
| Windsurf | `mcp_config.json` | HTTP với trình giữ chỗ tiêu đề bearer |
| Các ứng dụng khách khác | URL và tiêu đề Authorization | Streamable HTTP |

TgWitness sử dụng mã thông báo bearer mà không cần khám phá OAuth. Sử dụng cầu nối stdio cục bộ cho các ứng dụng khách có trình kết nối từ xa yêu cầu OAuth. Đối với VS Code, các biến đầu vào áp dụng cho môi trường **Local** và không được chuyển tiếp tới các phiên Copilot. Tài liệu tham khảo cấu hình: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Điểm nhập chuẩn cho cầu nối cục bộ là:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Sử dụng Python cục bộ của ứng dụng khách đã cài đặt phần bổ sung MCP. Đặt `TGWITNESS_MCP_TOKEN` trong môi trường được bảo vệ của nó. Giữ thông tin xác thực ngoài các đối số lệnh và URL. `tgwitness-mcp` là cùng một điểm nhập. Mô-đun `tgwitness.mcp_bridge` cũ và tên `TGWITNESS_ARCHIVE_TOKEN` vẫn được giữ lại làm đường dẫn tương thích kèm theo cảnh báo; các cấu hình mới sử dụng `mcp_server` và `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Chuyển tiếp tuyến đường `/mcp` của bảng điều khiển và giữ nguyên tiêu đề bearer. Việc mở cài đặt MCP với tư cách quản trị viên sẽ đăng ký nguồn (origin) hiện tại của bảng điều khiển cho lần chạy này. Để có một địa chỉ ổn định khả dụng ngay sau khi khởi động lại, hãy cấu hình `TGWITNESS_PUBLIC_URL` với nguồn HTTPS của bảng điều khiển trước khi khởi động bảng điều khiển. Các tiêu đề Host và tiêu đề được chuyển tiếp tùy ý không đăng ký một địa chỉ đáng tin cậy. Việc kiểm tra Host và Origin sẽ từ chối các nguồn trình duyệt không liên quan. Các phản hồi sử dụng `Cache-Control: no-store`; các giá trị ủy quyền không bao giờ được ghi vào nhật ký.

Địa chỉ `*.trycloudflare.com` chỉ là tạm thời. Khi việc khởi động lại đường hầm làm thay đổi tên máy chủ (hostname), hãy cập nhật URL công khai đã cấu hình và URL MCP của từng ứng dụng khách. Sử dụng một tên máy chủ ổn định cho các cấu hình ứng dụng khách đã lưu.

## Công cụ và giới hạn

| Công cụ | Dữ liệu đọc |
| --- | --- |
| `list_workspaces` | Các không gian làm việc được cấp quyền |
| `list_chats` | Các cuộc trò chuyện được cấp quyền |
| `search_messages` | Văn bản tin nhắn đã lưu trong khoảng thời gian đã chọn |
| `get_message_versions` | Các phiên bản đã thu thập và các ghi nhận xóa |
| `get_message_context` | ID của các tin nhắn lân cận đã thu thập |
| `get_journal_event` | Một bản ghi đã được làm sạch kèm theo tham chiếu nguồn của nó |
| `get_capture_status` | Trạng thái thu thập và các bản ghi phạm vi bao phủ được phép |

`tools/list` chỉ trả về các công cụ được cấp cho kết nối đó. Các lệnh gọi đến những công cụ khác sẽ bị từ chối. Các công cụ ngữ cảnh nhóm, phân đoạn (episode), thuật ngữ và chuỗi trả lời không được cung cấp trong bản dựng này; phần phụ trợ gói ngữ cảnh riêng biệt của chúng không được bao gồm.

Mọi thao tác đọc đều kiểm tra mã thông báo, công cụ và phạm vi không gian làm việc/cuộc trò chuyện, kể cả sau khi công việc của cơ sở dữ liệu hoàn tất. Giới hạn là 60 yêu cầu mỗi phút, 50 bản ghi mỗi trang, 64 KiB mỗi kết quả và thời hạn truy xuất kho lưu trữ là tám giây. Một lệnh gọi MCP hết thời gian chờ sẽ trả về lỗi công cụ yêu cầu khoảng thời gian hẹp hơn hoặc giới hạn thấp hơn.

Kết quả tin nhắn mang thuộc tính `untrusted_content: true`, ID không gian làm việc/cuộc trò chuyện/tin nhắn, trình tự sự kiện, mã băm đã lưu và liên kết bảng điều khiển. Các đối tượng Telegram thô, mã băm truy cập, phiên và khóa đều bị lược bỏ. Việc cắt bớt văn bản được đánh dấu rõ. Các chỉnh sửa, thông báo xóa và `missing_on_recheck` là những ghi nhận riêng biệt. Các bản ghi bị thiếu không chứng minh rằng một sự kiện chưa từng xảy ra.

Hãy coi các chỉ dẫn bên trong những tin nhắn đã thu thập là bằng chứng, tuyệt đối không coi đó là chỉ dẫn dành cho ứng dụng khách. Quyền truy cập chỉ đọc ngăn chặn việc thay đổi kho lưu trữ; ứng dụng khách vẫn có thể lưu giữ nội dung mà nó được phép đọc. Các mã băm xác định những bản ghi đã lưu và hỗ trợ kiểm tra tính toàn vẹn; chúng không chứng minh quyền tác giả trên Telegram hoặc việc thu thập đầy đủ.
