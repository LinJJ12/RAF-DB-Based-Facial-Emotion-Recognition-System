"""
数据库模块 (可选)
如果需要保存识别历史,可以使用此模块
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PredictionHistory(db.Model):
    """预测历史表 - 轻量级，只存储元数据和文件路径"""
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(50), nullable=False)
    emotion_cn = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), nullable=True)
    # 存储文件路径而非 base64（轻量级）
    original_image_path = db.Column(db.String(500), nullable=True)  # 原始图片文件路径
    preprocessed_image_path = db.Column(db.String(500), nullable=True)  # 预处理后图片路径
    thumbnail_path = db.Column(db.String(500), nullable=True)  # 缩略图路径（可选）
    # 视频相关字段
    video_path = db.Column(db.String(500), nullable=True)  # 视频文件路径
    frame_timestamp = db.Column(db.Float, nullable=True)  # 视频帧时间戳（秒）
    frame_index = db.Column(db.Integer, nullable=True)  # 视频帧索引
    # 轻量级 JSON 数据
    probabilities = db.Column(db.JSON, nullable=True)  # 概率分布（小数据）
    input_type = db.Column(db.String(20), default='image')  # 'image' 或 'video'
    created_at = db.Column(db.DateTime, default=datetime.now)  # 使用本地时间而非 UTC
    
    def to_dict(self):
        return {
            'id': self.id,
            'emotion': self.emotion,
            'emotion_cn': self.emotion_cn,
            'confidence': self.confidence,
            'model_used': self.model_used,
            'username': self.username,
            'original_image_path': self.original_image_path,
            'preprocessed_image_path': self.preprocessed_image_path,
            'thumbnail_path': self.thumbnail_path,
            'video_path': self.video_path,
            'frame_timestamp': self.frame_timestamp,
            'frame_index': self.frame_index,
            'probabilities': self.probabilities,
            'input_type': self.input_type,
            'created_at': self.created_at.isoformat()
        }

class UserSession(db.Model):
    """用户会话表 (如果需要用户功能)"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now)  # 使用本地时间
    last_active = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 使用本地时间


class User(db.Model):
    """用户表，用于存储用户信息（可与 auth.py 中的内存用户同步）"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')
    avatar = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)  # 使用本地时间

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }


class UserEmotionSummary(db.Model):
    """用户情绪统计汇总表（数据分析+心理健康共用）"""
    __tablename__ = 'user_emotion_summary'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    summary_date = db.Column(db.Date, nullable=False)
    
    # 基础统计
    total_predictions = db.Column(db.Integer, default=0)
    dominant_emotion = db.Column(db.String(50))
    dominant_emotion_cn = db.Column(db.String(50))
    dominant_emotion_count = db.Column(db.Integer, default=0)
    emotion_counts = db.Column(db.JSON)  # 各情绪的计数字典
    avg_confidence = db.Column(db.Float)
    
    # 情绪占比
    positive_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
    positive_rate = db.Column(db.Float)  # 积极占比%
    negative_rate = db.Column(db.Float)  # 消极占比%
    
    # 情绪波动指标
    stability_stddev = db.Column(db.Float)  # 标准差
    stability_change_rate = db.Column(db.Float)  # 变化率
    stability_level = db.Column(db.String(20))  # 稳定/一般/波动较大
    
    # 时间维度
    active_days = db.Column(db.Integer, default=0)
    
    updated_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'summary_date': self.summary_date.isoformat() if self.summary_date else None,
            'total_predictions': self.total_predictions,
            'dominant_emotion': self.dominant_emotion,
            'dominant_emotion_cn': self.dominant_emotion_cn,
            'dominant_emotion_count': self.dominant_emotion_count,
            'emotion_counts': self.emotion_counts,
            'avg_confidence': self.avg_confidence,
            'positive_count': self.positive_count,
            'negative_count': self.negative_count,
            'neutral_count': self.neutral_count,
            'positive_rate': self.positive_rate,
            'negative_rate': self.negative_rate,
            'stability_stddev': self.stability_stddev,
            'stability_change_rate': self.stability_change_rate,
            'stability_level': self.stability_level,
            'active_days': self.active_days,
            'updated_at': self.updated_at.isoformat()
        }


class HealthAssessment(db.Model):
    """心理健康评估表（心理健康界面专用）"""
    __tablename__ = 'health_assessment'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    assessment_date = db.Column(db.Date, nullable=False)
    
    # 评估结果
    health_score = db.Column(db.Integer)  # 健康得分 0-100
    risk_level = db.Column(db.String(20))  # low/medium/high
    risk_level_cn = db.Column(db.String(20))  # 低风险/中等风险/高风险
    
    alert_title = db.Column(db.String(100))
    alert_type = db.Column(db.String(20))  # success/warning/error
    alert_description = db.Column(db.Text)
    
    # 多条建议（JSON数组）
    suggestions = db.Column(db.JSON)
    
    # 引用汇总表的统计数据
    positive_rate = db.Column(db.Float)
    negative_rate = db.Column(db.Float)
    emotion_stability = db.Column(db.Float)  # 情绪稳定性
    stability_level = db.Column(db.String(20))
    based_on_days = db.Column(db.Integer, default=1)  # 基于多少天的数据
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'health_score': self.health_score,
            'risk_level': self.risk_level,
            'risk_level_cn': self.risk_level_cn,
            'alert_title': self.alert_title,
            'alert_type': self.alert_type,
            'alert_description': self.alert_description,
            'suggestions': self.suggestions,
            'positive_rate': self.positive_rate,
            'negative_rate': self.negative_rate,
            'emotion_stability': self.emotion_stability,
            'stability_level': self.stability_level,
            'based_on_days': self.based_on_days,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class VideoAnalysisResult(db.Model):
    """视频分析结果表（两个界面共用）"""
    __tablename__ = 'video_analysis_result'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    video_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # 基础信息
    total_frames = db.Column(db.Integer)
    duration_seconds = db.Column(db.Float)
    
    # 统计结果
    dominant_emotion = db.Column(db.String(50))
    dominant_emotion_cn = db.Column(db.String(50))
    avg_confidence = db.Column(db.Float)
    
    # 情绪分布（JSON）
    emotion_distribution = db.Column(db.JSON)  # {"happy": 45, "sad": 20, ...}
    
    # 稳定性评估
    stability_level = db.Column(db.String(20))
    stability_score = db.Column(db.Float)
    
    # 洞察摘要
    insight_title = db.Column(db.String(200))
    insight_type = db.Column(db.String(20))
    insight_description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'video_id': self.video_id,
            'total_frames': self.total_frames,
            'duration_seconds': self.duration_seconds,
            'dominant_emotion': self.dominant_emotion,
            'dominant_emotion_cn': self.dominant_emotion_cn,
            'avg_confidence': self.avg_confidence,
            'emotion_distribution': self.emotion_distribution,
            'stability_level': self.stability_level,
            'stability_score': self.stability_score,
            'insight_title': self.insight_title,
            'insight_type': self.insight_type,
            'insight_description': self.insight_description,
            'created_at': self.created_at.isoformat()
        }


class EmotionJournal(db.Model):
    """情绪日记表"""
    __tablename__ = 'emotion_journal'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    
    # 日记内容
    content = db.Column(db.Text, nullable=False)
    
    # 情绪信息
    emotion = db.Column(db.String(50))  # 英文情绪
    emotion_cn = db.Column(db.String(50))  # 中文情绪
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'content': self.content,
            'emotion': self.emotion,
            'emotion_cn': self.emotion_cn,
            'date': self.created_at.isoformat(),  # 兼容前端字段名
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class GratitudeRecord(db.Model):
    """感恩记录表（积极心理学练习）"""
    __tablename__ = 'gratitude_record'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    
    # 感恩事项（JSON格式，存储列表）
    items = db.Column(db.JSON, nullable=False)  # ['事项1', '事项2', '事项3']
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'items': self.items,
            'date': self.created_at.isoformat(),  # 兼容前端字段名
            'created_at': self.created_at.isoformat()
        }

def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # 轻量升级：如果 prediction_history 缺少 username 列，动态添加
        try:
            _upgrade_prediction_history_add_username_if_needed()
        except Exception as e:
            print('检查/升级 prediction_history.username 失败:', e)
        print("数据库表创建/检查完成!")


def _upgrade_prediction_history_add_username_if_needed():
    """如果是 SQLite，检查并添加新列（最小改动）。"""
    engine = db.get_engine()
    if engine.dialect.name != 'sqlite':
        return
    
    # 使用 begin() 确保事务正确提交
    with engine.begin() as conn:
        result = conn.execute(db.text("PRAGMA table_info('prediction_history')"))
        cols = result.fetchall()
        existing = {c[1] for c in cols}
        
        # 需要添加的新列（轻量级：只存路径，不存 base64）
        new_columns = {
            'username': 'TEXT',
            'original_image_path': 'TEXT',
            'preprocessed_image_path': 'TEXT',
            'thumbnail_path': 'TEXT',
            'video_path': 'TEXT',
            'frame_timestamp': 'REAL',
            'frame_index': 'INTEGER',
            'probabilities': 'TEXT',  # SQLite 的 JSON 类型实际存储为 TEXT
            'input_type': 'TEXT DEFAULT "image"'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in existing:
                try:
                    conn.execute(db.text(f"ALTER TABLE prediction_history ADD COLUMN {col_name} {col_type}"))
                    print(f"✅ 已为 prediction_history 增加列 {col_name}")
                except Exception as e:
                    print(f"❌ 添加列 {col_name} 失败: {e}")

# 如果要在app.py中使用数据库,添加以下代码:
"""
from flask_sqlalchemy import SQLAlchemy
from database import db, PredictionHistory, init_db

# 在Flask app配置中添加:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotion_recognition.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
init_db(app)

# 在predict_emotion函数中保存记录:
history = PredictionHistory(
    emotion=result['emotion'],
    emotion_cn=result['emotion_cn'],
    confidence=confidence,
    model_used=model_name
)
db.session.add(history)
db.session.commit()

# 添加查询历史的接口:
@app.route('/api/history', methods=['GET'])
def get_history():
    limit = request.args.get('limit', 50, type=int)
    histories = PredictionHistory.query.order_by(
        PredictionHistory.created_at.desc()
    ).limit(limit).all()
    return jsonify({
        'histories': [h.to_dict() for h in histories]
    })
"""

