import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
# ✅ 현재 위치(app/services) 기준 임포트
from services.palm_interpreter import PalmInterpreter

class PalmService:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.interpreter = PalmInterpreter()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=1)
        self.line_config = {
            0: {'ko': '운명선', 'name': 'fate', 'color': [140, 150, 255]},
            1: {'ko': '두뇌선', 'name': 'head', 'color': [255, 230, 150]},
            2: {'ko': '감정선', 'name': 'heart', 'color': [255, 120, 120]},
            3: {'ko': '생명선', 'name': 'life', 'color': [120, 255, 230]},
        }

    def analyze(self, image_bytes: bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        h, w = img.shape[:2]

        # 1. MediaPipe 분석 (손 크기 측정)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_res = self.hands.process(img_rgb)
        mounts, metrics = self._get_hand_metrics(mp_res, w, h)

        # 2. YOLO 분석 (손금 선 찾기)
        results = self.model.predict(img, conf=0.05, verbose=False)
        best_lines, lines_json = self._process_yolo_results(results)

        # 3. 피처 추출 (해석용 데이터 계산)
        features = self._calculate_features(best_lines, metrics)

        # 4. 리포트 생성
        report_html = self.interpreter.interpret(features, mounts, metrics)

        return {
            "lines": lines_json,
            "report": report_html,
            "image_size": {"width": w, "height": h}
        }

    def _get_hand_metrics(self, mp_res, w, h):
        mounts = {}
        metrics = {'height': 100.0, 'palm_width': 100.0}
        if mp_res.multi_hand_landmarks:
            lm = mp_res.multi_hand_landmarks[0].landmark
            def p(idx): return np.array([int(lm[idx].x * w), int(lm[idx].y * h)])
            metrics['height'] = float(np.linalg.norm(p(12) - p(0)))
            metrics['palm_width'] = float(np.linalg.norm(p(5) - p(17)))
            mounts['地'] = p(0).tolist()
            mounts['목성'] = p(5).tolist()
            mounts['토성'] = p(9).tolist()
            mounts['태양'] = p(13).tolist()
            mounts['수성'] = p(17).tolist()
            mounts['火'] = ((p(17) + p(0)) * 0.5).tolist()
        return mounts, metrics

    def _process_yolo_results(self, results):
        lines_json = []
        best_lines = {}
        if results and results[0].keypoints is not None:
            kpts_all = results[0].keypoints.xy.cpu().numpy()
            clses = results[0].boxes.cls.cpu().numpy()
            confs = results[0].boxes.conf.cpu().numpy()
            for idx, kpts in enumerate(kpts_all):
                cls_id = int(clses[idx])
                if cls_id not in self.line_config: continue
                if cls_id not in best_lines or confs[idx] > best_lines[cls_id]['conf']:
                    valid_pts = [[float(x), float(y)] for x, y in kpts if x > 0]
                    best_lines[cls_id] = {'conf': float(confs[idx]), 'points': np.array(valid_pts)}
            for cls_id, data in best_lines.items():
                lines_json.append({
                    "name": self.line_config[cls_id]['name'],
                    "label": self.line_config[cls_id]['ko'],
                    "color": self.line_config[cls_id]['color'],
                    "points": data['points'].tolist()
                })
        return best_lines, lines_json

    def _calculate_features(self, best_lines, metrics):
        features = {}
        for cls_id, data in best_lines.items():
            name = self.line_config[cls_id]['name']
            pts = data['points']
            curve_len = np.sum(np.sqrt(np.sum(np.diff(pts, axis=0)**2, axis=1)))
            euclidean = np.linalg.norm(pts[-1] - pts[0])
            features[name] = {
                'points': pts,
                'len_ratio': float(curve_len / metrics['height']),
                'curv': float(curve_len / (euclidean + 1e-6)),
                'conf': data['conf']
            }
        return features