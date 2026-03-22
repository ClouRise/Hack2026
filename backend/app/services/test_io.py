# test_io.py
import uuid
import secrets
from typing import Optional, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.models import Test, Section, Question, Formula, Session, Answer, question_metrics
from app.models.question import QuestionType
from app.models.formula import Formula as FormulaModel


# ====================================
# МАППИНГ ТИПОВ
# ====================================

FRONTEND_TO_DB_TYPE: dict[str, QuestionType] = {
    "single_choice":   QuestionType.SINGLE,
    "multiple_choice": QuestionType.MULTIPLE,
    "slider":          QuestionType.RANGE,
    "text":            QuestionType.TEXT,
    "textarea":        QuestionType.TEXTAREA,
    "yesno":           QuestionType.YESNO,
    "yes_no":          QuestionType.YESNO,
    "number":          QuestionType.NUMBER,
    "date":            QuestionType.DATE,
    "time":            QuestionType.TIME,
    "rating":          QuestionType.RATING,
}

DB_TO_FRONTEND_TYPE: dict[QuestionType, str] = {
    QuestionType.SINGLE:   "single_choice",
    QuestionType.MULTIPLE: "multiple_choice",
    QuestionType.RANGE:    "slider",
    QuestionType.TEXT:     "text",
    QuestionType.TEXTAREA: "textarea",
    QuestionType.YESNO:    "yes_no",
    QuestionType.NUMBER:   "number",
    QuestionType.DATE:     "date",
    QuestionType.TIME:     "time",
    QuestionType.RATING:   "rating",
}

# какие ключи срезать из опций перед отдачей гостю
GUEST_STRIP_FIELDS: dict[QuestionType, set[str]] = {
    QuestionType.SINGLE:   {"weight"},
    QuestionType.MULTIPLE: {"weight"},
    QuestionType.YESNO:    {"weight"},
    QuestionType.RANGE:    {"score_ranges"},
}

# какие поля из config выносить в корень JSON 
CONFIG_ROOT_FIELDS: dict[QuestionType, list[str]] = {
    QuestionType.SINGLE:   ["options", "score_ranges"],
    QuestionType.MULTIPLE: ["options", "score_ranges"],
    QuestionType.YESNO:    ["options", "score_ranges"],
    QuestionType.RANGE:    ["min", "max", "step", "labels", "score_ranges"],
    QuestionType.NUMBER:   ["min", "max", "step"],
    QuestionType.RATING:   ["min", "max"],
    QuestionType.TEXT:     ["placeholder"],
    QuestionType.TEXTAREA: ["placeholder"],
}

# какие поля из JSON вопроса сохранять в config JSONB при импорте.
CONFIG_SOURCE_FIELDS: dict[str, list[str]] = {
    "single_choice":   ["options"],
    "multiple_choice": ["options"],
    "yesno":           ["options"],
    "yes_no":          ["options"],
    "slider":          ["min", "max", "step", "labels", "score_ranges"],
    "number":          ["min", "max", "step"],
    "rating":          ["min", "max"],
    "text":            ["placeholder"],
    "textarea":        ["placeholder"],
}

# ====================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ====================================

def build_question_config(q_data: dict) -> dict:
    """собирает JSONB config из полей вопроса."""
    fields = CONFIG_SOURCE_FIELDS.get(q_data["type"], [])
    return {
        field: q_data[field]
        for field in fields
        if field in q_data
    }


def expand_question_config(config: dict, db_type: QuestionType) -> dict:
    """разворачивает JSONB config в поля для экспорта"""
    fields = CONFIG_ROOT_FIELDS.get(db_type, [])
    return {
        field: config[field]
        for field in fields
        if field in config
    }


def strip_sensitive_from_options(options: list, strip_keys: set) -> list:
    """убирает веса из словарей"""
    return [
        {k: v for k, v in opt.items() if k not in strip_keys}
        for opt in options
    ]


def remap_report_template(
    template:        dict,
    question_id_map: dict[str, uuid.UUID],
    metric_id_map:   dict[str, uuid.UUID],
) -> dict:
    """Заменяет старые UUID в report_template на новые после импорта."""
    def remap_block(block: dict) -> dict:
        b = block.copy()
        if b.get("metric_id"):
            b["metric_id"] = str(metric_id_map.get(b["metric_id"], b["metric_id"]))
        b["metric_ids"] = [
            str(metric_id_map.get(mid, mid)) for mid in b.get("metric_ids", [])
        ]
        b["question_ids"] = [
            str(question_id_map.get(qid, qid)) for qid in b.get("question_ids", [])
        ]
        return b

    return {
        "client":       [remap_block(b) for b in template.get("client", [])],
        "psychologist": [remap_block(b) for b in template.get("psychologist", [])],
    }


# =====================================
# ИМПОРТ: JSON в БД
# =====================================

async def import_test(
    db:              AsyncSession,
    data:            dict,
    psychologist_id: uuid.UUID,
) -> Test:
    """
    разбивает экспортный JSON по таблицам
    все UUID генерируются заново — по сути копия теста.
    next_question_id в опциях обновляется на новые UUID
    """

    #Тест
    test = Test(
        id=uuid.uuid4(),
        psychologist_id=psychologist_id,
        title=data["title"],
        description=data.get("description"),
        show_report_to_client=data.get("show_report_to_client", False),
        required_fields=data.get("client_fields", []),
        report_template=data.get("report_template", {"client": [], "psychologist": []}),
        access_link=secrets.token_urlsafe(16),
    )
    db.add(test)
    await db.flush()

    #Секции + вопросы 
    question_id_map: dict[str, uuid.UUID] = {}

    for section_data in data.get("sections", []):
        section = Section(
            id=uuid.uuid4(),
            test_id=test.id,
            order=section_data["order"],
            title=section_data["title"],
        )
        db.add(section)
        await db.flush()

        for q_data in section_data.get("questions", []):
            new_q_id = uuid.uuid4()
            question_id_map[q_data["id"]] = new_q_id

            question = Question(
                id=new_q_id,
                test_id=test.id,
                section_id=section.id,
                text=q_data["text"],
                type=FRONTEND_TO_DB_TYPE.get(q_data["type"], QuestionType.TEXT),
                order_index=q_data["order"],
                is_required=q_data.get("required", True),
                is_hidden=q_data.get("hidden_by_default", False),
                config=build_question_config(q_data),
            )
            db.add(question)

    await db.flush()

    #next_question_id
    for old_q_id, new_q_id in question_id_map.items():
        result = await db.execute(select(Question).where(Question.id == new_q_id))
        q = result.scalar_one_or_none()
        if not q or not q.config.get("options"):
            continue

        needs_update = False
        updated_options = []
        for opt in q.config["options"]:
            opt = opt.copy()
            if opt.get("next_question_id"):
                new_next = question_id_map.get(opt["next_question_id"])
                if new_next:
                    opt["next_question_id"] = str(new_next)
                    needs_update = True
            updated_options.append(opt)

        if needs_update:
            q.config = {**q.config, "options": updated_options}

    await db.flush()

    #метрики
    metric_id_map: dict[str, uuid.UUID] = {}

    for m_data in data.get("metrics", []):
        new_m_id = uuid.uuid4()
        metric_id_map[m_data["id"]] = new_m_id

        formula = Formula(
            id=new_m_id,
            test_id=test.id,
            name=m_data["name"],
            expression=m_data["operation"],
            ranges=m_data.get("interpretations", []),
            coefficient=m_data["coefficient"],
        )
        db.add(formula)
        await db.flush()

        for old_q_id in m_data.get("question_ids", []):
            new_q_id = question_id_map.get(old_q_id)
            if new_q_id:
                await db.execute(
                    insert(question_metrics).values(
                        question_id=new_q_id,
                        formula_id=new_m_id,
                    )
                )

    #перезаписываем UUID в report_template
    test.report_template = remap_report_template(
        data.get("report_template", {"client": [], "psychologist": []}),
        question_id_map,
        metric_id_map,
    )

    await db.commit()
    await db.refresh(test)
    return test


# =====================================
# ЭКСПОРТ: БД в JSON
# =====================================

async def export_test(db: AsyncSession, test_id: uuid.UUID) -> dict:
    """собирает полный JSON из БД"""

    result = await db.execute(
        select(Test)
        .where(Test.id == test_id, Test.is_deleted == False)
        .options(
            selectinload(Test.sections).selectinload(Section.questions),
            selectinload(Test.formula).selectinload(Formula.questions),
        )
    )
    test: Optional[Test] = result.scalar_one_or_none()
    if not test:
        raise ValueError(f"Тест {test_id} не найден")

    sections_out = []
    for section in sorted(test.sections, key=lambda s: cast(Section, s).order):
        questions_out = []
        for q in sorted(section.questions, key=lambda q: q.order_index):
            questions_out.append({
                "id":                str(q.id),
                "section_id":        str(q.section_id),
                "order":             q.order_index,
                "text":              q.text,
                "type":              DB_TO_FRONTEND_TYPE.get(q.type, q.type.value),
                "required":          q.is_required,
                "hidden_by_default": q.is_hidden,
                **expand_question_config(q.config or {}, q.type),
            })

        sections_out.append({
            "id":        str(section.id),
            "order":     section.order,
            "title":     section.title,
            "questions": questions_out,
        })

    metrics_out = [
        {
            "id":              str(f.id),
            "name":            f.name,
            "operation":       f.expression,
            "question_ids":    [str(q.id) for q in f.questions],
            "coefficient":     f.coefficient,
            "interpretations": f.ranges,
        }
        for f in test.formula
    ]

    return {
        "title":                 test.title,
        "description":           test.description,
        "show_report_to_client": test.show_report_to_client,
        "client_fields":         test.required_fields,
        "report_template":       test.report_template,
        "sections":              sections_out,
        "metrics":               metrics_out,
    }


# =====================================
# ПОЛУЧЕНИЕ ТЕСТА ДЛЯ ГОСТЯ
# =====================================

async def get_test_for_guest(db: AsyncSession, access_link: str) -> dict:
    """
    возвращает тест без весов и score_ranges.
    """
    result = await db.execute(
        select(Test)
        .where(
            Test.access_link == access_link,
            Test.is_active   == True,
            Test.is_deleted  == False,
        )
        .options(
            selectinload(Test.sections).selectinload(Section.questions)
        )
    )
    test: Optional[Test] = result.scalar_one_or_none()
    if not test:
        raise ValueError("Тест не найден или недоступен")

    sections_out = []
    for section in sorted(test.sections, key=lambda s: cast(Section, s).order):
        questions_out = []
        for q in sorted(section.questions, key=lambda q: q.order_index):
            cfg = q.config or {}
            strip_keys = GUEST_STRIP_FIELDS.get(q.type, set())
            expanded = expand_question_config(cfg, q.type)

            if "options" in expanded and strip_keys:
                expanded["options"] = strip_sensitive_from_options(
                    expanded["options"], strip_keys
                )

            expanded.pop("score_ranges", None)

            questions_out.append({
                "id": str(q.id),
                "order": q.order_index,
                "text": q.text,
                "type": DB_TO_FRONTEND_TYPE.get(q.type, q.type.value),
                "required": q.is_required,
                "hidden_by_default": q.is_hidden,
                **expanded,
            })

        sections_out.append({
            "id": str(section.id),
            "order": section.order,
            "title": section.title,
            "questions": questions_out,
        })

    return {
        "test_id": str(test.id),
        "title": test.title,
        "description": test.description,
        "client_fields": test.required_fields,
        "sections": sections_out,
    }


# ══════════════════════════════════════════════
# СОХРАНЕНИЕ ОТВЕТОВ СЕССИИ
# ══════════════════════════════════════════════

def resolve_answer_weight(answer_value, question: Question) -> Optional[float]:
    """
    вычисляет вес ответа на основе конфига вопроса
    возвращает None для типов без весов
    """
    cfg = question.config or {}

    if question.type in (QuestionType.SINGLE, QuestionType.YESNO):
        for opt in cfg.get("options", []):
            if opt["id"] == answer_value or opt.get("text") == answer_value:
                return float(opt["weight"]) if "weight" in opt else None

    if question.type == QuestionType.MULTIPLE:
        selected = set(answer_value) if isinstance(answer_value, list) else set()
        weights = [
            float(opt["weight"])
            for opt in cfg.get("options", [])
            if (opt["id"] in selected or opt.get("text") in selected) and "weight" in opt
        ]
        return sum(weights) if weights else None

    if question.type == QuestionType.RANGE:
        if isinstance(answer_value, dict):
            val = (float(answer_value.get("min", 0)) + float(answer_value.get("max", 0))) / 2
        else:
            val = float(answer_value)
        for sr in cfg.get("score_ranges", []):
            if sr["from"] <= val <= sr["to"]:
                return float(sr["weight"]) if "weight" in sr else None
        return None

    if question.type in (QuestionType.NUMBER, QuestionType.RATING):
        return float(answer_value)

    return None


async def save_session_answers(
    db:         AsyncSession,
    session_id: uuid.UUID,
    data:       dict,
) -> None:
    """принимает JSON с ответами от фронта и считает веса и пишет в таблицу answers"""
    session_result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    session: Optional[Session] = session_result.scalar_one_or_none()
    if not session:
        raise ValueError(f"Сессия {session_id} не найдена")

    question_ids = [uuid.UUID(a["question_id"]) for a in data.get("answers", [])]

    questions_result = await db.execute(
        select(Question).where(Question.id.in_(question_ids))
    )
    questions_by_id: dict[uuid.UUID, Question] = {
        q.id: q for q in questions_result.scalars().all()
    }

    for answer_data in data.get("answers", []):
        q_id     = uuid.UUID(answer_data["question_id"])
        q_value  = answer_data["answer"]
        question = questions_by_id.get(q_id)

        if not question:
            continue

        db.add(Answer(
            id=uuid.uuid4(),
            session_id=session_id,
            question_id=q_id,
            value={"answer": q_value},
            weight=resolve_answer_weight(q_value, question),
        ))

    if guest_info := data.get("guest_info"):
        session.client_extra = {
            item["field_label"]: item["value"]
            for item in guest_info
        }

    await db.commit()


# =====================================
# ПОДСЧЁТ МЕТРИК
# =====================================

def find_interpretation(value: float, ranges: list) -> str | None:
    """по числовому значению находит подходящий диапазон и возвращает его описание"""
    for r in ranges:
        if r["from"] <= value <= r["to"]:
            return r.get("description")
    return None


def apply_operation(expression: str, weights: list[float], coefficient: float) -> float:
    """применяет операцию к списку весов и умножает на коэффициент"""
    if not weights:
        return 0.0

    match expression:
        case "sum":     result = sum(weights)
        case "avg":     result = sum(weights) / len(weights)
        case "min":     result = min(weights)
        case "max":     result = max(weights)
        case "percent": result = (sum(weights) / len(weights)) * 100
        case _:         result = sum(weights)

    return result * coefficient


async def calculate_and_save_metrics(
    db:         AsyncSession,
    session_id: uuid.UUID,
) -> dict:
    """
    считает метрики по всем формулам теста и сохраняет в session.metrics
    """
    result = await db.execute(
        select(Session)
        .where(Session.id == session_id)
        .options(
            selectinload(Session.test).selectinload(Test.formula).selectinload(FormulaModel.questions),
            selectinload(Session.answers),
        )
    )
    session: Optional[Session] = result.scalar_one_or_none()
    if not session:
        raise ValueError(f"Сессия {session_id} не найдена")

    weights_by_question: dict[uuid.UUID, float] = {
        a.question_id: a.weight
        for a in session.answers
        if a.weight is not None
    }

    metrics: dict = {}

    for formula in session.test.formula:
        weights = [
            weights_by_question[q.id]
            for q in formula.questions
            if q.id in weights_by_question
        ]

        value = apply_operation(formula.expression, weights, formula.coefficient)
        interpretation = find_interpretation(value, formula.ranges or [])

        metrics[str(formula.id)] = {
            "name":           formula.name,
            "value":          value,
            "interpretation": interpretation,
        }

    session.metrics = metrics
    await db.commit()

    return metrics