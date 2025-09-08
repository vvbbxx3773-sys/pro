import sqlite3
import json
import os

DATABASE_NAME = 'user_data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 30000;")
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            فحص_الكليشة TEXT,
            فحص_الصورة TEXT,
            channel_username TEXT,
            subscription_message TEXT,
            subscription_media TEXT,
            sent_to_users TEXT,
            shortcuts TEXT,
            shortcuts_enabled BOOLEAN,
            اوامر_الكليشة TEXT,
            اوامر_الصورة TEXT,
            added_members_ids TEXT,
            muted_by_user_ids TEXT,
            self_destruct_settings TEXT,
            final_destruct_global_settings TEXT 
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_channels (
            user_id INTEGER,
            from_channel_id TEXT,
            to_channels_ids TEXT,
            PRIMARY KEY (user_id, from_channel_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_copy_status (
            user_id INTEGER PRIMARY KEY,
            copy_enabled BOOLEAN
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_email_send_status (
            user_id INTEGER PRIMARY KEY,
            total INTEGER,
            sent INTEGER,
            failed INTEGER,
            active BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_media_features_status (
            user_id INTEGER,
            chat_id INTEGER,
            feature_name TEXT,
            enabled BOOLEAN,
            PRIMARY KEY (user_id, chat_id, feature_name)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_command_status (
            user_id INTEGER,
            chat_id INTEGER,
            command_name TEXT,
            active BOOLEAN,
            extra_data TEXT,
            PRIMARY KEY (user_id, chat_id, command_name)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_contests (
            user_id INTEGER,
            channel_id TEXT,
            target_peer TEXT,
            keyword TEXT,
            pattern TEXT,
            PRIMARY KEY (user_id, channel_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_monitoring_settings (
            user_id INTEGER PRIMARY KEY,
            monitoring_channel_name TEXT,
            current_channel_id INTEGER,
            full_monitoring BOOLEAN
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_users_data (
            user_id INTEGER,
            monitored_user_id INTEGER,
            first_name TEXT,
            full_name TEXT,
            username TEXT,
            user_bio TEXT,
            profile_photos_count TEXT,
            stories_count TEXT,
            PRIMARY KEY (user_id, monitored_user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_hunting_status (
            user_id INTEGER PRIMARY KEY,
            is_hunting BOOLEAN,
            hunt_attempts INTEGER,
            current_hunt_channel_id INTEGER,
            current_hunt_pattern TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_ai_settings (
            user_id INTEGER PRIMARY KEY,
            bot_status BOOLEAN,
            stopped_chats TEXT,
            trigger_name TEXT,
            api_key TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_simulator_settings (
            user_id INTEGER PRIMARY KEY,
            simulated_bot_id INTEGER,
            current_action TEXT,
            simulation_pattern TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_font_settings (
            user_id INTEGER PRIMARY KEY,
            bold_enabled BOOLEAN,
            tshwesh_enabled BOOLEAN,
            ramz_enabled BOOLEAN,
            fi_enabled BOOLEAN,
            prr_enabled BOOLEAN,
            lafeta_enabled BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_reporting_status (
            user_id INTEGER PRIMARY KEY,
            reporting_active BOOLEAN,
            report_type TEXT,
            report_count INTEGER,
            last_report_comment TEXT,
            current_report_chat_id INTEGER,
            current_report_message_id INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_memes (
            user_id INTEGER,
            keyword TEXT,
            link TEXT,
            PRIMARY KEY (user_id, keyword)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_mirroring_data (
            owner_user_id INTEGER,
            chat_id INTEGER,
            mirrored_user_id INTEGER,
            chat_name TEXT,
            user_name TEXT,
            user_username TEXT,
            chat_type TEXT,
            PRIMARY KEY (owner_user_id, chat_id, mirrored_user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_collection_status (
            user_id INTEGER PRIMARY KEY,
            is_collecting BOOLEAN,
            current_bot_username TEXT,
            last_collected_count INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_broadcasting_status (
            user_id INTEGER PRIMARY KEY,
            is_broadcasting BOOLEAN,
            broadcast_type TEXT,
            sleep_time INTEGER,
            target_chats_data TEXT,
            message_id INTEGER,
            chat_id_of_message INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_tag_status (
            user_id INTEGER,
            chat_id INTEGER,
            is_tagging BOOLEAN,
            tag_type TEXT,
            tag_delay INTEGER,
            message_text TEXT,
            PRIMARY KEY (user_id, chat_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_id_templates (
            user_id INTEGER PRIMARY KEY,
            id_template TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_storage_settings (
            user_id INTEGER PRIMARY KEY,
            storage_group_id INTEGER,
            storage_group_title TEXT
        )
    ''')    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_flash_status (
            user_id INTEGER PRIMARY KEY, 
            flashing_in_progress BOOLEAN
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_rename_settings (
            user_id INTEGER PRIMARY KEY,
            name_update_enabled BOOLEAN,
            bio_update_enabled BOOLEAN,
            name_timezone TEXT,
            bio_timezone TEXT,
            time_format_key TEXT,
            bio_templates TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile_backup (
            user_id INTEGER PRIMARY KEY,
            original_first_name TEXT,
            original_last_name TEXT,
            original_bio TEXT
        )
    ''')
    # جدول حالة النشر
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_broadcasting_status (
        user_id INTEGER PRIMARY KEY,
        is_broadcasting BOOLEAN DEFAULT 0,
        broadcast_type TEXT,
        sleep_time INTEGER,
        message_id INTEGER,
        chat_id_of_message INTEGER
    )
    ''')
    
    # جدول المجموعات المخصصة
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_custom_groups (
        user_id INTEGER,
        group_name TEXT,
        PRIMARY KEY (user_id, group_name)
    )
    ''')
    

    conn.commit()
    return conn


def get_user_data(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        data_dict = dict(data)
        if 'added_members_ids' in data_dict and data_dict['added_members_ids']:
            data_dict['added_members_ids'] = json.loads(data_dict['added_members_ids'])
        else:
            data_dict['added_members_ids'] = []
        if 'muted_by_user_ids' in data_dict and data_dict['muted_by_user_ids']:
            data_dict['muted_by_user_ids'] = json.loads(data_dict['muted_by_user_ids'])
        else:
            data_dict['muted_by_user_ids'] = []
        if 'self_destruct_settings' in data_dict and data_dict['self_destruct_settings']:
            data_dict['self_destruct_settings'] = json.loads(data_dict['self_destruct_settings'])
        else:
            data_dict['self_destruct_settings'] = {}
        if 'final_destruct_global_settings' in data_dict and data_dict['final_destruct_global_settings']:
            data_dict['final_destruct_global_settings'] = json.loads(data_dict['final_destruct_global_settings'])
        else:
            data_dict['final_destruct_global_settings'] = {"active": False, "time_minutes": None, "timers": {}}
        return data_dict
    else:
        return {
            "user_id": user_id,
            "فحص_الكليشة": """
✦━───━✦✦━───━✦  
⚝ 𝓞𝔀𝓷𝓮𝓻 ⤠ {mention}  
⚝ 𝓟𝔂𝓽𝓱𝓸𝓷 ⤠ {pyver}  
⚝ 𝓣𝓮𝓵𝓮𝓽𝓱𝓸𝓷 ⤠ {telever}  
⚝ 𝓤𝓹𝓽𝓲𝓶𝓮 ⤠ {uptime}  
⚝ 𝓟𝓲𝓷𝓰 ⤠ {ping}  
⚝ 𝓓𝓪𝓽𝓮 ⤠ {date}  
✦━───━✦✦━───━✦
""",
            "فحص_الصورة": None,
            "channel_username": None,
            "subscription_message": "لا يمكنك مراسلتي إلا بعد الاشتراك في قناتي: {channel_username}",
            "subscription_media": None,
            "sent_to_users": "[]",
            "shortcuts": "{}",
            "shortcuts_enabled": True,
            "اوامر_الكليشة": None,
            "اوامر_الصورة": None,
            "added_members_ids": [],
            "muted_by_user_ids": [],
            "self_destruct_settings": {},
            "final_destruct_global_settings": {"active": False, "time_minutes": None, "timers": {}}
        }

def save_user_data(user_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    فحص_الكليشة = data.get("فحص_الكليشة")
    فحص_الصورة = data.get("فحص_الصورة")
    channel_username = data.get("channel_username")
    subscription_message = data.get("subscription_message")
    subscription_media = data.get("subscription_media")
    sent_to_users = data.get("sent_to_users")
    shortcuts = data.get("shortcuts")
    shortcuts_enabled = data.get("shortcuts_enabled")
    اوامر_الكليشة = data.get("اوامر_الكليشة")
    اوامر_الصورة = data.get("اوامر_الصورة")
    added_members_ids = json.dumps(data.get("added_members_ids", []))
    muted_by_user_ids = json.dumps(data.get("muted_by_user_ids", []))
    self_destruct_settings = json.dumps(data.get("self_destruct_settings", {}))
    final_destruct_global_settings = json.dumps(data.get("final_destruct_global_settings", {"active": False, "time_minutes": None, "timers": {}}))

    cursor.execute('''
        INSERT OR REPLACE INTO user_settings (user_id, فحص_الكليشة, فحص_الصورة, channel_username, subscription_message, subscription_media, sent_to_users, shortcuts, shortcuts_enabled, اوامر_الكليشة, اوامر_الصورة, added_members_ids, muted_by_user_ids, self_destruct_settings, final_destruct_global_settings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, فحص_الكليشة, فحص_الصورة, channel_username, subscription_message, subscription_media, sent_to_users, shortcuts, shortcuts_enabled, اوامر_الكليشة, اوامر_الصورة, added_members_ids, muted_by_user_ids, self_destruct_settings, final_destruct_global_settings))
    conn.commit()
    conn.close()




def get_flash_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT flashing_in_progress FROM user_flash_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row[0]) if row else False  # التعديل الأساسي هنا

def save_flash_status(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO user_flash_status 
                  (user_id, flashing_in_progress) VALUES (?, ?)''', 
                  (user_id, 1 if status else 0))
    conn.commit()
    conn.close()




def get_email_send_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT total, sent, failed, active FROM user_email_send_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"total": row['total'], "sent": row['sent'], "failed": row['failed'], "active": bool(row['active'])}
    else:
        return {"total": 0, "sent": 0, "failed": 0, "active": False}

def save_email_send_status(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    total = status.get("total", 0)
    sent = status.get("sent", 0)
    failed = status.get("failed", 0)
    active = status.get("active", False)
    cursor.execute('''
        INSERT OR REPLACE INTO user_email_send_status (user_id, total, sent, failed, active)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, total, sent, failed, active))
    conn.commit()
    conn.close()

def get_media_feature_status(user_id, chat_id, feature_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT enabled FROM user_media_features_status
        WHERE user_id = ? AND chat_id = ? AND feature_name = ?
    ''', (user_id, chat_id, feature_name))
    row = cursor.fetchone()
    conn.close()
    return bool(row['enabled']) if row else False

def save_media_feature_status(user_id, chat_id, feature_name, enabled_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_media_features_status (user_id, chat_id, feature_name, enabled)
        VALUES (?, ?, ?, ?)
    ''', (user_id, chat_id, feature_name, enabled_status))
    conn.commit()
    conn.close()

def get_command_status(user_id, chat_id, command_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT active, extra_data FROM user_command_status
        WHERE user_id = ? AND chat_id = ? AND command_name = ?
    ''', (user_id, chat_id, command_name))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"active": bool(row['active']), "extra_data": row['extra_data']}
    else:
        return {"active": False, "extra_data": None}

def save_command_status(user_id, chat_id, command_name, active_status, extra_data=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_command_status (user_id, chat_id, command_name, active, extra_data)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, chat_id, command_name, active_status, extra_data))
    conn.commit()
    conn.close()

def get_user_contest_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id, target_peer, keyword, pattern FROM user_contests WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()

    contests_data = {}
    for row in rows:
        contests_data[row['channel_id']] = {
            "target_peer": row['target_peer'],
            "keyword": row['keyword'],
            "pattern": row['pattern']
        }
    return contests_data

def save_user_contest_setting(user_id, channel_id, target_peer, keyword, pattern):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_contests (user_id, channel_id, target_peer, keyword, pattern)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, channel_id, target_peer, keyword, pattern))
    conn.commit()
    conn.close()

def get_all_active_contests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id, target_peer, keyword, pattern FROM user_contests')
    rows = cursor.fetchall()
    conn.close()

    contests_data = {}
    for row in rows:
        contests_data[str(row['channel_id'])] = {
            "target_peer": row['target_peer'],
            "keyword": row['keyword'],
            "pattern": row['pattern']
        }
    return contests_data


def delete_user_contest_setting(user_id, channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_contests WHERE user_id = ? AND channel_id = ?', (user_id, channel_id))
    conn.commit()
    conn.close()

def clear_all_user_contests(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_contests WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_monitoring_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_monitoring_settings WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "monitoring_channel_name": row['monitoring_channel_name'],
            "current_channel_id": row['current_channel_id'],
            "full_monitoring": bool(row['full_monitoring'])
        }
    else:
        return {
            "monitoring_channel_name": 'قناة_مراقبة_الحسابات',
            "current_channel_id": None,
            "full_monitoring": False
        }

def save_monitoring_settings(user_id, settings):
    conn = get_db_connection()
    cursor = conn.cursor()
    monitoring_channel_name = settings.get("monitoring_channel_name", 'قناة_مراقبة_الحسابات')
    current_channel_id = settings.get("current_channel_id")
    full_monitoring = settings.get("full_monitoring", False)
    cursor.execute('''
        INSERT OR REPLACE INTO user_monitoring_settings (user_id, monitoring_channel_name, current_channel_id, full_monitoring)
        VALUES (?, ?, ?, ?)
    ''', (user_id, monitoring_channel_name, current_channel_id, full_monitoring))
    conn.commit()
    conn.close()

def get_monitored_users_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM monitored_users_data WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    monitored_data = {}
    for row in rows:
        monitored_data[row['monitored_user_id']] = {
            "user_id": row['monitored_user_id'],
            "first_name": row['first_name'],
            "full_name": row['full_name'],
            "username": row['username'],
            "user_bio": row['user_bio'],
            "profile_photos_count": row['profile_photos_count'],
            "stories_count": row['stories_count']
        }
    return monitored_data

def save_monitored_user_data(user_id, monitored_user_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    m_user_id = monitored_user_data["user_id"]
    first_name = monitored_user_data["first_name"]
    full_name = monitored_user_data["full_name"]
    username = monitored_user_data["username"]
    user_bio = monitored_user_data["user_bio"]
    profile_photos_count = monitored_user_data["profile_photos_count"]
    stories_count = monitored_user_data["stories_count"]

    cursor.execute('''
        INSERT OR REPLACE INTO monitored_users_data (user_id, monitored_user_id, first_name, full_name, username, user_bio, profile_photos_count, stories_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, m_user_id, first_name, full_name, username, user_bio, profile_photos_count, stories_count))
    conn.commit()
    conn.close()

def delete_monitored_user_data(user_id, monitored_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM monitored_users_data WHERE user_id = ? AND monitored_user_id = ?', (user_id, monitored_user_id))
    conn.commit()
    conn.close()

def clear_all_monitored_users_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM monitored_users_data WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_hunting_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_hunting, hunt_attempts, current_hunt_channel_id, current_hunt_pattern FROM user_hunting_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "is_hunting": bool(row['is_hunting']),
            "hunt_attempts": row['hunt_attempts'],
            "current_hunt_channel_id": row['current_hunt_channel_id'],
            "current_hunt_pattern": row['current_hunt_pattern']
        }
    else:
        return {
            "is_hunting": False,
            "hunt_attempts": 0,
            "current_hunt_channel_id": None,
            "current_hunt_pattern": None
        }

def save_hunting_status(user_id, status_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_hunting = status_data.get("is_hunting", False)
    hunt_attempts = status_data.get("hunt_attempts", 0)
    current_hunt_channel_id = status_data.get("current_hunt_channel_id")
    current_hunt_pattern = status_data.get("current_hunt_pattern")
    cursor.execute('''
        INSERT OR REPLACE INTO user_hunting_status (user_id, is_hunting, hunt_attempts, current_hunt_channel_id, current_hunt_pattern)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, is_hunting, hunt_attempts, current_hunt_channel_id, current_hunt_pattern))
    conn.commit()
    conn.close()

def get_ai_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT bot_status, stopped_chats, trigger_name, api_key FROM user_ai_settings WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "bot_status": bool(row['bot_status']),
            "stopped_chats": set(json.loads(row['stopped_chats'])) if row['stopped_chats'] else set(),
            "trigger_name": row['trigger_name'],
            "api_key": row['api_key']
        }
    else:
        return {
            "bot_status": False,
            "stopped_chats": set(),
            "trigger_name": None,
            "api_key": None
        }

def save_ai_settings(user_id, settings):
    conn = get_db_connection()
    cursor = conn.cursor()
    bot_status = settings.get("bot_status", False)
    stopped_chats = json.dumps(list(settings.get("stopped_chats", set())))
    trigger_name = settings.get("trigger_name")
    api_key = settings.get("api_key")
    cursor.execute('''
        INSERT OR REPLACE INTO user_ai_settings (user_id, bot_status, stopped_chats, trigger_name, api_key)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, bot_status, stopped_chats, trigger_name, api_key))
    conn.commit()
    conn.close()


def get_simulator_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT simulated_bot_id, current_action, simulation_pattern FROM user_simulator_settings WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "simulated_bot_id": row['simulated_bot_id'],
            "current_action": row['current_action'],
            "simulation_pattern": row['simulation_pattern']
        }
    else:
        return {
            "simulated_bot_id": None,
            "current_action": "none",
            "simulation_pattern": ""
        }

def save_simulator_settings(user_id, settings):
    conn = get_db_connection()
    cursor = conn.cursor()
    simulated_bot_id = settings.get("simulated_bot_id")
    current_action = settings.get("current_action", "none")
    simulation_pattern = settings.get("simulation_pattern", "")
    cursor.execute('''
        INSERT OR REPLACE INTO user_simulator_settings (user_id, simulated_bot_id, current_action, simulation_pattern)
        VALUES (?, ?, ?, ?)
    ''', (user_id, simulated_bot_id, current_action, simulation_pattern))
    conn.commit()
    conn.close()

def get_font_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_font_settings WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "bold_enabled": bool(row['bold_enabled']),
            "tshwesh_enabled": bool(row['tshwesh_enabled']),
            "ramz_enabled": bool(row['ramz_enabled']),
            "fi_enabled": bool(row['fi_enabled']),
            "prr_enabled": bool(row['prr_enabled']),
            "lafeta_enabled": bool(row['lafeta_enabled'])
        }
    else:
        return {
            "bold_enabled": False,
            "tshwesh_enabled": False,
            "ramz_enabled": False,
            "fi_enabled": False,
            "prr_enabled": False,
            "lafeta_enabled": False
        }

def save_font_settings(user_id, settings):
    conn = get_db_connection()
    cursor = conn.cursor()
    bold_enabled = settings.get("bold_enabled", False)
    tshwesh_enabled = settings.get("tshwesh_enabled", False)
    ramz_enabled = settings.get("ramz_enabled", False)
    fi_enabled = settings.get("fi_enabled", False)
    prr_enabled = settings.get("prr_enabled", False)
    lafeta_enabled = settings.get("lafeta_enabled", False)
    cursor.execute('''
        INSERT OR REPLACE INTO user_font_settings (user_id, bold_enabled, tshwesh_enabled, ramz_enabled, fi_enabled, prr_enabled, lafeta_enabled)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, bold_enabled, tshwesh_enabled, ramz_enabled, fi_enabled, prr_enabled, lafeta_enabled))
    conn.commit()
    conn.close()

def get_reporting_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_reporting_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "reporting_active": bool(row['reporting_active']),
            "report_type": row['report_type'],
            "report_count": row['report_count'],
            "last_report_comment": row['last_report_comment'],
            "current_report_chat_id": row['current_report_chat_id'],
            "current_report_message_id": row['current_report_message_id']
        }
    else:
        return {
            "reporting_active": False,
            "report_type": None,
            "report_count": 0,
            "last_report_comment": None,
            "current_report_chat_id": None,
            "current_report_message_id": None
        }

def save_reporting_status(user_id, status_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    reporting_active = status_data.get("reporting_active", False)
    report_type = status_data.get("report_type")
    report_count = status_data.get("report_count", 0)
    last_report_comment = status_data.get("last_report_comment")
    current_report_chat_id = status_data.get("current_report_chat_id")
    current_report_message_id = status_data.get("current_report_message_id")
    cursor.execute('''
        INSERT OR REPLACE INTO user_reporting_status (user_id, reporting_active, report_type, report_count, last_report_comment, current_report_chat_id, current_report_message_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, reporting_active, report_type, report_count, last_report_comment, current_report_chat_id, current_report_message_id))
    conn.commit()
    conn.close()

def get_user_memes(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT keyword, link FROM user_memes WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    memes_data = {}
    for row in rows:
        memes_data[row['keyword']] = row['link']
    return memes_data

def save_user_meme(user_id, keyword, link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_memes (user_id, keyword, link)
        VALUES (?, ?, ?)
    ''', (user_id, keyword, link))
    conn.commit()
    conn.close()

def delete_user_meme(user_id, keyword):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_memes WHERE user_id = ? AND keyword = ?', (user_id, keyword))
    conn.commit()
    conn.close()

def clear_all_user_memes(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_memes WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def add_mirroring_entry(owner_user_id, chat_id, mirrored_user_id, chat_name, user_name, user_username, chat_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_mirroring_data
        (owner_user_id, chat_id, mirrored_user_id, chat_name, user_name, user_username, chat_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (owner_user_id, chat_id, mirrored_user_id, chat_name, user_name, user_username, chat_type))
    conn.commit()
    conn.close()

def get_mirroring_data_for_owner(owner_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id, mirrored_user_id, chat_name, user_name, user_username, chat_type FROM user_mirroring_data WHERE owner_user_id = ?', (owner_user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    mirroring_data = {}
    for row in rows:
        chat_id = row['chat_id']
        mirrored_user_id = row['mirrored_user_id']
        if chat_id not in mirroring_data:
            mirroring_data[chat_id] = {}
        mirroring_data[chat_id][mirrored_user_id] = {
            "chat_name": row['chat_name'],
            "user_name": row['user_name'],
            "user_username": row['user_username'],
            "chat_type": row['chat_type']
        }
    return mirroring_data

def remove_mirroring_entry(owner_user_id, chat_id, mirrored_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_mirroring_data WHERE owner_user_id = ? AND chat_id = ? AND mirrored_user_id = ?', (owner_user_id, chat_id, mirrored_user_id))
    conn.commit()
    conn.close()

def clear_all_mirroring_for_owner(owner_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_mirroring_data WHERE owner_user_id = ?', (owner_user_id,))
    conn.commit()
    conn.close()


def get_collection_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_collecting, current_bot_username, last_collected_count FROM user_collection_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "is_collecting": bool(row['is_collecting']),
            "current_bot_username": row['current_bot_username'],
            "last_collected_count": row['last_collected_count']
        }
    else:
        return {
            "is_collecting": False,
            "current_bot_username": None,
            "last_collected_count": 0
        }

def save_collection_status(user_id, status_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_collecting = status_data.get("is_collecting", False)
    current_bot_username = status_data.get("current_bot_username")
    last_collected_count = status_data.get("last_collected_count", 0)
    cursor.execute('''
        INSERT OR REPLACE INTO user_collection_status (user_id, is_collecting, current_bot_username, last_collected_count)
        VALUES (?, ?, ?, ?)
    ''', (user_id, is_collecting, current_bot_username, last_collected_count))
    conn.commit()
    conn.close()

#نشر

def get_broadcasting_status(user_id):
    """ندور حالة االنشر لكل مستخدم حتى ماتزرب السالفة"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_broadcasting_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "is_broadcasting": bool(row['is_broadcasting']),
            "broadcast_type": row['broadcast_type'],
            "sleep_time": row['sleep_time'],
            "message_id": row['message_id'],
            "chat_id_of_message": row['chat_id_of_message']
        }
    else:
        return {
            "is_broadcasting": False,
            "broadcast_type": None,
            "sleep_time": 0,
            "message_id": None,
            "chat_id_of_message": None
        }

def save_broadcasting_status(user_id, status):
    """حفظ حالة النشر للمستخدم"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO user_broadcasting_status 
    (user_id, is_broadcasting, broadcast_type, sleep_time, message_id, chat_id_of_message)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        int(status["is_broadcasting"]),
        status["broadcast_type"],
        status["sleep_time"],
        status["message_id"],
        status["chat_id_of_message"]
    ))
    
    conn.commit()
    conn.close()


def get_custom_groups(user_id):
    """النشر الجديد يبدي منا"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT group_name FROM user_custom_groups WHERE user_id = ?', (user_id,))
    groups = [row['group_name'] for row in cursor.fetchall()]
    conn.close()
    return groups

def save_custom_groups(user_id, groups):
    """حفظ المجموعات المخصصة للمستخدم"""
    conn = get_db_connection()
    cursor = conn.cursor()
    

    cursor.execute('DELETE FROM user_custom_groups WHERE user_id = ?', (user_id,))
    

    for group in groups:
        cursor.execute('INSERT INTO user_custom_groups (user_id, group_name) VALUES (?, ?)', 
                      (user_id, group))
    
    conn.commit()
    conn.close()

def get_tag_status(user_id, chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_tag_status WHERE user_id = ? AND chat_id = ?', (user_id, chat_id))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "is_tagging": bool(row['is_tagging']),
            "tag_type": row['tag_type'],
            "tag_delay": row['tag_delay'],
            "message_text": row['message_text']
        }
    else:
        return {
            "is_tagging": False,
            "tag_type": None,
            "tag_delay": None,
            "message_text": None
        }

def save_tag_status(user_id, chat_id, status_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_tagging = status_data.get("is_tagging", False)
    tag_type = status_data.get("tag_type")
    tag_delay = status_data.get("tag_delay")
    message_text = status_data.get("message_text")
    cursor.execute('''
        INSERT OR REPLACE INTO user_tag_status (user_id, chat_id, is_tagging, tag_type, tag_delay, message_text)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, chat_id, is_tagging, tag_type, tag_delay, message_text))
    conn.commit()
    conn.close()

def get_id_template(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id_template FROM user_id_templates WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row['id_template']
    else:
        return """** معلومات المستخدم **
⋆ـ┄─┄─┄─┄─┄──┄─┄─┄┄ـ⋆
** ✦╎الاسـم    ⇠ ** {fullname}
** ✦╎المعـرف  ⇠ ** {username}
** ✦╎الايـدي   ⇠ ** `{userid}`
** ✦╎الرتبـــه  ⇠ {rank} **
** ✦╎الصـور   ⇠ ** {count}
** ✦╎الحساب ⇠ ** {mention}
** ✦╎البايـو    ⇠ ** {bio}
⋆ـ┄─┄─┄─┄─┄──┄─┄─┄┄ـ⋆
"""

def save_id_template_for_user(user_id, template_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_id_templates (user_id, id_template)
        VALUES (?, ?)
    ''', (user_id, template_text))
    conn.commit()
    conn.close()

def get_user_storage_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT storage_group_id, storage_group_title FROM user_storage_settings WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "storage_group_id": row['storage_group_id'],
            "storage_group_title": row['storage_group_title']
        }
    else:
        return {
            "storage_group_id": None,
            "storage_group_title": f"مجموعة التخزين{user_id}" 
        }

def save_user_storage_settings(user_id, storage_group_id, storage_group_title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_storage_settings (user_id, storage_group_id, storage_group_title)
        VALUES (?, ?, ?)
    ''', (user_id, storage_group_id, storage_group_title))
    conn.commit()
    conn.close()


def get_rename_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_rename_settings WHERE user_id = ?', (user_id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        settings = dict(data)
        if settings['bio_templates']:
            settings['bio_templates'] = json.loads(settings['bio_templates'])
        else:
            settings['bio_templates'] = []
        return settings
    else:
        return {
            "user_id": user_id,
            "name_update_enabled": False,
            "bio_update_enabled": False,
            "name_timezone": None,
            "bio_timezone": None,
            "time_format_key": "1", # هنا لا تنسى هاي ياكلب من ترجع عدل
            "bio_templates": []
        }

def save_rename_settings(user_id, settings):
    conn = get_db_connection()
    cursor = conn.cursor()

    name_update_enabled = settings.get("name_update_enabled", False)
    bio_update_enabled = settings.get("bio_update_enabled", False)
    name_timezone = settings.get("name_timezone")
    bio_timezone = settings.get("bio_timezone")
    time_format_key = settings.get("time_format_key", "1")
    bio_templates = json.dumps(settings.get("bio_templates", []))

    cursor.execute('''
        INSERT OR REPLACE INTO user_rename_settings (user_id, name_update_enabled, bio_update_enabled, name_timezone, bio_timezone, time_format_key, bio_templates)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name_update_enabled, bio_update_enabled, name_timezone, bio_timezone, time_format_key, bio_templates))
    conn.commit()
    conn.close()





def get_user_channels_data(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT from_channel_id, to_channels_ids FROM user_channels WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    # يجب إرجاعها كقائمة من القواميس ليسهل التعامل معها في الكود الرئيسي حتى ماننبعر
    return [{'from_channel_id': row['from_channel_id'], 'to_channels_ids': row['to_channels_ids']} for row in rows]


def save_user_channels_data(user_id, from_channel_id, to_channels_ids_json):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_channels (user_id, from_channel_id, to_channels_ids)
        VALUES (?, ?, ?)
    ''', (user_id, from_channel_id, to_channels_ids_json))
    conn.commit()
    conn.close()

def delete_user_channel_data(user_id, from_channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_channels WHERE user_id = ? AND from_channel_id = ?', (user_id, from_channel_id))
    conn.commit()
    conn.close()

def get_copy_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT copy_enabled FROM user_copy_status WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row['copy_enabled']) if row else True # الافتراضي هو True (مفعل)


def save_copy_status(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_copy_status (user_id, copy_enabled)
        VALUES (?, ?)
    ''', (user_id, status))
    conn.commit()
    conn.close()


def get_all_user_channels_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    # جلب جميع القنوات المصدر ووجهاتها، مع معرف المستخدم الذي يمتلك الإعداد
    cursor.execute('SELECT user_id, from_channel_id, to_channels_ids FROM user_channels')
    rows = cursor.fetchall()
    conn.close()
    return [{'user_id': row['user_id'], 'from_channel_id': row['from_channel_id'], 'to_channels_ids': row['to_channels_ids']} for row in rows]




def get_profile_backup(user_id):
    """يستعيد بيانات الملف الشخصي الأصلية لمستخدم معين."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profile_backup WHERE user_id = ?', (user_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return dict(data)
    else:
        return None

def save_profile_backup(user_id, first_name, last_name, bio):
    """يحفظ بيانات الملف الشخصي الأصلية لمستخدم معين."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_profile_backup (user_id, original_first_name, original_last_name, original_bio)
        VALUES (?, ?, ?, ?)
    ''', (user_id, first_name, last_name, bio))
    conn.commit()
    conn.close()

def delete_profile_backup(user_id):
    """يحذف بيانات النسخ الاحتياطي للملف الشخصي لمستخدم معين."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_profile_backup WHERE user_id = ?', (user_id,)) #يارب انت العون والرجاء 
    conn.commit()
    conn.close()

initialize_db()


