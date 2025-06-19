import streamlit as st
import json
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="조화로의 길: 빛과 어둠을 품은 소녀",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 (금색의 코르다 스타일)
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: #f5f5f5;
        color: #333;
    }
    
    /* 메인 컨테이너 */
    .main-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 800px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* 제목 스타일 */
    .game-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .game-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        height: 60px;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* 특별한 진행 버튼 스타일 */
    .chapter-progress-button {
        background: linear-gradient(45deg, #ff6b6b 0%, #ffa726 100%) !important;
        font-size: 1.4rem !important;
        height: 70px !important;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4); }
        to { box-shadow: 0 8px 30px rgba(255, 167, 38, 0.6); }
    }
    
    /* 텍스트 입력 스타일 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        color: #333;
        font-size: 1.1rem;
        padding: 10px;
    }
    
    /* 캐릭터 이름 */
    .character-name {
        color: #333;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    /* 나레이션 */
    .narration {
        font-style: italic;
        color: #d0d0d0;
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        font-size: 1.2rem;
        line-height: 1.8;
    }
    
    /* 메시지 박스 스타일 */
    .message-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem auto;
        max-width: 600px;
        border: 2px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        color: #333;
        font-size: 1.1rem;
        line-height: 1.6;
        position: relative;
    }
    
    /* 설정 패널 텍스트 색상 수정 */
    .settings-panel {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #333;
    }
    
    .settings-panel h3 {
        color: #333;
    }
    
    .settings-panel p {
        color: #333;
    }
    
    /* 특별한 선택지 효과 */
    .choice-light {
        background: linear-gradient(45deg, #ffeaa7 0%, #fab1a0 100%) !important;
        border: 2px solid #fdcb6e !important;
    }
    
    .choice-dark {
        background: linear-gradient(45deg, #636e72 0%, #2d3436 100%) !important;
        border: 2px solid #74b9ff !important;
    }
    
    .choice-balance {
        background: linear-gradient(45deg, #a29bfe 0%, #6c5ce7 100%) !important;
        border: 2px solid #fd79a8 !important;
    }
    
    /* 캐릭터별 호감도 색상 */
    .affection-yoonho { color: #e17055; }
    .affection-doyoon { color: #00b894; }
    .affection-minjun { color: #636e72; }
    .affection-joowon { color: #00cec9; }
    .affection-yoojun { color: #74b9ff; }
    .affection-eunho { color: #fdcb6e; }
</style>
""", unsafe_allow_html=True)

# 게임 데이터 초기화
def init_game_data():
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {
            'current_scene': 'main_menu',
            'player_name': '',
            'current_chapter': 'prologue',
            'current_episode': 1,
            'current_scene_index': 0,
            'affection': {
                'yoonho': 0, 'doyoon': 0, 'minjun': 0,
                'joowon': 0, 'yoojun': 0, 'eunho': 0
            },
            'player_stats': {
                'light_control': 0, 'dark_control': 0,
                'balance': 0, 'confidence': 0
            },
            'story_flags': {},
            'choices_made': [],
            'save_data': [],
            # 게임 설정
            'auto_mode': False,
            'auto_speed': 3.0,
            # 새로운 기능들
            'bgm_enabled': True,
            'sound_enabled': True,
            'text_speed': 2,
            'seen_scenes': set(),
            'gallery_unlocked': [],
            'current_route': None,
            'total_playtime': 0,
            'achievements': [],
            'last_save_time': None,
            # 프롤로그 완료 여부 추가
            'prologue_completed': False,
            # 시크릿 캐릭터 언락
            'secret_characters': {'eunho': False},
            # 캐릭터별 만남 순서 추가
            'met_characters': [],
            'character_meeting_order': [],
            # 스페셜 이벤트 플래그
            'special_events': {},
            # 루트 분기 관련
            'route_points': {
                'yoonho': 0, 'doyoon': 0, 'minjun': 0,
                'joowon': 0, 'yoojun': 0, 'eunho': 0
            }
        }

# 스탯 및 호감도 표시 함수 (개선된 버전)
def show_status_panel():
    st.sidebar.markdown("### 📊 캐릭터 스탯")
    
    # 플레이어 능력치
    stats = st.session_state.game_state['player_stats']
    
    # 빛의 힘
    light_progress = max(0.0, min(stats['light_control'] / 10, 1.0))
    st.sidebar.progress(light_progress)
    st.sidebar.caption(f"✨ 빛의 힘: {stats['light_control']}/10")
    
    # 어둠의 힘
    dark_progress = max(0.0, min(stats['dark_control'] / 10, 1.0))
    st.sidebar.progress(dark_progress)
    st.sidebar.caption(f"🌙 어둠의 힘: {stats['dark_control']}/10")
    
    # 균형
    balance_progress = max(0.0, min(stats['balance'] / 10, 1.0))
    st.sidebar.progress(balance_progress)
    st.sidebar.caption(f"⚖️ 균형: {stats['balance']}/10")
    
    # 자신감
    confidence_progress = max(0.0, min(stats['confidence'] / 10, 1.0))
    st.sidebar.progress(confidence_progress)
    st.sidebar.caption(f"💪 자신감: {stats['confidence']}/10")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💕 호감도")
    
    # 남주들 호감도
    affection = st.session_state.game_state['affection']
    secret_unlocked = st.session_state.game_state.get('secret_characters', {})
    
    male_leads = {
        'yoonho': '🔥 신윤호 (학생회장)',
        'doyoon': '💚 김도윤 (보건위원)', 
        'minjun': '⚔️ 이민준 (어둠 속성)',
        'joowon': '🌪️ 남주원 (자유로운 영혼)',
        'yoojun': '🌊 한유준 (신비한 예언자)',
        'eunho': '🌟 정은호 (???)' if not secret_unlocked.get('eunho', False) else '🌟 정은호 (완벽주의자)'
    }
    
    for char_id, char_name in male_leads.items():
        love_level = affection[char_id]
        progress_val = max(0.0, min(love_level / 100, 1.0))
        
        # 정은호가 언락되지 않았으면 잠금 표시
        if char_id == 'eunho' and not secret_unlocked.get('eunho', False):
            st.sidebar.progress(0.0)
            st.sidebar.caption(f"🔒 {char_name}: LOCKED")
        else:
            st.sidebar.progress(progress_val)
            
            # 호감도에 따른 상태 표시
            if love_level >= 80:
                status = "💖 열렬한 사랑"
            elif love_level >= 60:
                status = "💕 깊은 애정"
            elif love_level >= 40:
                status = "💛 좋은 감정"
            elif love_level >= 20:
                status = "😊 호감"
            else:
                status = "😐 평범"
                
            st.sidebar.caption(f"{char_name}: {love_level}% ({status})")
    
    # 만난 캐릭터 순서 표시
    met_chars = st.session_state.game_state.get('met_characters', [])
    if met_chars:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🤝 만난 순서")
        for i, char in enumerate(met_chars, 1):
            char_names = {
                'yoonho': '신윤호', 'doyoon': '김도윤', 'minjun': '이민준',
                'joowon': '남주원', 'yoojun': '한유준', 'eunho': '정은호'
            }
            st.sidebar.caption(f"{i}. {char_names.get(char, char)}")

# 갤러리 기능 (기존과 동일)
def show_gallery():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #333;">🖼️ 갤러리</h2>', unsafe_allow_html=True)
    
    unlocked = st.session_state.game_state.get('gallery_unlocked', [])
    
    if not unlocked:
        st.info("🔒 아직 해금된 이미지가 없습니다. 스토리를 진행하여 특별한 순간들을 모아보세요!")
    else:
        cols = st.columns(3)
        for i, img_id in enumerate(unlocked):
            with cols[i % 3]:
                st.image(f"placeholder_{img_id}.jpg", caption=f"추억 {img_id}")
    
    if st.button("🏠 메인 메뉴로"):
        st.session_state.game_state['current_scene'] = 'main_menu'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
# 업적 시스템 (확장된 버전)
def check_achievements():
    achievements = st.session_state.game_state.get('achievements', [])
    stats = st.session_state.game_state['player_stats']
    affection = st.session_state.game_state['affection']
    met_chars = st.session_state.game_state.get('met_characters', [])
    
    # 새로운 업적 체크
    new_achievements = []
    
    # 기본 업적들
    if 'first_choice' not in achievements and len(st.session_state.game_state['choices_made']) >= 1:
        new_achievements.append('first_choice')
    
    if 'max_light' not in achievements and stats['light_control'] >= 10:
        new_achievements.append('max_light')
        
    if 'max_dark' not in achievements and stats['dark_control'] >= 10:
        new_achievements.append('max_dark')
    
    # 정은호 제외한 호감도 계산 (시크릿 캐릭터)
    non_secret_affection = {k: v for k, v in affection.items() if k != 'eunho'}
    if 'first_love' not in achievements and any(love >= 50 for love in non_secret_affection.values()):
        new_achievements.append('first_love')
    
    if 'prologue_complete' not in achievements and st.session_state.game_state.get('prologue_completed', False):
        new_achievements.append('prologue_complete')
    
    # 새로운 업적들
    if 'perfect_balance' not in achievements and stats['balance'] >= 8 and stats['light_control'] >= 5 and stats['dark_control'] >= 5:
        new_achievements.append('perfect_balance')
    
    if 'social_butterfly' not in achievements and len(met_chars) >= 3:
        new_achievements.append('social_butterfly')
    
    if 'confident_soul' not in achievements and stats['confidence'] >= 8:
        new_achievements.append('confident_soul')
    
    if 'harem_route' not in achievements and sum(1 for love in non_secret_affection.values() if love >= 30) >= 3:
        new_achievements.append('harem_route')
    
    if 'first_meeting' not in achievements and len(met_chars) >= 1:
        new_achievements.append('first_meeting')
    
    if 'meet_all_main' not in achievements and len(met_chars) >= 5:  # 5명 모두 만나기
        new_achievements.append('meet_all_main')
    
    # 캐릭터별 특별 업적 (정은호 제외)
    for char_id, love_val in affection.items():
        if char_id != 'eunho':  # 정은호는 시크릿이므로 제외
            char_achievement = f'love_{char_id}'
            if char_achievement not in achievements and love_val >= 70:
                new_achievements.append(char_achievement)
    
    # 정은호 언락 업적
    if 'secret_unlock_eunho' not in achievements and st.session_state.game_state.get('secret_characters', {}).get('eunho', False):
        new_achievements.append('secret_unlock_eunho')
    
    # 정은호 사랑 업적 (언락 후에만)
    if st.session_state.game_state.get('secret_characters', {}).get('eunho', False):
        if 'love_eunho' not in achievements and affection['eunho'] >= 70:
            new_achievements.append('love_eunho')
    
    # 새 업적이 있으면 알림
    for achievement in new_achievements:
        if achievement not in achievements:
            achievements.append(achievement)
            show_achievement_popup(achievement)
    
    st.session_state.game_state['achievements'] = achievements

def show_achievement_popup(achievement_id):
    achievement_data = {
        'first_choice': {'title': '첫 번째 선택', 'desc': '첫 선택지를 완료했습니다', 'icon': '🎯'},
        'max_light': {'title': '빛의 마스터', 'desc': '빛의 힘을 최대치로 올렸습니다', 'icon': '✨'},
        'max_dark': {'title': '어둠의 지배자', 'desc': '어둠의 힘을 최대치로 올렸습니다', 'icon': '🌙'},
        'first_love': {'title': '첫사랑의 시작', 'desc': '누군가와 깊은 유대를 형성했습니다', 'icon': '💕'},
        'prologue_complete': {'title': '운명의 시작', 'desc': '프롤로그를 완료했습니다', 'icon': '📖'},
        'perfect_balance': {'title': '완벽한 균형', 'desc': '빛과 어둠의 완벽한 조화를 이뤘습니다', 'icon': '⚖️'},
        'social_butterfly': {'title': '사교계의 나비', 'desc': '3명 이상의 캐릭터와 만났습니다', 'icon': '🦋'},
        'confident_soul': {'title': '자신감 넘치는 영혼', 'desc': '높은 자신감을 가지게 되었습니다', 'icon': '💪'},
        'harem_route': {'title': '모든 이의 마음', 'desc': '여러 캐릭터가 당신에게 호감을 가집니다', 'icon': '💝'},
        'first_meeting': {'title': '새로운 만남', 'desc': '첫 번째 캐릭터를 만났습니다', 'icon': '🤝'},
        'meet_all_main': {'title': '모든 인연', 'desc': '메인 캐릭터 5명을 모두 만났습니다', 'icon': '👥'},
        # 캐릭터별 업적
        'love_yoonho': {'title': '불타는 마음', 'desc': '신윤호와 깊은 사랑에 빠졌습니다', 'icon': '🔥'},
        'love_doyoon': {'title': '치유의 사랑', 'desc': '김도윤과 깊은 사랑에 빠졌습니다', 'icon': '💚'},
        'love_minjun': {'title': '어둠 속의 빛', 'desc': '이민준과 깊은 사랑에 빠졌습니다', 'icon': '⚔️'},
        'love_joowon': {'title': '자유로운 바람', 'desc': '남주원과 깊은 사랑에 빠졌습니다', 'icon': '🌪️'},
        'love_yoojun': {'title': '신비한 인연', 'desc': '한유준과 깊은 사랑에 빠졌습니다', 'icon': '🌊'},
        'love_eunho': {'title': '완벽한 조화', 'desc': '정은호와 깊은 사랑에 빠졌습니다', 'icon': '🌟'},
        'secret_unlock_eunho': {'title': '숨겨진 진실', 'desc': '시크릿 캐릭터 정은호를 발견했습니다', 'icon': '🔓'}
    }
    
    if achievement_id in achievement_data:
        data = achievement_data[achievement_id]
        st.success(f"🏆 업적 달성! {data['icon']} {data['title']}: {data['desc']}")

# 업적 보기 화면 (확장된 버전)
def show_achievements():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #333;">🏆 업적</h2>', unsafe_allow_html=True)
    
    achievement_data = {
        'first_choice': {'title': '첫 번째 선택', 'desc': '첫 선택지를 완료했습니다', 'icon': '🎯'},
        'prologue_complete': {'title': '운명의 시작', 'desc': '프롤로그를 완료했습니다', 'icon': '📖'},
        'first_meeting': {'title': '새로운 만남', 'desc': '첫 번째 캐릭터를 만났습니다', 'icon': '🤝'},
        'social_butterfly': {'title': '사교계의 나비', 'desc': '3명 이상의 캐릭터와 만났습니다', 'icon': '🦋'},
        'meet_all_main': {'title': '모든 인연', 'desc': '메인 캐릭터 5명을 모두 만났습니다', 'icon': '👥'},
        'max_light': {'title': '빛의 마스터', 'desc': '빛의 힘을 최대치로 올렸습니다', 'icon': '✨'},
        'max_dark': {'title': '어둠의 지배자', 'desc': '어둠의 힘을 최대치로 올렸습니다', 'icon': '🌙'},
        'perfect_balance': {'title': '완벽한 균형', 'desc': '빛과 어둠의 완벽한 조화를 이뤘습니다', 'icon': '⚖️'},
        'confident_soul': {'title': '자신감 넘치는 영혼', 'desc': '높은 자신감을 가지게 되었습니다', 'icon': '💪'},
        'first_love': {'title': '첫사랑의 시작', 'desc': '누군가와 깊은 유대를 형성했습니다', 'icon': '💕'},
        'harem_route': {'title': '모든 이의 마음', 'desc': '여러 캐릭터가 당신에게 호감을 가집니다', 'icon': '💝'},
        'love_yoonho': {'title': '불타는 마음', 'desc': '신윤호와 깊은 사랑에 빠졌습니다', 'icon': '🔥'},
        'love_doyoon': {'title': '치유의 사랑', 'desc': '김도윤과 깊은 사랑에 빠졌습니다', 'icon': '💚'},
        'love_minjun': {'title': '어둠 속의 빛', 'desc': '이민준과 깊은 사랑에 빠졌습니다', 'icon': '⚔️'},
        'love_joowon': {'title': '자유로운 바람', 'desc': '남주원과 깊은 사랑에 빠졌습니다', 'icon': '🌪️'},
        'love_yoojun': {'title': '신비한 인연', 'desc': '한유준과 깊은 사랑에 빠졌습니다', 'icon': '🌊'},
        'love_eunho': {'title': '완벽한 조화', 'desc': '정은호와 깊은 사랑에 빠졌습니다', 'icon': '🌟'},
        'secret_unlock_eunho': {'title': '숨겨진 진실', 'desc': '시크릿 캐릭터 정은호를 발견했습니다', 'icon': '🔓'},
        'story_complete': {'title': '이야기의 끝', 'desc': '메인 스토리를 완료했습니다', 'icon': '📖'}
    }
    
    unlocked = st.session_state.game_state.get('achievements', [])
    
    # 카테고리별로 업적 분류 (정은호 시크릿 처리)
    secret_unlocked = st.session_state.game_state.get('secret_characters', {}).get('eunho', False)
    
    love_achievements = ['first_love', 'love_yoonho', 'love_doyoon', 'love_minjun', 'love_joowon', 'love_yoojun']
    if secret_unlocked:
        love_achievements.extend(['love_eunho', 'secret_unlock_eunho'])
    
    categories = {
        '📖 스토리 진행': ['first_choice', 'prologue_complete', 'story_complete'],
        '🤝 인간관계': ['first_meeting', 'social_butterfly', 'meet_all_main', 'harem_route'],
        '💪 능력 개발': ['max_light', 'max_dark', 'perfect_balance', 'confident_soul'],
        '💕 로맨스': love_achievements
    }
    
    for category, ach_list in categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(2)
        for i, ach_id in enumerate(ach_list):
            if ach_id in achievement_data:
                data = achievement_data[ach_id]
                with cols[i % 2]:
                    if ach_id in unlocked:
                        st.success(f"{data['icon']} **{data['title']}**\n\n{data['desc']}")
                    else:
                        # 정은호 관련 업적은 언락 전까지 숨김
                        if ach_id in ['love_eunho', 'secret_unlock_eunho'] and not secret_unlocked:
                            st.info(f"🔒 **시크릿**\n\n특별한 조건을 만족하면 해금됩니다")
                        else:
                            st.info(f"🔒 **???**\n\n미해금 업적")
    
    st.markdown(f"**전체 진행률: {len(unlocked)}/{len(achievement_data)} ({int(len(unlocked)/len(achievement_data)*100)}%)**")
    
    if st.button("🏠 메인 메뉴로"):
        st.session_state.game_state['current_scene'] = 'main_menu'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def save_game():
    save_data = st.session_state.game_state.copy()
    save_data['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.game_state['save_data'] = save_data
    st.success("게임이 저장되었습니다!")
    time.sleep(1)

def load_game():
    if st.session_state.game_state.get('save_data'):
        st.session_state.game_state.update(st.session_state.game_state['save_data'])
        st.success("게임을 불러왔습니다!")
        time.sleep(1)
        return True
    else:
        st.error("저장된 게임이 없습니다.")
        return False

# 설정 화면 (완전한 버전)
def show_settings():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #333;">⚙️ 게임 설정</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; font-size: 0.9rem;">조화로의 길: 빛과 어둠을 품은 소녀</p>', unsafe_allow_html=True)
    
    # 설정 패널
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    
    # 오토 모드 설정
    st.markdown("### 🤖 오토 모드")
    
    # 현재 설정값 표시
    current_auto = st.session_state.game_state.get('auto_mode', False)
    current_speed = st.session_state.game_state.get('auto_speed', 3.0)
    
    auto_mode = st.checkbox("자동 진행 모드 활성화", 
                           value=current_auto,
                           key="auto_mode_checkbox")
    
    # 설정값 즉시 업데이트
    st.session_state.game_state['auto_mode'] = auto_mode
    if auto_mode != current_auto:
        st.success("✅ 오토 모드 설정이 변경되었습니다!")
    
    if auto_mode:
        auto_speed = st.slider("자동 진행 속도 (초)", 
                             min_value=1.0, max_value=10.0, 
                             value=current_speed, 
                             step=0.5,
                             key="auto_speed_slider")
        
        # 속도 설정값 즉시 업데이트
        st.session_state.game_state['auto_speed'] = auto_speed
        if auto_speed != current_speed:
            st.success(f"✅ 자동 진행 속도가 {auto_speed}초로 설정되었습니다!")
        
        st.info(f"💡 {auto_speed}초마다 자동으로 다음 장면으로 넘어갑니다.")
    else:
        st.info("💡 버튼을 클릭해서 수동으로 진행합니다.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 사운드 설정
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown("### 🎵 사운드 설정")
    
    bgm_enabled = st.checkbox("배경음악 활성화", 
                             value=st.session_state.game_state.get('bgm_enabled', True))
    st.session_state.game_state['bgm_enabled'] = bgm_enabled
    
    sound_enabled = st.checkbox("효과음 활성화", 
                               value=st.session_state.game_state.get('sound_enabled', True))
    st.session_state.game_state['sound_enabled'] = sound_enabled
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 텍스트 설정
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown("### 📝 텍스트 설정")
    
    text_speed = st.slider("텍스트 출력 속도", 
                          min_value=1, max_value=5, 
                          value=st.session_state.game_state.get('text_speed', 2))
    st.session_state.game_state['text_speed'] = text_speed
    
    st.markdown('<p style="color: #333;">텍스트 속도가 높을수록 빠르게 출력됩니다.</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 게임 통계
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 게임 통계")
    
    choices_made = len(st.session_state.game_state.get('choices_made', []))
    met_chars = len(st.session_state.game_state.get('met_characters', []))
    achievements = len(st.session_state.game_state.get('achievements', []))
    
    st.markdown(f'<p style="color: #333;">선택한 결정: {choices_made}개</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333;">만난 캐릭터: {met_chars}명</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333;">달성한 업적: {achievements}개</p>', unsafe_allow_html=True)
    
    # 현재 스탯 상태
    stats = st.session_state.game_state['player_stats']
    st.markdown('<hr style="margin: 1rem 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #333; font-weight: bold;">현재 스탯:</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333;">✨ 빛의 힘: {stats["light_control"]}/10</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333;">🌙 어둠의 힘: {stats["dark_control"]}/10</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333;">⚖️ 균형: {stats["balance"]}/10</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333;">💪 자신감: {stats["confidence"]}/10</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 게임 정보
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown("### ℹ️ 게임 정보")
    
    st.markdown('<p style="color: #333;">게임 제목: 조화로의 길: 빛과 어둠을 품은 소녀</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #333;">버전: 1.0.0</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #333;">장르: 로맨스 판타지 오토메 게임</p>', unsafe_allow_html=True)
    
    # 저장 데이터 정보
    save_data = st.session_state.game_state.get('save_data')
    if save_data and 'save_time' in save_data:
        st.markdown(f'<p style="color: #333;">마지막 저장: {save_data["save_time"]}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 돌아가기 버튼
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 메인 메뉴로 돌아가기"):
            st.session_state.game_state['current_scene'] = 'main_menu'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
# 메인 메뉴
def show_main_menu():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 게임 제목
    st.markdown('<h1 class="game-title">🌙 조화로의 길: 빛과 어둠을 품은 소녀 ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; font-size: 1rem; margin-top: -1rem;">調和への道：光と闇を抱く少女</p>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">~ 빛과 어둠 사이에서 피어나는 사랑 ~</p>', unsafe_allow_html=True)
    
    # 분위기 있는 인트로 텍스트
    st.markdown("""
    <div class="narration">
    천 년에 한 번 태어나는 이중속성자...<br>
    빛과 어둠을 동시에 품은 소녀의 운명은 과연..?<br><br>
    마법학원에서 펼쳐지는 여섯 남주와의 감동적인 로맨스 판타지
    </div>
    """, unsafe_allow_html=True)
    
    # 오토 모드 상태 표시
    auto_status = "🤖 자동 모드 ON" if st.session_state.game_state.get('auto_mode', False) else "✋ 수동 모드"
    st.markdown(f'<p style="text-align: center; color: #888; font-size: 0.9rem;">{auto_status}</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 이름 입력
        st.markdown("### 👑 주인공 이름 설정")
        player_name = st.text_input("이름을 입력해주세요", 
                                  value=st.session_state.game_state.get('player_name', ''),
                                  placeholder="예: 이하늘")
        
        if player_name:
            st.session_state.game_state['player_name'] = player_name
        
        st.markdown("---")
        
        # 메뉴 버튼들
        if st.button("🌟 새로 시작하기"):
            if player_name:
                st.session_state.game_state['current_scene'] = 'prologue'
                st.session_state.game_state['current_episode'] = 1
                st.session_state.game_state['current_scene_index'] = 0
                st.session_state.game_state['prologue_completed'] = False
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")
        
        if st.button("📚 이어서 하기"):
            if load_game():
                st.rerun()
        
        if st.button("💾 게임 저장하기"):
            save_game()
        
        if st.button("⚙️ 설정"):
            st.session_state.game_state['current_scene'] = 'settings'
            st.rerun()
            
        # 새로운 메뉴들
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🖼️ 갤러리"):
                st.session_state.game_state['current_scene'] = 'gallery'
                st.rerun()
        
        with col_b:
            if st.button("🏆 업적"):
                st.session_state.game_state['current_scene'] = 'achievements'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 프롤로그 데이터 생성 함수
def get_prologue_episodes():
    player_name = st.session_state.game_state.get('player_name', '공주')
    
    return {
        1: {
            'title': '운명적 탄생',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '17년 전, 어느 작은 마을의 한적한 밤...'
                },
                {
                    'type': 'narration',
                    'text': '달이 가장 높이 뜬 자정, 운명적인 순간이 찾아왔다.'
                },
                {
                    'type': 'narration',
                    'text': '한 아이가 이 세상에 태어나는 순간, 하늘과 땅이 요동쳤다.'
                },
                {
                    'type': 'narration',
                    'text': '그 순간, 마을 전체가 빛과 어둠으로 뒤덮였다.\n정오인데도 별이 보이고, 한밤중인데도 태양빛이 스며들었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '마을 사람 1',
                    'text': '이, 이게 무슨 일이야...! 낮과 밤이 뒤섞이고 있어!'
                },
                {
                    'type': 'dialogue',
                    'character': '마을 사람 2',
                    'text': '저주받은 아이다! 분명 불길한 징조야!'
                },
                {
                    'type': 'narration',
                    'text': '사람들은 두려움에 떨며 집 안으로 숨어들었다.\n부모조차 갓난아기를 제대로 안아보지 못했다.'
                },
                {
                    'type': 'narration',
                    'text': '작은 생명이 세상에 가져온 것은 축복이 아닌, 깊은 두려움이었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '산파',
                    'text': '이 아이... 보통 아이가 아니에요. 뭔가 특별한 힘이 느껴져요.'
                },
                {
                    'type': 'narration',
                    'text': '그 날 밤, 마을에는 이상한 소문이 퍼지기 시작했다.\n"천 년에 한 번 태어나는 이중속성자가 나타났다"고...'
                }
            ]
        },
        2: {
            'title': '어린 시절의 따뜻한 기억들',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '1-4살까지의 희미한 기억들...\n\n비록 짧았지만, 가족과 함께한 소중한 시간들이 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'우리 {player_name}... 엄마가 가장 사랑하는 보물이야... ♪'
                },
                {
                    'type': 'narration',
                    'text': '어머니는 매일 밤 따뜻한 자장가를 불러주셨다.\n그 목소리는 마법보다도 더 강력한 힘을 가지고 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'{player_name}, 아빠가 높이 높이 들어올려줄게! 무서워하지 마!'
                },
                {
                    'type': 'narration',
                    'text': '아버지의 강하고 따뜻한 손길...\n그 품에서는 세상의 모든 두려움이 사라졌다.'
                },
                {
                    'type': 'dialogue',
                    'character': '남동생 민호',
                    'text': f'누나! 같이 그림 그리자! 누나가 그린 꽃이 제일 예뻐!'
                },
                {
                    'type': 'narration',
                    'text': '남동생 민호와 함께 그림 그리며 놀던 평온한 오후들...\n가족만의 작은 정원에서 꽃을 기르던 행복한 시간들...'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'{player_name}는 특별한 아이야. 그 특별함을 두려워하지 말고, 자랑스러워해야 해.'
                },
                {
                    'type': 'narration',
                    'text': '그때는 몰랐다.\n이 따뜻하고 소중한 행복이 곧 산산조각날 것이라는 걸...'
                },
                {
                    'type': 'narration',
                    'text': '그리고 그 모든 기억들이 깊은 어둠 속으로 사라져버릴 것이라는 걸...'
                }
            ]
        },
        3: {
            'title': '운명의 날',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '5살 생일날... 가족들이 정성스럽게 준비해준 특별한 하루였다.'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'{player_name}, 생일 축하해! 엄마 아빠가 정말 특별한 케이크를 준비했어.'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': '우리 공주님, 5살이 되었구나. 촛불을 불어서 소원을 빌어봐.'
                },
                {
                    'type': 'dialogue',
                    'character': f'어린 {player_name}',
                    'text': '와아! 케이크다! 너무 예뻐요! 가족들과 영원히 함께 있고 싶어요!'
                },
                {
                    'type': 'narration',
                    'text': '그 순간, 너무나 순수하고 강렬한 감정이 폭발했다.\n기쁨, 사랑, 행복... 어린 마음이 감당하기엔 너무 큰 감정들이었다.'
                },
                {
                    'type': 'narration',
                    'text': '순간적으로 온 집이 눈부신 빛으로 가득 차더니 급속히 깊은 어둠에 휩싸였다.'
                },
                {
                    'type': 'dialogue',
                    'character': '민호',
                    'text': '누나...? 무서워... 이게 뭐야...?'
                },
                {
                    'type': 'narration',
                    'text': '빛과 어둠이 격렬하게 충돌하며 집 전체가 무너지기 시작했다.\n모든 것이 혼돈 속으로 빨려들어갔다.'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'{player_name}! 괜찮다, 아빠가 있어! 무서워하지 마!'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'{player_name}... 괜찮아, 엄마가 끝까지 지켜줄게... 사랑해...'
                },
                {
                    'type': 'narration',
                    'text': '정신을 잃어가는 마지막 순간...\n어머니가 자신을 감싸 안으며 속삭이던 따뜻한 목소리가 들렸다.'
                },
                {
                    'type': 'narration',
                    'text': '그리고... 깊고 어두운 침묵이 찾아왔다.'
                },
                {
                    'type': 'narration',
                    'text': '...\n\n...\n\n...'
                },
                {
                    'type': 'narration',
                    'text': '언제인지 모를 시간이 흐른 후, 작은 몸이 폐허 속에서 깨어났다.'
                },
                {
                    'type': 'narration',
                    'text': '주변은 온통 잿더미와 부서진 잔해들뿐...\n가족은 어디에도 보이지 않았다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'어린 {player_name}',
                    'text': '엄마...? 아빠...? 민호는...? 여기... 여기가 어디예요...?'
                },
                {
                    'type': 'narration',
                    'text': '하지만 그 이후로는 아무것도 기억나지 않았다.\n모든 소중한 추억들이 깊은 어둠 속으로 사라져버렸다.'
                },
                {
                    'type': 'narration',
                    'text': '17년이 지난 지금까지도, 그날의 진실은 베일에 감싸여 있다.'
                },
                {
                    'type': 'choice',
                    'text': '17년이 지난 지금, 때때로 마음 깊은 곳에서 울려오는 목소리가 있다...',
                    'options': [
                        {
                            'text': '기억나지 않지만... 분명 소중한 사람들이 있었을 것이다',
                            'effects': {'confidence': 1, 'light_control': 1}
                        },
                        {
                            'text': '이 공허함과 슬픔... 무언가 잃어버린 것 같다',
                            'effects': {'confidence': -1, 'balance': 1}
                        },
                        {
                            'text': '알 수 없는 죄책감이 나를 괴롭힌다',
                            'effects': {'confidence': -2, 'dark_control': 1}
                        }
                    ]
                },
                {
                    'type': 'narration',
                    'text': '프롤로그가 끝났습니다.\n\n이제 본격적인 이야기가 시작됩니다...'
                }
            ]
        }
    }

# 프롤로그 표시 (수정된 버전)
def show_prologue():
    current_ep = st.session_state.game_state.get('current_episode', 1)
    
    # 프롤로그 데이터 동적 생성
    PROLOGUE_EPISODES = get_prologue_episodes()
    
    if current_ep > len(PROLOGUE_EPISODES):
        st.session_state.game_state['current_scene'] = 'chapter_1'
        st.session_state.game_state['current_episode'] = 1
        st.session_state.game_state['current_scene_index'] = 0
        st.rerun()
        return
    
    episode = PROLOGUE_EPISODES[current_ep]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 에피소드 제목
    st.markdown(f'<h2 style="text-align: center; color: #333;">📖 프롤로그 {current_ep} - {episode["title"]}</h2>', unsafe_allow_html=True)
    
    # 오토 모드 상태 표시
    auto_mode = st.session_state.game_state.get('auto_mode', False)
    auto_speed = st.session_state.game_state.get('auto_speed', 3.0)
    
    if auto_mode:
        st.markdown(f'<div style="text-align: center; color: #666; font-size: 0.9rem; margin: 1rem 0;">🤖 자동 모드 - {auto_speed}초마다 자동 진행</div>', unsafe_allow_html=True)
    
    # 장면별 표시
    scene_index = st.session_state.game_state.get('current_scene_index', 0)
    
    if scene_index < len(episode['scenes']):
        scene = episode['scenes'][scene_index]
        
        # 자동 진행을 위한 타이머 설정
        if auto_mode and 'scene_start_time' not in st.session_state:
            st.session_state.scene_start_time = time.time()
        
        if scene['type'] == 'narration':
            st.markdown(f'<div class="message-box">{scene["text"]}</div>', unsafe_allow_html=True)
            
        elif scene['type'] == 'dialogue':
            st.markdown(f'<div class="character-name">{scene["character"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="message-box">"{scene["text"]}"</div>', unsafe_allow_html=True)
            
        elif scene['type'] == 'choice':
            st.markdown(f'<div class="message-box">{scene["text"]}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                for i, option in enumerate(scene['options']):
                    if st.button(option['text'], key=f"prologue_choice_{current_ep}_{i}"):
                        # 선택지 효과 적용
                        for stat, value in option['effects'].items():
                            st.session_state.game_state['player_stats'][stat] += value
                        
                        # 선택지 기록
                        st.session_state.game_state['choices_made'].append({
                            'chapter': 'prologue',
                            'episode': current_ep,
                            'choice': option['text'],
                            'effects': option['effects']
                        })
                        
                        # 업적 체크
                        check_achievements()
                        
                        # 다음 장면으로
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                        if 'scene_start_time' in st.session_state:
                            del st.session_state.scene_start_time
                        st.rerun()
            return
        
        # 오토 모드 처리
        if auto_mode and scene['type'] != 'choice':
            if 'scene_start_time' not in st.session_state:
                st.session_state.scene_start_time = time.time()
                
            elapsed_time = time.time() - st.session_state.scene_start_time
            
            # 설정된 시간이 지나면 자동 진행
            if elapsed_time >= auto_speed:
                if scene_index + 1 < len(episode['scenes']):
                    st.session_state.game_state['current_scene_index'] = scene_index + 1
                else:
                    # 프롤로그의 마지막 에피소드인지 확인
                    if current_ep >= len(PROLOGUE_EPISODES):
                        # 프롤로그 완료 플래그 설정
                        st.session_state.game_state['prologue_completed'] = True
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                        check_achievements()
                    else:
                        st.session_state.game_state['current_episode'] = current_ep + 1
                        st.session_state.game_state['current_scene_index'] = 0
                if 'scene_start_time' in st.session_state:
                    del st.session_state.scene_start_time
                st.rerun()
            else:
                # 남은 시간 표시
                remaining = auto_speed - elapsed_time
                st.markdown(f'<p style="text-align: center; color: #888;">⏱️ {remaining:.1f}초 후 자동 진행</p>', unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
        
        # 메시지 박스 스타일로 다음 버튼 (선택지가 아닌 경우)
        if scene['type'] != 'choice':
            col1, col2, col3 = st.columns([4, 1, 4])
            with col2:
                if st.button("▶", key=f"prologue_next_{current_ep}_{scene_index}", help="다음"):
                    if scene_index + 1 < len(episode['scenes']):
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                    else:
                        # 프롤로그의 마지막 에피소드인지 확인
                        if current_ep >= len(PROLOGUE_EPISODES):
                            # 프롤로그 완료 플래그 설정
                            st.session_state.game_state['prologue_completed'] = True
                            st.session_state.game_state['current_scene_index'] = scene_index + 1
                            check_achievements()
                        else:
                            st.session_state.game_state['current_episode'] = current_ep + 1
                            st.session_state.game_state['current_scene_index'] = 0
                    if 'scene_start_time' in st.session_state:
                        del st.session_state.scene_start_time
                    st.rerun()
    
    # 프롤로그 완료 시 Chapter 1 진행 버튼 표시
    else:
        if current_ep >= len(PROLOGUE_EPISODES):
            st.session_state.game_state['prologue_completed'] = True
            check_achievements()
            
            st.markdown('<div class="message-box">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; color: #333;">🎉 프롤로그 완료! 🎉</h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #666;">과거의 기억을 되찾은 당신... 이제 본격적인 이야기가 시작됩니다!</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🌟 Chapter 1: 마법학원에서의 새로운 시작 🌟", 
                           key="start_chapter1", 
                           help="Chapter 1으로 진행하기"):
                    st.session_state.game_state['current_scene'] = 'chapter_1'
                    st.session_state.game_state['current_episode'] = 1
                    st.session_state.game_state['current_scene_index'] = 0
                    if 'scene_start_time' in st.session_state:
                        del st.session_state.scene_start_time
                    st.rerun()
    
    # 진행 상황 표시
    if scene_index < len(episode['scenes']):
        progress = min(max((scene_index + 1) / len(episode['scenes']), 0.0), 1.0)
        st.progress(progress)
        st.markdown(f'<p style="text-align: center; color: #888;">프롤로그 에피소드 {current_ep}/3 - 진행률: {int(progress * 100)}%</p>', unsafe_allow_html=True)
    else:
        st.progress(1.0)
        st.markdown('<p style="text-align: center; color: #888;">프롤로그 완료! 🎉</p>', unsafe_allow_html=True)
    
    # 메뉴 버튼들
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.button("🏠 메뉴"):
            st.session_state.game_state['current_scene'] = 'main_menu'
            if 'scene_start_time' in st.session_state:
                del st.session_state.scene_start_time
            st.rerun()
    with col2:
        if st.button("⚙️ 설정"):
            st.session_state.game_state['current_scene'] = 'settings'
            if 'scene_start_time' in st.session_state:
                del st.session_state.scene_start_time
            st.rerun()
    with col3:
        if st.button("🏆 업적"):
            st.session_state.game_state['current_scene'] = 'achievements'
            if 'scene_start_time' in st.session_state:
                del st.session_state.scene_start_time
            st.rerun()
    with col4:
        if st.button("💾 저장"):
            save_game()
    with col5:
        if current_ep > 1:
            if st.button("🔄 이전"):
                st.session_state.game_state['current_episode'] = current_ep - 1
                st.session_state.game_state['current_scene_index'] = 0
                if 'scene_start_time' in st.session_state:
                    del st.session_state.scene_start_time
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 메뉴
def show_main_menu():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 게임 제목
    st.markdown('<h1 class="game-title">🌙 조화로의 길: 빛과 어둠을 품은 소녀 ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; font-size: 1rem; margin-top: -1rem;">調和への道：光と闇を抱く少女</p>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">~ 빛과 어둠 사이에서 피어나는 사랑 ~</p>', unsafe_allow_html=True)
    
    # 분위기 있는 인트로 텍스트
    st.markdown("""
    <div class="narration">
    천 년에 한 번 태어나는 이중속성자...<br>
    빛과 어둠을 동시에 품은 소녀의 운명은 과연..?<br><br>
    마법학원에서 펼쳐지는 여섯 남주와의 감동적인 로맨스 판타지
    </div>
    """, unsafe_allow_html=True)
    
    # 오토 모드 상태 표시
    auto_status = "🤖 자동 모드 ON" if st.session_state.game_state.get('auto_mode', False) else "✋ 수동 모드"
    st.markdown(f'<p style="text-align: center; color: #888; font-size: 0.9rem;">{auto_status}</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 이름 입력
        st.markdown("### 👑 주인공 이름 설정")
        player_name = st.text_input("이름을 입력해주세요", 
                                  value=st.session_state.game_state.get('player_name', ''),
                                  placeholder="예: 이하늘")
        
        if player_name:
            st.session_state.game_state['player_name'] = player_name
        
        st.markdown("---")
        
        # 메뉴 버튼들
        if st.button("🌟 새로 시작하기"):
            if player_name:
                st.session_state.game_state['current_scene'] = 'prologue'
                st.session_state.game_state['current_episode'] = 1
                st.session_state.game_state['current_scene_index'] = 0
                st.session_state.game_state['prologue_completed'] = False
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")
        
        if st.button("📚 이어서 하기"):
            if load_game():
                st.rerun()
        
        if st.button("💾 게임 저장하기"):
            save_game()
        
        if st.button("⚙️ 설정"):
            st.session_state.game_state['current_scene'] = 'settings'
            st.rerun()
            
        # 새로운 메뉴들
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🖼️ 갤러리"):
                st.session_state.game_state['current_scene'] = 'gallery'
                st.rerun()
        
        with col_b:
            if st.button("🏆 업적"):
                st.session_state.game_state['current_scene'] = 'achievements'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 프롤로그 데이터 생성 함수
def get_prologue_episodes():
    player_name = st.session_state.game_state.get('player_name', '공주')
    
    return {
        1: {
            'title': '운명적 탄생',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '17년 전, 어느 작은 마을의 한적한 밤...'
                },
                {
                    'type': 'narration',
                    'text': '달이 가장 높이 뜬 자정, 운명적인 순간이 찾아왔다.'
                },
                {
                    'type': 'narration',
                    'text': '한 아이가 이 세상에 태어나는 순간, 하늘과 땅이 요동쳤다.'
                },
                {
                    'type': 'narration',
                    'text': '그 순간, 마을 전체가 빛과 어둠으로 뒤덮였다.\n정오인데도 별이 보이고, 한밤중인데도 태양빛이 스며들었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '마을 사람 1',
                    'text': '이, 이게 무슨 일이야...! 낮과 밤이 뒤섞이고 있어!'
                },
                {
                    'type': 'dialogue',
                    'character': '마을 사람 2',
                    'text': '저주받은 아이다! 분명 불길한 징조야!'
                },
                {
                    'type': 'narration',
                    'text': '사람들은 두려움에 떨며 집 안으로 숨어들었다.\n부모조차 갓난아기를 제대로 안아보지 못했다.'
                },
                {
                    'type': 'narration',
                    'text': '작은 생명이 세상에 가져온 것은 축복이 아닌, 깊은 두려움이었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '산파',
                    'text': '이 아이... 보통 아이가 아니에요. 뭔가 특별한 힘이 느껴져요.'
                },
                {
                    'type': 'narration',
                    'text': '그 날 밤, 마을에는 이상한 소문이 퍼지기 시작했다.\n"천 년에 한 번 태어나는 이중속성자가 나타났다"고...'
                }
            ]
        },
        2: {
            'title': '어린 시절의 따뜻한 기억들',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '1-4살까지의 희미한 기억들...\n\n비록 짧았지만, 가족과 함께한 소중한 시간들이 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'우리 {player_name}... 엄마가 가장 사랑하는 보물이야... ♪'
                },
                {
                    'type': 'narration',
                    'text': '어머니는 매일 밤 따뜻한 자장가를 불러주셨다.\n그 목소리는 마법보다도 더 강력한 힘을 가지고 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'{player_name}, 아빠가 높이 높이 들어올려줄게! 무서워하지 마!'
                },
                {
                    'type': 'narration',
                    'text': '아버지의 강하고 따뜻한 손길...\n그 품에서는 세상의 모든 두려움이 사라졌다.'
                },
                {
                    'type': 'dialogue',
                    'character': '남동생 민호',
                    'text': f'누나! 같이 그림 그리자! 누나가 그린 꽃이 제일 예뻐!'
                },
                {
                    'type': 'narration',
                    'text': '남동생 민호와 함께 그림 그리며 놀던 평온한 오후들...\n가족만의 작은 정원에서 꽃을 기르던 행복한 시간들...'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'{player_name}는 특별한 아이야. 그 특별함을 두려워하지 말고, 자랑스러워해야 해.'
                },
                {
                    'type': 'narration',
                    'text': '그때는 몰랐다.\n이 따뜻하고 소중한 행복이 곧 산산조각날 것이라는 걸...'
                },
                {
                    'type': 'narration',
                    'text': '그리고 그 모든 기억들이 깊은 어둠 속으로 사라져버릴 것이라는 걸...'
                }
            ]
        },
        3: {
            'title': '운명의 날',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '5살 생일날... 가족들이 정성스럽게 준비해준 특별한 하루였다.'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'{player_name}, 생일 축하해! 엄마 아빠가 정말 특별한 케이크를 준비했어.'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': '우리 공주님, 5살이 되었구나. 촛불을 불어서 소원을 빌어봐.'
                },
                {
                    'type': 'dialogue',
                    'character': f'어린 {player_name}',
                    'text': '와아! 케이크다! 너무 예뻐요! 가족들과 영원히 함께 있고 싶어요!'
                },
                {
                    'type': 'narration',
                    'text': '그 순간, 너무나 순수하고 강렬한 감정이 폭발했다.\n기쁨, 사랑, 행복... 어린 마음이 감당하기엔 너무 큰 감정들이었다.'
                },
                {
                    'type': 'narration',
                    'text': '순간적으로 온 집이 눈부신 빛으로 가득 차더니 급속히 깊은 어둠에 휩싸였다.'
                },
                {
                    'type': 'dialogue',
                    'character': '민호',
                    'text': '누나...? 무서워... 이게 뭐야...?'
                },
                {
                    'type': 'narration',
                    'text': '빛과 어둠이 격렬하게 충돌하며 집 전체가 무너지기 시작했다.\n모든 것이 혼돈 속으로 빨려들어갔다.'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'{player_name}! 괜찮다, 아빠가 있어! 무서워하지 마!'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'{player_name}... 괜찮아, 엄마가 끝까지 지켜줄게... 사랑해...'
                },
                {
                    'type': 'narration',
                    'text': '정신을 잃어가는 마지막 순간...\n어머니가 자신을 감싸 안으며 속삭이던 따뜻한 목소리가 들렸다.'
                },
                {
                    'type': 'narration',
                    'text': '그리고... 깊고 어두운 침묵이 찾아왔다.'
                },
                {
                    'type': 'narration',
                    'text': '...\n\n...\n\n...'
                },
                {
                    'type': 'narration',
                    'text': '언제인지 모를 시간이 흐른 후, 작은 몸이 폐허 속에서 깨어났다.'
                },
                {
                    'type': 'narration',
                    'text': '주변은 온통 잿더미와 부서진 잔해들뿐...\n가족은 어디에도 보이지 않았다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'어린 {player_name}',
                    'text': '엄마...? 아빠...? 민호는...? 여기... 여기가 어디예요...?'
                },
                {
                    'type': 'narration',
                    'text': '하지만 그 이후로는 아무것도 기억나지 않았다.\n모든 소중한 추억들이 깊은 어둠 속으로 사라져버렸다.'
                },
                {
                    'type': 'narration',
                    'text': '17년이 지난 지금까지도, 그날의 진실은 베일에 감싸여 있다.'
                },
                {
                    'type': 'choice',
                    'text': '17년이 지난 지금, 때때로 마음 깊은 곳에서 울려오는 목소리가 있다...',
                    'options': [
                        {
                            'text': '기억나지 않지만... 분명 소중한 사람들이 있었을 것이다',
                            'effects': {'confidence': 1, 'light_control': 1}
                        },
                        {
                            'text': '이 공허함과 슬픔... 무언가 잃어버린 것 같다',
                            'effects': {'confidence': -1, 'balance': 1}
                        },
                        {
                            'text': '알 수 없는 죄책감이 나를 괴롭힌다',
                            'effects': {'confidence': -2, 'dark_control': 1}
                        }
                    ]
                },
                {
                    'type': 'narration',
                    'text': '프롤로그가 끝났습니다.\n\n이제 본격적인 이야기가 시작됩니다...'
                }
            ]
        }
    }
# Chapter 1 데이터 생성 함수 (대폭 확장된 버전)
def get_chapter1_episodes():
    player_name = st.session_state.game_state.get('player_name', '공주')
    
    return {
        1: {
            'title': '잿빛 일상',
            'scenes': [
                {
                    'type': 'narration',
                    'text': f'새벽 4시... {player_name}는 또다시 악몽에서 깨어났다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '하아... 또 그 꿈이야...'
                },
                {
                    'type': 'narration',
                    'text': '불타는 집, 들리지 않는 비명들... 항상 같은 악몽이었다.\n기억나지 않는 과거가 꿈속에서만 되살아났다.'
                },
                {
                    'type': 'narration',
                    'text': '5시... 침대 옆 서랍에서 작은 약병을 꺼냈다.\n감정 억제 약물. 하루도 빠뜨릴 수 없는 필수품이었다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '괜찮아... 오늘도 버텨보자.'
                },
                {
                    'type': 'narration',
                    'text': '거울 속 창백한 자신을 바라보며 다짐했다.\n다른 사람들에게 피해를 주지 않기 위해... 조용히, 눈에 띄지 않게.'
                },
                {
                    'type': 'narration',
                    'text': '6시... 다른 학생들이 오기 전 미리 교실에 도착했다.\n가장 뒷자리 구석. 그곳이 나의 자리였다.'
                },
                {
                    'type': 'choice',
                    'text': '오늘 하루를 어떻게 보낼까?',
                    'options': [
                        {
                            'text': '최대한 조용히 있으면서 눈에 띄지 않게 지내자',
                            'effects': {'confidence': -1, 'balance': 1},
                            'affection_effects': {}
                        },
                        {
                            'text': '조금이라도 다른 사람들과 대화해보자',
                            'effects': {'confidence': 1, 'light_control': 1},
                            'affection_effects': {}
                        },
                        {
                            'text': '그냥 수업에만 집중하자',
                            'effects': {'balance': 1},
                            'affection_effects': {}
                        },
                        {
                            'text': '일기를 써서 감정을 정리해보자',
                            'effects': {'balance': 2, 'confidence': 1},
                            'affection_effects': {}
                        }
                    ]
                }
            ]
        },
        2: {
            'title': '첫 번째 사고',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '마법학 수업 시간... 오늘도 평범하게 지나가기를 바랐다.'
                },
                {
                    'type': 'dialogue',
                    'character': '마법학 교수',
                    'text': '오늘은 이중속성에 대해 설명해보겠습니다. 물론 이론상으로만 존재하죠.'
                },
                {
                    'type': 'narration',
                    'text': '그 순간, 교실 안의 모든 시선이 나에게 집중되는 것을 느꼈다.'
                },
                {
                    'type': 'dialogue',
                    'character': '학생 A',
                    'text': '저기 앉은 애가 바로...'
                },
                {
                    'type': 'dialogue',
                    'character': '학생 B',
                    'text': '진짜 위험한 거 아냐? 가족들도...'
                },
                {
                    'type': 'narration',
                    'text': '속삭이는 소리들이 귓가에 맴돌았다.\n감정이 요동치기 시작했고... 책상 위의 잉크병이 얼어붙었다가 끓어올랐다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '미안해요... 죄송해요...'
                },
                {
                    'type': 'narration',
                    'text': '급하게 교실을 빠져나갔다. 또다시 실패했다.\n복도에서 홀로 서서 진정하려 애썼다.'
                },
                {
                    'type': 'choice',
                    'text': '이런 상황에서 어떻게 해야 할까?',
                    'options': [
                        {
                            'text': '보건실에 가서 진정제를 받자',
                            'effects': {'confidence': -1, 'balance': 1},
                            'affection_effects': {'doyoon': 5},
                            'next_episode': 'doyoon_route'
                        },
                        {
                            'text': '옥상에 올라가서 혼자 진정하자',
                            'effects': {'dark_control': 1, 'confidence': -1},
                            'affection_effects': {},
                            'next_episode': 'joowon_route'
                        },
                        {
                            'text': '도서관에 가서 마음을 가라앉히자',
                            'effects': {'balance': 1},
                            'affection_effects': {'yoojun': 3},
                            'next_episode': 'yoojun_route'
                        },
                        {
                            'text': '학교 뒷마당으로 가서 혼자 있자',
                            'effects': {'confidence': -1, 'dark_control': 1},
                            'affection_effects': {},
                            'next_episode': 'minjun_route'
                        }
                    ]
                }
            ]
        },
        'doyoon_route': {
            'title': '김도윤과의 따뜻한 만남',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '보건실 문을 두드렸다. 안에서는 누군가 부드러운 목소리로 "들어오세요"라고 말했다.'
                },
                {
                    'type': 'dialogue',
                    'character': '김도윤',
                    'text': '어머, 이렇게 아픈데 왜 혼자 참고 있어요?'
                },
                {
                    'type': 'narration',
                    'text': '능력 폭주로 손바닥에 화상과 동상이 동시에 생겨있었다.\n아무에게도 말하지 못하고 혼자 끙끙 앓고 있었는데...'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '괜찮아요... 저는 원래 이래요.'
                },
                {
                    'type': 'dialogue',
                    'character': '김도윤',
                    'text': '괜찮지 않아 보이는데요? 치료받으세요.'
                },
                {
                    'type': 'narration',
                    'text': '도윤의 부드러운 치유 마법에 처음으로 아픔이 사라졌다.\n이런 따뜻함을 느낀 건 언제 이후였을까...'
                },
                {
                    'type': 'dialogue',
                    'character': '김도윤',
                    'text': '이중속성... 정말 힘들겠어요. 감정 조절이 어려우시죠?'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '어떻게... 아시는 거예요?'
                },
                {
                    'type': 'dialogue',
                    'character': '김도윤',
                    'text': '치유 마법을 쓰면서 상대방의 마음 상태를 조금 느낄 수 있거든요. 많이 아프셨구나...'
                },
                {
                    'type': 'narration',
                    'text': '도윤의 눈에는 따뜻한 연민과 진심어린 걱정이 담겨있었다.\n처음으로 누군가가 나를 동정이 아닌 진심으로 걱정해주는 것 같았다.'
                },
                {
                    'type': 'dialogue',
                    'character': '김도윤',
                    'text': '아프면 언제든 오세요. 아픈 건 숨기는 게 아니에요.'
                },
                {
                    'type': 'choice',
                    'text': '도윤의 친절에 어떻게 반응할까?',
                    'options': [
                        {
                            'text': '고마워요... 하지만 자주 올 수는 없을 것 같아요',
                            'effects': {'confidence': -1},
                            'affection_effects': {'doyoon': 3}
                        },
                        {
                            'text': '정말 괜찮을까요? 제가 위험하지 않나요?',
                            'effects': {'confidence': -1, 'balance': 1},
                            'affection_effects': {'doyoon': 5}
                        },
                        {
                            'text': '감사해요. 오랜만에 따뜻함을 느꼈어요',
                            'effects': {'confidence': 1, 'light_control': 1},
                            'affection_effects': {'doyoon': 8}
                        }
                    ]
                }
            ]
        },
        'joowon_route': {
            'title': '남주원과의 운명적 만남',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '옥상으로 올라가는 도중... 감정 억제가 실패하기 시작했다.'
                },
                {
                    'type': 'narration',
                    'text': '바닥은 빛으로 타들어가고, 천장은 어둠에 침식되기 시작했다.\n빛과 어둠이 통제 불가능하게 폭주하고 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '학생들',
                    'text': '으아악! 도망가!'
                },
                {
                    'type': 'narration',
                    'text': '아래층에서 다른 학생들이 비명을 지르며 도망쳤다.\n또다시... 또다시 피해를 주고 말았다.'
                },
                {
                    'type': 'dialogue',
                    'character': '남주원',
                    'text': '우와! 이거 완전 신기한데? 어떻게 하는 거야?'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '도, 도망가세요! 위험해요!'
                },
                {
                    'type': 'dialogue',
                    'character': '남주원',
                    'text': '위험? 이거 멋진데? 빛과 어둠이 춤추는 것 같아!'
                },
                {
                    'type': 'narration',
                    'text': '주원이 바람 마법으로 폭주하는 속성들을 부드럽게 정리해주었다.\n처음으로... 내 힘을 무서워하지 않는 사람을 만났다.'
                },
                {
                    'type': 'dialogue',
                    'character': '남주원',
                    'text': '너 정말 대단해! 이런 힘을 가지고 있다니!'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '대단한 게 아니라... 위험한 거예요. 사람들이 다칠 수 있어요.'
                },
                {
                    'type': 'dialogue',
                    'character': '남주원',
                    'text': '그럼 조절하는 법을 배우면 되잖아! 이름이 뭐야? 나는 남주원! 앞으로 친구하자!'
                },
                {
                    'type': 'choice',
                    'text': '주원의 제안에 어떻게 반응할까?',
                    'options': [
                        {
                            'text': '고마워... 하지만 나와 친구가 되면 위험해',
                            'effects': {'confidence': -1, 'dark_control': 1},
                            'affection_effects': {'joowon': 3}
                        },
                        {
                            'text': '정말... 친구가 되어줄 거야?',
                            'effects': {'confidence': 1, 'light_control': 1},
                            'affection_effects': {'joowon': 8}
                        },
                        {
                            'text': '왜... 무서워하지 않는 거야?',
                            'effects': {'balance': 1},
                            'affection_effects': {'joowon': 5}
                        },
                        {
                            'text': '나... 정말 괴물이 아닐까?',
                            'effects': {'confidence': -2, 'dark_control': 2},
                            'affection_effects': {'joowon': 2}
                        }
                    ]
                }
            ]
        },
        'yoojun_route': {
            'title': '한유준과의 신비한 만남',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '도서관 깊숙한 곳... 고대 문헌 코너에서 혼자 책을 읽고 있었다.'
                },
                {
                    'type': 'narration',
                    'text': '마음을 진정시키려 했지만, 여전히 손끝에서 빛과 어둠이 번갈아 흘러나왔다.'
                },
                {
                    'type': 'narration',
                    'text': '그때 누군가 조용히 다가와서 한 권의 책을 놓고 갔다.\n『이중속성자의 진실』이라는 고대 예언서였다.'
                },
                {
                    'type': 'narration',
                    'text': '책을 열어보니... 내 상황과 정확히 일치하는 내용들이 적혀있었다.\n이런 책이 존재한다는 것 자체가 신기했다.'
                },
                {
                    'type': 'dialogue',
                    'character': '한유준',
                    'text': '그 책... 도움이 되길 바라.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '어떻게 이런 책을... 누구세요?'
                },
                {
                    'type': 'dialogue',
                    'character': '한유준',
                    'text': '한유준이야. 그리고... 네 미래는 보이지 않는다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '그게 무슨 뜻이에요?'
                },
                {
                    'type': 'dialogue',
                    'character': '한유준',
                    'text': '정해진 운명이 없다는 뜻이야. 그것이 오히려... 희망일지도.'
                },
                {
                    'type': 'narration',
                    'text': '유준이 물로 만든 작은 꽃을 선물했다. 투명하고 아름다운 꽃이었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '한유준',
                    'text': '물의 흐름처럼... 유연하게 살아가렴.'
                },
                {
                    'type': 'choice',
                    'text': '유준의 신비로운 말에 어떻게 반응할까?',
                    'options': [
                        {
                            'text': '운명이 없다는 게... 무서워요',
                            'effects': {'confidence': -1, 'dark_control': 1},
                            'affection_effects': {'yoojun': 3}
                        },
                        {
                            'text': '희망이라는 말... 오랜만에 들어봐요',
                            'effects': {'confidence': 1, 'light_control': 1},
                            'affection_effects': {'yoojun': 8}
                        },
                        {
                            'text': '당신은... 정말 신비로운 사람이네요',
                            'effects': {'balance': 1},
                            'affection_effects': {'yoojun': 5}
                        }
                    ]
                }
            ]
        },
        'minjun_route': {
            'title': '이민준과의 조용한 만남',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '학교 뒷마당... 아무도 오지 않는 조용한 곳이었다.'
                },
                {
                    'type': 'narration',
                    'text': '고목나무 그늘 아래 앉아서 무릎을 끌어안고 있었다.\n혼자 있고 싶었지만, 마음은 여전히 어지러웠다.'
                },
                {
                    'type': 'narration',
                    'text': '그때 나뭇가지가 부러지는 소리가 들렸다.\n누군가 조용히 다가오고 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '이민준',
                    'text': '...여기 있었구나.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '어떻게... 저를 찾으셨어요?'
                },
                {
                    'type': 'narration',
                    'text': '민준이 조금 떨어진 곳에 앉으며 말했다.\n가까이 오지 않는 것이 배려처럼 느껴졌다.'
                },
                {
                    'type': 'dialogue',
                    'character': '이민준',
                    'text': '...어둠 속성자끼리는 서로 느낄 수 있어. 특히 마음이 불안할 때는.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '당신도... 이런 적이 있나요?'
                },
                {
                    'type': 'dialogue',
                    'character': '이민준',
                    'text': '...많이. 처음엔 부모님도 무서워했어. 어둠 속성이라는 이유로.'
                },
                {
                    'type': 'narration',
                    'text': '민준의 목소리에는 깊은 이해와 공감이 담겨있었다.\n같은 아픔을 겪은 사람만이 가질 수 있는 따뜻함이었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '이민준',
                    'text': '...혼자가 아니야. 적어도 나는... 너를 이해해.'
                },
                {
                    'type': 'choice',
                    'text': '민준의 위로에 어떻게 반응할까?',
                    'options': [
                        {
                            'text': '감사해요... 혼자가 아니라는 게 위로가 돼요',
                            'effects': {'confidence': 1, 'balance': 1},
                            'affection_effects': {'minjun': 8}
                        },
                        {
                            'text': '당신은 어떻게 극복했나요?',
                            'effects': {'balance': 2},
                            'affection_effects': {'minjun': 6}
                        },
                        {
                            'text': '저도... 언젠가는 괜찮아질까요?',
                            'effects': {'confidence': -1, 'light_control': 1},
                            'affection_effects': {'minjun': 5}
                        }
                    ]
                }
            ]
        },
3: {
            'title': '학생회장과의 첫 만남',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '점심시간... 학생회실에서 "면담 요청"이 왔다.'
                },
                {
                    'type': 'narration',
                    'text': '무슨 일일까? 혹시 퇴학당하는 건 아닐까?\n불안한 마음으로 학생회실 문을 두드렸다.'
                },
                {
                    'type': 'dialogue',
                    'character': '신윤호',
                    'text': '들어와. 앉아.'
                },
                {
                    'type': 'narration',
                    'text': '학생회장 신윤호... 완벽하다는 소문이 자자한 그 사람이다.\n나와는 정반대의 존재.'
                },
                {
                    'type': 'dialogue',
                    'character': '신윤호',
                    'text': '사고 빈도가... 좀 높네.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '죄송합니다. 앞으로 더 조심할게요.'
                },
                {
                    'type': 'narration',
                    'text': '윤호는 서류를 보며 뭔가 말하려다가 입을 다물기를 반복했다.\n귀끝이 조금씩 빨갛게 달아오르는 게 보였다.'
                },
                {
                    'type': 'dialogue',
                    'character': '신윤호',
                    'text': '그런데... 도움이 필요한 일은 없어? 학교 적응이라든지...'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '아, 저는 괜찮습니다!'
                },
                {
                    'type': 'dialogue',
                    'character': '신윤호',
                    'text': '별로 특별히 신경 쓰는 건 아니야! 그냥... 학생회 업무니까!'
                },
                {
                    'type': 'narration',
                    'text': '얼굴이 더 빨갛게 되면서 주변 온도가 살짝 올라갔다.\n의외로... 귀여운 면이 있었다.'
                },
                {
                    'type': 'choice',
                    'text': '윤호의 서툰 친절에 어떻게 반응할까?',
                    'options': [
                        {
                            'text': '학생회장님이 저 같은 사람을 신경써주실 필요 없어요',
                            'effects': {'confidence': -1},
                            'affection_effects': {'yoonho': 3}
                        },
                        {
                            'text': '감사해요. 정말 따뜻한 마음이시네요',
                            'effects': {'confidence': 1, 'light_control': 1},
                            'affection_effects': {'yoonho': 8}
                        },
                        {
                            'text': '저... 많이 부담스럽죠?',
                            'effects': {'balance': 1},
                            'affection_effects': {'yoonho': 5}
                        },
                        {
                            'text': '학생회장님도 완벽하지 않으시네요',
                            'effects': {'confidence': 2},
                            'affection_effects': {'yoonho': 6}
                        }
                    ]
                }
            ]
        },
        4: {
            'title': '모든 시선이 집중되는 날',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '오늘은 특별히 더 많은 시선을 받는 것 같았다.\n복도를 지날 때마다 수군거리는 소리가 들렸다.'
                },
                {
                    'type': 'dialogue',
                    'character': '학생 A',
                    'text': '저 애가 그 이중속성자래...'
                },
                {
                    'type': 'dialogue',
                    'character': '학생 B',
                    'text': '가족들 죽인 거 맞대. 무서워...'
                },
                {
                    'type': 'narration',
                    'text': '하지만 이상하게도... 며칠 전과는 달랐다.\n몇몇 사람들의 시선에는 적대감이 아닌 다른 감정이 담겨있었다.'
                },
                {
                    'type': 'narration',
                    'text': '주원이가 창문 너머로 손을 흔들어주고,\n도윤이가 복도에서 따뜻한 미소를 지어준다.'
                },
                {
                    'type': 'narration',
                    'text': '민준이가 지나가며 작은 고개 끄덕임을 해주고,\n윤호가 학생회 공지에서 은근히 배려를 보여준다.'
                },
                {
                    'type': 'narration',
                    'text': '유준이가 도서관에서 의미심장한 미소를 보내준다.'
                },
                {
                    'type': 'choice',
                    'text': '이런 변화를 어떻게 받아들일까?',
                    'options': [
                        {
                            'text': '감사하지만... 혹시 동정하는 건 아닐까?',
                            'effects': {'confidence': -1, 'dark_control': 1},
                            'affection_effects': {}
                        },
                        {
                            'text': '처음으로... 혼자가 아니라는 느낌이야',
                            'effects': {'confidence': 2, 'light_control': 2},
                            'affection_effects': {'joowon': 2, 'doyoon': 2, 'minjun': 2, 'yoonho': 2, 'yoojun': 2}
                        },
                        {
                            'text': '아직은 조심스럽지만... 기대해봐도 될까?',
                            'effects': {'balance': 2, 'confidence': 1},
                            'affection_effects': {'joowon': 1, 'doyoon': 1, 'minjun': 1, 'yoonho': 1, 'yoojun': 1}
                        }
                    ]
                }
            ]
        },
        5: {
            'title': '작은 기적의 순간',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '마법 실습 시간... 오늘은 조금 다를 수 있을까?'
                },
                {
                    'type': 'narration',
                    'text': '언제나처럼 빛과 어둠이 뒤섞여 불안정했지만...\n이번엔 포기하지 않기로 했다.'
                },
                {
                    'type': 'narration',
                    'text': '주원이의 격려하는 시선, 도윤이의 걱정스러운 표정,\n민준이의 조용한 응원, 윤호의 긴장한 모습, 유준이의 신비로운 미소...'
                },
                {
                    'type': 'narration',
                    'text': '그들을 생각하며 천천히 마법을 시도해보았다.'
                },
                {
                    'type': 'narration',
                    'text': '빛과 어둠이... 처음으로 조화를 이루었다!\n작고 불안정하지만, 분명한 성공이었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '마법 실습 교수',
                    'text': '오? 훌륭한 진전이군요!'
                },
                {
                    'type': 'narration',
                    'text': '교실 안에서 작은 박수소리가 들렸다.\n모든 사람은 아니었지만... 몇몇은 진심으로 축하해주고 있었다.'
                },
                {
                    'type': 'choice',
                    'text': '이 작은 성공을 어떻게 받아들일까?',
                    'options': [
                        {
                            'text': '이건 그냥 운이었어... 다음엔 또 실패할 거야',
                            'effects': {'confidence': -1, 'dark_control': 1},
                            'affection_effects': {}
                        },
                        {
                            'text': '작은 발걸음이지만... 분명한 진전이야!',
                            'effects': {'confidence': 2, 'light_control': 1, 'balance': 1},
                            'affection_effects': {'joowon': 3, 'doyoon': 3, 'yoonho': 3}
                        },
                        {
                            'text': '모두 덕분이야... 혼자였다면 불가능했을 거야',
                            'effects': {'confidence': 1, 'balance': 2},
                            'affection_effects': {'joowon': 4, 'doyoon': 4, 'minjun': 4, 'yoonho': 4, 'yoojun': 4}
                        }
                    ]
                }
            ]
        },
        6: {
            'title': '새로운 시작',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '며칠이 지나고... 확실히 달라진 것들이 있었다.'
                },
                {
                    'type': 'narration',
                    'text': '여전히 모든 사람이 받아주는 건 아니지만,\n적어도 몇 명의 진짜 친구들이 생겼다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'{player_name}',
                    'text': '일기를 써보자... 오늘의 기분을.'
                },
                {
                    'type': 'narration',
                    'text': '"오늘은... 조금 다른 하루였다.\n처음으로 혼자가 아니라는 느낌이 들었다."'
                },
                {
                    'type': 'narration',
                    'text': '일기장에 적은 이 문장이... 17년 만에 처음으로 희망적인 글이었다.'
                },
                {
                    'type': 'choice',
                    'text': 'Chapter 1의 마지막... 어떤 마음가짐으로 끝낼까?',
                    'options': [
                        {
                            'text': '아직 갈 길이 멀지만... 이제 시작이야',
                            'effects': {'confidence': 2, 'light_control': 1, 'balance': 1},
                            'affection_effects': {'joowon': 3, 'doyoon': 3, 'yoonho': 3}
                        },
                        {
                            'text': '이런 행복이 계속될까... 아직 불안해',
                            'effects': {'dark_control': 2, 'balance': 1},
                            'affection_effects': {'minjun': 3, 'yoojun': 3}
                        },
                        {
                            'text': '변화를 받아들이고 더 용감해져보자',
                            'effects': {'confidence': 3, 'light_control': 2},
                            'affection_effects': {'joowon': 5, 'doyoon': 5, 'yoonho': 5, 'yoojun': 5, 'minjun': 5}
                        },
                        {
                            'text': '완벽하지 않아도 괜찮아... 나다운 속도로',
                            'effects': {'confidence': 1, 'balance': 3},
                            'affection_effects': {'doyoon': 4, 'minjun': 4, 'yoojun': 4}
                        }
                    ]
                }
            ]
        }
    }

# 캐릭터 만남 추가 함수
def add_character_meeting(character_id):
    if character_id not in st.session_state.game_state.get('met_characters', []):
        st.session_state.game_state['met_characters'].append(character_id)
        st.session_state.game_state['character_meeting_order'].append(character_id)
        check_achievements()  # 만남 업적 체크

# 특별한 선택지 표시 함수
def show_enhanced_choice(scene, episode_key, scene_index):
    st.markdown(f'<div class="message-box">{scene["text"]}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        for i, option in enumerate(scene['options']):
            # 선택지 효과 미리보기
            effects_preview = []
            
            for stat, value in option['effects'].items():
                if value > 0:
                    effects_preview.append(f"{stat} +{value}")
                elif value < 0:
                    effects_preview.append(f"{stat} {value}")
            
            affection_preview = []
            for char, value in option.get('affection_effects', {}).items():
                if value > 0:
                    char_names = {'yoonho': '신윤호', 'doyoon': '김도윤', 'minjun': '이민준', 'joowon': '남주원', 'yoojun': '한유준'}
                    affection_preview.append(f"{char_names.get(char, char)} +{value}")
            
            preview_text = ""
            if effects_preview:
                preview_text += f"📊 {', '.join(effects_preview)}"
            if affection_preview:
                if preview_text:
                    preview_text += " | "
                preview_text += f"💕 {', '.join(affection_preview)}"
            
            button_text = option['text']
            if preview_text:
                button_text += f"\n{preview_text}"
            
            if st.button(button_text, key=f"ch1_enhanced_choice_{episode_key}_{scene_index}_{i}"):
                # 선택지 효과 적용
                for stat, value in option['effects'].items():
                    st.session_state.game_state['player_stats'][stat] += value
                
                # 호감도 효과 적용
                for char, value in option.get('affection_effects', {}).items():
                    st.session_state.game_state['affection'][char] += value
                    # 캐릭터 만남 기록
                    if value > 0:
                        add_character_meeting(char)
                
                # 다음 에피소드 분기 처리
                if 'next_episode' in option:
                    next_ep = option['next_episode']
                    st.session_state.game_state['current_episode'] = next_ep
                    st.session_state.game_state['current_scene_index'] = 0
                else:
                    # 다음 장면으로
                    st.session_state.game_state['current_scene_index'] = scene_index + 1
                
                # 선택지 기록
                st.session_state.game_state['choices_made'].append({
                    'chapter': 'chapter_1',
                    'episode': episode_key,
                    'choice': option['text'],
                    'effects': option['effects'],
                    'affection_effects': option.get('affection_effects', {})
                })
                
                # 업적 체크
                check_achievements()
                
                st.rerun()

# Chapter 1 표시 함수 (완성 버전)
def show_chapter1():
    current_ep = st.session_state.game_state.get('current_episode', 1)
    
    # Chapter 1 데이터 동적 생성
    CHAPTER1_EPISODES = get_chapter1_episodes()
    
    if current_ep > len(CHAPTER1_EPISODES):
        st.session_state.game_state['current_scene'] = 'chapter_2'
        st.session_state.game_state['current_episode'] = 1
        st.session_state.game_state['current_scene_index'] = 0
        st.rerun()
        return
    
    # 현재 에피소드가 숫자가 아닌 경우 (루트별 에피소드)
    if isinstance(current_ep, str):
        episode_key = current_ep
    else:
        episode_key = current_ep
    
    if episode_key not in CHAPTER1_EPISODES:
        # 잘못된 에피소드인 경우 기본으로 돌아감
        st.session_state.game_state['current_episode'] = 1
        st.rerun()
        return
        
    episode = CHAPTER1_EPISODES[episode_key]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 에피소드 제목
    if isinstance(episode_key, int):
        st.markdown(f'<h2 style="text-align: center; color: #333;">🏫 Chapter 1-{episode_key} - {episode["title"]}</h2>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h2 style="text-align: center; color: #333;">🏫 Chapter 1 - {episode["title"]}</h2>', unsafe_allow_html=True)
    
    # 오토 모드 상태 표시
    auto_mode = st.session_state.game_state.get('auto_mode', False)
    auto_speed = st.session_state.game_state.get('auto_speed', 3.0)
    
    if auto_mode:
        st.markdown(f'<div style="text-align: center; color: #666; font-size: 0.9rem; margin: 1rem 0;">🤖 자동 모드 - {auto_speed}초마다 자동 진행</div>', unsafe_allow_html=True)
    
    # 장면별 표시
    scene_index = st.session_state.game_state.get('current_scene_index', 0)
    
    if scene_index < len(episode['scenes']):
        scene = episode['scenes'][scene_index]
        
        if scene['type'] == 'narration':
            st.markdown(f'<div class="message-box">{scene["text"]}</div>', unsafe_allow_html=True)
            
        elif scene['type'] == 'dialogue':
            st.markdown(f'<div class="character-name">{scene["character"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="message-box">"{scene["text"]}"</div>', unsafe_allow_html=True)
            
        elif scene['type'] == 'choice':
            # 강화된 선택지 표시
            show_enhanced_choice(scene, episode_key, scene_index)
            return
        
        # 다음 버튼 (선택지가 아닌 경우)
        if scene['type'] != 'choice':
            col1, col2, col3 = st.columns([4, 1, 4])
            with col2:
                if st.button("▶", key=f"ch1_next_{episode_key}_{scene_index}", help="다음"):
                    if scene_index + 1 < len(episode['scenes']):
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                    else:
                        # 에피소드 완료 - 다음 에피소드로
                        if isinstance(episode_key, str):
                            # 루트 에피소드가 끝나면 다음 일반 에피소드로
                            st.session_state.game_state['current_episode'] = 3
                        else:
                            # 일반 에피소드라면 다음 번호로
                            if episode_key >= 6:  # 마지막 에피소드
                                st.session_state.game_state['current_scene'] = 'chapter_2'
                                st.session_state.game_state['current_episode'] = 1
                            else:
                                st.session_state.game_state['current_episode'] = episode_key + 1
                        st.session_state.game_state['current_scene_index'] = 0
                    st.rerun()
    else:
        # 에피소드 완료
        st.markdown('<div class="message-box">에피소드 완료!</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if isinstance(episode_key, str):
                if st.button("다음으로"):
                    st.session_state.game_state['current_episode'] = 3
                    st.session_state.game_state['current_scene_index'] = 0
                    st.rerun()
            elif episode_key < 6:
                if st.button("다음 에피소드"):
                    st.session_state.game_state['current_episode'] = episode_key + 1
                    st.session_state.game_state['current_scene_index'] = 0
                    st.rerun()
            else:
                if st.button("Chapter 2로"):
                    st.session_state.game_state['current_scene'] = 'chapter_2'
                    st.session_state.game_state['current_episode'] = 1
                    st.session_state.game_state['current_scene_index'] = 0
                    st.rerun()
    
    # 진행 상황 표시
    if scene_index < len(episode['scenes']):
        progress = min(max((scene_index + 1) / len(episode['scenes']), 0.0), 1.0)
        st.progress(progress)
        if isinstance(episode_key, int):
            st.markdown(f'<p style="text-align: center; color: #888;">Chapter 1 에피소드 {episode_key}/6 - 진행률: {int(progress * 100)}%</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="text-align: center; color: #888;">Chapter 1 특별 에피소드 - 진행률: {int(progress * 100)}%</p>', unsafe_allow_html=True)
    
    # 만난 캐릭터 정보 표시
    met_chars = st.session_state.game_state.get('met_characters', [])
    if met_chars:
        char_names = {'yoonho': '신윤호', 'doyoon': '김도윤', 'minjun': '이민준', 'joowon': '남주원', 'yoojun': '한유준'}
        met_names = [char_names.get(char, char) for char in met_chars]
        st.markdown(f'<p style="text-align: center; color: #666; font-size: 0.9rem;">만난 캐릭터: {", ".join(met_names)}</p>', unsafe_allow_html=True)
    
    # 메뉴 버튼들
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.button("🏠 메뉴"):
            st.session_state.game_state['current_scene'] = 'main_menu'
            st.rerun()
    with col2:
        if st.button("⚙️ 설정"):
            st.session_state.game_state['current_scene'] = 'settings'
            st.rerun()
    with col3:
        if st.button("🏆 업적"):
            st.session_state.game_state['current_scene'] = 'achievements'
            st.rerun()
    with col4:
        if st.button("💾 저장"):
            save_game()
    with col5:
        if st.button("🔄 이전"):
            if isinstance(episode_key, str):
                st.session_state.game_state['current_episode'] = 2
                st.session_state.game_state['current_scene_index'] = 0
            elif episode_key > 1:
                st.session_state.game_state['current_episode'] = episode_key - 1
                st.session_state.game_state['current_scene_index'] = 0
            else:
                st.session_state.game_state['current_scene'] = 'prologue'
                st.session_state.game_state['current_episode'] = 3
                st.session_state.game_state['current_scene_index'] = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 실행 함수
def main():
    init_game_data()
    
    # 사이드바에 스탯 표시
    show_status_panel()
    
    current_scene = st.session_state.game_state.get('current_scene', 'main_menu')
    
    if current_scene == 'main_menu':
        show_main_menu()
    elif current_scene == 'settings':
        show_settings()
    elif current_scene == 'gallery':
        show_gallery()
    elif current_scene == 'achievements':
        show_achievements()
    elif current_scene == 'prologue':
        show_prologue()
    elif current_scene == 'chapter_1':
        show_chapter1()
    elif current_scene == 'chapter_2':
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #333;">📚 Chapter 2 - 깊어지는 인연</h2>', unsafe_allow_html=True)
        st.markdown('<div class="message-box">Chapter 2는 개발 중입니다! 곧 업데이트 예정이에요 ✨</div>', unsafe_allow_html=True)
        
        if st.button("🏠 메인 메뉴로 돌아가기"):
            st.session_state.game_state['current_scene'] = 'main_menu'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
