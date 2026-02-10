import random
import numpy as np

class PalmInterpreter:
    def __init__(self):
        # 1. 분석 기준값 (Colab 코드 기준)
        self.TH = {
            'gap': [0.01, 0.03, 0.05, 0.07, 0.10, 0.13, 0.18], 
            'life_len': [0.30, 0.38, 0.44, 0.50, 0.56, 0.62, 0.70], 
            'curv': [1.02, 1.05, 1.09, 1.14, 1.20], 
            'slope': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8] 
        }

        # 2. 텍스트 데이터베이스 (Colab 원본 문구 그대로 반영)
        self.texts = {
            'life_start': {
                'glue': "🔒 <b>[신중한 완벽주의자]</b><br>돌다리도 두드려 보고 건너는 신중함을 타고났습니다. '실패하면 어떡하지?'라는 걱정이 많지만, 그 꼼꼼함 덕분에 큰 실수를 하지 않는 듬직한 사람입니다.",
                'tight': "👀 <b>[배려심 깊은 평화주의자]</b><br>남의 눈치를 조금 보는 편입니다. 배려심이 깊어 '착한 사람' 소리를 듣지만, 본인의 속마음은 꾹꾹 눌러담느라 답답할 때가 있죠?",
                'normal_tight': "🛡️ <b>[외유내강형]</b><br>안전지향적이지만 확신이 서면 과감하게 밀고 나가는 스타일입니다. 겉은 부드러워 보이지만 속은 단단한 바위 같습니다.",
                'normal': "⚖️ <b>[처세술의 달인]</b><br>가장 이상적인 밸런스입니다! 독립심과 협동심이 황금비율을 이루고 있군요. 적을 만들지 않으면서도 실속을 챙길 줄 아는 사회생활 만렙입니다.",
                'normal_loose': "🏃 <b>[자수성가의 싹]</b><br>부모님 품을 일찍 떠나거나 스스로의 힘으로 서려는 독립심이 강합니다. 누군가에게 기대기보다 내가 직접 성취했을 때 희열을 느낍니다.",
                'loose': "🦅 <b>[자유로운 영혼]</b><br>남들이 '예'라고 할 때 '아니오'라고 말할 수 있는 용기가 있습니다. 사회의 틀에 얽매이기보다 내 방식대로 삶을 개척하려는 배짱이 당신의 무기입니다.",
                'free': "🚀 <b>[시대를 앞서가는 혁신가]</b><br>와우, 완전히 분리된 KY선! 스티브 잡스 같은 혁신가들의 손금입니다. 남들은 이해 못 할 독창적인 생각과 과감한 결단력으로 세상을 놀라게 할 운명입니다."
            },
            'life_length_book': {
                'long': "🧬 <b>[축복받은 장수운]</b><br>생명선이 손목까지 시원하게 뻗었습니다. 타고난 면역력이 강해 잔병치레를 하더라도 금방 털고 일어나는 '오뚝이' 같은 회복력을 지녔습니다.",
                'middle': "🏃 <b>[균형 잡힌 웰빙 라이프]</b><br>생명선이 손목 위쪽에서 깔끔하게 마무리됩니다. 무리하지 않고 자신의 페이스를 조절할 줄 아는 현명함이 보입니다.",
                'short': "⚠️ <b>[짧고 굵은 불꽃]</b><br>수명이 짧다기보다 에너지를 한 번에 몰아서 쓰는 '단기 집중형'입니다. 열정이 넘쳐 몸을 혹사시키는 경향이 있으니, 쉼표를 찍는 연습이 필요합니다."
            },
            'life_curve_book': {
                'big': "💪 <b>[지치지 않는 에너자이저]</b><br>금성구가 매우 발달하여 가만히 있으면 병이 나는 스타일입니다. 육체적, 정신적 에너지가 차고 넘쳐 성공의 밑거름이 됩니다.",
                'moderate': "🌿 <b>[외유내강의 정석]</b><br>겉으로는 온화해 보이지만 내면에는 단단한 심지가 있습니다. 일할 땐 열정적이지만 쉴 때는 확실히 쉬는, 워라밸을 아는 현명한 사람입니다.",
                'small': "🍃 <b>[섬세한 감수성]</b><br>타고난 체력이 강한 편은 아니기에 쉽게 피로를 느낄 수 있습니다. 육체노동보다는 머리와 감성을 쓰는 분야에서 두각을 나타낼 것입니다."
            },
            'life_direction_book': {
                'thumb': "🏠 <b>[가정이 1순위]</b><br>당신에게 가장 중요한 가치는 '가족'과 '안정'입니다. 말년에는 따뜻한 노후를 보낼 것입니다.",
                'wrist': "🌲 <b>[안정을 택하는 나무]</b><br>익숙한 환경에서 꾸준하게 성과를 내며, 고독을 즐길 줄 아는 깊이 있는 사람입니다.",
                'pinky': "✈️ <b>[세계를 누비는 역마살]</b><br>이사, 이직, 해외 생활 등 끊임없이 새로운 환경을 찾아다니며 성공할 운명입니다."
            },
            'head_length_book': {
                'long': "🐢 <b>[깊이 생각하는 철학자]</b><br>모든 경우의 수를 계산한 뒤 움직이는 전략가 타입입니다.",
                'short': "⚡ <b>[직관이 번뜩이는 승부사]</b><br>복잡한 이론보다 직관을 믿으며, 순발력이 대단합니다."
            },
            'head_shape_book': {
                'straight': "📐 <b>[팩트폭격기 이과형]</b><br>논리와 데이터, 팩트를 중요시합니다. 일 처리가 깔끔하여 '일 잘한다'는 소리를 듣습니다.",
                'curved': "🎨 <b>[감성 충만 문과형]</b><br>상상력이 풍부하고 공감 능력이 좋아 예술이나 창의적인 일에서 빛을 발합니다."
            },
            'head_destination_book': {
                'mars_2': "💰 <b>[돈 냄새를 맡는 실리파]</b> 현실 감각이 매우 뛰어납니다.",
                'moon_upper': "👑 <b>[사람을 이끄는 리더]</b> 현실적인 문제 해결과 창의적 비전을 동시에 갖췄습니다.",
                'moon_middle': "🎉 <b>[아이디어 뱅크]</b> 유연한 사고방식과 재치 있는 입담을 가졌습니다.",
                'mercury': "🕵️ <b>[비상한 전략가]</b> 틈새시장을 찾아내는 능력이 탁월합니다.",
                'sun': "💎 <b>[스타성]</b> 자신을 돋보이게 하는 방법을 본능적으로 압니다."
            },
            'heart_start_book': {
                'standard': ["⚖️ <b>[이성과 감정의 황금비율]</b> 어떤 상황에서도 평정심을 유지합니다.", "⚖️ <b>[믿음직한 파트너]</b> 감정에 휘둘리지 않고 중심을 잡습니다."],
                'high': ["🔥 <b>[브레이크 없는 열정]</b> 사랑에 빠지면 물불 가리지 않습니다!", "💖 <b>[로맨티시스트]</b> 영화 같은 사랑을 꿈꾸는 낭만파입니다."],
                'low': ["❄️ <b>[침착한 포커페이스]</b> 누구보다 깊고 진중한 마음을 가졌습니다.", "🧊 <b>[이성주의자]</b> 감정보다 현실적인 조건을 먼저 고려합니다."]
            },
            'heart_shape_book': {
                'straight': ["📏 <b>[돌직구 직진]</b> 좋으면 좋다 확실하게 표현하는 쿨한 성격입니다.", "🎯 <b>[심플한 사랑]</b> 복잡하게 꼬인 관계보다 진심 공유를 선호합니다."],
                'curved': ["🌊 <b>[따뜻한 힐러]</b> 타인의 감정을 내 것처럼 느끼는 공감 능력이 좋습니다.", "🎨 <b>[예술적 감수성]</b> 풍부한 상상력과 부드러운 영혼을 가졌군요."],
                'hybrid': ["🎭 <b>[반전 매력]</b> 냉정과 열정 사이를 오가는 밀당의 고수입니다."]
            },
            'heart_end_book': {
                'jupiter': "🏰 <b>[신중한 로맨티시스트]</b> 한 번 마음을 열면 변치 않는 건실한 연애를 합니다.",
                'middle_down': "😎 <b>[쿨한 자유인]</b> 구속받는 것을 싫어하고 프라이버시를 중요시합니다."
            },
            'fate_path': {
                'support': "🤝 <b>[최고의 참모]</b> 보좌할 때 빛을 발하는 서포터형 인재입니다.",
                'self_made': "🌟 <b>[자수성가형 성공]</b> 오직 본인의 실력과 노력으로 성공을 일구어낼 운명입니다."
            },
            'fate_start_book': {
                'venus': ["👪 <b>[가문의 영광]</b> 가족의 전폭적인 지원을 받아 운이 열립니다.", "🛡️ <b>[뿌리 깊은 나무]</b> 보이지 않는 조력자가 늘 존재합니다."],
                'moon': ["🌟 <b>[대중의 별]</b> 사람을 끌어당기는 묘한 매력이 있어 인기를 얻습니다.", "🕊️ <b>[경계를 넘는 여행자]</b> 낯선 곳이나 해외에서 운이 트입니다."],
                'venus_moon_middle': ["🛠️ <b>[성실함의 승리]</b> 자신의 땀과 노력으로 운을 개척하는 정직한 사람입니다.", "🏗️ <b>[완벽한 설계자]</b> 철저한 계획으로 견고한 인생을 쌓아갑니다."]
            },
            'fate_end_book': {
                'saturn': ["🏅 <b>[명예로운 성공]</b> 스스로의 목표 달성에 큰 희열을 느낍니다.", "🏔️ <b>[정상의 고독]</b> 사회적 지위와 명성을 모두 거머쥘 운명입니다."],
                'head_stop': ["🛑 <b>[신중한 현실주의자]</b> 30대 중반쯤 한 번의 큰 결단이 필요합니다.", "🧩 <b>[인생의 변환점]</b> 영리함이 자산이 되어 큰 성공을 거둡니다."],
                'heart_stop': ["❤️ <b>[말년의 안식]</b> 행복한 노후를 중요시하게 됩니다.", "🧘 <b>[마음의 안식처]</b> 사랑하는 사람들과 평화로운 삶을 구축합니다."]
            },
            'special_signs': {
                'm_sign': "🏆 <b>[M자 손금]</b> 부와 명예를 거머쥘 희귀한 길상입니다.",
                'rich_triangle': "💰 <b>[재물 창고]</b> 평생 돈 걱정 없는 알부자 손금입니다.",
                'no_fate': "🦅 <b>[자유로운 운명]</b> 정해진 틀 없이 스스로 길을 만듭니다."
            },
            'spicy_title': "🔞 <b>[Forbidden] 관능의 심연</b>",
            'libido': {
                'level_5': "🔥 <b>[폭주하는 정복자]</b> 압도적인 스테미너를 가진 밤의 지배자입니다.",
                'level_3': "🍷 <b>[농밀한 탐닉자]</b> 상대를 중독시키는 테크니션입니다.",
                'level_1': "🍃 <b>[은밀한 관조자]</b> 정신적 굴복을 즐기는 위험한 타입입니다."
            },
            'seduction': {
                'bad_charmer': "😈 <b>[치명적인 조련사]</b> 상대를 정신적으로 해체하는 고수입니다.",
                'hot_lover': "❤️‍🔥 <b>[본능의 노예]</b> 장소를 가리지 않고 욕망을 폭발시킵니다.",
                'shy_fox': "🦊 <b>[낮져밤이]</b> 밀실에서 음탕한 본색을 드러내는 반전 매력입니다."
            },
            'fantasy': {
                'deep': "🦄 <b>[변태적 설계자]</b> 금기를 깨부수는 하드코어 판타지 신봉자입니다.",
                'real': "💼 <b>[현실주의 포식자]</b> 노골적인 육체 충돌 그 자체에 환장합니다."
            }
        }

    def _pick(self, data):
        """리스트면 랜덤 선택, 아니면 그대로 반환 (Colab 로직)"""
        if isinstance(data, list):
            return random.choice(data)
        return data

    # --- 분석 로직 함수들 (Colab 코드 기준) ---
    def get_step(self, value, thresholds):
        for i, th in enumerate(thresholds):
            if value < th: return i
        return len(thresholds)

    def analyze_life_length(self, f, h, wy):
        pts = f['points']; end_y = max(pts, key=lambda p: p[1])[1]
        if end_y > wy * 0.85: return 'long'
        elif end_y > wy * 0.65: return 'middle'
        else: return 'short'

    def analyze_life_curve(self, f, m):
        return 'big' if f['curv'] > 1.12 else ('moderate' if f['curv'] > 1.05 else 'small')

    def analyze_life_dir(self, f, m):
        pts = f['points']; dx = pts[-1][0] - pts[0][0]
        return 'pinky' if dx > 40 else ('thumb' if dx < -40 else 'wrist')

    def analyze_head_len(self, f, m):
        return 'long' if f['len_ratio'] > 0.4 else 'short'

    def analyze_head_shape(self, f):
        return 'straight' if f['curv'] < 1.05 else 'curved'

    def analyze_head_dest(self, f, m, h):
        pts = f['points']; ep = pts[-1]
        if ep[1] < h * 0.5: return 'mars_2'
        return 'moon_middle'

    def analyze_heart_start_book(self, f, h, py):
        pts = f['points']; sy = pts[0][1]
        return 'high' if sy < h * 0.35 else 'standard'

    def analyze_heart_shape_book(self, f):
        return 'curved' if f['curv'] > 1.08 else 'straight'

    def analyze_heart_end_book(self, f, m):
        pts = f['points']; ep = pts[-1]
        return 'jupiter' if ep[0] < m['목성'][0] + 20 else 'middle_down'

    def analyze_fate_start_book(self, f, m, features):
        pts = f['points']; sp = pts[0] if pts[0][1] > pts[-1][1] else pts[-1]
        if sp[0] < m['목성'][0]: return 'venus'
        elif sp[0] > m['수성'][0]: return 'moon'
        return 'venus_moon_middle'

    def analyze_fate_end_book(self, f, m, features):
        pts = f['points']; ep = pts[0] if pts[0][1] < pts[-1][1] else pts[-1]
        if 'heart' in features and abs(ep[1] - features['heart']['points'][0][1]) < 40: return 'heart_stop'
        if 'head' in features and abs(ep[1] - features['head']['points'][0][1]) < 40: return 'head_stop'
        return 'saturn'

    # --- 메인 해석 엔진 (기준 코드 반영) ---
    def interpret(self, features, mounts, hand_metrics):
        html_content = f"""
        <div class="palm-wrapper" style="font-family: 'Malgun Gothic', sans-serif; background: #f0f2f5; padding: 20px; border-radius: 20px;">
            <div style="background: white; padding: 10px 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #e74c3c;">
                <h2 style="margin: 0; color: #1a202c;">🏮 AI 베테랑 역술가 상세 보고서</h2>
            </div>
            <div class="palm-scroll-area" style="display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px;">
        """

        # 1. 생명선
        if 'life' in features:
            f = features['life']
            gap = features.get('head_life_gap', 0)
            step = self.get_step(gap, self.TH['gap'])
            keys = ['glue', 'tight', 'normal_tight', 'normal', 'normal_loose', 'loose', 'free', 'free']
            msg = [
                f"<b>[성향]</b> {self.texts['life_start'][keys[step]]}",
                f"<br><br><b>[건강]</b> {self.texts['life_length_book'][self.analyze_life_length(f, hand_metrics['height'], mounts['地'][1])]}",
                f"<br><br><b>[에너지]</b> {self.texts['life_curve_book'][self.analyze_life_curve(f, mounts)]}",
                f"<br><br><b>[방향]</b> {self.texts['life_direction_book'][self.analyze_life_dir(f, mounts)]}"
            ]
            html_content += self._make_slide_card("🌿 생명선 분석", "#78ffe6", "".join(msg))

        # 2. 두뇌선
        if 'head' in features:
            f = features['head']
            msg = [
                f"<b>[지능]</b> {self.texts['head_length_book'][self.analyze_head_len(f, mounts)]}",
                f"<br><br><b>[사고]</b> {self.texts['head_shape_book'][self.analyze_head_shape(f)]}",
                f"<br><br><b>[분야]</b> {self.texts['head_destination_book'][self.analyze_head_dest(f, mounts, hand_metrics['height'])]}"
            ]
            html_content += self._make_slide_card("🧠 두뇌선 분석", "#ffe696", "".join(msg))

        # 3. 감정선 (랜덤 선택 적용)
        if 'heart' in features:
            f = features['heart']
            s_res = self.analyze_heart_start_book(f, hand_metrics['height'], mounts['수성'][1])
            sh_res = self.analyze_heart_shape_book(f)
            msg = [
                f"<b>[온도]</b> {self._pick(self.texts['heart_start_book'][s_res])}",
                f"<br><br><b>[스타일]</b> {self._pick(self.texts['heart_shape_book'][sh_res])}",
                f"<br><br><b>[관계]</b> {self.texts['heart_end_book'][self.analyze_heart_end_book(f, mounts)]}"
            ]
            html_content += self._make_slide_card("❤️ 감정선 분석", "#ff7878", "".join(msg))

        # 4. 운명선 (랜덤 선택 및 특수 기호 적용)
        if 'fate' in features:
            f = features['fate']
            f_start = self.analyze_fate_start_book(f, mounts, features)
            f_end = self.analyze_fate_end_book(f, mounts, features)
            msg = [
                f"<b>[성공]</b> {self.texts['fate_path']['self_made' if f['conf'] > 0.4 else 'support']}",
                f"<br><br><b>[기반]</b> {self._pick(self.texts['fate_start_book'][f_start])}",
                f"<br><br><b>[결말]</b> {self._pick(self.texts['fate_end_book'][f_end])}"
            ]
            if f['conf'] > 0.4: msg.append(f"<br><br>{self.texts['special_signs']['m_sign']}")
            if f['conf'] > 0.35: msg.append(f"<br><br>{self.texts['special_signs']['rich_triangle']}")
            html_content += self._make_slide_card("🌟 운명선 분석", "#8c96ff", "".join(msg))
        else:
            html_content += self._make_slide_card("🌟 운명선", "#8c96ff", self.texts['special_signs']['no_fate'])

        # 5. 19금 파트 (Colab 기준 - seduction, fantasy 추가)
        msg = []
        sp_key = 'level_5' if ('life' in features and features['life']['curv'] > 1.1) else 'level_3'
        msg.append(self.texts['libido'][sp_key])
        
        if 'heart' in features:
            msg.append(f"<br><br>{self.texts['seduction']['hot_lover' if features['heart']['curv'] > 1.1 else 'shy_fox']}")
        
        if 'head' in features:
            msg.append(f"<br><br>{self.texts['fantasy']['deep' if features['head']['len_ratio'] > 0.45 else 'real']}")

        html_content += self._make_slide_card(self.texts['spicy_title'], "#e74c3c", "".join(msg))

        html_content += "</div></div>"
        return html_content

    def _make_slide_card(self, title, color, text):
        return f"""
        <div style="flex: 0 0 300px; background: white; padding: 25px; border-radius: 20px; border-top: 10px solid {color}; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-right: 15px;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.15em; color: #1a202c; font-weight: 800;">{title}</h3>
            <div style="font-size: 0.95em; line-height: 1.7; color: #4a5568;">{text}</div>
        </div>
        """