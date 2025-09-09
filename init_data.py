from core.database import SessionLocal, Base, engine
from models.tasks import Task, TaskType
from models.schedules import Schedule, ScheduleType
from models.study import Study, StudyType, StudySubject, Timetable
from models.meals import Meal, MealType, MealCategory
from models.points import Point, PointType, PointCategory, PointGoal, PointReward
from models.coins import Coin, CoinType, CoinCategory, CoinGoal, CoinShop, CoinExchange
from datetime import datetime, timedelta

def init_data():
    # テーブルを作成
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 既存のデータをクリア
        db.query(Task).delete()
        db.query(Schedule).delete()
        db.query(Study).delete()
        db.query(Timetable).delete()
        db.query(Meal).delete()
        db.query(Point).delete()
        db.query(PointGoal).delete()
        db.query(PointReward).delete()
        db.query(Coin).delete()
        db.query(CoinGoal).delete()
        db.query(CoinShop).delete()
        db.query(CoinExchange).delete()
        db.commit()
        
        # 毎日タスクのサンプルデータ
        daily_tasks = [
            Task(
                title="歯磨き",
                description="朝晩の歯磨き",
                fatigue=0,
                reward=10,
                completed=False,
                type=TaskType.DAILY,
                priority=1,
                duration=5,
                created_at=datetime.now()
            ),
            Task(
                title="朝食準備",
                description="健康的な朝食",
                fatigue=2,
                reward=15,
                completed=False,
                type=TaskType.DAILY,
                priority=2,
                duration=15,
                created_at=datetime.now()
            ),
            Task(
                title="運動",
                description="30分の運動",
                fatigue=5,
                reward=25,
                completed=False,
                type=TaskType.DAILY,
                priority=3,
                duration=30,
                created_at=datetime.now()
            ),
            Task(
                title="読書",
                description="30分の読書",
                fatigue=1,
                reward=20,
                completed=False,
                type=TaskType.DAILY,
                priority=2,
                duration=30,
                created_at=datetime.now()
            ),
        ]
        
        # 通常タスクのサンプルデータ
        normal_tasks = [
            Task(
                title="レポート提出",
                description="期末レポートの提出",
                deadline=datetime.now() + timedelta(days=7),
                priority=3,
                fatigue=8,
                reward=50,
                completed=False,
                type=TaskType.NORMAL,
                category="仕事",
                duration=120,
                created_at=datetime.now()
            ),
            Task(
                title="買い物",
                description="週末の買い物",
                deadline=datetime.now() + timedelta(days=2),
                priority=2,
                fatigue=3,
                reward=20,
                completed=True,
                type=TaskType.NORMAL,
                category="家事",
                duration=60,
                completed_at=datetime.now() - timedelta(hours=2),
                created_at=datetime.now() - timedelta(days=1)
            ),
            Task(
                title="掃除",
                description="部屋の掃除",
                deadline=datetime.now() + timedelta(days=3),
                priority=1,
                fatigue=5,
                reward=30,
                completed=False,
                type=TaskType.NORMAL,
                category="家事",
                duration=45,
                created_at=datetime.now()
            ),
            Task(
                title="メール返信",
                description="重要なメールへの返信",
                deadline=datetime.now() + timedelta(hours=6),
                priority=2,
                fatigue=1,
                reward=10,
                completed=False,
                type=TaskType.NORMAL,
                category="仕事",
                duration=15,
                created_at=datetime.now()
            ),
        ]
        
        # スケジュールのサンプルデータ
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        schedules = [
            Schedule(
                title="大学の授業",
                description="プログラミング基礎",
                start_time=today.replace(hour=9, minute=0),
                end_time=today.replace(hour=10, minute=30),
                schedule_type=ScheduleType.FIXED,
                priority=3,
                fatigue=2,
                category="学校",
                location="教室A"
            ),
            Schedule(
                title="アルバイト",
                description="コンビニ",
                start_time=today.replace(hour=14, minute=0),
                end_time=today.replace(hour=18, minute=0),
                schedule_type=ScheduleType.FIXED,
                priority=2,
                fatigue=4,
                category="バイト",
                location="コンビニ"
            ),
            Schedule(
                title="勉強時間",
                description="課題の復習",
                start_time=today.replace(hour=19, minute=0),
                end_time=today.replace(hour=21, minute=0),
                schedule_type=ScheduleType.FLEXIBLE,
                priority=2,
                fatigue=3,
                category="勉強",
                location="自宅"
            ),
            # 明日のスケジュール
            Schedule(
                title="部活",
                description="サッカー部",
                start_time=(today + timedelta(days=1)).replace(hour=16, minute=0),
                end_time=(today + timedelta(days=1)).replace(hour=18, minute=0),
                schedule_type=ScheduleType.FIXED,
                priority=2,
                fatigue=5,
                category="部活",
                location="グラウンド"
            ),
        ]
        
        # 勉強タスクのサンプルデータ
        studies = [
            Study(
                title="数学の微分積分",
                description="第3章の演習問題",
                subject=StudySubject.MATH,
                study_type=StudyType.ASSIGNMENT,
                priority=4,
                difficulty=3,
                estimated_hours=2.0,
                completed_hours=0.5,
                deadline=datetime.now() + timedelta(days=3),
                progress_percentage=25
            ),
            Study(
                title="プログラミング基礎",
                description="Pythonの基本文法",
                subject=StudySubject.PROGRAMMING,
                study_type=StudyType.SELF_STUDY,
                priority=3,
                difficulty=2,
                estimated_hours=1.5,
                completed_hours=1.0,
                deadline=datetime.now() + timedelta(days=7),
                progress_percentage=67
            ),
            Study(
                title="英語のリーディング",
                description="TOEIC対策",
                subject=StudySubject.LANGUAGE,
                study_type=StudyType.SELF_STUDY,
                priority=2,
                difficulty=2,
                estimated_hours=1.0,
                completed_hours=0.0,
                deadline=datetime.now() + timedelta(days=14),
                progress_percentage=0
            ),
            Study(
                title="物理の力学",
                description="ニュートンの運動法則",
                subject=StudySubject.SCIENCE,
                study_type=StudyType.LECTURE,
                priority=5,
                difficulty=4,
                estimated_hours=3.0,
                completed_hours=0.0,
                deadline=datetime.now() + timedelta(days=1),
                progress_percentage=0
            ),
            Study(
                title="歴史のレポート",
                description="明治維新について",
                subject=StudySubject.HISTORY,
                study_type=StudyType.ASSIGNMENT,
                priority=3,
                difficulty=2,
                estimated_hours=2.5,
                completed_hours=2.5,
                deadline=datetime.now() - timedelta(days=1),
                completed=True,
                progress_percentage=100,
                completed_at=datetime.now() - timedelta(hours=6)
            ),
        ]
        
        # 時間割のサンプルデータ
        timetable_entries = [
            # 月曜日
            Timetable(day_of_week=0, start_time="09:00", end_time="10:30", subject=StudySubject.MATH, title="微分積分", room="A101", teacher="田中先生"),
            Timetable(day_of_week=0, start_time="10:45", end_time="12:15", subject=StudySubject.PROGRAMMING, title="Python基礎", room="B203", teacher="佐藤先生"),
            Timetable(day_of_week=0, start_time="13:30", end_time="15:00", subject=StudySubject.LANGUAGE, title="英語", room="C305", teacher="Smith先生"),
            
            # 火曜日
            Timetable(day_of_week=1, start_time="09:00", end_time="10:30", subject=StudySubject.SCIENCE, title="物理", room="A102", teacher="山田先生"),
            Timetable(day_of_week=1, start_time="10:45", end_time="12:15", subject=StudySubject.LITERATURE, title="国語", room="B204", teacher="鈴木先生"),
            Timetable(day_of_week=1, start_time="13:30", end_time="15:00", subject=StudySubject.MATH, title="線形代数", room="A101", teacher="田中先生"),
            
            # 水曜日
            Timetable(day_of_week=2, start_time="09:00", end_time="10:30", subject=StudySubject.PROGRAMMING, title="データ構造", room="B203", teacher="佐藤先生"),
            Timetable(day_of_week=2, start_time="10:45", end_time="12:15", subject=StudySubject.HISTORY, title="日本史", room="C306", teacher="高橋先生"),
            Timetable(day_of_week=2, start_time="13:30", end_time="15:00", subject=StudySubject.LANGUAGE, title="英語", room="C305", teacher="Smith先生"),
            
            # 木曜日
            Timetable(day_of_week=3, start_time="09:00", end_time="10:30", subject=StudySubject.SCIENCE, title="化学", room="A103", teacher="伊藤先生"),
            Timetable(day_of_week=3, start_time="10:45", end_time="12:15", subject=StudySubject.MATH, title="統計学", room="A101", teacher="田中先生"),
            Timetable(day_of_week=3, start_time="13:30", end_time="15:00", subject=StudySubject.PROGRAMMING, title="アルゴリズム", room="B203", teacher="佐藤先生"),
            
            # 金曜日
            Timetable(day_of_week=4, start_time="09:00", end_time="10:30", subject=StudySubject.LITERATURE, title="現代文", room="B204", teacher="鈴木先生"),
            Timetable(day_of_week=4, start_time="10:45", end_time="12:15", subject=StudySubject.LANGUAGE, title="英語", room="C305", teacher="Smith先生"),
            Timetable(day_of_week=4, start_time="13:30", end_time="15:00", subject=StudySubject.HISTORY, title="世界史", room="C306", teacher="高橋先生"),
        ]
        
        # データベースに挿入
        for task in daily_tasks + normal_tasks:
            db.add(task)
        
        for schedule in schedules:
            db.add(schedule)
        
        for study in studies:
            db.add(study)
        
        for timetable in timetable_entries:
            db.add(timetable)
        
        # 食事のサンプルデータ
        meals = [
            Meal(
                name="和食定食",
                description="健康的な和食",
                meal_type=MealType.LUNCH,
                category=MealCategory.JAPANESE,
                calories=650,
                protein=25.0,
                carbs=80.0,
                fat=15.0,
                energy_boost=30,
                fatigue_reduction=20,
                is_recommended=True
            ),
            Meal(
                name="パスタカルボナーラ",
                description="クリーミーなパスタ",
                meal_type=MealType.DINNER,
                category=MealCategory.ITALIAN,
                calories=850,
                protein=35.0,
                carbs=95.0,
                fat=35.0,
                energy_boost=25,
                fatigue_reduction=15,
                is_recommended=False
            ),
            Meal(
                name="サラダとスープ",
                description="軽い食事",
                meal_type=MealType.LUNCH,
                category=MealCategory.HEALTHY,
                calories=350,
                protein=20.0,
                carbs=45.0,
                fat=8.0,
                energy_boost=15,
                fatigue_reduction=25,
                is_recommended=True
            ),
            Meal(
                name="ハンバーガーセット",
                description="ファストフード",
                meal_type=MealType.LUNCH,
                category=MealCategory.FAST_FOOD,
                calories=750,
                protein=30.0,
                carbs=85.0,
                fat=28.0,
                energy_boost=20,
                fatigue_reduction=10,
                is_recommended=False
            ),
            Meal(
                name="朝食セット",
                description="パンとコーヒー",
                meal_type=MealType.BREAKFAST,
                category=MealCategory.WESTERN,
                calories=450,
                protein=15.0,
                carbs=65.0,
                fat=12.0,
                energy_boost=35,
                fatigue_reduction=30,
                is_recommended=True
            ),
            Meal(
                name="中華丼",
                description="ボリューム満点",
                meal_type=MealType.DINNER,
                category=MealCategory.CHINESE,
                calories=900,
                protein=40.0,
                carbs=110.0,
                fat=25.0,
                energy_boost=30,
                fatigue_reduction=15,
                is_recommended=False
            ),
            Meal(
                name="フルーツサラダ",
                description="デザート",
                meal_type=MealType.SNACK,
                category=MealCategory.HEALTHY,
                calories=120,
                protein=2.0,
                carbs=25.0,
                fat=0.5,
                energy_boost=10,
                fatigue_reduction=15,
                is_recommended=True
            ),
            Meal(
                name="ラーメン",
                description="熱々のラーメン",
                meal_type=MealType.LUNCH,
                category=MealCategory.JAPANESE,
                calories=650,
                protein=25.0,
                carbs=85.0,
                fat=20.0,
                energy_boost=25,
                fatigue_reduction=20,
                is_recommended=False
            ),
        ]
        
        for meal in meals:
            db.add(meal)
        
        # ポイントのサンプルデータ
        points = [
            Point(
                amount=50,
                point_type=PointType.EARNED,
                category=PointCategory.TASK_COMPLETION,
                description="タスク完了: 歯磨き",
                balance_after=50
            ),
            Point(
                amount=25,
                point_type=PointType.EARNED,
                category=PointCategory.STUDY_PROGRESS,
                description="勉強進捗: 数学",
                balance_after=75
            ),
            Point(
                amount=30,
                point_type=PointType.EARNED,
                category=PointCategory.MEAL_HEALTHY,
                description="健康的な食事: 和食定食",
                balance_after=105
            ),
            Point(
                amount=20,
                point_type=PointType.SPENT,
                category=PointCategory.ENTERTAINMENT,
                description="報酬使用: ゲーム時間",
                balance_after=85
            ),
        ]
        
        # ポイント目標のサンプルデータ
        point_goals = [
            PointGoal(
                title="週間目標: 500ポイント獲得",
                description="今週中に500ポイントを獲得する",
                target_amount=500,
                current_amount=105,
                deadline=datetime.now() + timedelta(days=7),
                completed=False
            ),
            PointGoal(
                title="月間目標: 2000ポイント獲得",
                description="今月中に2000ポイントを獲得する",
                target_amount=2000,
                current_amount=105,
                deadline=datetime.now() + timedelta(days=30),
                completed=False
            ),
        ]
        
        # ポイント報酬のサンプルデータ
        point_rewards = [
            PointReward(
                title="ゲーム時間30分",
                description="30分間ゲームを楽しむ",
                cost=20,
                is_available=True,
                used_count=0
            ),
            PointReward(
                title="お菓子購入",
                description="好きなお菓子を購入",
                cost=50,
                is_available=True,
                used_count=0
            ),
            PointReward(
                title="映画鑑賞",
                description="映画を観に行く",
                cost=200,
                is_available=True,
                used_count=0
            ),
            PointReward(
                title="ショッピング",
                description="服や小物を購入",
                cost=300,
                is_available=True,
                used_count=0
            ),
        ]
        
        for point in points:
            db.add(point)
        
        for goal in point_goals:
            db.add(goal)
        
        for reward in point_rewards:
            db.add(reward)
        
        # コインのサンプルデータ
        coins = [
            Coin(
                amount=100,
                coin_type=CoinType.EARNED,
                category=CoinCategory.DAILY_LOGIN,
                description="デイリーログインボーナス",
                balance_after=100
            ),
            Coin(
                amount=50,
                coin_type=CoinType.EARNED,
                category=CoinCategory.TASK_COMPLETION,
                description="タスク完了: 朝食準備",
                balance_after=150
            ),
            Coin(
                amount=75,
                coin_type=CoinType.EARNED,
                category=CoinCategory.STUDY_PROGRESS,
                description="勉強進捗: 数学",
                balance_after=225
            ),
            Coin(
                amount=30,
                coin_type=CoinType.SPENT,
                category=CoinCategory.GAMING,
                description="ゲーム時間購入",
                balance_after=195
            ),
        ]
        
        # コイン目標のサンプルデータ
        coin_goals = [
            CoinGoal(
                title="週間目標: 500コイン獲得",
                description="今週中に500コインを獲得する",
                target_amount=500,
                current_amount=195,
                deadline=datetime.now() + timedelta(days=7),
                completed=False
            ),
            CoinGoal(
                title="月間目標: 2000コイン獲得",
                description="今月中に2000コインを獲得する",
                target_amount=2000,
                current_amount=195,
                deadline=datetime.now() + timedelta(days=30),
                completed=False
            ),
        ]
        
        # コインショップのサンプルデータ
        coin_shop_items = [
            CoinShop(
                title="ゲーム時間30分",
                description="30分間ゲームを楽しむ",
                cost=30,
                is_available=True,
                stock=10,
                used_count=0
            ),
            CoinShop(
                title="お菓子購入券",
                description="好きなお菓子を購入",
                cost=50,
                is_available=True,
                stock=-1,
                used_count=0
            ),
            CoinShop(
                title="映画鑑賞券",
                description="映画を観に行く",
                cost=200,
                is_available=True,
                stock=5,
                used_count=0
            ),
            CoinShop(
                title="ショッピング券",
                description="服や小物を購入",
                cost=300,
                is_available=True,
                stock=-1,
                used_count=0
            ),
        ]
        
        # 通貨交換のサンプルデータ
        coin_exchanges = [
            CoinExchange(
                from_currency="coin",
                to_currency="point",
                from_amount=50,
                to_amount=50,
                exchange_rate=1.0,
                description="コイン→ポイント交換"
            ),
        ]
        
        for coin in coins:
            db.add(coin)
        
        for goal in coin_goals:
            db.add(goal)
        
        for item in coin_shop_items:
            db.add(item)
        
        for exchange in coin_exchanges:
            db.add(exchange)
        
        db.commit()
        print("初期データの挿入が完了しました")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_data()
