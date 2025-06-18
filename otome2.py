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
            'prologue_completed': False
        }

# 스탯 및 호감도 표시 함수 (오류 수정됨)
def show_status_panel():
    st.sidebar.markdown("### 📊 캐릭터 스탯")
    
    # 플레이어 능력치
    stats = st.session_state.game_state['player_stats']
    st.sidebar.progress(max(0.0, min(stats['light_control'] / 10, 1.0)))
    st.sidebar.caption(f"✨ 빛의 힘: {stats['light_control']}/10")
    
    st.sidebar.progress(max(0.0, min(stats['dark_control'] / 10, 1.0)))
    st.sidebar.caption(f"🌙 어둠의 힘: {stats['dark_control']}/10")
    
    st.sidebar.progress(max(0.0, min(stats['balance'] / 10, 1.0)))
    st.sidebar.caption(f"⚖️ 균형: {stats['balance']}/10")
    
    st.sidebar.progress(max(0.0, min(stats['confidence'] / 10, 1.0)))
    st.sidebar.caption(f"💪 자신감: {stats['confidence']}/10")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💕 호감도")
    
    # 남주들 호감도
    affection = st.session_state.game_state['affection']
    male_leads = {
        'yoonho': '🔥 신윤호',
        'doyoon': '💚 김도윤', 
        'minjun': '⚔️ 이민준',
        'joowon': '🌪️ 남주원',
        'yoojun': '🌊 한유준',
        'eunho': '🌟 정은호'
    }
    
    for char_id, char_name in male_leads.items():
        love_level = affection[char_id]
        st.sidebar.progress(max(0.0, min(love_level / 100, 1.0)))
        
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

# 갤러리 기능
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

# 업적 시스템
def check_achievements():
    achievements = st.session_state.game_state.get('achievements', [])
    stats = st.session_state.game_state['player_stats']
    affection = st.session_state.game_state['affection']
    
    # 새로운 업적 체크
    new_achievements = []
    
    if 'first_choice' not in achievements and len(st.session_state.game_state['choices_made']) >= 1:
        new_achievements.append('first_choice')
    
    if 'max_light' not in achievements and stats['light_control'] >= 10:
        new_achievements.append('max_light')
        
    if 'max_dark' not in achievements and stats['dark_control'] >= 10:
        new_achievements.append('max_dark')
    
    if 'first_love' not in achievements and any(love >= 50 for love in affection.values()):
        new_achievements.append('first_love')
    
    # 프롤로그 완료 업적 추가
    if 'prologue_complete' not in achievements and st.session_state.game_state.get('prologue_completed', False):
        new_achievements.append('prologue_complete')
    
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
        'prologue_complete': {'title': '운명의 시작', 'desc': '프롤로그를 완료했습니다', 'icon': '📖'}
    }
    
    if achievement_id in achievement_data:
        data = achievement_data[achievement_id]
        st.success(f"🏆 업적 달성! {data['icon']} {data['title']}: {data['desc']}")

# 업적 보기 화면
def show_achievements():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #333;">🏆 업적</h2>', unsafe_allow_html=True)
    
    achievement_data = {
        'first_choice': {'title': '첫 번째 선택', 'desc': '첫 선택지를 완료했습니다', 'icon': '🎯'},
        'prologue_complete': {'title': '운명의 시작', 'desc': '프롤로그를 완료했습니다', 'icon': '📖'},
        'max_light': {'title': '빛의 마스터', 'desc': '빛의 힘을 최대치로 올렸습니다', 'icon': '✨'},
        'max_dark': {'title': '어둠의 지배자', 'desc': '어둠의 힘을 최대치로 올렸습니다', 'icon': '🌙'},
        'first_love': {'title': '첫사랑의 시작', 'desc': '누군가와 깊은 유대를 형성했습니다', 'icon': '💕'},
        'story_complete': {'title': '이야기의 끝', 'desc': '메인 스토리를 완료했습니다', 'icon': '📖'},
        'perfect_balance': {'title': '완벽한 균형', 'desc': '빛과 어둠의 완벽한 조화를 이뤘습니다', 'icon': '⚖️'}
    }
    
    unlocked = st.session_state.game_state.get('achievements', [])
    
    cols = st.columns(2)
    for i, (ach_id, data) in enumerate(achievement_data.items()):
        with cols[i % 2]:
            if ach_id in unlocked:
                st.success(f"{data['icon']} **{data['title']}**\n\n{data['desc']}")
            else:
                st.info(f"🔒 **???**\n\n미해금 업적")
    
    st.markdown(f"**진행률: {len(unlocked)}/{len(achievement_data)} ({int(len(unlocked)/len(achievement_data)*100)}%)**")
    
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
# 설정 화면 (설정 즉시 반영 수정됨)
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
    
    # 설정값 즉시 업데이트 (수정됨)
    st.session_state.game_state['auto_mode'] = auto_mode
    if auto_mode != current_auto:
        st.success("✅ 오토 모드 설정이 변경되었습니다!")
    
    if auto_mode:
        auto_speed = st.slider("자동 진행 속도 (초)", 
                             min_value=1.0, max_value=10.0, 
                             value=current_speed, 
                             step=0.5,
                             key="auto_speed_slider")
        
        # 속도 설정값 즉시 업데이트 (수정됨)
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
    
    # 텍스트를 검은색으로 표시하여 가독성 확보
    st.markdown('<p style="color: #333;">텍스트 속도가 높을수록 빠르게 출력됩니다.</p>', unsafe_allow_html=True)
    
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
# Chapter 1 데이터 생성 함수
# Chapter 1 데이터 생성 함수 (완전한 버전)
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
                    'type': 'choice',
                    'text': '이런 상황에서 어떻게 해야 할까?',
                    'options': [
                        {
                            'text': '보건실에 가서 진정제를 받자',
                            'effects': {'confidence': -1, 'balance': 1},
                            'affection_effects': {'doyoon': 5}
                        },
                        {
                            'text': '옥상에 올라가서 혼자 진정하자',
                            'effects': {'dark_control': 1, 'confidence': -1},
                            'affection_effects': {}
                        }
                    ]
                }
            ]
        }
    }

# Chapter 1 표시 (완전한 버전)
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
    
    episode = CHAPTER1_EPISODES[current_ep]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 에피소드 제목
    st.markdown(f'<h2 style="text-align: center; color: #333;">🏫 Chapter 1-{current_ep} - {episode["title"]}</h2>', unsafe_allow_html=True)
    
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
            st.markdown(f'<div class="message-box">{scene["text"]}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                for i, option in enumerate(scene['options']):
                    if st.button(option['text'], key=f"ch1_choice_{current_ep}_{scene_index}_{i}"):
                        # 선택지 효과 적용
                        for stat, value in option['effects'].items():
                            st.session_state.game_state['player_stats'][stat] += value
                        
                        # 호감도 효과 적용
                        for char, value in option.get('affection_effects', {}).items():
                            st.session_state.game_state['affection'][char] += value
                        
                        # 선택지 기록
                        st.session_state.game_state['choices_made'].append({
                            'chapter': 'chapter_1',
                            'episode': current_ep,
                            'choice': option['text'],
                            'effects': option['effects'],
                            'affection_effects': option.get('affection_effects', {})
                        })
                        
                        # 업적 체크
                        check_achievements()
                        
                        # 다음 장면으로
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                        st.rerun()
            return
        
        # 다음 버튼 (선택지가 아닌 경우)
        if scene['type'] != 'choice':
            col1, col2, col3 = st.columns([4, 1, 4])
            with col2:
                if st.button("▶", key=f"ch1_next_{current_ep}_{scene_index}", help="다음"):
                    if scene_index + 1 < len(episode['scenes']):
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                    else:
                        # Chapter 1의 마지막 에피소드인지 확인
                        if current_ep >= len(CHAPTER1_EPISODES):
                            st.session_state.game_state['current_scene'] = 'chapter_2'
                            st.session_state.game_state['current_episode'] = 1
                            st.session_state.game_state['current_scene_index'] = 0
                        else:
                            st.session_state.game_state['current_episode'] = current_ep + 1
                            st.session_state.game_state['current_scene_index'] = 0
                    st.rerun()
    else:
        # 에피소드 완료
        st.markdown('<div class="message-box">에피소드 완료!</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if current_ep < len(CHAPTER1_EPISODES):
                if st.button("다음 에피소드"):
                    st.session_state.game_state['current_episode'] = current_ep + 1
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
        st.markdown(f'<p style="text-align: center; color: #888;">Chapter 1 에피소드 {current_ep}/{len(CHAPTER1_EPISODES)} - 진행률: {int(progress * 100)}%</p>', unsafe_allow_html=True)
    
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
            if current_ep > 1:
                st.session_state.game_state['current_episode'] = current_ep - 1
                st.session_state.game_state['current_scene_index'] = 0
            else:
                st.session_state.game_state['current_scene'] = 'prologue'
                st.session_state.game_state['current_episode'] = 3
                st.session_state.game_state['current_scene_index'] = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
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
