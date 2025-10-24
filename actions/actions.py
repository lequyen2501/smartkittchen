from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random, re

# ---------------------- DANH SÁCH CÔNG THỨC ----------------------
RECIPES = {
    "phở bò": {
        "ingredients": ["bánh phở", "thịt bò", "hành", "gừng", "nước dùng", "gia vị"],
        "time": 40,
        "steps": [
            "Nấu nước dùng với xương bò, hành và gừng nướng",
            "Chần bánh phở và thịt bò",
            "Múc nước dùng, thêm hành, ngò và gia vị vừa ăn"
        ]
    },
    "bún bò huế": {
        "ingredients": ["bún", "chả", "thịt bò", "sả", "mắm ruốc"],
        "time": 45,
        "steps": [
            "Nấu nước dùng với sả và mắm ruốc",
            "Cho thịt bò và chả vào nồi",
            "Thêm bún, chan nước dùng và ăn nóng"
        ]
    },
    "cơm chiên dương châu": {
        "ingredients": ["cơm nguội", "trứng", "tôm", "lạp xưởng", "cà rốt", "đậu Hà Lan"],
        "time": 20,
        "steps": [
            "Xào trứng và nguyên liệu chín",
            "Cho cơm vào đảo đều",
            "Nêm nếm vừa ăn, rắc hành lá"
        ]
    },
    "cá kho tộ": {
        "ingredients": ["cá", "nước mắm", "đường", "tiêu", "ớt", "hành tỏi"],
        "time": 30,
        "steps": [
            "Ướp cá với nước mắm, đường, tiêu, hành tỏi",
            "Kho cá lửa nhỏ đến khi nước sệt lại",
            "Rắc tiêu và dùng nóng với cơm"
        ]
    },
    "canh chua cá": {
        "ingredients": ["cá", "cà chua", "dứa", "me", "rau thơm"],
        "time": 25,
        "steps": [
            "Nấu nước dùng với me, cà chua, dứa",
            "Thả cá vào, nêm nếm vừa ăn",
            "Thêm rau thơm, tắt bếp"
        ]
    },
    "trứng chiên rau củ": {
        "ingredients": ["trứng", "cà rốt", "hành lá", "dầu ăn", "gia vị"],
        "time": 12,
        "steps": [
            "Đánh trứng với gia vị",
            "Xào sơ rau củ, đổ trứng vào",
            "Chiên chín vàng hai mặt"
        ]
    },
    "trứng hấp nấm": {
        "ingredients": ["trứng", "nấm", "hành lá", "gia vị"],
        "time": 15,
        "steps": [
            "Đánh trứng với nước dùng và gia vị",
            "Cho nấm vào bát, đổ trứng lên",
            "Hấp 12–15 phút"
        ]
    },
    "cháo yến mạch": {
        "ingredients": ["yến mạch", "rau củ", "muối", "nước"],
        "time": 20,
        "steps": [
            "Nấu yến mạch với nước cho nở",
            "Thêm rau củ và muối",
            "Khuấy đều đến khi sệt lại"
        ]
    },
    "súp bí đỏ": {
        "ingredients": ["bí đỏ", "sữa tươi", "bơ", "hành tây", "muối"],
        "time": 25,
        "steps": [
            "Xào bí đỏ và hành tây",
            "Thêm nước nấu mềm rồi xay nhuyễn",
            "Đun lại với sữa và bơ, nêm nếm vừa ăn"
        ]
    },
    "gỏi cuốn": {
        "ingredients": ["bánh tráng", "tôm", "thịt", "rau sống", "bún"],
        "time": 15,
        "steps": [
            "Luộc tôm, thịt, cắt lát",
            "Cuốn cùng rau sống và bún vào bánh tráng",
            "Chấm cùng nước mắm chua ngọt"
        ]
    }
}

# ---------------------- HÀM HỖ TRỢ ----------------------
def find_by_ingredient(ing):
    return [d for d, info in RECIPES.items() if ing in info["ingredients"]]

def list_under_minutes(minutes):
    return [d for d, info in RECIPES.items() if info["time"] <= minutes]

# ---------------------- ACTIONS ----------------------

class ActionSuggestRecipe(Action):
    def name(self): return "action_suggest_recipe"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "").lower()
        picks = []

        for ing in ["trứng", "cá", "gà", "tôm", "bò"]:
            if ing in text:
                picks += find_by_ingredient(ing)

        if "phút" in text:
            m = re.search(r"(\d+)\s*phút", text)
            if m:
                picks += list_under_minutes(int(m.group(1)))

        dish = random.choice(picks or list(RECIPES.keys()))
        dispatcher.utter_message(text=f"Gợi ý: **{dish}**. Bạn muốn xem nguyên liệu hay cách nấu?")
        return []

class ActionAskIngredients(Action):
    def name(self): return "action_ask_ingredients"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "").lower()
        dish = next((d for d in RECIPES if d in text), None) or random.choice(list(RECIPES.keys()))
        dispatcher.utter_message(text=f"Nguyên liệu của **{dish}**: {', '.join(RECIPES[dish]['ingredients'])}.")
        return []

class ActionAskTime(Action):
    def name(self): return "action_ask_time"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "").lower()
        dish = next((d for d in RECIPES if d in text), None) or random.choice(list(RECIPES.keys()))
        dispatcher.utter_message(text=f"Món **{dish}** nấu khoảng **{RECIPES[dish]['time']} phút**.")
        return []

class ActionAskSteps(Action):
    def name(self): return "action_ask_steps"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "").lower()
        dish = next((d for d in RECIPES if d in text), None)
        if dish:
            steps = "\n- ".join(RECIPES[dish]["steps"])
            dispatcher.utter_message(text=f"Cách nấu **{dish}**:\n- {steps}")
        else:
            dispatcher.utter_message(text="Xin lỗi, hiện mình chưa có công thức cho món này. Bạn có thể hỏi món khác nhé!")
        return []

# ---------------------- PHẦN MỞ RỘNG ----------------------
class ActionHealthyRecipes(Action):
    def name(self): return "action_healthy_recipes"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Gợi ý món tốt cho sức khỏe:\n- Salad rau củ 🥗\n- Cháo yến mạch\n- Cá hấp gừng\n- Súp bí đỏ\n- Trứng hấp nấm 🍄")
        return []

class ActionDiabetesRecipes(Action):
    def name(self): return "action_diabetes_recipes"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Người bị tiểu đường nên ăn:\n- Cháo yến mạch, cá hấp, rau luộc\n- Tránh đồ chiên rán và thức ăn nhiều đường.")
        return []

class ActionMealTimeRecipes(Action):
    def name(self): return "action_mealtime_recipes"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "")
        if "sáng" in text:
            msg = "Bữa sáng nên ăn nhẹ: trứng luộc, bánh mì nguyên cám, sữa chua không đường."
        elif "trưa" in text:
            msg = "Bữa trưa nên ăn đủ chất: cơm gạo lứt, cá hấp, rau luộc."
        elif "tối" in text:
            msg = "Bữa tối nên ăn thanh đạm: salad, súp bí đỏ hoặc cháo yến mạch."
        else:
            msg = "Bạn có thể chọn món nhẹ như trái cây hoặc sinh tố."
        dispatcher.utter_message(text=msg)
        return []

class ActionCookingTips(Action):
    def name(self): return "action_cooking_tips"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Mẹo nấu ăn: dùng chảo chống dính, nêm muối sau cùng để rau xanh, và chiên bằng dầu nóng đều để không dính chảo.")
        return []

class ActionFoodStorage(Action):
    def name(self): return "action_food_storage"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Bảo quản: rau củ trong ngăn mát 3 ngày, trứng 7 ngày, cá đông lạnh 2 tuần. Đồ ăn thừa nên dùng trong 24h.")
        return []

class ActionSubstituteIngredient(Action):
    def name(self): return "action_substitute_ingredient"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Thay thế nguyên liệu:\n- Đường → mật ong\n- Nước mắm → muối & nước tương\n- Thịt → đậu phụ khi ăn chay\n- Dầu ăn → bơ hoặc dầu ô liu.")
        return []
