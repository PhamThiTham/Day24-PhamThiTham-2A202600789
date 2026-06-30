# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [ ] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [ ] Backup cũng phải ở trong lãnh thổ VN
- [ ] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [ ] Thu thập consent trước khi dùng data cho AI training
- [ ] Có mechanism để user rút consent (Right to Erasure)
- [ ] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [ ] Có incident response plan
- [ ] Alert tự động khi phát hiện breach
- [ ] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [ ] Đã bổ nhiệm Data Protection Officer
- [ ] DPO có thể liên hệ tại: dpo@medviet.com

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | CloudTrail + API access logs | ⬜ Todo | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ⬜ Todo | Security Team |

## F. Technical Solutions for Todo Items

### Audit Logging
- **Solution:** Implement FastAPI middleware để log tất cả API requests vào Elasticsearch hoặc AWS CloudWatch. Mỗi log entry bao gồm: timestamp, user ID, action, resource, IP address, HTTP method, response status code. Sử dụng cấu trúc JSON structured logging và ELK stack để visualize.
- **Cụ thể:**
  - Tạo middleware FastAPI ghi log vào file/DB
  - Tích hợp AWS CloudTrail cho infrastructure-level logging
  - Thiết lập log retention policy tối thiểu 12 tháng theo NĐ13
  - Dùng Grafana Loki hoặc ELK để search và visualize logs

### Breach Detection
- **Solution:** Thiết lập Prometheus + Alertmanager để monitoring real-time. Các alert rules bao gồm:
  1. **Phát hiện access bất thường:** > 10 failed login attempts trong 5 phút từ cùng 1 IP -> alert
  2. **Phát hiện data exfiltration:** > 1000 records được query trong 1 phút -> alert
  3. **Phát hiện PII leak:** Sử dụng Presidio scan trên response body để detect PII -> alert
- **Cụ thể:**
  - Cài đặt Prometheus metrics exporter trong FastAPI
  - Cấu hình các alert rules trong Prometheus
  - Tích hợp với PagerDuty/Email/Slack để notify security team
  - Xây dựng incident response runbook cho từng loại breach
  - Test incident response định kỳ (quarterly tabletop exercises)