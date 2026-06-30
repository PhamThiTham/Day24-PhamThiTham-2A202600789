# src/pii/detector.py
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider


def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    Sử dụng NLP engine mặc định (có hỗ trợ email detection built-in).
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có đúng 12 chữ số
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\b\d{12}\b",  # regex cho 12 chữ số
        score=0.9
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        patterns=[cccd_pattern],
        context=["cccd", "căn cước", "chứng minh", "cmnd"]
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (0[3|5|7|8|9]xxxxxxxx)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"\b0[35789]\d{8}\b",  # regex cho số điện thoại VN
            score=0.85
        )],
        context=["điện thoại", "sdt", "phone", "liên hệ"]
    )

    # --- TASK 2.2.3 ---
    # Sử dụng NLP engine mặc định (không cần spaCy Vietnamese model)
    # Presidio analyzer mặc định đã hỗ trợ PERSON và EMAIL_ADDRESS
    analyzer = AnalyzerEngine()

    # --- TASK 2.2.4 ---
    # Add các custom recognizer vào registry
    analyzer.registry.add_recognizer(cccd_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,
        language="en",  # Dùng English NLP engine mặc định
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
    return results