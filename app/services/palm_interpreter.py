import random

class PalmInterpreter:
    def __init__(self):
        # 1. 기준값 (Thresholds)
        self.TH = {
            'gap': [0.01, 0.03, 0.05, 0.07, 0.10, 0.13, 0.18], 
            'life_len': [0.30, 0.38, 0.44, 0.50, 0.56, 0.62, 0.70], 
            'curv': [1.02, 1.05, 1.09, 1.14, 1.20], 
            'slope': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8] 
        }

        # 2. 텍스트 데이터베이스 (운세 문구)
        self.texts = {
            'intro': [
                "어서 오십시오. 손바닥을 보니 당신만의 뜨거운 열망이 느껴지는군요. 당신의 무의식이 그려놓은 지도를 읽어드리겠습니다.",
                "손금은 당신이 살아온 치열한 흔적이자 운명의 설계도입니다. 숨겨진 당신의 '진짜' 모습을 읽어드리겠습니다."
            ],
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
                'big': "💪 <b>[지치지 않는 에너자이저]</b><br>육체적, 정신적 에너지가 차고 넘쳐 성공의 밑거름이 됩니다.",
                'moderate': "🌿 <b>[외유내강의 정석]</b><br>겉으로는 온화해 보이지만 내면에는 단단한 심지가 있습니다.",
                'small': "🍃 <b>[섬세한 감수성]</b><br>육체노동보다는 머리와 감성을 쓰는 분야에서 두각을 나타낼 것입니다."
            },
            'life_direction_book': {
                'thumb': "🏠 <b>[가정이 1순위]</b><br>당신에게 가장 중요한 가치는 '가족'과 '안정'입니다.",
                'wrist': "🌲 <b>[안정을 택하는 나무]</b><br>익숙한 환경에서 꾸준하게 성과를 내는 스타일입니다.",
                'pinky': "✈️ <b>[세계를 누비는 역마살]</b><br>이사, 이직, 해외 생활 등 끊임없이 새로운 환경에서 성공할 운명입니다."
            },
            'head_length_book': {
                'long': "🐢 <b>[깊이 생각하는 철학자]</b><br>모든 경우의 수를 계산한 뒤 움직이는 전략가입니다.",
                'short': "⚡ <b>[직관이 번뜩이는 승부사]</b><br>복잡한 이론보다 직관을 믿으며 순발력이 대단합니다."
            },
            'head_shape_book': {
                'straight': "📐 <b>[팩트폭격기 이과형]</b><br>논리와 데이터, 팩트를 중요시하는 깔끔한 일 처리의 소유자입니다.",
                'curved': "🎨 <b>[감성 충만 문과형]</b><br>상상력이 풍부하고 사람의 마음을 읽는 능력이 좋습니다."
            },
            'head_destination_book': {
                'mars_2': "💰 <b>[돈 냄새를 맡는 실리파]</b><br>현실 감각이 매우 뛰어나 재테크나 비즈니스에 강합니다.",
                'moon_upper': "👑 <b>[사람을 이끄는 리더]</b><br>책임감이 강해 조직을 이끄는 리더로서 존경받을 운명입니다.",
                'moon_middle': "🎉 <b>[아이디어 뱅크]</b><br>유연한 사고방식과 재치 있는 입담으로 분위기 메이커 역할을 합니다.",
                'moon_lower': "📚 <b>[영혼이 맑은 예술가]</b><br>정신적인 가치와 마음의 평화를 추구하는 독보적인 세계가 있습니다.",
                'mercury': "🕵️ <b>[비상한 전략가]</b><br>틈새시장을 찾아내는 능력이 탁월하여 컨설팅 분야에서 활약합니다.",
                'sun': "💎 <b>[화려한 스타성]</b><br>자신을 돋보이게 하는 방법을 아는 뷰티, 패션 분야의 인재입니다.",
                'saturn': "🙏 <b>[끝없는 구도자]</b><br>인간의 내면을 탐구하는 일에 깊은 관심이 있는 멘토 자질입니다."
            },
            'heart_start_book': {
                'standard': "⚖️ <b>[이성과 감정의 황금비율]</b><br>어떤 상황에서도 평정심을 유지하여 신뢰받습니다.",
                'high': "🔥 <b>[브레이크 없는 열정]</b><br>사랑에 빠지면 물불 가리지 않는 화끈한 감정 표현의 소유자입니다.",
                'low': "❄️ <b>[침착한 포커페이스]</b><br>누구보다 깊고 진중한 마음을 가진 의리파입니다."
            },
            'heart_shape_book': {
                'straight': "📏 <b>[돌직구 직진남녀]</b><br>솔직 담백하게 좋고 싫음을 확실히 표현하는 쿨한 성격입니다.",
                'curved': "🌊 <b>[따뜻한 감성 힐러]</b><br>타인의 감정을 내 것처럼 느끼는 따뜻한 마음씨를 가졌습니다.",
                'hybrid': "🎭 <b>[알다가도 모를 반전 매력]</b><br>냉정과 열정 사이를 오가는 매력적인 밀당의 고수입니다."
            },
            'heart_end_book': {
                'cross': "🔒 <b>[집착과 소유의 끝판왕]</b><br>사랑하는 사람을 완전히 소유하고 싶어 하는 독점욕이 있습니다.",
                'jupiter': "🏰 <b>[신중한 로맨티시스트]</b><br>자존심이 높고 한 번 마음을 열면 변치 않는 건실한 연애를 합니다.",
                'index_border': "🌻 <b>[해바라기]</b><br>평소엔 이성적이지만 사랑 앞에서는 맹목적이 됩니다.",
                'index_middle_down': "❤️‍🔥 <b>[가슴 속 마그마]</b><br>겉보기엔 얌전해 보이지만 속에는 뜨거운 열정이 가득합니다.",
                'index_middle_end': "💍 <b>[결혼하고 싶은 사람 1위]</b><br>최고의 배우자 감입니다. 성실하고 가정적입니다.",
                'middle_border': "🍲 <b>[금방 끓고 식는 냄비]</b><br>열정이 확 타올랐다가 금방 시들해질 수 있으니 주의하세요.",
                'middle_down': "😎 <b>[쿨내 진동하는 자유인]</b><br>구속받는 것을 싫어하고 쿨한 매력이 인기의 비결입니다.",
                'index_down_life': "🍎 <b>[위험한 유혹]</b><br>스릴을 즐기지만 그 끝은 상처일 수 있는 금단의 사랑을 주의하세요.",
                'middle_down_life': "👑 <b>[내 멋대로 하는 사랑]</b><br>자기중심적인 성향이 강해 고집을 부릴 수 있습니다."
            },
            'fate_path': {
                'support': "🤝 <b>[최고의 참모]</b><br>주도적으로 나서기보다 보좌할 때 빛을 발하는 서포터형 인재입니다.",
                'self_made': "🌟 <b>[맨주먹 성공 신화]</b><br>오직 자신의 실력과 노력으로 자수성가할 운명입니다.",
                'popular': "💖 <b>[대중의 별, 인기운]</b><br>사람을 끌어당기는 묘한 매력이 있어 타인의 도움으로 성공합니다.",
                'late': "🐢 <b>[대기만성의 아이콘]</b><br>중년 이후부터 갈수록 운이 트이는 대기만성형입니다."
            },
            'fate_start_book': {
                'venus': ["👪 <b>[가문의 영광: 금수저의 기운]</b><br>가족의 전폭적인 지원을 받아 운이 열립니다."],
                'mars_1': ["🦁 <b>[난세의 영웅: 야망가의 기질]</b><br>사회가 혼란스러울 때 더 큰 힘을 발휘하는 야망가입니다."],
                'venus_moon_middle': ["🛠️ <b>[성실함의 승리]</b><br>자신의 땀과 노력으로 운을 개척하는 정직한 사람입니다."],
                'mars_2': ["🤝 <b>[파트너 복이 터졌다]</b><br>능력 있는 사람과 손잡고 시너지를 낼 때 상상 이상의 결과가 옵니다."],
                'moon': ["🌟 <b>[대중의 아이돌]</b><br>타지나 해외에서 더 크게 성공할 운명이며 인기를 먹고 자랍니다."],
                'mars_plain': ["🔥 <b>[진흙 속의 연꽃]</b><br>초년의 시련은 당신을 강철처럼 단련시키기 위한 과정입니다."],
                'above_life': ["🐢 <b>[노력은 배신하지 않는다]</b><br>피나는 노력의 결실을 상징하며 분야의 일인자가 됩니다."],
                'above_head': ["💡 <b>[천재적 두뇌]</b><br>기발한 아이디어로 세상을 놀라게 할 준비가 되어 있습니다."],
                'above_heart': ["🏆 <b>[인생은 50부터]</b><br>은퇴를 걱정할 나이에 오히려 제2의 전성기를 맞이합니다."],
                'wrist_straight': ["🚀 <b>[직진 본능]</b><br>자신이 믿는 길을 향해 전차처럼 돌진하는 강직한 운명입니다."]
            },
            'fate_end_book': {
                'saturn': ["🏅 <b>[고독한 승부사]</b><br>명예를 중요하게 생각하며 스스로의 목표 달성에 희열을 느낍니다."],
                'jupiter': ["🤝 <b>[야망의 정치가]</b><br>사람들을 지휘하고 영향력을 행사하는 자리에 오를 운명입니다."],
                'sun': ["💰 <b>[화려한 재력가]</b><br>예술적 감각으로 큰 부를 축적하며 럭셔리한 삶을 삽니다."],
                'head_stop': ["🛑 <b>[돌다리 두드리기]</b><br>판단력을 믿고 과감하게 승부수를 던져야 할 때가 옵니다."],
                'heart_stop': ["❤️ <b>[은퇴 후의 여유]</b><br>말년에는 내면의 평화와 행복을 중요시하게 됩니다."]
            },
            'special_signs': {
                'm_sign': "🏆 <b>[전설의 대박 징조, M자 손금!]</b><br>중년 이후 막대한 부와 명예를 거머쥘 수 있는 희귀한 길상입니다.",
                'rich_triangle': "💰 <b>[돈이 마르지 않는 삼각 창고]</b><br>평생 돈 걱정 없이 살 알부자 손금의 증거입니다.",
                'no_fate': "🦅 <b>[길 없는 곳이 내 길]</b><br>정해진 운명이 없기에 당신이 걷는 곳이 곧 길이 됩니다."
            },
            'spicy_title': "🔞 <b>[Forbidden] 관능의 심연: 당신이 숨긴 짐승의 얼굴</b>",
            'libido': {
                'level_5': "🔥 <b>[폭주하는 정복자]</b><br>파괴적인 스테미너로 파트너를 압도하는 밤의 지배자입니다.",
                'level_3': "🍷 <b>[농밀한 쾌락 탐닉자]</b><br>상대를 중독시키는 섬세하고 집요한 터치를 가진 테크니션입니다.",
                'level_1': "🍃 <b>[은밀한 관조자]</b><br>상대를 정신적으로 굴복시키려는 뒤틀린 욕망을 가진 위험한 은둔자입니다."
            },
            'seduction': {
                'bad_charmer': "😈 <b>[치명적인 조련사]</b><br>상대를 정신적으로 해체하고 당신 발밑에 굴복하게 만듭니다.",
                'hot_lover': "❤️‍🔥 <b>[본능의 노예]</b><br>장소를 가리지 않고 폭발적인 본능을 발산하는 정열의 괴물입니다.",
                'shy_fox': "🦊 <b>[낮져밤이의 정석]</b><br>밀실 문이 잠기는 순간 음탕한 본색을 드러내는 반전 매력가입니다.",
                'cool_friend': "😎 <b>[쾌락 기계]</b><br>감정 없이 오직 말초적인 신경의 떨림에만 집중하는 냉혈한입니다.",
                'devoted_puppy': "🐶 <b>[자발적 노예]</b><br>상대의 가학적인 명령에도 순응하며 굴복당함을 즐기는 타입입니다."
            },
            'fantasy': {
                'deep': "🦄 <b>[판타지 광신도]</b><br>금지된 행위를 현실로 끌어들여야 살아있음을 느끼는 설계자입니다.",
                'real': "💼 <b>[현실주의 포식자]</b><br>가장 노골적인 육체의 물리적 충돌에만 집중하는 현실파입니다."
            }
        }

    def get_step(self, value, thresholds):
        for i, th in enumerate(thresholds):
            if value < th: return i
        return len(thresholds)

    def interpret(self, features, mounts, hand_metrics):
        html_content = f"""
        <div class="palm-wrapper" style="font-family: 'Malgun Gothic', sans-serif; background: #f0f2f5; padding: 20px; border-radius: 20px;">
            <div style="background: white; padding: 10px 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #e74c3c;">
                <h2 style="margin: 0; color: #1a202c;">🏮 AI 운명 보고서 V1.0</h2>
            </div>
            <div class="palm-scroll-area" style="display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px;">
        """

        # 1. 생명선
        if 'life' in features:
            f = features['life']
            msg = []
            gap = features.get('head_life_gap', 0)
            step = self.get_step(gap, self.TH['gap'])
            keys = ['glue', 'tight', 'normal_tight', 'normal', 'normal_loose', 'loose', 'free', 'free']
            msg.append(self.texts['life_start'][keys[step]])
            # ... 생명선 상세 분석 생략 가능 (코드 다이어트용)
            html_content += self._make_slide_card("🌿 생명선", "#78ffe6", "".join(msg))

        # 2. 두뇌선
        if 'head' in features:
            f = features['head']
            msg = [self.texts['head_length_book']['long' if f['len_ratio'] > 0.4 else 'short']]
            html_content += self._make_slide_card("🧠 두뇌선", "#ffe696", "".join(msg))

        # 3. 감정선
        if 'heart' in features:
            f = features['heart']
            msg = [self.texts['heart_shape_book']['curved' if f['curv'] > 1.05 else 'straight']]
            html_content += self._make_slide_card("❤️ 감정선", "#ff7878", "".join(msg))

        # 4. 운명선
        if 'fate' in features:
            msg = [self.texts['fate_path']['self_made']]
            html_content += self._make_slide_card("🌟 운명선", "#8c96ff", "".join(msg))
        else:
            html_content += self._make_slide_card("🌟 운명선", "#8c96ff", self.texts['special_signs']['no_fate'])

        # 5. 19금 파트
        spicy_msg = self.texts['libido']['level_3']
        html_content += self._make_slide_card(self.texts['spicy_title'], "#e74c3c", spicy_msg)

        html_content += "</div></div>"
        return html_content

    def _make_slide_card(self, title, color, text):
        return f"""
        <div style="flex: 0 0 280px; background: white; padding: 20px; border-radius: 20px; border-top: 10px solid {color}; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
            <h3 style="margin: 0 0 10px 0; font-size: 1.1em; color: #1a202c;">{title}</h3>
            <div style="font-size: 0.95em; line-height: 1.6; color: #4a5568;">{text}</div>
        </div>
        """