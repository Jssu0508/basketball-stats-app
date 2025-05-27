import streamlit as st
import time

# 玩家數據類別
class PlayerStats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.two_pt_made = 0
        self.two_pt_attempt = 0
        self.three_pt_made = 0
        self.three_pt_attempt = 0
        self.turnovers = 0
        self.assists = 0
        self.steals = 0

    def two_pt_display(self):
        if self.two_pt_attempt == 0:
            return "0/0 (0.0%)"
        percent = (self.two_pt_made / self.two_pt_attempt) * 100
        return f"{self.two_pt_made}/{self.two_pt_attempt} ({percent:.1f}%)"

    def three_pt_display(self):
        if self.three_pt_attempt == 0:
            return "0/0 (0.0%)"
        percent = (self.three_pt_made / self.three_pt_attempt) * 100
        return f"{self.three_pt_made}/{self.three_pt_attempt} ({percent:.1f}%)"

# 初始化
if "players" not in st.session_state:
    st.session_state.players = [PlayerStats() for _ in range(6)]
if "start_time" not in st.session_state:
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0.0
    st.session_state.timer_running = False

st.title("🏀 3v3 籃球數據統計")

# 計時器功能
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    fraction = int((seconds - int(seconds)) * 100)
    return f"{mins:02}:{secs:02}.{fraction:02}"

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ 開始", use_container_width=True):
        if not st.session_state.timer_running:
            st.session_state.timer_running = True
            st.session_state.start_time = time.time() - st.session_state.elapsed_time
with col2:
    if st.button("⏸️ 暫停", use_container_width=True):
        if st.session_state.timer_running:
            st.session_state.timer_running = False
            st.session_state.elapsed_time = time.time() - st.session_state.start_time
with col3:
    if st.button("🔁 歸零", use_container_width=True):
        st.session_state.timer_running = False
        st.session_state.elapsed_time = 0.0

# 更新時間
if st.session_state.timer_running:
    st.session_state.elapsed_time = time.time() - st.session_state.start_time
st.markdown(f"### ⏱️ 時間：{format_time(st.session_state.elapsed_time)}")

# 球員統計
for i in range(6):
    player = st.session_state.players[i]
    with st.expander(f"👤 Player {i+1}", expanded=True):
        st.markdown("#### 二分球")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"➕命中 P{i+1}", key=f"2pt_hit{i}"):
                player.two_pt_made += 1
                player.two_pt_attempt = max(player.two_pt_attempt, player.two_pt_made)
        with col2:
            if st.button(f"➖命中 P{i+1}", key=f"2pt_miss{i}"):
                player.two_pt_made = max(0, player.two_pt_made - 1)
        with col3:
            if st.button(f"➕出手 P{i+1}", key=f"2pt_attempt{i}"):
                player.two_pt_attempt += 1

        st.write(f"👉 命中率：{player.two_pt_display()}")

        st.markdown("#### 三分球")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"➕命中 P{i+1}", key=f"3pt_hit{i}"):
                player.three_pt_made += 1
                player.three_pt_attempt = max(player.three_pt_attempt, player.three_pt_made)
        with col2:
            if st.button(f"➖命中 P{i+1}", key=f"3pt_miss{i}"):
                player.three_pt_made = max(0, player.three_pt_made - 1)
        with col3:
            if st.button(f"➕出手 P{i+1}", key=f"3pt_attempt{i}"):
                player.three_pt_attempt += 1

        st.write(f"👉 命中率：{player.three_pt_display()}")

        st.markdown("#### 其他數據")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"失誤+1 P{i+1}", key=f"to{i}"):
                player.turnovers += 1
        with col2:
            if st.button(f"助攻+1 P{i+1}", key=f"ast{i}"):
                player.assists += 1
        with col3:
            if st.button(f"抄截+1 P{i+1}", key=f"stl{i}"):
                player.steals += 1

        st.write(f"失誤：{player.turnovers}，助攻：{player.assists}，抄截：{player.steals}")

        if st.button(f"🧹 清除 P{i+1}", key=f"reset{i}"):
            player.reset()

# 全部清除
if st.button("🔥 全部清除"):
    for player in st.session_state.players:
        player.reset()
