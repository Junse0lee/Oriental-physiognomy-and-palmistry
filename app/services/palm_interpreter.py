import random
import numpy as np

class PalmInterpreter:
    def __init__(self):
        # 1. 분석 기준값 (Thresholds)
        self.TH = {
            'gap': [0.01, 0.03, 0.05, 0.07, 0.10, 0.13, 0.18], 
            'life_len': [0.30, 0.38, 0.44, 0.50, 0.56, 0.62, 0.70], 
            'curv': [1.02, 1.05, 1.09, 1.14, 1.20], 
            'slope': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8] 
        }

        # 2. 구역(Mounts) 고정 텍스트
        self.mount_texts = {
            '목성': "👑 <b>[명예와 지배력]</b><br>검지 아래가 발달했습니다. 야망이 크고 리더십이 뛰어난 리더 타입입니다.",
            '토성': "🐢 <b>[책임과 인내]</b><br>중지 아래가 선명합니다. 신중하고 성실하며 철학적인 사고를 즐깁니다.",
            '태양': "💎 <b>[성공과 예술성]</b><br>약지 아래의 기운이 좋습니다. 창의적이며 대중의 인기를 얻을 운명입니다.",
            '수성': "💰 <b>[비즈니스와 사교]</b><br>새끼손가락 아래가 발달했습니다. 언변이 좋고 재물운을 끌어당기는 수완가입니다.",
            '地': "🌳 <b>[생명의 근원]</b><br>손목 위쪽 구역입니다. 타고난 건강 체질이며 기초가 탄탄한 타입입니다.",
            '火': "🦁 <b>[용기와 투쟁]</b><br>손바닥 중앙 부근입니다. 정의감이 넘치고 시련 앞에서도 굴하지 않는 강한 정신력을 가졌습니다."
        }

        # 3. 상세 운세 데이터베이스 (누락 방지 통합)
        self.texts = {
            'life_start': {
                'glue': "🔒 <b>[신중한 완벽주의자]</b><br>돌다리도 두드려 보고 건너는 신중함을 타고났습니다.",
                'tight': "👀 <b>[배려심 깊은 평화주의자]</b><br>남의 눈치를 조금 보는 편이지만 배려심이 깊습니다.",
                'normal_tight': "🛡️ <b>[외유내강형]</b><br>안전지향적이지만 확신이 서면 과감하게 밀고 나가는 스타일입니다.",
                'normal': "⚖️ <b>[처세술의 달인]</b><br>독립심과 협동심이 황금비율을 이루고 있군요.",
                'normal_loose': "🏃 <b>[자수성가의 싹]</b><br>스스로의 힘으로 서려는 독립심이 강합니다.",
                'loose': "🦅 <b>[자유로운 영혼]</b><br>남들이 '예'라고 할 때 '아니오'라고 말할 수 있는 용기가 있습니다.",
                'free': "🚀 <b>[시대를 앞서가는 혁신가]</b><br>와우, 완전히 분리된 KY선! 세상을 놀라게 할 운명입니다."
            },
            'life_length_book': {
                'long': "🧬 <b>[축복받은 장수운]</b><br>생명선이 시원하게 뻗었습니다. 회복력이 매우 강합니다.",
                'middle': "🏃 <b>[균형 잡힌 웰빙 라이프]</b><br>자신의 페이스를 조절할 줄 아는 현명함이 보입니다.",
                'short': "⚠️ <b>[짧고 굵은 불꽃]</b><br>에너지를 한 번에 몰아서 쓰는 열정적인 스타일입니다."
            },
            'life_curve_book': {
                'big': "💪 <b>[지치지 않는 에너자이저]</b><br>육체적 에너지가 차고 넘쳐 성공의 밑거름이 됩니다.",
                'moderate': "🌿 <b>[외유내강의 정석]</b><br>겉은 온화해 보이지만 내면에는 단단한 심지가 있습니다.",
                'small': "🍃 <b>[섬세한 감수성]</b><br>머리와 감성을 쓰는 분야에서 두각을 나타낼 것입니다."
            },
            'life_direction_book': {
                'thumb': "🏠 <b>[가정이 1순위]</b><br>당신에게 가장 중요한 가치는 '가족'과 '안정'입니다.",
                'wrist': "🌲 <b>[안정을 택하는 나무]</b><br>익숙한 환경에서 꾸준하게 성과를 내는 스타일입니다.",
                'pinky': "✈️ <b>[세계를 누비는 역마살]</b><br>끊임없이 새로운 환경에서 성공할 운명입니다."
            },
            'head_length_book': {
                'long': "🐢 <b>[깊이 생각하는 전략가]</b><br>모든 경우의 수를 계산한 뒤 움직이는 타입입니다.",
                'short': "⚡ <b>[직관이 번뜩이는 승부사]</b><br>복잡한 이론보다 직관을 믿으며 순발력이 대단합니다."
            },
            'head_shape_book': {
                'straight': "📐 <b>[팩트폭격기 이과형]</b><br>논리와 데이터, 팩트를 중요시하는 스타일입니다.",
                'curved': "🎨 <b>[감성 충만 문과형]</b><br>상상력이 풍부하고 사람의 마음을 잘 읽습니다."
            },
            'head_destination_book': {
                'mars_2': "💰 <b>[실리파]</b> 현실 감각이 매우 뛰어납니다.",
                'moon_middle': "🎉 <b>[아이디어 뱅크]</b> 유연한 사고와 재치가 넘칩니다.",
                'mercury': "🕵️ <b>[전략가]</b> 틈새시장을 찾아내는 능력이 탁월합니다.",
                'sun': "💎 <b>[스타성]</b> 자신을 돋보이게 하는 방법을 잘 압니다."
            },
            'heart_start_book': {
                'standard': "⚖️ <b>[황금비율]</b> 이성과 감정의 균형이 아주 좋습니다.",
                'high': "🔥 <b>[열정파]</b> 사랑에 빠지면 물불 가리지 않습니다.",
                'low': "❄️ <b>[포커페이스]</b> 진중하고 깊은 마음을 가진 의리파입니다."
            },
            'heart_shape_book': {
                'straight': "📏 <b>[직진 스타일]</b> 솔직하게 감정을 표현하는 쿨한 성격입니다.",
                'curved': "🌊 <b>[힐러 스타일]</b> 타인의 감정을 잘 보듬는 따뜻한 마음씨를 가졌습니다."
            },
            'heart_end_book': {
                'jupiter': "🏰 <b>[로맨티시스트]</b> 한 번 마음을 열면 변치 않습니다.",
                'middle_down': "😎 <b>[자유인]</b> 구속받는 것을 싫어하는 쿨한 매력이 있습니다."
            },
            'fate_path': {
                'support': "🤝 <b>[최고의 참모]</b> 보좌할 때 빛을 발하는 서포터형 인재입니다.",
                'self_made': "🌟 <b>[자수성가]</b> 오직 실력과 노력으로 성공할 운명입니다."
            },
            'fate_start_book': {
                'venus': ["👪 <b>[금수저의 기운]</b> 가족의 전폭적인 지원을 받습니다."],
                'moon': ["🌟 <b>[대중의 인기]</b> 타인의 도움으로 성공할 운명입니다."],
                'venus_moon_middle': ["🛠️ <b>[성실함의 승리]</b> 땀과 노력으로 운을 개척합니다."]
            },
            'fate_end_book': {
                'saturn': ["🏅 <b>[명예로운 성공]</b> 스스로의 목표 달성에 희열을 느낍니다."],
                'head_stop': ["🛑 <b>[신중한 결단]</b> 판단력을 믿고 승부수를 던져야 할 때가 옵니다."],
                'heart_stop': ["❤️ <b>[말년의 여유]</b> 행복한 노후를 중요시하게 됩니다."]
            },
            'special_signs': {
                'm_sign': "🏆 <b>[M자 손금]</b> 부와 명예를 거머쥘 희귀한 길상입니다.",
                'no_fate': "🦅 <b>[자유로운 운명]</b> 정해진 틀 없이 스스로 길을 만듭니다.",
                'rich_triangle': "💰 <b>[재물 창고]</b> 평생 돈 걱정 없는 알부자 손금입니다."
            },
            'spicy_title': "🔞 <b>[Forbidden] 관능의 심연</b>",
            'libido': {
                'level_5': "🔥 <b>[폭주하는 정복자]</b> 압도적인 스테미너를 가진 밤의 지배자입니다.",
                'level_3': "🍷 <b>[농밀한 탐닉자]</b> 상대를 중독시키는 테크니션입니다.",
                'level_1': "🍃 <b>[은밀한 관조자]</b> 정신적 굴복을 즐기는 위험한 타입입니다."
            }
        }

    # --- [수치 분석 핵심 로직 함수들 - 누락되었던 부분들] ---
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

    # --- [메인 해석 엔진] ---
    def interpret(self, features, mounts, hand_metrics):
        html_content = f"""
        <div class="palm-wrapper" style="font-family: 'Malgun Gothic', sans-serif; background: #f0f2f5; padding: 20px; border-radius: 20px;">
            <div style="background: white; padding: 10px 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #e74c3c;">
                <h2 style="margin: 0; color: #1a202c;">🏮 AI 운명 상세 보고서 V1.5</h2>
            </div>
            <div class="palm-scroll-area" style="display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px;">
        """

        # 1. 생명선 분석 (4대 지표 통합)
        if 'life' in features:
            f = features['life']
            msg = []
            gap = features.get('head_life_gap', 0)
            step = self.get_step(gap, self.TH['gap'])
            msg.append(f"<b>[성향]</b> {self.texts['life_start'][['glue', 'tight', 'normal_tight', 'normal', 'normal_loose', 'loose', 'free', 'free'][step]]}")
            msg.append(f"<br><br><b>[건강]</b> {self.texts['life_length_book'][self.analyze_life_length(f, hand_metrics['height'], mounts['地'][1])]}")
            msg.append(f"<br><br><b>[에너지]</b> {self.texts['life_curve_book'][self.analyze_life_curve(f, mounts)]}")
            msg.append(f"<br><br><b>[방향]</b> {self.texts['life_direction_book'][self.analyze_life_dir(f, mounts)]}")
            html_content += self._make_slide_card("🌿 생명선 상세 분석", "#78ffe6", "".join(msg))

        # 2. 두뇌선 분석
        if 'head' in features:
            f = features['head']
            msg = [f"<b>[지능]</b> {self.texts['head_length_book'][self.analyze_head_len(f, mounts)]}",
                   f"<br><br><b>[사고]</b> {self.texts['head_shape_book'][self.analyze_head_shape(f)]}",
                   f"<br><br><b>[분야]</b> {self.texts['head_destination_book'][self.analyze_head_dest(f, mounts, hand_metrics['height'])]}"]
            html_content += self._make_slide_card("🧠 두뇌선 상세 분석", "#ffe696", "".join(msg))

        # 3. 감정선 분석
        if 'heart' in features:
            f = features['heart']
            msg = [f"<b>[온도]</b> {self.texts['heart_start_book'][self.analyze_heart_start_book(f, hand_metrics['height'], mounts['수성'][1])]}",
                   f"<br><br><b>[스타일]</b> {self.texts['heart_shape_book'][self.analyze_heart_shape_book(f)]}",
                   f"<br><br><b>[관계]</b> {self.texts['heart_end_book'][self.analyze_heart_end_book(f, mounts)]}"]
            html_content += self._make_slide_card("❤️ 감정선 상세 분석", "#ff7878", "".join(msg))

        # 4. 운명선 분석
        if 'fate' in features:
            f = features['fate']
            msg = [f"<b>[성공]</b> {self.texts['fate_path']['self_made' if f['conf'] > 0.4 else 'support']}",
                   f"<br><br><b>[기반]</b> {random.choice(self.texts['fate_start_book'][self.analyze_fate_start_book(f, mounts, features)])}",
                   f"<br><br><b>[결말]</b> {random.choice(self.texts['fate_end_book'][self.analyze_fate_end_book(f, mounts, features)])}"]
            if f['conf'] > 0.4: msg.append(f"<br><br>{self.texts['special_signs']['m_sign']}")
            html_content += self._make_slide_card("🌟 운명선 상세 분석", "#8c96ff", "".join(msg))
        else:
            html_content += self._make_slide_card("🌟 운명선", "#8c96ff", self.texts['special_signs']['no_fate'])

        # 5. 구역(Mounts) 분석 카드 생성
        for m_name in ['목성', '토성', '태양', '수성', '地', '火']:
            if m_name in mounts:
                html_content += self._make_slide_card(f"⛰️ {m_name}구", "#E2C37B", self.mount_texts[m_name])

        # 6. 19금 파트
        spicy_key = 'level_5' if ('life' in features and features['life']['curv'] > 1.1) else 'level_3'
        html_content += self._make_slide_card(self.texts['spicy_title'], "#e74c3c", self.texts['libido'][spicy_key])

        html_content += "</div></div>"
        return html_content

    def _make_slide_card(self, title, color, text):
        return f"""
        <div style="flex: 0 0 280px; background: white; padding: 20px; border-radius: 20px; border-top: 10px solid {color}; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-right: 10px;">
            <h3 style="margin: 0 0 10px 0; font-size: 1.1em; color: #1a202c;">{title}</h3>
            <div style="font-size: 0.95em; line-height: 1.6; color: #4a5568;">{text}</div>
        </div>
        """