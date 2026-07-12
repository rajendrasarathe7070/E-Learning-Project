import mysql.connector
import psycopg2
from psycopg2.extras import execute_values
import re
import unicodedata

# === 1. कॉन्फ़िगरेशन ===
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',          
    'password': '231208',  
    
    'database': 'diploma_papers_db'  
}
MYSQL_TABLE = 'question_papers'  

SUPABASE_CONN_STRING = "postgresql://postgres.khpacdsusjofcdvzzhzs:Rajendra@7354368656@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
SUPABASE_TABLE = 'core_pyq'  
 

# === 2. कॉलम मैपिंग ===
# यहाँ 'id', 'year', 'exam_type' और 'pdf_link' सीधे कॉपी होंगे।
# 'branch_id', 'semester', 'slug' और 'subject_title' को हम नीचे खुद भरेंगे।
COLUMN_MAP = {
    'id': 'id',
    'year': 'year',
    'exam_type': 'session',
    'pdf_link': 'pdf_link'  # ✅ pdf_link यहाँ जोड़ दिया गया है (सुनिश्चित करें कि MySQL और Supabase दोनों में यह नाम सही हो)
}

# === 3. हेल्पर फंक्शन ===
def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def migrate():
    print("🔄 ट्रांसफर प्रक्रिया (Default Branch=1, Sem=4, with PDF Link) शुरू हो रही है...")
    
    try:
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor(dictionary=True) 
        
        mysql_cols = list(COLUMN_MAP.values())
        # 'subject' और 'paper_code' को अलग से निकाल रहे हैं मर्ज करने के लिए
        all_needed_cols = mysql_cols + ['paper_name', 'paper_code'] 
        
        select_query = f"SELECT {', '.join(all_needed_cols)} FROM {MYSQL_TABLE}"
        mysql_cursor.execute(select_query)
        rows = mysql_cursor.fetchall()
        
        print(f"📦 Local MySQL से {len(rows)} रिकॉर्ड्स मिले।")
        if not rows:
            print("🛑 कोई डेटा नहीं मिला।")
            return

        supabase_conn = psycopg2.connect(SUPABASE_CONN_STRING)
        supabase_cursor = supabase_conn.cursor()

        final_insert_rows = []
        existing_slugs = set() 

        for row in rows:
            # 1. subject और paper_code को मर्ज करना
            current_subject = str(row['paper_name'] or '').strip()
            current_code = str(row['paper_code'] or '').strip()
            combined_title = f"{current_subject} ({current_code})" if current_code else current_subject
            
            # 2. ऑटोमैटिक स्लग जनरेट करना
            current_year = str(row['year'] or '')
            slug_base = slugify(f"{current_subject} {current_code} {current_year}")
            
            slug = slug_base
            count = 1
            while slug in existing_slugs:
                slug = f"{slug_base}-{count}"
                count += 1
            existing_slugs.add(slug)

            # 3. सीधे मैप होने वाले डेटा को लिस्ट में डालना
            new_row_data = []
            for supabase_col in COLUMN_MAP.keys():
                mysql_col_name = COLUMN_MAP[supabase_col]
                new_row_data.append(row[mysql_col_name])
            
            # 4. नए जेनरेटेड कॉलम्स और डिफ़ॉल्ट वैल्यूज को लिस्ट में जोड़ना
            new_row_data.append(combined_title) 
            new_row_data.append(slug)
            new_row_data.append(1)  # ✅ branch_id = 1 (हमेशा)
            new_row_data.append(4)  # ✅ semester = 4 (हमेशा - पुराना सेमेस्टर ओवरराइड हो जाएगा)
            
            final_insert_rows.append(tuple(new_row_data))

        # 5. Supabase में बल्क इंसर्ट करना
        # सुनिश्चित करें कि आपकी Supabase टेबल में ये सभी कॉलम नाम बिल्कुल सही हैं
        supabase_cols = list(COLUMN_MAP.keys()) + ['subject', 'slug', 'branch_id', 'semester'] 
        supabase_cols_str = ", ".join(supabase_cols)
        insert_query = f"INSERT INTO {SUPABASE_TABLE} ({supabase_cols_str}) VALUES %s"
        
        execute_values(supabase_cursor, insert_query, final_insert_rows)
        supabase_conn.commit()
        
        print(f"✅ सफलतापूर्वक {len(final_insert_rows)} रिकॉर्ड्स कस्टमाइज्ड डेटा के साथ Supabase में ट्रांसफर हो गए!")

    except Exception as e:
        print(f"❌ एरर आया: {e}")
        if 'supabase_conn' in locals():
            supabase_conn.rollback()
            
    finally:
        if 'mysql_conn' in locals() and mysql_conn.is_connected(): mysql_conn.close()
        if 'supabase_conn' in locals(): supabase_conn.close()
        print("🔌 कनेक्शन्स सुरक्षित बंद कर दिए गए हैं।")

if __name__ == "__main__":
    migrate()
