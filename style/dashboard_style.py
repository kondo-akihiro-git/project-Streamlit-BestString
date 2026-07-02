# style/dashboard_style.py

# 基本スタイル
TYPOGRAPHY_VARIANT = "body2"
CARD_ELEVATION = 0
CONTAINER_BORDER = True
CONTAINER_GAP = None
CARD_CONTENT_SX = {
    "paddingBottom": "8px",
    "&:last-child": {"paddingBottom": "8px"},
}

# ガットが切れている/切れていない場合のCardスタイル
BROKEN_CARD_SX = {
    "backgroundColor": "#e0e0e0",
    "opacity": 0.7,
    "&:last-child": {"paddingBottom": "0px"},
}
NORMAL_CARD_SX = {}

# 縦横ストリングの高さを固定するスタイル
TITLE_BOX_SX = {"minHeight": 50}

# 画像のスタイル
IMAGE_BOX_SX_TEMPLATE = {
    "backgroundImage": "url({image_url})",
    "backgroundRepeat": "no-repeat",
    "backgroundPosition": "center",
    "backgroundSize": "auto 100%",
    "minHeight": 180,
}