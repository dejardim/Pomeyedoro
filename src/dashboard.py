import time
import requests
import streamlit as st


BACKEND_URL = "http://localhost:8000/api/eye-count"

# Global variables to hold the blinking data
all_blink_sessions = []


def get_eye_count():
    """Fetches the count of eye blinks from the backend."""
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        return response.json().get('count')
    else:
        st.write("Error fetching eye blink data!")
        return None


def update_blink_data_sidebar():
    """Updates the blinking data in the sidebar."""
    global all_blink_sessions

    st.sidebar.header("Blinking Data")

    if not all_blink_sessions:
        st.sidebar.text("INSUFFICIENT DATA")
        return

    last_session_blinks = all_blink_sessions[-1]
    mean_blinks = sum(all_blink_sessions) / len(all_blink_sessions)
    
    st.sidebar.markdown(f"**Session Blinks**: {last_session_blinks}")
    st.sidebar.markdown(f"**Mean Blinks per Session**: {mean_blinks:.2f}")


def pomodoro_timer(session_duration):
    global session_number

    with st.empty():
        while True:
            initial_eye_count = get_eye_count()

            for i in range(session_duration, 0, -1):
                st.write(f'Session: {i} seconds remaining')
                time.sleep(1)
                st.write("") # clear the previous time

            final_eye_count = get_eye_count()
            
            if final_eye_count and initial_eye_count:
                current_blinks = final_eye_count - initial_eye_count

                all_blink_sessions.append(current_blinks)
                update_blink_data_sidebar()

                message = f"You blinked {current_blinks} times during this session!"
                st.write(message)

                time.sleep(3)


def main():
    st.title("Eye-Tracking with Pomeyedoro")
    update_blink_data_sidebar()  # Display initial blink data

    session_duration = st.slider('Session Duration (in seconds)', 10, 3600, 1500)

    if st.button("Start Pomeyedoro"):
        pomodoro_timer(session_duration)


if __name__ == "__main__":
    main()
