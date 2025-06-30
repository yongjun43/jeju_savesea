# 🌊 Jeju SaveSea: 해양 쓰레기 탐지 및 예측 AI 시스템

> 위성 이미지 및 CCTV 데이터를 기반으로 제주 연안의 **해양 쓰레기 탐지·예측**을 수행하는 통합 AI 파이프라인 프로젝트입니다.

---

## 🧭 프로젝트 개요

- **문제 정의**  
  제주 연안의 해양 쓰레기는 지속적으로 발생하고 있지만, 인력 부족과 넓은 범위로 인해 사전 대응이 어렵습니다.

- **목표**  
  위성 이미지 및 CCTV를 활용한 실시간 쓰레기 탐지와 시계열 예측 모델을 통해 **쓰레기 핫스팟 예측 및 대응 지원**.

---

## 🧠 주요 기술 구성

| 모듈 | 기술 스택 / 모델 |
|------|-------------------|
| 🛰️ 위성 기반 탐지 | YOLOv8-nano (Tiny Object Detection) |
| 🧹 초해상도 보정 | EDSR, NAFNet, SRCNN, HAT |
| 🔁 시계열 예측 | POI 기반 Trash 흐름 추정 모델 |
| 🌐 웹 프론트 | HTML/JS 기반 시각화 (`mysite/`) |

---

## 📂 폴더 구조

```
jeju_savesea/
├── HSP-yolov8/              # 위성 기반 쓰레기 탐지 (YOLOv8)
├── SR/                      # 초해상도 복원 (EDSR, HAT, NAFNet 등)
├── POIRecommender/          # 쓰레기 이동 경로 예측 (POI 기반)
├── mysite/                  # 웹 시각화 프론트엔드
├── jeju_icon/               # 지도 시각화용 아이콘 모음
├── assets/                  # 결과 이미지 / 예시 샘플
├── data/                    # 샘플 이미지 / 메타데이터
├── scripts/                 # 실행 스크립트 (추론, 시각화)
└── README.md                # 본 문서
```


---

## 🔍 주요 모듈 설명

### 🔹 HSP-yolov8 (해양 쓰레기 탐지)
- YOLOv8 기반으로 소형 객체 (plastic, rope 등) 탐지
- 위성 이미지 기반 전이학습 (DOTA 활용)
- 커스텀 손실 함수 및 Tiny Object 전처리 적용

### 🔹 SR (초해상도 보정)
- EDSR, HAT, SRCNN 등 다양한 모델로 위성 해상도 향상
- `jeju_frames.ipynb`: 실제 CCTV 프레임 보정 실험
- `SRCNN_NAFNet.ipynb`: 최신 lightweight 모델 실험 포함

### 🔹 POIRecommender (이동 예측)
- 해양 쓰레기 분포 위치 기반 주변 유입 예상
- 시계열 구조 + POI(관광지/하천 위치) 기반 추정
- KoAlpaca 기반 RAG 실험도 포함됨

### 🔹 mysite (웹 시각화)
- 지도 상에서 쓰레기 탐지 결과 및 예측 위치 시각화
- 실시간 추론 결과 렌더링 구성 가능

---

## 📊 주요 성과

| 항목 | 성과 |
|------|------|
| 위성 탐지 정확도 (YOLOv8-nano) | **mAP 0.742** |
| 초해상도 적용 후 PSNR 개선 | **+5.2dB** (NAFNet 기준) |
| 쓰레기 예측 정확도 (F1) | **81.9%** |
| 본선 진출 | 2024 제주 위성활용 경진대회 🏅 |

---

## 🖼️ 결과 예시

| 입력 위성 이미지 | 쓰레기 탐지 결과 | 초해상도 적용 결과 |
|------------------|------------------|---------------------|
| ![](assets/input.png) | ![](assets/yolo_result.png) | ![](assets/sr_result.png) |

---

## ⚙️ 실행 방법

```bash
# 1. 설치
pip install -r requirements.txt

# 2. 탐지 실행
python scripts/detect_trash.py --img data/sample.png

# 3. 예측 실행
python scripts/predict_hotspot.py --history data/trash_history.csv

# 4. 초해상도 실행 (예시)
python SR/edsr/test.py --img data/lowres.png
