"""
重新计算情绪汇总数据
根据预测历史记录重新生成准确的情绪汇总
"""
from database import db, UserEmotionSummary, PredictionHistory
from app import app
from datetime import date
from collections import Counter

with app.app_context():
    try:
        # 获取今天的所有预测记录
        today = date.today()
        
        # 先删除今天的情绪汇总（重新计算）
        UserEmotionSummary.query.filter_by(
            username='admin',
            summary_date=today
        ).delete()
        db.session.commit()
        
        print("✅ 已清除今天的旧汇总数据")
        
        # 获取今天 admin 用户的所有预测历史
        today_start = today
        today_predictions = PredictionHistory.query.filter(
            PredictionHistory.username == 'admin',
            db.func.date(PredictionHistory.created_at) == today_start
        ).all()
        
        print(f"\n📊 找到 {len(today_predictions)} 条今天的预测记录：")
        
        if not today_predictions:
            print("❌ 没有找到预测记录")
            exit(0)
        
        # 统计情绪分布
        emotion_counts = Counter()
        confidences = []
        
        for pred in today_predictions:
            print(f"  - {pred.emotion_cn} (置信度: {pred.confidence:.2%})")
            emotion_counts[pred.emotion_cn] += 1
            confidences.append(pred.confidence)
        
        print(f"\n📈 情绪分布: {dict(emotion_counts)}")
        
        # 计算主导情绪
        dominant_emotion_cn = emotion_counts.most_common(1)[0][0]
        dominant_emotion_count = emotion_counts[dominant_emotion_cn]
        
        # 中文到英文映射
        cn_to_en = {
            '生气': 'anger', '厌恶': 'disgust', '害怕': 'fear',
            '高兴': 'happy', '平静': 'normal', '悲伤': 'sad', '惊讶': 'surprise'
        }
        
        # 计算积极/消极/中性
        positive_emotions_cn = ['高兴', '惊讶']
        negative_emotions_cn = ['悲伤', '生气', '厌恶', '害怕']
        
        positive_count = sum(emotion_counts.get(e, 0) for e in positive_emotions_cn)
        negative_count = sum(emotion_counts.get(e, 0) for e in negative_emotions_cn)
        neutral_count = emotion_counts.get('平静', 0)
        
        total = len(today_predictions)
        avg_confidence = sum(confidences) / total if confidences else 0
        
        # 创建新的汇总记录
        summary = UserEmotionSummary(
            username='admin',
            summary_date=today,
            total_predictions=total,
            dominant_emotion=cn_to_en.get(dominant_emotion_cn, dominant_emotion_cn),
            dominant_emotion_cn=dominant_emotion_cn,
            dominant_emotion_count=dominant_emotion_count,
            emotion_counts=dict(emotion_counts),
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            positive_rate=round(positive_count / total, 2) if total > 0 else 0,
            negative_rate=round(negative_count / total, 2) if total > 0 else 0,
            avg_confidence=round(avg_confidence, 2)
        )
        
        db.session.add(summary)
        db.session.commit()
        
        print(f"\n✅ 已创建新的情绪汇总记录：")
        print(f"  总识别次数: {total}")
        print(f"  主导情绪: {dominant_emotion_cn} (出现 {dominant_emotion_count} 次)")
        print(f"  积极次数: {positive_count}")
        print(f"  消极次数: {negative_count}")
        print(f"  中性次数: {neutral_count}")
        print(f"  平均置信度: {avg_confidence:.2%}")
        print(f"\n🎉 请刷新管理界面查看更新后的数据！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
